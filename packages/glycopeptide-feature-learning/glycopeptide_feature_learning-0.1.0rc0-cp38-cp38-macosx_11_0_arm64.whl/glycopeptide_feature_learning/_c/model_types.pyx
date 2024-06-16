# cython: embedsignature=True
cimport cython
from cpython cimport PyTuple_GetItem, PyTuple_Size, PyList_GET_ITEM, PyList_GET_SIZE, PySet_Size, PyTuple_GET_ITEM
from cpython cimport PyDict_GetItem, PyDict_SetItem, PyObject
from cpython.int cimport PyInt_AsLong, PyInt_FromLong
from libc.stdlib cimport malloc, calloc, free
from libc.math cimport log10, log, sqrt, exp

import numpy as np
cimport numpy as np

np.import_array()

from numpy.math cimport isnan

import six
from collections import OrderedDict

from ms_deisotope._c.peak_set cimport DeconvolutedPeak, DeconvolutedPeakSet

from brainpy._c.double_vector cimport (
    DoubleVector as dvec,
    make_double_vector,
    make_double_vector_with_size,
    free_double_vector,
    double_vector_append,
    double_vector_to_list)

from glycresoft._c.structure.fragment_match_map cimport (
    FragmentMatchMap, PeakFragmentPair)

from glycopeptidepy._c.structure.base cimport AminoAcidResidueBase, SequencePosition
from glycopeptidepy._c.structure.sequence_methods cimport _PeptideSequenceCore
from glycopeptidepy._c.structure.fragment cimport (
    PeptideFragment, FragmentBase, StubFragment,
    IonSeriesBase, ChemicalShiftBase)
from glycopeptidepy._c.structure.glycan cimport GlycosylationManager

from glypy.utils.enum import Enum
from glypy.utils.cenum cimport EnumValue, IntEnumValue, EnumMeta
from glypy.structure.glycan_composition import FrozenMonosaccharideResidue
from glypy._c.structure.glycan_composition cimport _CompositionBase

from glycresoft.tandem.glycopeptide.core_search import approximate_internal_size_of_glycan

from glycopeptidepy.structure.fragment import IonSeries


from glycopeptide_feature_learning.amino_acid_classification import (
    AminoAcidClassification)
from glycopeptide_feature_learning._c.amino_acid_classification cimport (
    classify_residue_frank, classify_amide_bond_frank)

cdef:
    IonSeriesBase IonSeries_b, IonSeries_y, IonSeries_c, IonSeries_z, IonSeries_stub_glycopeptide, IonSeries_oxonium

IonSeries_b = IonSeries.b
IonSeries_y = IonSeries.y
IonSeries_c = IonSeries.c
IonSeries_z = IonSeries.z
IonSeries_stub_glycopeptide = IonSeries.stub_glycopeptide
IonSeries_oxonium = IonSeries.oxonium_ion


@six.add_metaclass(EnumMeta)
class FragmentSeriesClassification(object):
    __enum_type__ = IntEnumValue

    b = 0
    y = 1
    stub_glycopeptide = 2
    unassigned = 3


# the number of ion series to consider is one less than the total number of series
# because unassigned is a special case which no matched peaks will receive
cdef int FragmentSeriesClassification_max = max(filter(lambda x: x[1].value is not None, FragmentSeriesClassification),
                                                key=lambda x: x[1].value)[1].value - 1

# the number of backbone ion series to consider is two less because the stub_glycopeptide
# series is not a backbone fragmentation series
cdef int BackboneFragmentSeriesClassification_max = FragmentSeriesClassification_max - 1


cdef int AminoAcidClassification_max = max(filter(lambda x: x[1].value is not None, AminoAcidClassification),
                                           key=lambda x: x[1].value)[1].value


class FragmentTypeClassification(AminoAcidClassification):
    pass

cdef EnumValue FragmentTypeClassification_pro = FragmentTypeClassification.pro


cdef int FragmentTypeClassification_max = max(filter(lambda x: x[1].value is not None, FragmentTypeClassification),
                                              key=lambda x: x[1].value)[1].value

# consider fragments with up to 2 monosaccharides attached to a backbone fragment
cdef int BackboneFragment_max_glycosylation_size = 2
# consider fragments of up to charge 4+
cdef int FragmentCharge_max = 4
# consider up to 14 monosaccharides of glycan still attached to a stub ion
cdef int StubFragment_max_glycosylation_size = 14

cdef int StubFragment_max_labile_monosaccharides = 6

cdef:
    EnumValue FragmentSeriesClassification_unassigned = FragmentSeriesClassification.unassigned
    EnumValue FragmentSeriesClassification_stub_glycopeptide = FragmentSeriesClassification.stub_glycopeptide
    EnumValue FragmentSeriesClassification_b = FragmentSeriesClassification.b
    EnumValue FragmentSeriesClassification_y = FragmentSeriesClassification.y


cpdef int get_nterm_index_from_fragment(PeptideFragment fragment, _PeptideSequenceCore structure):
    cdef:
        IonSeriesBase series
        size_t size
        int direction, index

    series = fragment.get_series()
    size = structure.get_size()
    direction = series.direction
    if direction < 0:
        index = size + (direction * fragment.position + direction)
    else:
        index = fragment.position - 1
    return index


cpdef int get_cterm_index_from_fragment(PeptideFragment fragment, _PeptideSequenceCore structure):
    cdef:
        IonSeriesBase series
        size_t size
        int direction, index

    series = fragment.get_series()
    size = structure.get_size()
    direction = series.direction
    if direction < 0:
        index = size + (series.direction * fragment.position)
    else:
        index = fragment.position
    return index


cdef class _FragmentType(object):

    @staticmethod
    cdef _FragmentType _create(type fragment_type, EnumValue nterm, EnumValue cterm, EnumValue series, int glycosylated, int charge, PeakFragmentPair peak_pair, _PeptideSequenceCore sequence):
        cdef _FragmentType self = <_FragmentType>fragment_type.__new__(fragment_type)
        self.nterm = nterm
        self.cterm = cterm
        self.series = series
        self.glycosylated = glycosylated
        self.charge = charge
        self.peak_pair = peak_pair
        self.sequence = sequence

        cdef int series_int = self.series.int_value()

        self._is_assigned = (series_int != FragmentSeriesClassification_unassigned.int_value())
        self._is_stub_glycopeptide = (self._is_assigned and series_int == FragmentSeriesClassification_stub_glycopeptide.int_value())
        self._is_backbone = (self._is_assigned and series_int != FragmentSeriesClassification_stub_glycopeptide.int_value())
        return self

    def __init__(self, nterm, cterm, series, glycosylated, charge, peak_pair, sequence):
        self.nterm = nterm
        self.cterm = cterm
        self.series = series
        self.glycosylated = glycosylated
        self.charge = charge
        self.peak_pair = peak_pair
        self.sequence = sequence

        self._is_assigned = (self.series != FragmentSeriesClassification_unassigned)
        self._is_stub_glycopeptide = (self._is_assigned and self.series == FragmentSeriesClassification_stub_glycopeptide)
        self._is_backbone = (self._is_assigned and self.series != FragmentSeriesClassification_stub_glycopeptide)

    def __iter__(self):
        yield self.nterm
        yield self.cterm
        yield self.series
        yield self.glycosylated
        yield self.charge
        yield self.peak_pair
        yield self.sequence

    def __getitem__(self, int i):
        if i == 0:
            return self.nterm
        elif i == 1:
            return self.cterm
        elif i == 2:
            return self.series
        elif i == 3:
            return self.glycosylated
        elif i == 4:
            return self.charge
        elif i == 5:
            return self.peak_pair
        elif i == 6:
            return self.sequence
        else:
            raise IndexError(i)

    cdef DeconvolutedPeak get_peak(self):
        return self.peak_pair.peak

    cdef FragmentBase get_fragment(self):
        return self.peak_pair.fragment

    @property
    def peak(self):
        if self.peak_pair is None:
            raise ValueError("Does not represent a peak-fragment match!")
        return self.get_peak()

    @property
    def fragment(self):
        if self.peak_pair is None:
            raise ValueError("Does not represent a peak-fragment match!")
        return self.get_fragment()

    cpdef bint is_assigned(self):
        return self._is_assigned

    cpdef bint is_backbone(self):
        return self._is_backbone

    cpdef bint is_stub_glycopeptide(self):
        return self._is_stub_glycopeptide

    def __str__(self):
        return '(%s, %s, %s, %r, %r)' % (
            self[0].name if self[0] else '',
            self[1].name if self[1] else '',
            self[2].name, self[3], self[4])

    def __repr__(self):
        peak_pair = self.peak_pair
        if peak_pair is None:
            return "{self.__class__.__name__}(Unassigned)".format(self=self)
        else:
            return "{self.__class__.__name__}({self.fragment.name}, {self.peak.charge})".format(self=self)

    cdef long get_feature_count(self):
        return PyInt_AsLong(type(self).feature_count)

    cpdef np.ndarray[feature_dtype_t, ndim=1, mode='c'] _allocate_feature_array(self):
        cdef:
            Py_ssize_t k
            np.npy_intp knd

        k = self.get_feature_count()
        knd = k
        return np.PyArray_ZEROS(1, &knd, np.NPY_UINT8, 0)

    cpdef np.ndarray[feature_dtype_t, ndim=1, mode='c'] as_feature_vector(self, dict context=None):
        cdef:
            np.ndarray[feature_dtype_t, ndim=1] X
            size_t offset
        X = self._allocate_feature_array()
        offset = 0
        self.build_feature_vector(X, offset, context)
        return X

    @cython.boundscheck(False)
    @cython.wraparound(False)
    cpdef Py_ssize_t build_feature_vector(self, feature_dtype_t[::1] X, Py_ssize_t offset, dict context=None):
        cdef:
            Py_ssize_t k_ftypes, k_series, k_unassigned, k_charge
            Py_ssize_t k_charge_series, k_glycosylated, k, index

        k_ftypes = (FragmentTypeClassification_max + 1)
        k_series = (FragmentSeriesClassification_max + 1)
        k_unassigned = 1
        k_charge = FragmentCharge_max + 1
        k_charge_series = k_charge * k_series

        k_glycosylated = BackboneFragment_max_glycosylation_size + 1

        k = (
            (k_ftypes * 2) + k_series + k_unassigned + k_charge + k_charge_series +
            k_glycosylated)

        if self.nterm is not None:
            X[self.nterm.int_value()] = 1
        offset += k_ftypes

        if self.cterm is not None:
            X[offset + self.cterm.int_value()] = 1
        offset += k_ftypes

        if self._is_assigned:
            X[offset + self.series.int_value()] = 1
        offset += k_series

        # track the unassigned placeholder observation separately
        X[offset] = int(not self._is_assigned)
        offset += k_unassigned

        # use charge - 1 because there is no 0 charge
        if self._is_backbone:
            X[offset + (self.charge - 1)] = 1
        offset += k_charge

        if self._is_assigned:
            index = (self.series.int_value() * k_charge) + (self.charge - 1)
            X[offset + index] = 1
        offset += k_charge_series

        # non-stub ion glycosylation
        if self._is_backbone:
            X[offset + (<PeptideFragment>self.peak_pair.fragment).get_glycosylation_size()] = 1
        offset += k_glycosylated
        return offset


@cython.binding(True)
@cython.boundscheck(False)
@cython.wraparound(False)
cpdef np.ndarray[feature_dtype_t, ndim=2, mode='c'] encode_classification(cls, list classification):
    cdef:
        size_t i, n, j, k
        _FragmentType row
        np.npy_intp[2] knd
        np.ndarray[feature_dtype_t, ndim=2, mode='c'] X
        feature_dtype_t[:, ::1] Xview
        dict context_cache

    context_cache = {}
    n = PyList_GET_SIZE(classification)
    if n == 0:
        k = 0
        knd[0] = n
        knd[1] = k
        return np.PyArray_ZEROS(2, knd, np.NPY_UINT8, 0)
    i = 0
    row = <_FragmentType>PyList_GET_ITEM(classification, i)

    k = row.get_feature_count()
    knd[0] = n
    knd[1] = k
    X = <np.ndarray[feature_dtype_t, ndim=2, mode='c']>np.PyArray_ZEROS(2, knd, np.NPY_UINT8, 0)
    Xview = X
    row.build_feature_vector(Xview[i, :], 0, context_cache)
    for i in range(1, n):
        row = <_FragmentType>PyList_GET_ITEM(classification, i)
        row.build_feature_vector(Xview[i, :], 0, context_cache)
    return X


cdef EnumValue encode_peptide_fragment_series(IonSeriesBase series):
    if series.int_code == IonSeries_b.int_code:
        return FragmentSeriesClassification_b
    elif series.int_code == IonSeries_y.int_code:
        return FragmentSeriesClassification_y
    else:
        raise KeyError(series.name)


@cython.binding(True)
cpdef from_peak_peptide_fragment_pair(cls, PeakFragmentPair peak_fragment_pair, _PeptideSequenceCore structure):
    cdef:
        DeconvolutedPeak peak
        PeptideFragment fragment
        tuple terms
        EnumValue nterm, cterm

    peak = peak_fragment_pair.peak
    fragment = peak_fragment_pair.fragment
    residue = <object>PyList_GET_ITEM(fragment.flanking_amino_acids, 0)
    residue2 = <object>PyList_GET_ITEM(fragment.flanking_amino_acids, 1)
    terms = classify_amide_bond_frank(residue, residue2)
    nterm = <EnumValue>PyTuple_GET_ITEM(terms, 0)
    cterm = <EnumValue>PyTuple_GET_ITEM(terms, 1)
    glycosylation = fragment._is_glycosylated()

    inst = _FragmentType._create(
        <type>cls,
        nterm,
        cterm,
        encode_peptide_fragment_series(fragment.get_series()),
        glycosylation,
        min(peak.charge, FragmentCharge_max + 1),
        peak_fragment_pair,
        structure
    )
    return inst

@cython.binding(True)
cpdef build_fragment_intensity_matches(cls, gpsm, bint include_unassigned_sum=True):

    cdef:
        list fragment_classification
        np.ndarray[double, ndim=1] intensities
        dvec* intensities_acc
        set counted
        double matched_total, total, unassigned, normalized, peak_intensity
        FragmentMatchMap solution_map
        PeakFragmentPair peak_fragment_pair
        DeconvolutedPeak peak
        DeconvolutedPeakSet peak_set
        FragmentBase fragment
        IonSeriesBase series
        _PeptideSequenceCore structure
        int glycosylation_size
        size_t i
        np.npy_intp n

    fragment_classification = []

    matched_total = 0
    peak_set = gpsm.deconvoluted_peak_set
    total = 0
    for i in range(peak_set.get_size()):
        peak = peak_set.getitem(i)
        total += peak.intensity

    structure = gpsm.target
    counted = set()
    solution_map = <FragmentMatchMap>gpsm.solution_map
    if solution_map is None:
        gpsm.match()
        solution_map = <FragmentMatchMap>gpsm.solution_map

    intensities_acc = make_double_vector_with_size(PySet_Size(solution_map.members))

    for peak_fragment_pair in solution_map.members:
        peak = peak_fragment_pair.peak
        fragment = peak_fragment_pair.fragment

        if peak._index.neutral_mass not in counted:
            matched_total += peak.intensity
            counted.add(peak._index.neutral_mass)

        series = fragment.get_series()
        if series.int_code == IonSeries_oxonium.int_code:
            continue

        double_vector_append(intensities_acc, peak.intensity)
        # intensities_acc.append(peak)
        if series.int_code == IonSeries_stub_glycopeptide.int_code:
            glycosylation_size = (<StubFragment>fragment).get_glycosylation_size()
            fragment_classification.append(
                _FragmentType._create(
                    <type>cls,
                    None,
                    None,
                    FragmentSeriesClassification_stub_glycopeptide,
                    min(glycosylation_size, StubFragment_max_glycosylation_size),
                    min(peak.charge, FragmentCharge_max + 1),
                    peak_fragment_pair,
                    structure
                )
            )
        else:
            inst = from_peak_peptide_fragment_pair(cls, peak_fragment_pair, structure)
            fragment_classification.append(inst)

    normalized = 0.0
    if include_unassigned_sum:
        # n = PyList_GET_SIZE(intensities_acc) + 1
        n = intensities_acc.used + 1
        intensities = np.PyArray_ZEROS(1, &n, np.NPY_DOUBLE, 0)
        for i in range(n - 1):
            # peak = <DeconvolutedPeak>PyList_GET_ITEM(intensities_acc, i)
            peak_intensity = intensities_acc.v[i]
            intensities[i] = peak_intensity
            normalized += peak_intensity

        unassigned = total - matched_total
        intensities[n - 1] = (unassigned)
        normalized += unassigned
        ft = cls(None, None, FragmentSeriesClassification_unassigned, 0, 0, None, None)
        fragment_classification.append(ft)
    else:
        # n = PyList_GET_SIZE(intensities_acc)
        n = intensities_acc.used
        intensities = np.PyArray_ZEROS(1, &n, np.NPY_DOUBLE, 0)
        for i in range(n):
            # peak = <DeconvolutedPeak>PyList_GET_ITEM(intensities_acc, i)
            peak_intensity = intensities_acc.v[i]
            intensities[i] = peak_intensity
            normalized += peak_intensity

    free_double_vector(intensities_acc)
    if normalized / total > 1.0:
        total *= (normalized / total)
    return fragment_classification, intensities, total


cdef EnumValue _get_nterm_neighbor_fast(_FragmentType self, int offset, int index):
    index = index - offset
    if index < 0:
        return None
    else:
        residue = self.sequence.get(index).amino_acid
        return classify_residue_frank(residue)


@cython.binding(True)
cpdef EnumValue get_nterm_neighbor(_FragmentType self, int offset=1):
    cdef:
        int index
    index = get_nterm_index_from_fragment(<PeptideFragment>self.get_fragment(), self.sequence)
    return _get_nterm_neighbor_fast(self, offset, index)


cdef EnumValue _get_cterm_neighbor_fast(_FragmentType self, int offset, int index):
    index = index + offset
    if index > self.sequence.get_size() - 1:
        return None
    else:
        residue = self.sequence.get(index).amino_acid
        return classify_residue_frank(residue)


@cython.binding(True)
cpdef EnumValue get_cterm_neighbor(_FragmentType self, int offset=1):
    cdef:
        int index
    index = get_cterm_index_from_fragment(<PeptideFragment>self.get_fragment(), self.sequence)
    index += offset
    if index > self.sequence.get_size() - 1:
        return None
    else:
        residue = self.sequence.get(index).amino_acid
        return classify_residue_frank(residue)


@cython.binding(True)
@cython.boundscheck(False)
@cython.wraparound(False)
cpdef Py_ssize_t encode_neighboring_residues(_FragmentType self, feature_dtype_t[::1] X, Py_ssize_t offset, dict context=None):
    cdef:
        Py_ssize_t k_ftypes, k, i
        long bond_offset_depth, index
        EnumValue nterm, cterm
        PeptideFragment fragment

    bond_offset_depth = PyInt_AsLong(self.bond_offset_depth)
    k_ftypes = (FragmentTypeClassification_max + 1)
    k = (k_ftypes * 2) * bond_offset_depth

    if self._is_backbone:
        fragment = <PeptideFragment>self.get_fragment()
        index = get_nterm_index_from_fragment(fragment, self.sequence)
        for i in range(1, bond_offset_depth + 1):
            nterm = _get_nterm_neighbor_fast(self, i, index)
            if nterm is not None:
                X[offset + nterm.int_value()] = 1
            offset += k_ftypes
        index = get_cterm_index_from_fragment(fragment, self.sequence)
        for i in range(1, bond_offset_depth + 1):
            cterm = _get_cterm_neighbor_fast(self, i, index)
            if cterm is not None:
                X[offset + cterm.int_value()] = 1
            offset += k_ftypes
    else:
        offset += k
    return offset


@cython.binding(True)
@cython.boundscheck(False)
@cython.wraparound(False)
cpdef Py_ssize_t specialize_proline(_FragmentType self, feature_dtype_t[::1] X, Py_ssize_t offset, dict context=None):
    cdef:
        Py_ssize_t k_charge_cterm_pro, k_series_cterm_pro, k_glycosylated_proline
        Py_ssize_t k
        int index

    k_charge_cterm_pro = (FragmentCharge_max + 1)
    k_series_cterm_pro = (BackboneFragmentSeriesClassification_max + 1)
    k_glycosylated_proline = BackboneFragment_max_glycosylation_size + 1

    k = (k_charge_cterm_pro + k_series_cterm_pro + k_glycosylated_proline)

    if self._is_backbone and self.cterm.int_value() == FragmentTypeClassification_pro.int_value():
        index = (self.charge - 1)
        X[offset + index] = 1
        offset += k_charge_cterm_pro
        X[offset + self.series.int_value()] = 1
        offset += k_series_cterm_pro
        X[offset + (<PeptideFragment>self.peak_pair.fragment).get_glycosylation_size()] = 1
        offset += k_glycosylated_proline
    else:
        offset += k
    return offset


@cython.binding(True)
@cython.boundscheck(False)
@cython.wraparound(False)
cpdef Py_ssize_t encode_stub_information(_FragmentType self, feature_dtype_t[::1] X, Py_ssize_t offset, dict context=None):
    cdef:
        Py_ssize_t k_glycosylated_stubs, k_sequence_composition_stubs
        Py_ssize_t k, i, n
        int index, c
        tuple tp_c
        list ctr
        EnumValue tp
        PyObject* ptemp

    k_glycosylated_stubs = StubFragment_max_glycosylation_size + 1
    k_sequence_composition_stubs = FragmentTypeClassification_max + 1
    k = k_glycosylated_stubs + k_sequence_composition_stubs


    if self._is_stub_glycopeptide:
        X[offset + (self.glycosylated)] = 1
        offset += k_glycosylated_stubs

        if context is not None:
            ptemp = PyDict_GetItem(context, "classify_sequence_by_residues")
            if ptemp == NULL:
                ctr = classify_sequence_by_residues(self.sequence)
                PyDict_SetItem(context, "classify_sequence_by_residues", ctr)
            else:
                ctr = <list>ptemp
        else:
            ctr = classify_sequence_by_residues(self.sequence)
        n = PyList_GET_SIZE(ctr)
        for i in range(n):
            tp_c = <tuple>PyList_GET_ITEM(ctr, i)
            tp = <EnumValue>PyTuple_GetItem(tp_c, 0)
            c = PyInt_AsLong(<object>PyTuple_GetItem(tp_c, 1))
            X[offset + tp.int_value()] = c
        offset += k_sequence_composition_stubs
    else:
        offset += k_glycosylated_stubs + k_sequence_composition_stubs
    return offset


cdef object _FUC = FrozenMonosaccharideResidue.from_iupac_lite("Fuc")
cdef object _DHEX = FrozenMonosaccharideResidue.from_iupac_lite("dHex")
cdef int StubFragment_max_fucose = 6

cdef long count_deoxyhexose(glycan_composition):
    cdef:
        long k
    if isinstance(glycan_composition, _CompositionBase):
        gc = <_CompositionBase>glycan_composition
        k = PyInt_AsLong(_CompositionBase._getitem_fast(gc, _FUC)) + PyInt_AsLong(_CompositionBase._getitem_fast(gc, _DHEX))
    else:
        k = glycan_composition._getitem_fast(_FUC) + glycan_composition._getitem_fast(_DHEX)
    return k

@cython.boundscheck(False)
@cython.binding(True)
@cython.wraparound(False)
cpdef Py_ssize_t encode_stub_fucosylation(_FragmentType self, feature_dtype_t[::1] X, Py_ssize_t offset, dict context=None):
    cdef:
        int k_fucose, k_stub_charges, k_fucose_x_charge, loss_size, d, expected
        StubFragment frag
        PyObject* tmp

    k_fucose = (StubFragment_max_fucose) + 1
    k_stub_charges = FragmentCharge_max + 1
    k_fucose_x_charge = (k_fucose * k_stub_charges)

    if self._is_stub_glycopeptide:
        frag = <StubFragment>self.peak_pair.fragment
        if context is not None:
            tmp = PyDict_GetItem(context, "count_deoxyhexose")
            if tmp == NULL:
                expected = count_deoxyhexose(self.sequence.glycan_composition)
                PyDict_SetItem(context, 'count_deoxyhexose', PyInt_FromLong(expected))
            else:
                expected = PyInt_AsLong(<object>tmp)
        else:
            expected = 1
        if expected:
            loss_size = count_deoxyhexose(frag.glycosylation)
            if loss_size >= k_fucose:
                loss_size = k_fucose - 1
        else:
            loss_size = 0
        d = k_fucose * (self.charge - 1) + loss_size
        X[offset + d] = 1
    offset += k_fucose_x_charge
    return offset


@cython.binding(True)
@cython.cdivision(True)
cpdef int get_cleavage_site_distance_from_center(_FragmentType self):
    cdef:
        int index, center
        size_t seq_size
    index = get_cterm_index_from_fragment(<PeptideFragment>self.get_fragment(), self.sequence)
    seq_size = self.sequence.get_size()
    center = (seq_size // 2)
    return abs(center - index)


@cython.binding(True)
@cython.boundscheck(False)
@cython.wraparound(False)
cpdef Py_ssize_t encode_cleavage_site_distance_from_center(_FragmentType self, feature_dtype_t[::1] X, Py_ssize_t offset, dict context=None):
    cdef:
        Py_ssize_t k_distance, k_series, k
        long max_distance, series_offset, distance

    max_distance = PyInt_AsLong(self.max_cleavage_site_distance_from_center)
    k_distance = max_distance + 1
    k_series = BackboneFragmentSeriesClassification_max + 1
    k = k_distance * k_series
    if self._is_backbone:
        distance = get_cleavage_site_distance_from_center(self)
        distance = min(distance, max_distance)
        series_offset = self.series.int_value() * k_distance
        X[offset + series_offset + distance] = 1
    offset += (k_distance * k_series)
    return offset


@cython.binding(True)
@cython.boundscheck(False)
@cython.wraparound(False)
cpdef Py_ssize_t encode_stub_charge(_FragmentType self, feature_dtype_t[::1] X, Py_ssize_t offset, dict context=None):
    cdef:
        Py_ssize_t k_glycosylated_stubs, k_stub_charges, k_glycosylated_stubs_x_charge
        Py_ssize_t k
        long loss_size, d

    k_glycosylated_stubs = (StubFragment_max_glycosylation_size * 2) + 1
    k_stub_charges = FragmentCharge_max + 1
    k_glycosylated_stubs_x_charge = (k_glycosylated_stubs * k_stub_charges)
    k = k_glycosylated_stubs_x_charge

    if self._is_stub_glycopeptide:
        # TODO: Using the approximation provides a mildly better model fit on mixed sialylated/non-sialylated data
        # but requires a full re-analysis. Save for the future.
        # loss_size = PyInt_AsLong(approximate_internal_size_of_glycan(self.sequence.glycan)) - self.glycosylated
        loss_size = ((<GlycosylationManager>self.sequence._glycosylation_manager).get_total_glycosylation_size()) - self.glycosylated
        if loss_size >= k_glycosylated_stubs:
            loss_size = k_glycosylated_stubs - 1
        d = k_glycosylated_stubs * (self.charge - 1) + loss_size
        X[offset + d] = 1
    offset += k_glycosylated_stubs_x_charge
    return offset


@cython.binding(True)
@cython.boundscheck(False)
@cython.wraparound(False)
cpdef Py_ssize_t encode_stub_charge_loss_approximate(_FragmentType self, feature_dtype_t[::1] X, Py_ssize_t offset, dict context=None):
    cdef:
        Py_ssize_t k_glycosylated_stubs, k_stub_charges, k_glycosylated_stubs_x_charge
        Py_ssize_t k
        long loss_size, d

    k_glycosylated_stubs = (StubFragment_max_glycosylation_size * 2) + 1
    k_stub_charges = FragmentCharge_max + 1
    k_glycosylated_stubs_x_charge = (k_glycosylated_stubs * k_stub_charges)
    k = k_glycosylated_stubs_x_charge

    if self._is_stub_glycopeptide:
        # TODO: Using the approximation provides a mildly better model fit on mixed sialylated/non-sialylated data
        # but requires a full re-analysis. Save for the future.
        loss_size = PyInt_AsLong(approximate_internal_size_of_glycan(self.sequence.glycan)) - self.glycosylated
        if loss_size >= k_glycosylated_stubs:
            loss_size = k_glycosylated_stubs - 1
        d = k_glycosylated_stubs * (self.charge - 1) + loss_size
        X[offset + d] = 1
    offset += k_glycosylated_stubs_x_charge
    return offset


cdef:
    object _specialize_proline = specialize_proline
    object _encode_stub_information = encode_stub_information
    object _encode_stub_fucosylation = encode_stub_fucosylation
    object _encode_neighboring_residues = encode_neighboring_residues
    object _encode_cleavage_site_distance_from_center = encode_cleavage_site_distance_from_center
    object _encode_stub_charge = encode_stub_charge
    object _encode_stub_charge_loss_approximate = encode_stub_charge_loss_approximate


@cython.binding(True)
@cython.boundscheck(False)
@cython.wraparound(False)
cpdef Py_ssize_t StubChargeModel_build_feature_vector(_FragmentType self, feature_dtype_t[::1] X, Py_ssize_t offset, dict context=None):
    # X, offset = super(StubChargeModel, self).build_feature_vector(X, offset)
    # X, offset = self.encode_stub_charge(X, offset)

    # Directly invoke feature vector construction because super() costs too much
    # in a tight loop
    cdef:
        tuple out

    offset = _FragmentType.build_feature_vector(self, X, offset, context)
    offset = specialize_proline(self, X, offset, context)
    offset = encode_stub_information(self, X, offset, context)
    offset = encode_stub_fucosylation(self, X, offset, context)
    offset = encode_neighboring_residues(self, X, offset, context)
    offset = encode_stub_charge(self, X, offset, context)
    return offset


@cython.binding(True)
@cython.boundscheck(False)
@cython.wraparound(False)
cpdef Py_ssize_t StubChargeModelApproximate_build_feature_vector(_FragmentType self, feature_dtype_t[::1] X, Py_ssize_t offset, dict context=None):
    # Directly invoke feature vector construction because super() costs too much
    # in a tight loop
    cdef:
        tuple out

    offset = _FragmentType.build_feature_vector(self, X, offset, context)
    offset = specialize_proline(self, X, offset, context)
    offset = encode_stub_information(self, X, offset, context)
    offset = encode_stub_fucosylation(self, X, offset, context)
    offset = encode_neighboring_residues(self, X, offset, context)
    offset = encode_stub_charge_loss_approximate(self, X, offset, context)
    return offset


cdef object _NEUAC = FrozenMonosaccharideResidue.from_iupac_lite("NeuAc")
cdef object _NEUGC = FrozenMonosaccharideResidue.from_iupac_lite("NeuGc")


@cython.binding(True)
@cython.boundscheck(False)
@cython.wraparound(False)
cpdef Py_ssize_t encode_labile_monosaccharides_charge(_FragmentType self, feature_dtype_t[::1] X, Py_ssize_t offset, dict context=None):
    cdef:
        size_t k_labile_monosaccharides, k_stub_charges, k_labile_monosaccharides_x_charge
        PyObject* tmp
        long loss_size, d
    k_labile_monosaccharides = (StubFragment_max_labile_monosaccharides) + 1
    k_stub_charges = FragmentCharge_max + 1
    k_labile_monosaccharides_x_charge = (k_labile_monosaccharides * k_stub_charges)

    if self._is_stub_glycopeptide:
        if context is not None:
            tmp = PyDict_GetItem(context, "count_labile_monosaccharides")
            if tmp == NULL:
                loss_size = count_labile_monosaccharides(self.sequence.glycan_composition)
                PyDict_SetItem(context, 'count_labile_monosaccharides', PyInt_FromLong(loss_size))
            else:
                loss_size = PyInt_AsLong(<object>tmp)
        else:
            loss_size = count_labile_monosaccharides(self.sequence.glycan_composition)

        if loss_size >= k_labile_monosaccharides:
            loss_size = k_labile_monosaccharides - 1
        d = k_labile_monosaccharides * (self.charge - 1) + loss_size
        X[offset + d] = 1
    offset += k_labile_monosaccharides_x_charge
    return offset


cdef long count_labile_monosaccharides(glycan_composition):
    cdef:
        long k
    if isinstance(glycan_composition, _CompositionBase):
        gc = <_CompositionBase>glycan_composition
        k = PyInt_AsLong(_CompositionBase._getitem_fast(gc, _NEUAC)) + PyInt_AsLong(_CompositionBase._getitem_fast(gc, _NEUGC))
    else:
        k = glycan_composition._getitem_fast(_NEUAC) + glycan_composition._getitem_fast(_NEUGC)
    return k

@cython.binding(True)
@cython.boundscheck(False)
@cython.wraparound(False)
cpdef Py_ssize_t LabileMonosaccharideAwareModel_build_feature_vector(_FragmentType self, feature_dtype_t[::1] X, Py_ssize_t offset, dict context=None):
    # Directly invoke feature vector construction because super() costs too much
    # in a tight loop
    cdef:
        tuple out

    offset = _FragmentType.build_feature_vector(self, X, offset, context)
    offset = specialize_proline(self, X, offset, context)
    offset = encode_stub_information(self, X, offset, context)
    offset = encode_stub_fucosylation(self, X, offset, context)
    offset = encode_neighboring_residues(self, X, offset, context)
    offset = encode_stub_charge(self, X, offset, context)
    offset = encode_labile_monosaccharides_charge(self, X, offset, context)
    return offset


@cython.binding(True)
@cython.boundscheck(False)
@cython.wraparound(False)
cpdef Py_ssize_t LabileMonosaccharideAwareModelApproximate_build_feature_vector(_FragmentType self, feature_dtype_t[::1] X, Py_ssize_t offset, dict context=None):
    # Directly invoke feature vector construction because super() costs too much
    # in a tight loop

    offset = _FragmentType.build_feature_vector(self, X, offset, context)
    offset = specialize_proline(self, X, offset, context)
    offset = encode_stub_information(self, X, offset, context)
    offset = encode_stub_fucosylation(self, X, offset, context)
    offset = encode_neighboring_residues(self, X, offset, context)
    offset = encode_stub_charge_loss_approximate(self, X, offset, context)
    offset = encode_labile_monosaccharides_charge(self, X, offset, context)
    return offset


cpdef list classify_sequence_by_residues(_PeptideSequenceCore sequence):
    cdef:
        size_t i, n, m
        int* residue_tp_counts
        AminoAcidResidueBase res
        EnumValue e
        list result

    residue_tp_counts = <int*>calloc(AminoAcidClassification_max, sizeof(int))
    n = sequence.get_size()
    for i in range(n):
        res = sequence.get(i).amino_acid
        e = classify_residue_frank(res)
        residue_tp_counts[e.int_value()] += 1

    result = []
    m = 0
    for i in range(AminoAcidClassification_max):
        if residue_tp_counts[i] > 0:
            m += residue_tp_counts[i]
            result.append((AminoAcidClassification[i], residue_tp_counts[i]))
    result.append((AminoAcidClassification['x'], n - m))
    free(residue_tp_counts)
    return result