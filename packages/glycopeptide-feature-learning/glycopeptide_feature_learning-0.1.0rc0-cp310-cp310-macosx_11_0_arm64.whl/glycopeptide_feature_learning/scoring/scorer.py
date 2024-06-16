from collections import defaultdict
from contextlib import contextmanager
import math
from typing import Dict, List, Optional, Union

import numpy as np

from glycopeptidepy import IonSeries

from glycresoft.tandem.glycopeptide.scoring.coverage_weighted_binomial import (
    CoverageWeightedBinomialScorer)
from glycresoft.tandem.glycopeptide.scoring.simple_score import SignatureAwareCoverageScorer
from glycresoft.tandem.glycopeptide.scoring.precursor_mass_accuracy import MassAccuracyMixin

from glycopeptide_feature_learning.multinomial_regression import (
    MultinomialRegressionFit, least_squares_scale_coefficient)
from glycopeptide_feature_learning.approximation import PearsonResidualCDF
from glycopeptide_feature_learning.partitions import SplitModelFit, partition_cell_spec
from glycopeptide_feature_learning.scoring.base import HelperMethods

from glycopeptide_feature_learning.utils import distcorr

from .predicate import PredicateTreeBase, ModelBindingScorer

from ._c.score_set import ModelScoreSet


def pad(x, p=0.5):
    return (1 - p) * x + p


def unpad(x, p=0.5):
    return (x - p) / (1 - p)


class CachedModelPrediction(object):
    __slots__ = ("fragment_specifications", "experimental_intensities", "total_signal",
                 "feature_vectors", "reliability_vector")

    def __init__(self, fragment_specifications, experimental_intensities, total_signal, feature_vectors):
        self.fragment_specifications = fragment_specifications
        self.experimental_intensities = experimental_intensities
        self.total_signal = total_signal
        self.feature_vectors = feature_vectors
        self.reliability_vector = None

    def __iter__(self):
        yield self.fragment_specifications
        yield self.experimental_intensities
        yield self.total_signal
        yield self.feature_vectors

    def __reduce__(self):
        return self.__class__, tuple(self)



def _predict_yhat_from_feature_and_coefs(features: np.ndarray, coefs: np.ndarray) -> np.ndarray:
    yhat = np.exp(features.dot(coefs))
    yhat /= (1 + yhat.sum())
    return yhat


class _ModelPredictionCachingBase(object):
    def _transform_matched_peaks(self):
        if self._is_model_cached(self.model_fit):
            return self._get_cached_model_transform(self.model_fit)
        result = self._transform_matched_peaks_uncached()
        self._cache_model_transform(self.model_fit, result)
        return result

    def _init_cache(self):
        self._cached_model = None
        self._cached_transform = None
        self._cached_reliabilities = None

    def _get_predicted_intensities(self):
        c, intens, t, X = self._transform_matched_peaks()
        yhat = _predict_yhat_from_feature_and_coefs(X, self.model_fit.coef)
        return c, intens, t, yhat

    def _cache_model_transform(self, model_fit, transform):
        self._cached_model = model_fit
        self._cached_transform = CachedModelPrediction(*transform)

    def _is_model_cached(self, model_fit):
        return self.model_fit is self._cached_model

    def _get_cached_model_transform(self, model_fit):
        return self._cached_transform

    def _clear_cache(self):
        self._cached_model = None
        self._cached_transform = None
        self._cached_reliabilities = None

    def _transform_matched_peaks_uncached(self):
        model_fit = self.model_fit
        c, intens, t = model_fit.model_type.build_fragment_intensity_matches(self)
        X = model_fit.model_type.encode_classification(c)
        return (c, intens, t, X)

    def _get_reliabilities(self, fragment_match_features, base_reliability=0.5):
        is_model_cached = False
        cached_data = None
        # Does not actually populate the cache if the model hasn't had its result
        # cached in the first place.
        if self._is_model_cached(self.model_fit):
            is_model_cached = True
            cached_data = self._get_cached_model_transform(self.model_fit)
            if cached_data.reliability_vector is not None:
                return cached_data.reliability_vector
        if self._cached_reliabilities is None:
            self._cached_reliabilities = reliability = self.model_fit._calculate_reliability(
                self, fragment_match_features, base_reliability=base_reliability)
        else:
            reliability = self._cached_reliabilities
        if is_model_cached:
            if cached_data is not None:
                cached_data.reliability_vector = reliability
        return reliability


def spectral_angle(y, yhat) -> float:
    """
    The angle between two vectors where 0 indicates the vectors are identical.

    Without the inverse cosine transformation * 2/pi, this is just the dot product
    similarity.
    """
    num = y.dot(yhat)
    den = np.sqrt(y.dot(y) * yhat.dot(yhat))
    return np.arccos(num / den) * 2 / np.pi


class MultinomialRegressionScorerBase(_ModelPredictionCachingBase, MassAccuracyMixin):

    partition_key: Optional[int] = -1

    _glycan_score: Optional[float] = None
    _glycan_coverage: Optional[float] = None
    _peptide_score: Optional[float] = None

    def _calculate_pearson_residuals(self, use_reliability=True, base_reliability=0.5):
        r"""Calculate the raw Pearson residuals of the Multinomial model

        .. math::
            \frac{y - \hat{y}}{\hat{y} * (1 - \hat{y}) * r}

        Parameters
        ----------
        use_reliability : bool, optional
            Whether or not to use the fragment reliabilities to adjust the weight of
            each matched peak
        base_reliability : float, optional
            The lowest reliability a peak may have, compressing the range of contributions
            from the model based on the experimental evidence

        Returns
        -------
        np.ndarray
            The Pearson residuals
        """
        c, intens, t, yhat = self._get_predicted_intensities()
        if self.model_fit.reliability_model is None or not use_reliability:
            reliability = np.ones_like(yhat)
        else:
            reliability = self._get_reliabilities(c, base_reliability=base_reliability)
        # standardize intensity
        intens = intens / t
        # remove the unassigned signal term
        intens = intens[:-1]
        yhat = yhat[:-1]

        delta = (intens - yhat) ** 2
        mask = intens > yhat
        # reduce penalty for exceeding predicted intensity
        delta[mask] = delta[mask] / 2.
        denom = yhat * (1 - yhat)
        denom *= (reliability[:-1])  # divide by the reliability
        pearson_residuals = delta / denom
        return pearson_residuals

    def _get_intensity_observed_expected(self, use_reliability=False, base_reliability=0.5):
        """Get the vector of matched experimental intensities and their predicted intensities.

        If the reliability model is used, the peak intensities are recalibrated according
        to a multinomial variance model with the reliabilities as weights.

        Parameters
        ----------
        use_reliability : bool, optional
            Whether or not to use the fragment reliabilities to adjust the weight of
            each matched peak
        base_reliability : float, optional
            The lowest reliability a peak may have, compressing the range of contributions
            from the model based on the experimental evidence

        Returns
        -------
        np.ndarray:
            Matched experimental peak intensities
        np.ndarray:
            Predicted peak intensities
        """
        c, intens, t, yhat = self._get_predicted_intensities()
        p = (intens / t)[:-1]
        yhat = yhat[:-1]
        if len(p) == 1:
            return 0., 0.
        if use_reliability:
            reliability = self._get_reliabilities(c, base_reliability=base_reliability)[:-1]
            p = t * p / np.sqrt(t * reliability * p * (1 - p))
            yhat = t * yhat / np.sqrt(t * reliability * yhat * (1 - yhat))
        return p, yhat

    def get_predicted_intensities_series(self, series, use_reliability=True, base_reliability=0.5):
        c, intens, t, yhat = self._get_predicted_intensities()
        if self.model_fit.reliability_model is None or not use_reliability:
            reliability = np.ones_like(yhat)
        else:
            reliability = self._get_reliabilities(c, base_reliability=base_reliability)
        keep_c = []
        keep_intens = []
        keep_yhat = []
        keep_reliability = []

        for i in range(len(c)):
            if c[i].series in series:
                keep_c.append(c[i])
                keep_intens.append(intens[i])
                keep_yhat.append(yhat[i])
                keep_reliability.append(reliability[i])
        if use_reliability:
            return keep_c, np.array(keep_intens), t, np.array(keep_yhat), np.array(keep_reliability)
        else:
            return keep_c, np.array(keep_intens), t, np.array(keep_yhat)

    def _calculate_correlation_coef(self, use_reliability=False, base_reliability=0.5):
        p, yhat = self._get_intensity_observed_expected(use_reliability, base_reliability)
        return np.corrcoef(p, yhat)[0, 1]

    def _calculate_correlation_distance(self, use_reliability=False, base_reliability=0.5):
        p, yhat = self._get_intensity_observed_expected(use_reliability, base_reliability)
        return distcorr(p, yhat)

    def _transform_correlation(self, use_reliability=False, base_reliability=0.5):
        r = self._calculate_correlation_coef(use_reliability=use_reliability, base_reliability=base_reliability)
        if np.isnan(r):
            r = -0.5
        c = (r + 1) / 2.
        return c

    def _transform_correlation_distance(self, use_reliability=False, base_reliability=0.5):
        r = self._calculate_correlation_distance(use_reliability=use_reliability, base_reliability=base_reliability)
        if np.isnan(r):
            r = -0.5
        c = (r + 1) / 2.
        return c

    def total_correlation(self):
        return self._calculate_correlation_coef()

    def total_spectral_angle(self, use_reliability=False, base_reliability=0.5):
        p, yhat = self._get_intensity_observed_expected(use_reliability, base_reliability)
        return spectral_angle(p, yhat)

    def peptide_correlation(self):
        c, inten, t, y, rel = self.get_predicted_intensities_series(
            ['b', 'y'], True)
        return np.corrcoef(inten, y)[1, 0]

    def peptide_spectral_angle(self):
        c, inten, t, y, rel = self.get_predicted_intensities_series(["b", "y"], True)
        return spectral_angle(inten, y)

    def glycan_correlation(self):
        c, inten, t, y, rel = self.get_predicted_intensities_series(
            ['stub_glycopeptide'], True)
        return np.corrcoef(inten, y)[1, 0]

    def glycan_spectral_angle(self):
        c, inten, t, y, rel = self.get_predicted_intensities_series(["stub_glycopeptide"], True)
        return spectral_angle(inten, y)

    def peptide_reliability(self):
        result = self.get_predicted_intensities_series(
            (IonSeries.b, IonSeries.y))[4]
        return result

    def glycan_reliability(self):
        result = self.get_predicted_intensities_series(
            (IonSeries.stub_glycopeptide, ))[4]
        return result

    def _get_predicted_points(self, scaled=True):
        c, intens, t, yhat = self.model_fit._get_predicted_intensities(self)
        mz = [ci.peak.mz for ci in c if ci.peak_pair]
        intensities = yhat[:-1] * (least_squares_scale_coefficient(yhat[:-1], intens[:-1]) if scaled else 1.0)
        return zip(mz, intensities)

    def _get_predicted_peaks(self, *args, **kwargs):
        return self._get_predicted_intensities(*args, **kwargs)

    def glycan_score(self, error_tolerance=2e-5, use_reliability=True, base_reliability=0.5, core_weight=0.4,
                     coverage_weight=0.5, fragile_fucose=False, ** kwargs):
        if self._glycan_score is None:
            self._glycan_score = self.calculate_glycan_score(
                error_tolerance, use_reliability, base_reliability, core_weight, coverage_weight,
                fragile_fucose=fragile_fucose, **kwargs)
        return self._glycan_score

    def peptide_score(self, error_tolerance=2e-5, use_reliability=True, base_reliability=0.5, **kwargs):
        if self._peptide_score is None:
            self._peptide_score = self.calculate_peptide_score(
                error_tolerance, use_reliability, base_reliability, **kwargs)
        return self._peptide_score

    def __reduce__(self):
        return self.__class__, (self.scan, self.target, self.mass_shift, self.model_fit, self.partition)


class MultinomialRegressionScorer(HelperMethods, CoverageWeightedBinomialScorer, MultinomialRegressionScorerBase):

    def __init__(self, scan, sequence, mass_shift=None, model_fit=None, partition=None):
        super(MultinomialRegressionScorer, self).__init__(scan, sequence, mass_shift)
        self.structure = self.target
        self.model_fit = model_fit
        self.partition = partition
        self.error_tolerance = None
        self._init_cache()

    def _calculate_pearson_residual_score(self, use_reliability=True, base_reliability=0.5):
        """Compute a model-based score by summing the Pearson residuals after transforming
        through them an empirically measured CDF and followed by a -log10 transform.

        Parameters
        ----------
        use_reliability : bool, optional
            Whether or not to use the fragment reliabilities to adjust the weight of
            each matched peak
        base_reliability : float, optional
            The lowest reliability a peak may have, compressing the range of contributions
            from the model based on the experimental evidence

        Returns
        -------
        float:
            The model score
        """
        pearson_residuals = self._calculate_pearson_residuals(
            use_reliability, base_reliability)
        model_score = - \
            np.log10(PearsonResidualCDF(pearson_residuals) + 1e-6).sum()
        if np.isnan(model_score):
            model_score = 0.0
        c, intens, t, yhat = self._get_predicted_intensities()
        reliability = self._get_reliabilities(
            c, base_reliability=base_reliability)[:-1]
        reliability = unpad(reliability, base_reliability)
        intensity_component = np.log10(intens[:-1]).dot(reliability + 1.0)
        return model_score + intensity_component

    def match(self, error_tolerance=2e-5, *args, **kwargs):
        self.error_tolerance = error_tolerance
        return super(MultinomialRegressionScorer, self).match(
            error_tolerance=error_tolerance, *args, **kwargs)

    def calculate_glycan_score(self, use_reliability=True, base_reliability=0.5, core_weight=0.4, coverage_weight=0.6,
                               fragile_fucose=False, **kwargs):
        c, intens, t, yhat = self._get_predicted_intensities()
        if self.model_fit.reliability_model is None or not use_reliability:
            reliability = np.ones_like(yhat)
        else:
            reliability = self._get_reliabilities(c, base_reliability=base_reliability)
        stubs = []
        intens = intens / t
        for i in range(len(c)):
            if c[i].series == 'stub_glycopeptide':
                stubs.append((c[i], intens[i], yhat[i], reliability[i]))
        if not stubs:
            return 0
        c, intens, yhat, reliability = zip(*stubs)
        intens = np.array(intens)
        yhat = np.array(yhat)
        reliability = np.array(reliability)
        if use_reliability:
            corr = (np.corrcoef(t * intens / np.sqrt(t * reliability * intens * (1 - intens)),
                                t * yhat / np.sqrt(t * reliability * yhat * (1 - yhat)))[0, 1])
        else:
            corr = np.corrcoef(intens, yhat)[0, 1]
        if np.isnan(corr):
            corr = -0.5
        corr = (1.0 + corr) / 2.0
        corr_score = corr * 10.0
        delta = (intens - yhat) ** 2
        mask = intens > yhat
        delta[mask] = delta[mask] / 2.
        denom = yhat * (1 - yhat) * reliability
        stub_component = -np.log10(PearsonResidualCDF(delta / denom) + 1e-6).sum()

        if np.isnan(stub_component):
            stub_component = 0
        oxonium_component = self._signature_ion_score()
        coverage = self._calculate_glycan_coverage(
            core_weight, coverage_weight, fragile_fucose=fragile_fucose)
        glycan_score = (np.log10(intens * t).dot(reliability + 1) + corr_score + stub_component
                        ) * coverage + oxonium_component
        return max(glycan_score, 0)

    def calculate_peptide_score(self, use_reliability=True, base_reliability=0.5):
        c, intens, t, yhat = self._get_predicted_intensities()
        if self.model_fit.reliability_model is None or not use_reliability:
            reliability = np.ones_like(yhat)
        else:
            reliability = self._get_reliabilities(c, base_reliability=base_reliability)
        series_set = ('b', 'y')
        backbones = []
        intens = intens / t
        for i in range(len(c)):
            if c[i].series in series_set:
                backbones.append((c[i], intens[i], yhat[i], reliability[i]))
        if not backbones:
            return 0
        c, intens, yhat, reliability = zip(*backbones)
        intens = np.array(intens)
        yhat = np.array(yhat)
        reliability = np.array(reliability)

        # peptide reliability is usually less powerful, so it does not benefit
        # us to use the normalized correlation coefficient here
        corr = np.corrcoef(intens, yhat)[0, 1]
        if np.isnan(corr):
            corr = -0.5
        # peptide fragment correlation is weaker than the overall correlation.
        corr = (3.0 + corr) / 4.0
        corr_score = corr * 10.0 * np.log(len(backbones))

        delta = (intens - yhat) ** 2
        mask = intens > yhat
        delta[mask] = delta[mask] / 2.
        denom = yhat * (1 - yhat) * reliability
        peptide_score = -np.log10(PearsonResidualCDF(delta / denom) + 1e-6).sum()
        if np.isnan(peptide_score):
            peptide_score = 0.0
        # peptide backbone coverage without separate term for glycosylation site parsimony
        n_term_ions, c_term_ions = self._compute_coverage_vectors()[:2]
        coverage_score = ((n_term_ions + c_term_ions[::-1])).sum() / float(self.n_theoretical)
        peptide_score = (np.log10(intens * t).dot(reliability + 1) + peptide_score)
        # peptide_score *= corr
        peptide_score += corr_score
        peptide_score *= coverage_score
        return peptide_score

    @classmethod
    def get_score_set_type(cls):
        return ModelScoreSet

    def calculate_score(self, error_tolerance=2e-5, backbone_weight=None,
                        glycosylated_weight=None, stub_weight=None,
                        use_reliability=True, base_reliability=0.5,
                        weighting=None, *args, **kwargs):
        intensity = -math.log10(self._intensity_component_binomial())
        # fragments_matched = -math.log10(self._fragment_matched_binomial())
        fragments_matched = 0.0
        coverage_score = self._coverage_score(backbone_weight, glycosylated_weight, stub_weight)
        mass_accuracy = self._precursor_mass_accuracy_score()
        signature_component = self._signature_ion_score()
        model_score = self._calculate_pearson_residual_score(
            use_reliability=use_reliability,
            base_reliability=base_reliability)
        self._score = (intensity + fragments_matched + model_score)
        if weighting is None:
            pass
        elif weighting == 'correlation':
            self._score += self._transform_correlation(False) * 10.0
        elif weighting == 'normalized_correlation':
            self._score += self._transform_correlation(True, base_reliability=base_reliability) * 10.0
        elif weighting in ('correlation_distance', 'distance_correlation'):
            self._score += self._transform_correlation_distance(False) * 10.0
        elif weighting in ('normalized_correlation_distance', 'normalized_distance_correlation'):
            self._score += self._transform_correlation_distance(True, base_reliability=base_reliability) * 10.0
        else:
            raise ValueError("Unrecognized Weighting Scheme %s" % (weighting,))
        self._score *= coverage_score
        self._score += (mass_accuracy + signature_component)
        return self._score


class _MultiModelCache(object):

    def _cache_model_transform(self, model_fit, transform):
        self._feature_cache[model_fit] = CachedModelPrediction(*transform)

    def _is_model_cached(self, model_fit):
        return model_fit in self._feature_cache

    def _get_cached_model_transform(self, model_fit):
        return self._feature_cache[model_fit]

    def _clear_cache(self):
        self._feature_cache.clear()
        self._cached_reliabilities = None

    def _init_cache(self):
        self._feature_cache = dict()
        self._cached_reliabilities = None


class _ModelMixtureBase(_MultiModelCache):
    def _iter_model_fits(self):
        for model_fit in self.model_fits:
            self.model_fit = model_fit
            yield model_fit
        self.model_fit = self.model_fits[0]

    def _calculate_mixture_coefficients(self):
        if len(self.model_fits) == 1:
            return np.array([1.])
        ps = np.empty(len(self.model_fits))
        for i, model_fit in enumerate(self._iter_model_fits()):
            pearson = self._calculate_pearson_residuals().sum()
            if np.isnan(pearson) or pearson == 0:
                pearson = 1.0
            ps[i] = (1. / pearson) ** self.power
        total = ps.sum() + 1e-6 * ps.shape[0]
        if np.isnan(total):
            ps[np.isnan(ps)] = 0
            total = ps.sum() + 1e-6 * ps.shape[0]
        return ps / total

    def _mixture_apply(self, fn, *args, **kwargs):
        return self.mixture_coefficients.dot(
            [fn(self, *args, **kwargs) for _ in self._iter_model_fits()])


class MultinomialRegressionMixtureScorer(_ModelMixtureBase, MultinomialRegressionScorer):

    def __init__(self, scan, sequence, mass_shift=None, model_fits=None, partition=None, power=4):
        super(MultinomialRegressionMixtureScorer, self).__init__(
            scan, sequence, mass_shift, model_fit=model_fits[0], partition=partition)
        self.model_fits = list(model_fits)
        self.power = power
        self._init_cache()
        self.mixture_coefficients = None

    def __reduce__(self):
        return self.__class__, (self.scan, self.target, self.mass_shift, self.model_fits, self.partition, self.power)

    def _calculate_pearson_residual_score(self, use_reliability=True, base_reliability=0.5):
        scores = []
        for model_fit in self._iter_model_fits():
            score = super(
                MultinomialRegressionMixtureScorer, self)._calculate_pearson_residual_score(
                    use_reliability=use_reliability, base_reliability=base_reliability)
            scores.append(score)
        return np.dot(scores, self.mixture_coefficients)

    def calculate_glycan_score(self, use_reliability=True, base_reliability=0.5, fragile_fucose=False, **kwargs):
        scores = []
        for model_fit in self._iter_model_fits():
            score = super(
                MultinomialRegressionMixtureScorer, self).calculate_glycan_score(
                    use_reliability=use_reliability, base_reliability=base_reliability,
                    fragile_fucose=fragile_fucose, **kwargs)
            scores.append(score)
        return np.dot(scores, self.mixture_coefficients)

    def calculate_peptide_score(self, use_reliability=True, base_reliability=0.5, **kwargs):
        scores = []
        for model_fit in self._iter_model_fits():
            score = super(
                MultinomialRegressionMixtureScorer, self).calculate_peptide_score(
                    use_reliability=use_reliability, base_reliability=base_reliability, **kwargs)
            scores.append(score)
        return np.dot(scores, self.mixture_coefficients)

    def _calculate_correlation_coef(self, use_reliability=False, base_reliability=0.5):
        scores = []
        for model_fit in self._iter_model_fits():
            score = super(
                MultinomialRegressionMixtureScorer, self)._calculate_correlation_coef(
                    use_reliability=use_reliability, base_reliability=base_reliability)
            scores.append(score)
        return np.array(scores)

    def _calculate_correlation_distance(self, use_reliability=False, base_reliability=0.5):
        scores = []
        for model_fit in self._iter_model_fits():
            score = super(
                MultinomialRegressionMixtureScorer, self)._calculate_correlation_distance(
                    use_reliability=use_reliability, base_reliability=base_reliability)
            scores.append(score)
        return np.array(scores)

    def _transform_correlation(self, use_reliability=False, base_reliability=0.5):
        r = self._calculate_correlation_coef(
            use_reliability=use_reliability, base_reliability=base_reliability)
        r[np.isnan(r)] = -0.5
        c = (r + 1) / 2.
        return np.dot(c, self.mixture_coefficients)

    def _transform_correlation_distance(self, use_reliability=False, base_reliability=0.5):
        r = self._calculate_correlation_distance(
            use_reliability=use_reliability, base_reliability=base_reliability)
        r[np.isnan(r)] = -0.5
        c = (r + 1) / 2.
        return np.dot(c, self.mixture_coefficients)

    def calculate_score(self, error_tolerance=2e-5, backbone_weight=None,
                        glycosylated_weight=None, stub_weight=None,
                        use_reliability=True, base_reliability=0.5,
                        weighting=None, *args, **kwargs):
        self.mixture_coefficients = self._calculate_mixture_coefficients()
        return super(MultinomialRegressionMixtureScorer, self).calculate_score(
            error_tolerance=error_tolerance, backbone_weight=backbone_weight,
            glycosylated_weight=glycosylated_weight, stub_weight=stub_weight,
            use_reliability=use_reliability, base_reliability=base_reliability,
            weighting=weighting, *args, **kwargs)


class PredicateTree(PredicateTreeBase):
    _scorer_type = MultinomialRegressionMixtureScorer
    _short_peptide_scorer_type = MultinomialRegressionMixtureScorer

    @classmethod
    def get_score_set_type(cls):
        return ModelScoreSet


class SplitScorer(HelperMethods, MultinomialRegressionScorerBase, SignatureAwareCoverageScorer):

    _glycan_score = None
    _peptide_score = None

    def __init__(self, scan, sequence, mass_shift=None, model_fit=None, partition=None):
        super(SplitScorer, self).__init__(scan, sequence, mass_shift)
        self.structure = self.target
        self.model_fit = model_fit
        self.partition = partition
        self.error_tolerance = None
        self._init_cache()

    def match(self, error_tolerance=2e-5, *args, **kwargs):
        self.error_tolerance = error_tolerance
        return super(SplitScorer, self).match(
            error_tolerance=error_tolerance, *args, **kwargs)

    def calculate_peptide_score(self, error_tolerance=2e-5, use_reliability=True, base_reliability=0.5,
                                coverage_weight=1.0, *args, **kwargs):
        c, intens, t, yhat = self._get_predicted_intensities()
        if self.model_fit.reliability_model is None or not use_reliability:
            reliability = np.ones_like(yhat)
        else:
            reliability = self._get_reliabilities(c, base_reliability=base_reliability)
        series_set = ('b', 'y')
        backbones = []
        intens = intens / t
        for i in range(len(c)):
            if c[i].series in series_set:
                backbones.append((c[i], intens[i], yhat[i], reliability[i]))
        if not backbones:
            return 0

        c, intens, yhat, reliability = zip(*backbones)
        intens = np.array(intens)
        yhat = np.array(yhat)
        reliability = np.array(reliability)

        # peptide reliability is usually less powerful, so it does not benefit
        # us to use the normalized correlation coefficient here
        corr = np.corrcoef(intens, yhat)[0, 1]
        if np.isnan(corr):
            corr = -0.5
        # peptide fragment correlation is weaker than the overall correlation.
        corr = (1.0 + corr) / 2.0
        corr_score = corr * 2.0 * np.log10(len(backbones))

        delta = (intens - yhat) ** 2
        mask = intens > yhat
        delta[mask] = delta[mask] / 2.
        denom = yhat * (1 - yhat) * reliability
        peptide_score = -np.log10(PearsonResidualCDF(delta / denom) + 1e-6)
        if np.all(np.isnan(peptide_score)):
            peptide_score = 0.0
        mass_accuracy = [1 - abs(ci.peak_pair.mass_accuracy() / error_tolerance) ** 4 for ci in c]
        # peptide backbone coverage without separate term for glycosylation site parsimony
        n_term_ions, c_term_ions = self._compute_coverage_vectors()[:2]
        coverage_score = ((n_term_ions + c_term_ions[::-1])).sum() / (2.0 * (len(self.target) - 1))
        # the 0.17 term ensures that the maximum value of the -log10 transform of the cdf is
        # mapped to approximately 1.0 (1.02). The maximum value is guaranteed to 6.0 because
        # the minimum value returned from the CDF is 0 + 1e-6 padding, which maps to 6.
        peptide_score = ((np.log10(intens * t) * mass_accuracy * (
            unpad(reliability, base_reliability) + 0.75) * (0.17 * peptide_score))).sum()
        peptide_score += corr_score
        peptide_score *= coverage_score ** coverage_weight
        return peptide_score

    def calculate_glycan_score(self, error_tolerance=2e-5, use_reliability=True, base_reliability=0.5, core_weight=0.4,
                               coverage_weight=0.5, fragile_fucose=False, **kwargs):
        c, intens, t, yhat = self._get_predicted_intensities()
        if self.model_fit.reliability_model is None or not use_reliability:
            reliability = np.ones_like(yhat)
        else:
            reliability = self._get_reliabilities(c, base_reliability=base_reliability)
        stubs = []
        intens = intens / t
        for i in range(len(c)):
            if c[i].series == 'stub_glycopeptide':
                stubs.append((c[i], intens[i], yhat[i], reliability[i]))
        if not stubs:
            return 0

        c, intens, yhat, reliability = zip(*stubs)
        intens = np.array(intens)
        yhat = np.array(yhat)
        reliability = np.array(reliability)

        delta = (intens - yhat) ** 2
        mask = intens > yhat
        delta[mask] = delta[mask] / 2.
        denom = yhat * (1 - yhat) * reliability
        stub_component = -np.log10(PearsonResidualCDF(delta / denom) + 1e-6)
        if np.all(np.isnan(stub_component)):
            stub_component = 0
        oxonium_component = self._signature_ion_score()
        coverage = self._calculate_glycan_coverage(
            core_weight, coverage_weight, fragile_fucose=fragile_fucose)
        mass_accuracy = [1 - abs(ci.peak_pair.mass_accuracy() / error_tolerance) ** 4 for ci in c]
        # the 0.17 term ensures that the maximum value of the -log10 transform of the cdf is
        # mapped to approximately 1.0 (1.02). The maximum value is guaranteed to 6.0 because
        # the minimum value returned from the CDF is 0 + 1e-6 padding, which maps to 6.
        glycan_score = ((np.log10(intens * t) * mass_accuracy * (
            unpad(reliability, base_reliability) + 1) * (
            0.17 * stub_component)).sum()) * coverage + oxonium_component
        return max(glycan_score, 0)

    def _localization_score(self, glycosylated_weight=1.0, **kwargs):
        (n_term, c_term, stub_count,
         glycosylated_n_term_ions, glycosylated_c_term_ions) = self._compute_coverage_vectors()

        glycosylated_coverage_score = self._compute_glycosylated_coverage(
            glycosylated_n_term_ions,
            glycosylated_c_term_ions) + 1e-3
        localization_score = (glycosylated_coverage_score * glycosylated_weight)
        return localization_score

    def calculate_score(self, error_tolerance=2e-5, peptide_weight=0.65, glycosylated_weight=1.,
                        base_reliability=0.5, *args, **kwargs):
        # intensity = -math.log10(self._intensity_component_binomial())
        mass_accuracy = self._precursor_mass_accuracy_score()
        signature_component = self._signature_ion_score()

        localization_score = self._localization_score(glycosylated_weight)

        score = peptide_weight * self.peptide_score(error_tolerance, True, base_reliability)
        score += (1 - peptide_weight) * self.glycan_score(error_tolerance, True, base_reliability)
        score += mass_accuracy
        score += signature_component
        score += localization_score
        self._score = score
        return score


try:
    from glycopeptide_feature_learning.scoring._c.scorer import (
        calculate_peptide_score, _calculate_pearson_residuals,
        predict_yhat_from_feature_and_coefs as _predict_yhat_from_feature_and_coefs)
    MultinomialRegressionScorerBase._calculate_pearson_residuals = _calculate_pearson_residuals
    SplitScorer.calculate_peptide_score = calculate_peptide_score
except ImportError as err:
    print(err)


class MixtureSplitScorer(_ModelMixtureBase, SplitScorer):
    def __init__(self, scan, sequence, mass_shift=None, model_fits=None, partition=None, power=4):
        super(MixtureSplitScorer, self).__init__(
            scan, sequence, mass_shift, model_fit=model_fits[0], partition=partition)
        self.model_fits = list(model_fits)
        self.power = power
        self._init_cache()
        self.mixture_coefficients = None

    def __reduce__(self):
        return self.__class__, (self.scan, self.target, self.mass_shift, self.model_fits, self.partition, self.power)

    def calculate_glycan_score(self, error_tolerance=2e-5, use_reliability=True, base_reliability=0.5,
                               core_weight=0.4, coverage_weight=0.5, fragile_fucose=False, **kwargs):
        scores = []
        for model_fit in self._iter_model_fits():
            score = super(
                MixtureSplitScorer, self).calculate_glycan_score(
                    error_tolerance=error_tolerance,
                    use_reliability=use_reliability, base_reliability=base_reliability,
                    core_weight=core_weight, coverage_weight=coverage_weight, fragile_fucose=fragile_fucose
                    **kwargs)
            scores.append(score)
        return np.dot(scores, self.mixture_coefficients)

    def calculate_peptide_score(self, error_tolerance=2e-5, use_reliability=True, base_reliability=0.5,
                                **kwargs):
        scores = []
        for model_fit in self._iter_model_fits():
            score = super(
                MixtureSplitScorer, self).calculate_peptide_score(
                    error_tolerance=error_tolerance,
                    use_reliability=use_reliability, base_reliability=base_reliability, **kwargs)
            scores.append(score)
        return np.dot(scores, self.mixture_coefficients)

    def calculate_score(self, error_tolerance=2e-5, peptide_weight=0.65, glycosylated_weight=0.1,
                        base_reliability=0.5, *args, **kwargs):
        self.mixture_coefficients = self._calculate_mixture_coefficients()
        score = super(MixtureSplitScorer, self).calculate_score(
            error_tolerance, peptide_weight, glycosylated_weight, base_reliability, *args, **kwargs)
        self._clear_cache()
        return score

    def peptide_correlation(self):
        return self._mixture_apply(lambda x: super(MixtureSplitScorer, x).peptide_correlation())

    def glycan_correlation(self):
        return self._mixture_apply(lambda x: super(MixtureSplitScorer, x).glycan_correlation())

    def total_correlation(self):
        return self._mixture_apply(lambda x: super(MixtureSplitScorer, x).total_correlation())

    def peptide_spectral_angle(self):
        return self._mixture_apply(lambda x: super(MixtureSplitScorer, x).peptide_spectral_angle())

    def glycan_spectral_angle(self):
        return self._mixture_apply(lambda x: super(MixtureSplitScorer, x).glycan_spectral_angle())

    def total_spectral_angle(self, use_reliability=False, base_reliability=0.5):
        return self._mixture_apply(lambda x: super(MixtureSplitScorer, x).total_spectral_angle(use_reliability, base_reliability))


class SplitScorerTree(PredicateTree):
    _scorer_type = MixtureSplitScorer
    _short_peptide_scorer_type = MixtureSplitScorer


class PartialSplitScorer(SplitScorer):

    def calculate_glycan_score(self, error_tolerance=2e-5, use_reliability=True, base_reliability=0.5, core_weight=0.4,
                               coverage_weight=0.5, fragile_fucose=False, extended_glycan_search=True, **kwargs):
        c, intens, t, yhat = self._get_predicted_intensities()
        # use_reliability = False
        if self.model_fit.reliability_model is None or not use_reliability:
            reliability = np.ones_like(yhat)
        else:
            reliability = self._get_reliabilities(c, base_reliability=base_reliability)
        stubs = []
        intens = intens / t
        n_signif_frags = 0
        for i in range(len(c)):
            ci = c[i]
            if ci.series == 'stub_glycopeptide':
                stubs.append((ci, intens[i], yhat[i], reliability[i]))
                if ci.fragment.glycosylation_size > 1:
                    n_signif_frags += 1
        if not stubs:
            return 0

        c, intens, yhat, reliability = zip(*stubs)
        intens = np.array(intens)
        yhat = np.array(yhat)
        reliability = np.array(reliability)
        if len(intens) > 1:
            corr = np.corrcoef(intens, yhat)[0, 1]
            if np.isnan(corr):
                corr = -0.5
        else:
            corr = -0.5
        corr = (1.0 + corr) / 2.0
        corr_score = corr * (n_signif_frags) + \
            reliability.sum()
        oxonium_component = self._signature_ion_score()
        coverage = self._calculate_glycan_coverage(
            core_weight, coverage_weight,
            fragile_fucose=fragile_fucose,
            extended_glycan_search=extended_glycan_search)
        mass_accuracy = [1 - abs(ci.peak_pair.mass_accuracy() / error_tolerance) ** 4 for ci in c]
        glycan_prior = self.target.glycan_prior
        glycan_score = ((np.log10(intens * t) * mass_accuracy
            ).sum() + corr_score) * coverage + oxonium_component + (
                coverage * glycan_prior)
        return max(glycan_score, 0)


try:
    from glycopeptide_feature_learning.scoring._c.scorer import (
        calculate_partial_glycan_score as _calculate_partial_glycan_score)
    PartialSplitScorer.calculate_glycan_score = _calculate_partial_glycan_score
except ImportError:
    pass


class MixturePartialSplitScorer(_ModelMixtureBase, PartialSplitScorer):
    def __init__(self, scan, sequence, mass_shift=None, model_fits=None, partition=None, power=4):
        super(MixturePartialSplitScorer, self).__init__(
            scan, sequence, mass_shift, model_fit=model_fits[0], partition=partition)
        self.model_fits = list(model_fits)
        self.power = power
        self._init_cache()
        self.mixture_coefficients = None

    def __reduce__(self):
        return self.__class__, (self.scan, self.target, self.mass_shift, self.model_fits, self.partition, self.power)

    def calculate_glycan_score(self, error_tolerance=2e-5, use_reliability=True, base_reliability=0.5,
                               core_weight=0.4, coverage_weight=0.5, fragile_fucose=False, **kwargs):
        scores = []
        for model_fit in self._iter_model_fits():
            score = super(
                MixturePartialSplitScorer, self).calculate_glycan_score(
                    error_tolerance=error_tolerance,
                    use_reliability=use_reliability, base_reliability=base_reliability,
                    core_weight=core_weight, coverage_weight=coverage_weight, fragile_fucose=fragile_fucose,
                    **kwargs)
            scores.append(score)
        return np.dot(scores, self.mixture_coefficients)

    def calculate_peptide_score(self, error_tolerance=2e-5, use_reliability=True, base_reliability=0.5,
                                **kwargs):
        scores = []
        for model_fit in self._iter_model_fits():
            score = super(
                MixturePartialSplitScorer, self).calculate_peptide_score(
                    error_tolerance=error_tolerance,
                    use_reliability=use_reliability, base_reliability=base_reliability, **kwargs)
            scores.append(score)
        return np.dot(scores, self.mixture_coefficients)

    def calculate_score(self, error_tolerance=2e-5, peptide_weight=0.65, glycosylated_weight=0.1,
                        base_reliability=0.5, *args, **kwargs):
        self.mixture_coefficients = self._calculate_mixture_coefficients()
        score = super(MixturePartialSplitScorer, self).calculate_score(
            error_tolerance, peptide_weight, glycosylated_weight, base_reliability, *args, **kwargs)
        self._clear_cache()
        return score

    def get_auxiliary_data(self):
        data = super(MixturePartialSplitScorer, self).get_auxiliary_data()
        data['mixture_coefficients'] = self.mixture_coefficients
        data['partition'] = self.partition
        return data

    def peptide_correlation(self):
        return self._mixture_apply(lambda x: super(MixturePartialSplitScorer, x).peptide_correlation())

    def glycan_correlation(self):
        return self._mixture_apply(lambda x: super(MixturePartialSplitScorer, x).glycan_correlation())

    def total_correlation(self):
        return self._mixture_apply(lambda x: super(MixturePartialSplitScorer, x).total_correlation())

    def peptide_spectral_angle(self):
        return self._mixture_apply(lambda x: super(MixturePartialSplitScorer, x).peptide_spectral_angle())

    def glycan_spectral_angle(self):
        return self._mixture_apply(lambda x: super(MixturePartialSplitScorer, x).glycan_spectral_angle())

    def total_spectral_angle(self, use_reliability=False, base_reliability=0.5):
        return self._mixture_apply(
            lambda x: super(MixturePartialSplitScorer, x).total_spectral_angle(use_reliability, base_reliability)
        )


class PartialSplitScorerTree(PredicateTree):
    _scorer_type = MixturePartialSplitScorer
    _short_peptide_scorer_type = MixturePartialSplitScorer


class PartitionedPartialSplitScorer(_MultiModelCache, PartialSplitScorer):
    model_selectors: SplitModelFit

    _peptide_correlation: Optional[float] = None
    _glycan_correlation: Optional[float] = None

    _peptide_spectral_angle: Optional[float] = None
    _glycan_spectral_angle: Optional[float] = None

    def __init__(self, scan, sequence, mass_shift=None, model_selectors=None, partition=None):
        super().__init__(scan, sequence, mass_shift)
        self.structure = self.target
        self.model_fit = None
        self.model_selectors = model_selectors
        self.partition = partition
        self.error_tolerance = None
        self._init_cache()

    def calculate_peptide_score(self, error_tolerance=2e-5, use_reliability=True, base_reliability=0.5,
                                coverage_weight=1.0, *args, **kwargs):
        peptide_model = self.model_selectors.get_peptide_model(self)
        self.model_fit = peptide_model
        value = super().calculate_peptide_score(
            error_tolerance, use_reliability,
            base_reliability,
            coverage_weight,
            *args, **kwargs)
        self.model_fit = None
        return value

    @contextmanager
    def with_peptide_model(self):
        self.model_fit = self.model_selectors.get_peptide_model(self)
        yield self
        self.model_fit = None

    @contextmanager
    def with_glycan_model(self):
        self.model_fit = self.model_selectors.get_glycan_model(self)
        yield self
        self.model_fit = None

    def calculate_glycan_score(self, error_tolerance=2e-5, use_reliability=True, base_reliability=0.5, core_weight=0.4,
                               coverage_weight=0.5, fragile_fucose=False, **kwargs):
        glycan_model = self.model_selectors.get_glycan_model(self)
        self.model_fit = glycan_model
        value = super().calculate_glycan_score(
            error_tolerance,
            use_reliability,
            base_reliability,
            core_weight,
            coverage_weight,
            fragile_fucose,
            **kwargs)
        self.model_fit = None
        return value

    def peptide_correlation(self):
        if self._peptide_correlation is not None:
            return self._peptide_correlation
        peptide_model = self.model_selectors.get_peptide_model(self)
        self.model_fit = peptide_model
        value = super().peptide_correlation()
        self.model_fit = None
        self._peptide_correlation = value
        return value

    def glycan_correlation(self):
        if self._glycan_correlation is not None:
            return self._glycan_correlation
        glycan_model = self.model_selectors.get_glycan_model(self)
        self.model_fit = glycan_model
        value = super().glycan_correlation()
        self.model_fit = None
        self._glycan_correlation = value
        return value

    def peptide_reliability(self):
        with self.with_peptide_model():
            result = self.get_predicted_intensities_series(
                (IonSeries.b, IonSeries.y))[4]
        return result

    def glycan_reliability(self):
        with self.with_glycan_model():
            result = self.get_predicted_intensities_series(
                (IonSeries.stub_glycopeptide, ))[4]
        return result

    def _get_predicted_peaks(self, use_reliability=False, base_reliability=0.5):
        all_intens = []
        all_yhat = []
        all_c = []
        all_reliability = []

        self.model_fit = self.model_selectors.get_peptide_model(self)
        c, intens, t, yhat = self._get_predicted_intensities()

        if use_reliability:
            reliability = reliability = self._get_reliabilities(c, base_reliability=base_reliability)
        else:
            reliability = None

        for i, ci in enumerate(c):
            if ci.is_backbone():
                all_c.append(ci)
                all_intens.append(intens[i])
                all_yhat.append(yhat[i])
                if use_reliability:
                    all_reliability.append(reliability[i])

        self.model_fit = self.model_selectors.get_glycan_model(self)
        c, intens, t, yhat = self._get_predicted_intensities()
        if use_reliability:
            reliability = reliability = self._get_reliabilities(c, base_reliability=base_reliability)
        else:
            reliability = None

        for i, ci in enumerate(c):
            if ci.is_stub_glycopeptide():
                all_c.append(ci)
                all_intens.append(intens[i])
                all_yhat.append(yhat[i])
                if use_reliability:
                    all_reliability.append(reliability[i])

        self.model_fit = None
        all_intens = np.array(all_intens)
        all_yhat = np.array(all_yhat)

        if use_reliability:
            return all_c, all_intens, t, all_yhat, np.array(all_reliability)
        else:
            return all_c, all_intens, t, all_yhat

    def _get_intensity_observed_expected(self, use_reliability=False, base_reliability=0.5):
        """Get the vector of matched experimental intensities and their predicted intensities.

        If the reliability model is used, the peak intensities are recalibrated according
        to a multinomial variance model with the reliabilities as weights.

        Parameters
        ----------
        use_reliability : bool, optional
            Whether or not to use the fragment reliabilities to adjust the weight of
            each matched peak
        base_reliability : float, optional
            The lowest reliability a peak may have, compressing the range of contributions
            from the model based on the experimental evidence

        Returns
        -------
        np.ndarray:
            Matched experimental peak intensities
        np.ndarray:
            Predicted peak intensities
        """
        out = self._get_predicted_peaks(
            use_reliability=use_reliability,
            base_reliability=base_reliability
        )

        c, all_intens, t, all_yhat = out
        return all_intens, all_yhat

    def peptide_spectral_angle(self):
        if self._peptide_spectral_angle is not None:
            return self._peptide_spectral_angle
        peptide_model = self.model_selectors.get_peptide_model(self)
        self.model_fit = peptide_model
        value = super().peptide_spectral_angle()
        self.model_fit = None
        self._peptide_spectral_angle = value
        return value

    def glycan_spectral_angle(self):
        if self._glycan_spectral_angle is not None:
            return self._glycan_spectral_angle
        glycan_model = self.model_selectors.get_glycan_model(self)
        self.model_fit = glycan_model
        value = super().glycan_spectral_angle()
        self.model_fit = None
        self._glycan_spectral_angle = value
        return value


class PartitionedPredicateTree(PredicateTreeBase):
    _scorer_type = PartitionedPartialSplitScorer
    _short_peptide_scorer_type = PartitionedPartialSplitScorer


    @classmethod
    def from_json(cls, d: Union[List, Dict]):
        arranged_data: Dict[partition_cell_spec, List[MultinomialRegressionFit]] = defaultdict(list)
        n = None
        # Check whether the payload is just a raw list of (spec, model) pairs or a wrapper
        # with extra metadata
        if isinstance(d, dict):
            meta = d['metadata']
            d = d['models']
            omit_labile = meta.get('omit_labile', False)
        else:
            meta = dict()
            omit_labile = False
        for spec_d, model_d in d:
            model = SplitModelFit.from_json(model_d)
            spec = partition_cell_spec.from_json(spec_d)
            # Ensure that all model specifications have the same number of dimensions for
            # the tree reconstruction to be consistent
            if n is None:
                n = len(spec) - 1
            else:
                assert n == (len(spec) - 1)
            arranged_data[spec].append(model)
        for spec, models in arranged_data.items():
            scorer_type = cls._scorer_type_for_spec(spec)
            arranged_data[spec] = cls._bind_model_scorer(scorer_type, models, spec)
        arranged_data = dict(arranged_data)
        root = cls.build_tree(arranged_data, 0, n, arranged_data)
        return cls(root, n, omit_labile)

    @classmethod
    def _bind_model_scorer(cls, scorer_type, models, partition=None):
        return ModelBindingScorer(scorer_type, model_selectors=models[0], partition=partition)


try:
    from ._c.scorer import (
        calculate_peptide_score_no_glycosylation,
        calculate_partial_glycan_score_no_glycosylated_peptide_coverage)
except ImportError:
    pass


class NoGlycosylatedPeptidePartitionedPartialSplitScorer(PartitionedPartialSplitScorer):

    def calculate_peptide_score(self, error_tolerance=2e-5, use_reliability=True, base_reliability=0.5,
                                coverage_weight=0.7, *args, **kwargs):
        peptide_model = self.model_selectors.get_peptide_model(self)
        self.model_fit = peptide_model
        value = calculate_peptide_score_no_glycosylation(
            self,
            error_tolerance, use_reliability,
            base_reliability,
            coverage_weight,
            *args, **kwargs)
        self.model_fit = None
        return value

    def calculate_glycan_score(self, error_tolerance=2e-5, use_reliability=True, base_reliability=0.5, core_weight=0.4,
                               coverage_weight=0.5, fragile_fucose=False, **kwargs):
        glycan_model = self.model_selectors.get_glycan_model(self)
        self.model_fit = glycan_model
        value = calculate_partial_glycan_score_no_glycosylated_peptide_coverage(
            self,
            error_tolerance,
            use_reliability,
            base_reliability,
            core_weight,
            coverage_weight,
            fragile_fucose,
            **kwargs)
        self.model_fit = None
        return value

    def peptide_coverage(self):
        return self._calculate_peptide_coverage_no_glycosylated()

    def _localization_score(self, glycosylated_weight=1, **kwargs):
        return 0


class NoGlycosylatedPeptidePartitionedPredicateTree(PartitionedPredicateTree):
    _scorer_type = NoGlycosylatedPeptidePartitionedPartialSplitScorer
    _short_peptide_scorer_type = NoGlycosylatedPeptidePartitionedPartialSplitScorer
