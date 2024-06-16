#cython: embedsignature=True
cimport cython

import numpy as np
cimport numpy as np

from libc.stdlib cimport malloc, realloc, free
from libc.math cimport fabs

from cpython.object cimport PyObject
from cpython.dict cimport PyDict_GetItem, PyDict_SetItem, PyDict_Next
from cpython.tuple cimport PyTuple_GET_ITEM, PyTuple_GET_SIZE
from cpython.sequence cimport PySequence_List
from cpython.list cimport PyList_GET_SIZE, PyList_GET_ITEM, PyList_Append, PyList_GetItem

np.import_array()

from ms_deisotope._c.peak_set cimport DeconvolutedPeak, DeconvolutedPeakSet

from glycopeptidepy._c.structure.base cimport (AminoAcidResidueBase, ModificationBase)
from glycopeptidepy._c.structure.fragment cimport (FragmentBase, PeptideFragment, IonSeriesBase)

from glycresoft._c.structure.fragment_match_map cimport (PeakFragmentPair, FragmentMatchMap, ByPeakIndexIndex)

from glycopeptidepy.structure import Modification, AminoAcidResidue
from glycopeptidepy.structure.sequence_composition import AminoAcidSequenceBuildingBlock

from collections import defaultdict

from glycopeptide_feature_learning._c.data_source cimport RankedPeak


cdef object _AminoAcidSequenceBuildingBlock = AminoAcidSequenceBuildingBlock


cdef str NOISE = "noise"
cdef int OUT_OF_RANGE_INT = 999


@cython.nonecheck(False)
@cython.cdivision(True)
cdef bint isclose(double x, double y, double rtol=1.e-5, double atol=1.e-8) nogil:
    return fabs(x-y) <= (atol + rtol * fabs(y))


DEF INTENSITY_RATIO_MIN = -4
DEF INTENSITY_RATIO_MAX = 5
DEF INTENSITY_RATIO_SIZE = abs(INTENSITY_RATIO_MIN) + INTENSITY_RATIO_MAX + 1


@cython.boundscheck(False)
@cython.wraparound(False)
cpdef int8_t[::1] make_index(match):
    cdef:
        DeconvolutedPeakSet peaks
        DeconvolutedPeak peak
        FragmentMatchMap solution_map
        ByPeakIndexIndex index
        PeakFragmentPair pfp
        object obj
        dict annotations
        PyObject* ptmp
        Py_ssize_t k
        np.npy_intp knd

        size_t i, n
        np.ndarray[int8_t, ndim=1, mode='c'] acc
        int8_t* cacc

    annotations = match.annotations
    ptmp = PyDict_GetItem(annotations, "fragmodel_peak_match_index")
    if ptmp != NULL:
        return <object>ptmp

    peaks = match.deconvoluted_peak_set
    solution_map = match.solution_map

    k = n = peaks.get_size()
    knd = k
    acc = np.PyArray_ZEROS(1, &knd, np.NPY_INT8, 0)
    cacc = &acc[0]

    for obj in solution_map.members:
        pfp = <PeakFragmentPair>obj
        cacc[pfp.peak._index.neutral_mass] = 1

    PyDict_SetItem(annotations, "fragmodel_peak_match_index", acc)
    return acc



@cython.cdivision(True)
cdef int intensity_ratio_function(DeconvolutedPeak peak1, DeconvolutedPeak peak2) nogil:
    cdef double ratio
    ratio = peak1.intensity / (peak2.intensity)
    if ratio >= 5:
        return -4
    elif 2.5 <= ratio < 5:
        return -3
    elif 1.7 <= ratio < 2.5:
        return -2
    elif 1.3 <= ratio < 1.7:
        return -1
    elif 1.0 <= ratio < 1.3:
        return 0
    elif 0.8 <= ratio < 1.0:
        return 1
    elif 0.6 <= ratio < 0.8:
        return 2
    elif 0.4 <= ratio < 0.6:
        return 3
    elif 0.2 <= ratio < 0.4:
        return 4
    elif 0. <= ratio < 0.2:
        return 5


cpdef set get_peak_index(FragmentMatchMap self):
    cdef:
        PeakFragmentPair pfp
        DeconvolutedPeak peak
        set result

    result = set()
    for obj in self.members:
        pfp = <PeakFragmentPair>obj
        peak = pfp.peak
        result.add(peak._index.neutral_mass)
    return result


@cython.freelist(100)
cdef class TargetProperties:

    @staticmethod
    cdef TargetProperties from_glycopeptide(_PeptideSequenceCore glycopeptide):
        cdef:
            TargetProperties self

        self = TargetProperties.__new__(TargetProperties)
        self.peptide_backbone_mass = glycopeptide.get_peptide_backbone_mass()
        return self


cdef class FeatureBase(object):

    cpdef list find_matches(self, DeconvolutedPeak peak, DeconvolutedPeakSet peak_list, object structure=None, TargetProperties props=None):
        raise NotImplementedError()

    def __init__(self, tolerance=2e-5, name=None, intensity_ratio=OUT_OF_RANGE_INT,
                 from_charge=OUT_OF_RANGE_INT, to_charge=OUT_OF_RANGE_INT, feature_type='',
                 terminal=''):
        self.name = str(name)
        self.tolerance = tolerance
        self.intensity_ratio = intensity_ratio
        self.from_charge = from_charge
        self.to_charge = to_charge
        self.feature_type = feature_type
        self.terminal = terminal

    def __eq__(self, FeatureBase other):
        cdef:
            bint v
        v = self.intensity_ratio == other.intensity_ratio
        if not v:
            return v
        v = self.from_charge == other.from_charge
        if not v:
            return v
        v = self.to_charge == other.to_charge
        if not v:
            return v
        v = self.feature_type == other.feature_type
        if not v:
            return v
        # v = self.terminal == other.terminal
        # if not v:
        #     return v
        return True

    def __lt__(self, FeatureBase other):
        cdef:
            bint v
            int eq_count
        eq_count = 0
        v = self.intensity_ratio <= other.intensity_ratio
        eq_count += self.intensity_ratio == other.intensity_ratio
        if not v:
            return v
        v = self.from_charge <= other.from_charge
        eq_count += self.from_charge == other.from_charge
        if not v:
            return v
        v = self.to_charge <= other.to_charge
        eq_count += self.to_charge == other.to_charge
        if not v:
            return v
        if eq_count == 3:
            return False
        return True

    def __gt__(self, FeatureBase other):
        cdef:
            bint v
            int eq_count
        eq_count = 0
        v = self.intensity_ratio >= other.intensity_ratio
        eq_count += self.intensity_ratio == other.intensity_ratio
        if not v:
            return v
        v = self.from_charge >= other.from_charge
        eq_count += self.from_charge == other.from_charge
        if not v:
            return v
        v = self.to_charge >= other.to_charge
        eq_count += self.to_charge == other.to_charge
        if not v:
            return v
        if eq_count == 3:
            return False
        return True

    def __ne__(self, other):
        return not (self == other)

    cpdef bint is_valid_match(self, size_t from_peak, size_t to_peak,
                              FragmentMatchMap solution_map, structure=None, set peak_indices=None):
        if peak_indices is not None:
            return to_peak in peak_indices
        return solution_map.by_peak_index.has_key(to_peak)

    def specialize(self, from_charge, to_charge, intensity_ratio):
        raise NotImplementedError()

    def unspecialize(self):
        raise NotImplementedError()

    def __call__(self, peak1, peak2, structure=None):
        raise NotImplementedError()

    def to_json(self):
        d = {}
        d['name'] = self.name
        d['tolerance'] = self.tolerance
        d['intensity_ratio'] = self.intensity_ratio
        d['from_charge'] = self.from_charge
        d['to_charge'] = self.to_charge
        d['feature_type'] = self.feature_type
        d['terminal'] = self.terminal
        return d

    def __reduce__(self):
        return self.__class__, (self.tolerance, self.name, self.intensity_ratio, self.from_charge,
                                self.to_charge, self.feature_type, self.terminal)

    @classmethod
    def from_json(cls, d):
        feature_type = d['feature_type']
        if feature_type == LinkFeature.get_feature_type():
            return LinkFeature.from_json(d)
        elif feature_type == ComplementFeature.get_feature_type():
            return ComplementFeature.from_json(d)
        else:
            return MassOffsetFeature.from_json(d)


cdef class MassOffsetFeature(FeatureBase):
    @classmethod
    def get_feature_type(cls):
        return ''

    cpdef bint test(self, DeconvolutedPeak peak1, DeconvolutedPeak peak2):
        return self._test(peak1, peak2)

    @cython.cdivision(True)
    cdef inline bint _test(self, DeconvolutedPeak peak1, DeconvolutedPeak peak2) nogil:
        cdef:
            double intensity_ratio
            int from_charge, to_charge
        intensity_ratio = self.intensity_ratio
        from_charge = self.from_charge
        to_charge = self.to_charge
        if (intensity_ratio == OUT_OF_RANGE_INT or
            intensity_ratio_function(peak1, peak2) == intensity_ratio) and\
           ((from_charge == OUT_OF_RANGE_INT and to_charge == OUT_OF_RANGE_INT) or
                (from_charge == peak1.charge and to_charge == peak2.charge)):

            return fabs((peak1.neutral_mass + self.offset - peak2.neutral_mass) / peak2.neutral_mass) <= self.tolerance
        return False

    cpdef list find_matches(self, DeconvolutedPeak peak, DeconvolutedPeakSet peak_list, object structure=None, TargetProperties props=None):
        cdef:
            list matches
            tuple peaks_in_range
            size_t i, n
        matches = []
        peaks_in_range = peak_list.all_peaks_for(peak.neutral_mass + self.offset, self.tolerance)
        n = PyTuple_GET_SIZE(peaks_in_range)
        for i in range(n):
            peak2 = <DeconvolutedPeak>PyTuple_GET_ITEM(peaks_in_range, i)
            if peak is not peak2 and self._test(peak, peak2):
                matches.append(peak2)
        return matches

    def __init__(self, offset, tolerance=2e-5, name=None, intensity_ratio=OUT_OF_RANGE_INT,
                 from_charge=OUT_OF_RANGE_INT, to_charge=OUT_OF_RANGE_INT, feature_type='',
                 terminal=''):
        if name is None:
            name = "F:" + str(offset)

        super(MassOffsetFeature, self).__init__(
            tolerance, name, intensity_ratio, from_charge, to_charge, feature_type,
            terminal)

        self.offset = offset
        self._init_hash()

    def _init_hash(self):
        self._hash = hash((self.offset, self.intensity_ratio, self.from_charge,
                           self.to_charge))

    def __eq__(self, other):
        if isinstance(other, MassOffsetFeature):
            v = isclose(self.offset, (<MassOffsetFeature>other).offset)
            if not v:
                return v
            return super(MassOffsetFeature, self).__eq__(other)
        return False

    def __lt__(self, other):
        cdef:
            bint v
        if isinstance(other, MassOffsetFeature):
            v = isclose(self.offset, (<MassOffsetFeature>other).offset)
            if v:
                return False
            v = self.offset < (<MassOffsetFeature>other).offset
            if not v:
                return False
            return super(MassOffsetFeature, self).__lt__(other)
        return False

    def __gt__(self, other):
        cdef:
            bint v
        if isinstance(other, MassOffsetFeature):
            v = isclose(self.offset, (<MassOffsetFeature>other).offset)
            if v:
                return False
            v = self.offset > (<MassOffsetFeature>other).offset
            if not v:
                return False
            return super(MassOffsetFeature, self).__gt__(other)
        return False

    def __hash__(self):
        return self._hash

    def __call__(self, DeconvolutedPeak peak1, DeconvolutedPeak peak2, structure=None):
        return self._test(peak1, peak2)

    def specialize(self, from_charge, to_charge, intensity_ratio):
        return self.__class__(
            self.offset, self.tolerance, self.name, intensity_ratio,
            from_charge, to_charge, self.feature_type, self.terminal)

    def unspecialize(self):
        return self.__class__(
            self.offset, self.tolerance, self.name, OUT_OF_RANGE_INT,
            OUT_OF_RANGE_INT, OUT_OF_RANGE_INT, self.feature_type, self.terminal)

    def _get_display_fields(self):
        fields = {}
        # fields['feature_type'] = self.feature_type
        fields['offset'] = self.offset
        if self.from_charge != OUT_OF_RANGE_INT:
            fields["from_charge"] = self.from_charge
        if self.to_charge != OUT_OF_RANGE_INT:
            fields['to_charge'] = self.to_charge
        if self.intensity_ratio != OUT_OF_RANGE_INT:
            fields["intensity_ratio"] = self.intensity_ratio
        terms = []
        for k, v in fields.items():
            if isinstance(v, int):
                terms.append("%s=%d" % (k, v))
            elif isinstance(v, float):
                terms.append("%s=%0.4f" % (k, v))
            else:
                terms.append("%s=%r" % (k, v))
        return terms

    def __repr__(self):
        terms = self._get_display_fields()
        return "{}(name={!r}, {})".format(
            self.__class__.__name__, self.name, ", ".join(terms))

    def to_json(self):
        d = super(MassOffsetFeature, self).to_json()
        d['offset'] = self.offset
        return d

    def __reduce__(self):
        return self.__class__, (self.offset, self.tolerance, self.name, self.intensity_ratio,
                                self.from_charge, self.to_charge, self.feature_type, self.terminal)

    @classmethod
    def from_json(cls, d):
        inst = cls(
            d['offset'], d['tolerance'], d['name'], d['intensity_ratio'],
            d['from_charge'], d['to_charge'], d['feature_type'], d['terminal'])
        return inst


cpdef list get_amino_acids_around(_PeptideSequenceCore peptide, int position, IonSeriesBase series):
    cdef:
        int length
        list result

    length = peptide.get_size()
    result = []
    if series.direction > 0:
        if position > 0:
            result.append(peptide.get(position - 1).amino_acid)
        result.append(peptide.get(position).amino_acid)
        if position < length - 2:
            result.append(peptide.get(position + 1).amino_acid)
    elif series.direction < 0:
        if position > 1:
            result.append(peptide.get(length - (position - 1)).amino_acid)
        result.append(peptide.get(length - position).amino_acid)
        if position < length - 2:
            result.append(peptide.get(length - (position + 1)).amino_acid)
    return result


@cython.final
cdef class LinkFeature(MassOffsetFeature):
    @classmethod
    def get_feature_type(cls):
        return 'link'

    def __init__(self, amino_acid, tolerance=2e-5, name=None, intensity_ratio=OUT_OF_RANGE_INT,
                 from_charge=OUT_OF_RANGE_INT, to_charge=OUT_OF_RANGE_INT, feature_type=None,
                 terminal=''):
        if feature_type is None:
            feature_type = LinkFeature.get_feature_type()
        offset = amino_acid.mass
        if name is None:
            name = str(amino_acid)
        super(LinkFeature, self).__init__(
            offset,
            tolerance,
            name,
            intensity_ratio,
            from_charge,
            to_charge,
            feature_type=feature_type)
        self.amino_acid = amino_acid

    @property
    def amino_acid(self):
        return self._amino_acid

    @amino_acid.setter
    def amino_acid(self, value):
        self._amino_acid = value
        if isinstance(value, AminoAcidResidueBase):
            self._amino_acid_residue = value
        else:
            self._amino_acid_residue = value.residue

    def specialize(self, from_charge, to_charge, intensity_ratio):
        return self.__class__(
            self.amino_acid, self.tolerance, self.name, intensity_ratio, from_charge,
            to_charge, self.feature_type, self.terminal)

    def unspecialize(self):
        return self.__class__(
            self.amino_acid, self.tolerance, self.name, OUT_OF_RANGE_INT, OUT_OF_RANGE_INT,
            OUT_OF_RANGE_INT, self.feature_type, self.terminal)

    def to_json(self):
        d = super(LinkFeature, self).to_json()
        try:
            d['amino_acid_residue'] = self.amino_acid.residue.symbol
            d['amino_acid_modification'] = [m.name for m in self.amino_acid.modifications]
        except AttributeError:
            d['amino_acid_residue'] = self.amino_acid.symbol
            d['amino_acid_modification'] = []
        return d

    @classmethod
    def from_json(cls, d):
        res = d['amino_acid_residue']
        mods = d['amino_acid_modification']
        res = AminoAcidResidue(res)
        mods = [Modification(m) for m in mods]
        amino_acid = AminoAcidSequenceBuildingBlock(res, mods)
        inst = cls(
            amino_acid, d['tolerance'], d['name'], d['intensity_ratio'],
            d['from_charge'], d['to_charge'], d['terminal'])
        return inst

    def __reduce__(self):
        return self.__class__, (self.amino_acid, self.tolerance, self.name, self.intensity_ratio,
                                self.from_charge, self.to_charge, self.feature_type, self.terminal)

    cdef bint _amino_acid_in_fragment(self, PeptideFragment fragment):
        cdef:
            bint validated_aa
            list flanking_amino_acids
            size_t j
        validated_aa = False
        flanking_amino_acids = fragment.flanking_amino_acids
        for j in range(2):
            if abs(self._amino_acid_residue.mass - (<AminoAcidResidueBase>PyList_GET_ITEM(flanking_amino_acids, j)).mass) < 1e-5:
                validated_aa = True
                break
        return validated_aa

    cdef inline bint _amino_acid_in_list(self, list aas):
        cdef:
            bint validated_aa
            list flanking_amino_acids
            size_t j, n
        validated_aa = False
        n = PyList_GET_SIZE(aas)
        for j in range(n):
            if abs(self._amino_acid_residue.mass - (<AminoAcidResidueBase>PyList_GET_ITEM(aas, j)).mass) < 1e-5:
                validated_aa = True
                break
        return validated_aa

    cpdef bint amino_acid_in_fragment(self, PeptideFragment fragment):
        return self._amino_acid_in_fragment(fragment)

    # NOTE: Overridden at inference time!
    cpdef bint is_valid_match(self, size_t from_peak, size_t to_peak,
                              FragmentMatchMap solution_map, structure=None,
                              set peak_indices=None):
        cdef:
            bint validated_aa
            list matched_fragments, flanking_amino_acids
            size_t i, n, j
            FragmentBase frag
            AminoAcidResidueBase residue


        if peak_indices is not None:
            is_peak_expected = to_peak in peak_indices
        else:
            is_peak_expected = solution_map.by_peak_index.has_key(to_peak)

        if not is_peak_expected:
            return False

        matched_fragments = solution_map.by_peak_index.getitem(from_peak)

        validated_aa = False

        residue = self._amino_acid_residue

        n = PyList_GET_SIZE(matched_fragments)
        for i in range(n):
            frag = <FragmentBase>PyList_GET_ITEM(matched_fragments, i)
            if not isinstance(frag, PeptideFragment):
                continue
            validated_aa = self._amino_acid_in_fragment(<PeptideFragment>frag)
            if validated_aa:
                break
        return validated_aa


@cython.cdivision(True)
cdef inline double ppm_error(double x, double y) nogil:
    return fabs(x - y) / y


@cython.final
cdef class ComplementFeature(MassOffsetFeature):

    @classmethod
    def get_feature_type(cls):
        return "complement"

    def __init__(self, offset, tolerance=2e-5, name=None, intensity_ratio=OUT_OF_RANGE_INT,
                 from_charge=OUT_OF_RANGE_INT, to_charge=OUT_OF_RANGE_INT, feature_type=None,
                 terminal=''):

        if not feature_type:
            feature_type = ComplementFeature.get_feature_type()
        if name is None:
            name = "Complement:" + str(offset)

        super(ComplementFeature, self).__init__(
            offset,
            tolerance,
            name,
            intensity_ratio,
            from_charge,
            to_charge,
            feature_type=feature_type,
            terminal=terminal)

    @cython.cdivision(True)
    cdef inline bint _test_relative(self, DeconvolutedPeak peak1, DeconvolutedPeak peak2, double reference_mass) nogil:
        cdef:
            double intensity_ratio
            int from_charge, to_charge
        intensity_ratio = self.intensity_ratio
        from_charge = self.from_charge
        to_charge = self.to_charge
        if (intensity_ratio == OUT_OF_RANGE_INT or
            intensity_ratio_function(peak1, peak2) == intensity_ratio) and\
           ((from_charge == OUT_OF_RANGE_INT and to_charge == OUT_OF_RANGE_INT) or
                (from_charge == peak1.charge and to_charge == peak2.charge)):

            return ppm_error(peak2.neutral_mass + peak1.neutral_mass, reference_mass) < self.tolerance
        return False

    @cython.cdivision(True)
    cpdef list find_matches(self, DeconvolutedPeak peak, DeconvolutedPeakSet peak_list, object structure=None, TargetProperties props=None):
        cdef:
            list matches
            tuple peaks_in_range
            double reference_mass, delta_mass, tolerance
            size_t i, n

        tolerance = self.tolerance
        matches = []
        if props is not None:
            reference_mass = props.peptide_backbone_mass
        elif isinstance(structure, _PeptideSequenceCore):
            reference_mass = (<_PeptideSequenceCore>structure).get_peptide_backbone_mass()
        else:
            reference_mass = structure.peptide_backbone_mass
        reference_mass += self.offset
        delta_mass = reference_mass - peak.neutral_mass

        peaks_in_range = peak_list.all_peaks_for(delta_mass, 2 * tolerance)
        n = PyTuple_GET_SIZE(peaks_in_range)
        for i in range(n):
            peak2 = <DeconvolutedPeak>PyTuple_GET_ITEM(peaks_in_range, i)
            # if peak is not peak2 and self._test_relative(peak, peak2, reference_mass):
            if peak is not peak2 and ppm_error(peak2.neutral_mass + peak.neutral_mass, reference_mass) < self.tolerance:
                matches.append(peak2)
        return matches


cdef class FittedFeatureBase(object):

    cpdef list find_matches(self, DeconvolutedPeak peak, DeconvolutedPeakSet peak_list, structure=None, TargetProperties props=None):
        result = self.feature.find_matches(peak, peak_list, structure, props)
        return result

    cpdef bint is_valid_match(self, size_t from_peak, size_t to_peak,
                              FragmentMatchMap solution_map, structure=None, set peak_indices=None):
        return self.feature.is_valid_match(from_peak, to_peak, solution_map, structure, peak_indices)

    @cython.cdivision(True)
    cpdef double _feature_probability(self, double p=0.5):
        return (p * self.on_series) / (
            (p * self.on_series) + ((1 - p) * self.off_series))


cdef class FeatureFunctionEstimatorBase(object):
    cpdef match_peaks(self, gpsm, DeconvolutedPeakSet peaks, int min_rank=1):
        cdef:
            list related, matches, fragments
            FragmentMatchMap solution_map
            RankedPeak peak, match

            size_t i_peaks, n_peaks, i_fragments, n_fragments, i_matches, n_matches
            bint is_on_series, is_match_expected
            PeakRelation pr
            FragmentBase k
            TargetProperties props
            set peak_index_set
            _PeptideSequenceCore structure

        related = []

        n_peaks = peaks.get_size()

        solution_map = gpsm.solution_map
        structure = gpsm.structure

        props = TargetProperties.from_glycopeptide(structure)
        peak_index_set = get_peak_index(solution_map)

        if n_peaks == 0:
            return
        elif not isinstance(peaks.getitem(0), RankedPeak):
            raise TypeError("Must provide RankedPeak instances")

        for i_peaks in range(n_peaks):
            peak = <RankedPeak>peaks.getitem(i_peaks)
            if peak.rank < min_rank:
                continue

            fragments = solution_map.by_peak_index.getitem(peak._index.neutral_mass)
            n_fragments = PyList_GET_SIZE(fragments)
            is_on_series = False
            for i_fragments in range(n_fragments):
                k = <FragmentBase>PyList_GET_ITEM(fragments, i_fragments)
                if k.get_series().int_code == self.series.int_code:
                    is_on_series = True
                    break

            matches = self.feature_function.find_matches(peak, peaks, structure, props)
            n_matches = PyList_GET_SIZE(matches)
            for i_matches in range(n_matches):
                match = <RankedPeak>PyList_GET_ITEM(matches, i_matches)
                if peak is match or match.rank < min_rank:
                    continue

                pr = None
                if self.track_relations:
                    pr = PeakRelation._create(peak, match, self.feature_function, None)
                    related.append(pr)

                is_match_expected = self.feature_function.is_valid_match(
                    peak._index.neutral_mass,
                    match._index.neutral_mass,
                    solution_map,
                    structure,
                    peak_index_set
                )
                if is_on_series and is_match_expected:
                    self.total_on_series_satisfied += 1
                    if self.track_relations:
                        pr.series = self.series
                else:
                    self.total_off_series_satisfied += 1
                    if self.track_relations:
                        pr.series = NOISE
            if is_on_series:
                self.total_on_series += 1
            else:
                self.total_off_series += 1
        if len(related) > 0 and self.track_relations:
            self.peak_relations.append((gpsm, related))


cdef class FragmentationFeatureBase(object):

    cpdef list find_matches(self, DeconvolutedPeak peak, DeconvolutedPeakSet peak_list, structure=None, TargetProperties props=None):
        cdef:
            list matches, pairs
            DeconvolutedPeak match
            tuple key
            size_t i, n
            PyObject* ptemp
            FeatureBase fit

        matches = self.feature.find_matches(peak, peak_list, structure, props)
        pairs = []
        n = PyList_GET_SIZE(matches)
        for i in range(n):
            match = <DeconvolutedPeak>PyList_GET_ITEM(matches, i)
            rel = PeakRelation._create(peak, match, None, self.series)
            key = (rel.intensity_ratio, rel.from_charge, rel.to_charge)
            ptemp = PyDict_GetItem(self.fits, key)
            if ptemp != NULL:
                fit = <FeatureBase>ptemp
                rel.feature = fit
                pairs.append(rel)

        return pairs

    cpdef bint is_valid_match(self, size_t from_peak, size_t to_peak,
                              FragmentMatchMap solution_map, structure=None, set peak_indices=None):
        return self.feature.is_valid_match(from_peak, to_peak, solution_map, structure, peak_indices)


cdef class FragmentationModelBase(object):

    cdef size_t get_size(self):
        return PyList_GET_SIZE(self.feature_table)

    cpdef find_matches(self, scan, FragmentMatchMap solution_map, structure, TargetProperties props=None):
        cdef:
            object matches_to_features
            DeconvolutedPeakSet deconvoluted_peak_set
            PeakFragmentPair peak_fragment
            PeakRelation rel
            DeconvolutedPeak peak
            FragmentBase fragment
            FragmentationFeatureBase feature
            list rels
            size_t i, n, j, k

        matches_to_features = defaultdict(list)
        deconvoluted_peak_set = <DeconvolutedPeakSet>scan.deconvoluted_peak_set
        n = self.get_size()

        for obj in solution_map.members:
            peak_fragment = <PeakFragmentPair>obj
            peak = peak_fragment.peak
            fragment = peak_fragment.fragment
            if fragment.get_series().name != self.series.name:
                continue
            for i in range(n):
                feature = <FragmentationFeatureBase>PyList_GET_ITEM(self.feature_table, i)
                rels = feature.find_matches(peak, deconvoluted_peak_set, structure, props)
                k = PyList_GET_SIZE(rels)
                for j in range(k):
                    rel = <PeakRelation>PyList_GET_ITEM(rels, j)
                    if feature.is_valid_match(rel.from_peak._index.neutral_mass, rel.to_peak._index.neutral_mass, solution_map, structure):
                        matches_to_features[rel.from_peak._index.neutral_mass].append(rel)
                        matches_to_features[rel.to_peak._index.neutral_mass].append(rel)
        return matches_to_features

    @cython.cdivision(True)
    @cython.nonecheck(False)
    cpdef double _score_peak(self, DeconvolutedPeak peak, list matched_features, FragmentMatchMap solution_map, structure):
        cdef:
            double gamma, a, b
            double max_probability, current_probability

            list relations, acc, groups
            PeakRelation relation, best_relation
            FittedFeatureBase feature
            PyObject* ptemp
            PyObject* pvalue
            Py_ssize_t pos
            dict grouped_features

            size_t i, j, n, m

        gamma = self.offset_probability
        a = 1.0
        b = 1.0
        n = PyList_GET_SIZE(matched_features)
        if n == 0:
            return (gamma * a) / ((gamma * a) + ((1 - gamma) * b))
        grouped_features = dict()
        for i in range(n):
            relation = <PeakRelation>PyList_GET_ITEM(matched_features, i)
            key = relation.peak_key()
            ptemp = PyDict_GetItem(grouped_features, key)
            if ptemp == NULL:
                acc = []
                PyDict_SetItem(grouped_features, key, acc)
            else:
                acc = <list>ptemp
            PyList_Append(acc, relation)

        pos = 0
        while PyDict_Next(grouped_features, &pos, &ptemp, &pvalue):
            relations = <list>pvalue
            m = PyList_GET_SIZE(relations)
            max_probability = 0
            best_relation = None
            for j in range(m):
                relation = <PeakRelation>PyList_GET_ITEM(relations, j)
                feature = <FittedFeatureBase>relation.feature
                current_probability = feature._feature_probability(gamma)
                if current_probability > max_probability:
                    max_probability = current_probability
                    best_relation = relation
            relation = best_relation
            feature = <FittedFeatureBase>relation.feature
            if feature.on_series == 0:
                continue
            a *= feature.on_series
            b *= feature.off_series
        return (gamma * a) / ((gamma * a) + ((1 - gamma) * b))


cdef list get_item_default_list(dict d, object key):
    cdef:
        PyObject* ptemp
        list result
    ptemp = PyDict_GetItem(d, key)
    if ptemp == NULL:
        result = []
        PyDict_SetItem(d, key, result)
        return result
    result = <list>ptemp
    return result


cdef class FragmentationModelCollectionBase(object):

    cpdef dict find_matches(self, scan, FragmentMatchMap solution_map, structure, TargetProperties props=None):
        cdef:
            dict match_to_features, models

            set peak_index_set
            DeconvolutedPeakSet deconvoluted_peak_set
            DeconvolutedPeak peak

            bint is_peptide_fragment, is_link, is_valid
            PeakFragmentPair peak_fragment
            FragmentBase fragment
            IonSeriesBase fragment_series

            FragmentationModelBase model
            FragmentationFeatureBase feature

            PeakRelation rel
            list rels, surrounding_aas

            PyObject* ptemp
            size_t i, n, j, k

        match_to_features = dict()
        deconvoluted_peak_set = scan.deconvoluted_peak_set
        models = self.models

        peak_index_set = get_peak_index(solution_map)

        for obj in solution_map.members:
            peak_fragment = <PeakFragmentPair>obj
            peak = peak_fragment.peak
            fragment = peak_fragment.fragment
            fragment_series = fragment.get_series()
            is_peptide_fragment = isinstance(fragment, PeptideFragment)
            surrounding_aas = None
            ptemp = PyDict_GetItem(models, fragment_series)
            if ptemp == NULL:
                continue
            model = <FragmentationModelBase>ptemp
            n = model.get_size()
            for i in range(n):
                feature = <FragmentationFeatureBase>PyList_GET_ITEM(model.feature_table, i)
                is_link = isinstance(feature.feature, LinkFeature)
                if is_link and is_peptide_fragment:
                    if surrounding_aas is None:
                        surrounding_aas = get_amino_acids_around(
                            <_PeptideSequenceCore>structure,
                            (<PeptideFragment>peak_fragment.fragment).position,
                            fragment_series
                        )

                    if not (<LinkFeature>feature.feature)._amino_acid_in_list(surrounding_aas):
                        continue

                rels = feature.find_matches(peak, deconvoluted_peak_set, structure, props)
                k = PyList_GET_SIZE(rels)
                for j in range(k):
                    rel = <PeakRelation>PyList_GET_ITEM(rels, j)
                    if is_link:
                        is_valid = MassOffsetFeature.is_valid_match(
                            feature.feature,
                            rel.from_peak._index.neutral_mass,
                            rel.to_peak._index.neutral_mass,
                            solution_map,
                            structure,
                            peak_index_set
                        )
                    else:
                        is_valid = feature.feature.is_valid_match(
                            rel.from_peak._index.neutral_mass,
                            rel.to_peak._index.neutral_mass,
                            solution_map,
                            structure,
                            peak_index_set
                        )
                    if is_valid:
                        PyList_Append(
                            get_item_default_list(match_to_features, rel.from_peak._index.neutral_mass),
                            rel)
                        PyList_Append(
                            get_item_default_list(match_to_features, rel.to_peak._index.neutral_mass),
                            rel)
        return match_to_features

    cpdef dict score(self, scan, FragmentMatchMap solution_map, structure):
        cdef:
            dict match_to_features

            PeakFragmentPair peak_fragment
            PeakRelation rel
            TargetProperties props

            DeconvolutedPeak peak
            FragmentBase fragment

            FragmentationFeatureBase feature

            FragmentationModelBase model

            list features
            dict fragment_probabilities
            dict models

            PyObject* ptemp
            size_t i, n, j, k
        models = self.models
        props = TargetProperties.from_glycopeptide(structure)
        match_to_features = self.find_matches(scan, solution_map, structure, props)
        fragment_probabilities = {}
        for obj in solution_map.members:
            peak_fragment = <PeakFragmentPair>obj
            peak = peak_fragment.peak
            fragment = <FragmentBase>peak_fragment.fragment

            ptemp = PyDict_GetItem(models, fragment.get_series())
            if ptemp == NULL:
                continue
            model = <FragmentationModelBase>ptemp

            ptemp = PyDict_GetItem(match_to_features, peak._index.neutral_mass)
            if ptemp == NULL:
                features = EMPTY_LIST
            else:
                features = <list>ptemp
            PyDict_SetItem(
                fragment_probabilities,
                peak_fragment,
                model._score_peak(peak, features, solution_map, structure))
        return fragment_probabilities


cdef list EMPTY_LIST = []


@cython.freelist(100000)
@cython.final
cdef class PeakRelation(object):

    def __init__(self, DeconvolutedPeak from_peak, DeconvolutedPeak to_peak, feature, intensity_ratio=None, series=None):
        cdef:
            int intensity_ratio_
        if intensity_ratio is None:
            intensity_ratio_ = intensity_ratio_function(from_peak, to_peak)
        else:
            intensity_ratio_ = intensity_ratio
        if series is None:
            series = NOISE
        self.from_peak = from_peak
        self.to_peak = to_peak
        self.feature = feature
        self.intensity_ratio = intensity_ratio_
        self.from_charge = from_peak.charge
        self.to_charge = to_peak.charge
        self.series = series

    def __reduce__(self):
        return self.__class__, (self.from_peak, self.to_peak, self.feature, self.intensity_ratio, self.series)

    def __eq__(self, PeakRelation other):
        cdef:
            bint v
        if other is None:
            return False
        v = self.from_peak._eq(other.from_peak)
        if not v:
            return v
        v = self.to_peak._eq(other.to_peak)
        if not v:
            return v
        v = self.feature == other.feature
        if not v:
            return v
        v = self.intensity_ratio == other.intensity_ratio
        if not v:
            return v
        v = self.from_charge == other.from_charge
        if not v:
            return v
        v = self.to_charge == other.to_charge
        if not v:
            return v
        v = self.series == other.series
        if not v:
            return v
        return True

    def __ne__(self, other):
        return not (self == other)

    def __lt__(self, PeakRelation other):
        cdef:
            bint v
        v = self.from_peak.neutral_mass < other.from_peak.neutral_mass
        if not v:
            return v
        v = self.to_peak.neutral_mass < other.to_peak.neutral_mass
        if not v:
            return v
        v = self.from_charge < other.from_charge
        if not v:
            return v
        v = self.to_charge < other.to_charge
        if not v:
            return v
        v = self.intensity_ratio < other.intensity_ratio
        if not v:
            return v
        return True

    def __gt__(self, PeakRelation other):
        cdef:
            bint v
        v = self.from_peak.neutral_mass > other.from_peak.neutral_mass
        if not v:
            return v
        v = self.to_peak.neutral_mass > other.to_peak.neutral_mass
        if not v:
            return v
        v = self.from_charge > other.from_charge
        if not v:
            return v
        v = self.to_charge > other.to_charge
        if not v:
            return v
        v = self.intensity_ratio > other.intensity_ratio
        if not v:
            return v
        return True

    def __repr__(self):
        cdef:
            str template
        template = "<PeakRelation {s.from_peak.neutral_mass}({s.from_charge}) ->" +\
            " {s.to_peak.neutral_mass}({s.to_charge}) by {s.feature.name} on {s.series}>"
        return template.format(s=self)

    cpdef tuple peak_key(self):
        if self.from_peak._index.neutral_mass < self.to_peak._index.neutral_mass:
            return self.from_peak._index.neutral_mass, self.to_peak._index.neutral_mass
        else:
            return self.to_peak._index.neutral_mass, self.from_peak._index.neutral_mass

    @staticmethod
    cdef PeakRelation _create(DeconvolutedPeak from_peak, DeconvolutedPeak to_peak, feature, IonSeriesBase series):
        cdef PeakRelation self = PeakRelation.__new__(PeakRelation)
        self.from_peak = from_peak
        self.to_peak = to_peak
        self.feature = feature

        self.intensity_ratio = intensity_ratio_function(from_peak, to_peak)

        self.from_charge = from_peak.charge
        self.to_charge = to_peak.charge

        if series is None:
            self.series = NOISE
        else:
            self.series = series

        return self


cdef int create_partitioned_fit_table(uint16_t p1_charge_max, uint16_t p2_charge_max, partitioned_fit_table_t* destination) nogil:
    cdef:
        size_t size_total, p1_i, p2_i
        size_t step_1, step_2
        int16_t ir_i
        feature_fit_t* fit_state

    size_total = (<size_t>p1_charge_max) * (<size_t>p2_charge_max) * (<size_t>INTENSITY_RATIO_SIZE)
    destination.p1_charge_max = p1_charge_max
    destination.p2_charge_max = p2_charge_max
    destination.size = size_total
    destination.fits = <feature_fit_t*>malloc(size_total * sizeof(feature_fit_t))
    if destination.fits == NULL:
        return 1
    step_1 = (<size_t>p2_charge_max) * INTENSITY_RATIO_SIZE
    step_2 = INTENSITY_RATIO_SIZE
    for p1_i in range(p1_charge_max):
        for p2_i in range(p2_charge_max):
            for ir_i in range(INTENSITY_RATIO_SIZE):
                fit_state = &destination.fits[p1_i * step_1 + p2_i * step_2 + ir_i]
                fit_state.partition.from_charge = p1_i + 1 # Looping starting at 0, but labeling starting from 1
                fit_state.partition.to_charge = p2_i + 1
                fit_state.partition.intensity_ratio = ir_i + INTENSITY_RATIO_MIN # Addition of a negative
                fit_state.on_count = 0
                fit_state.off_count = 0
                fit_state.on_series = 0.0
                fit_state.off_series = 0.0
    return 0


cdef size_t compute_partition_offset(partitioned_fit_table_t* self, uint16_t from_charge, uint16_t to_charge, int16_t intensity_ratio) nogil:
    cdef:
        size_t i, step_1, step_2
    if intensity_ratio == OUT_OF_RANGE_INT:
        intensity_ratio = INTENSITY_RATIO_MIN
    step_1 = (<size_t>self.p2_charge_max) * INTENSITY_RATIO_SIZE
    step_2 = INTENSITY_RATIO_SIZE
    i = step_1 * <size_t>(from_charge - 1) # Indexing starting at 0, but labeling starting from 1
    i += step_2 * <size_t>(to_charge - 1)
    i += intensity_ratio - INTENSITY_RATIO_MIN # Subtraction of a negative
    return i


cdef feature_fit_t* partitioned_fit_table_get(partitioned_fit_table_t* self, uint16_t from_charge, uint16_t to_charge, int16_t intensity_ratio) nogil:
    cdef:
        size_t i
    i = compute_partition_offset(self, from_charge, to_charge, intensity_ratio)
    if i >= self.size:
        return NULL
    return &self.fits[i]

cdef feature_fit_t* partitioned_fit_table_get_partition(partitioned_fit_table_t* self, partition_t* partition) nogil:
    cdef:
        size_t i
    i = compute_partition_offset(self, partition.from_charge, partition.to_charge, partition.intensity_ratio)
    if i >= self.size:
        return NULL
    return &self.fits[i]


def _test_partition_table():
    cdef:
        uint16_t from_charge, to_charge
        size_t size_total, p1_i, p2_i
        int16_t ir_i
        size_t step_1, step_2
        feature_fit_t* fit_state
        partitioned_fit_table_t self
    from_charge = 5
    to_charge = 5
    assert create_partitioned_fit_table(from_charge, to_charge, &self) == 0

    for p1_i in range(1, from_charge + 1):
        for p2_i in range(1, to_charge + 1):
            for ir_i in range(INTENSITY_RATIO_MIN, INTENSITY_RATIO_MAX + 1):
                fit_state = partitioned_fit_table_get(&self, p1_i, p2_i, ir_i)
                assert fit_state != NULL
                assert fit_state.partition.from_charge == p1_i
                assert fit_state.partition.to_charge == p2_i
                assert fit_state.partition.intensity_ratio == ir_i
