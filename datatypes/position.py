import itertools
import re
from collections import defaultdict
from typing import Generator

from datatypes import MotifClasses
from dynamic_constants import DynamicConstants


class Position(dict):
    def __init__(self, position: int, sequences: Generator, variants_flattened: list, variant_dict: defaultdict,
                 entropy: float = None, variant_data: bool = False):
        """
            Data structure for kmer positions

            Describes the data structure for kmer positions within the alignment

            :param position: A zero-based index for position number
            :param sequences: A list of type Variant containing variants seen at current position
            :param variants_flattened: A flattened list of all variants. Note: Only used for processing
            :param variant_dict: A default dictionary of lists to store the sequence idx for later getting description data
            :param entropy: The Shannon entropy at the current kmer position
            :param variant_data: Whether to derive variant data from the sequence headers.

            :type position: int
            :type sequences: Generator
            :type variants_flattened: list
            :type variant_dict: defaultdict
            :type entropy: float
        """

        self.position = position
        self.entropy = entropy
        self.variants_flattened = variants_flattened
        self.supports = len(self.variants_flattened)
        self.sequences = self._motif_classify(sequences)
        self.variants = len(self.sequences)

        self._set_desc_data(variant_dict) if variant_data else None

    def _set_desc_data(self, variant_dict):
        """
            Sets the data from the header as attributes in the variant object.

            :param variant_dict: A defaultdict of list containing idx of sequences
            :type variant_dict: defaultdict
        """

        expr = re.compile(DynamicConstants.HEADER_REGEX)

        for dict_variant, variant in itertools.product(variant_dict, self.sequences):
            if dict_variant != variant.sequence:
                continue
            idx = variant_dict[dict_variant]

            for ids in idx:
                header = DynamicConstants.SEQ_DESCRIPTIONS[ids]

                mapping = [x.groupdict() for x in expr.finditer(header)][0]

                for key, value in mapping.items():
                    variant[key] = value

    def __setattr__(self, key, value):
        # This really makes me sad, find a way around this mess TODO: fix this please, also in Variant
        dict.__setitem__(self, key, value)

    def __getattr__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            raise AttributeError

    def __getstate__(self):
        state = self.copy()
        del state['variants_flattened']

        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

    @classmethod
    def _motif_classify(cls, variants: Generator) -> list:
        """
        Given a list of Variant objects sort by the count of each, and  classify each variant into motif classes

        :param variants: A list of Variant objects
        :type variants: Generator

        :return: A list containing Variant objects sorted by count and each variant classified into motif classes
        """

        variants = sorted(variants, key=lambda x: x.count, reverse=True)

        for idx, variant in enumerate(variants):
            if idx == 0:
                variants[idx].motif_short = 'I'
                variants[idx].motif_long = MotifClasses.I
            elif idx == 1:
                variants[idx].motif_short = 'Ma'
                variants[idx].motif_long = MotifClasses.Ma
            elif variants[idx].count > 1:
                variants[idx].motif_short = 'Mi'
                variants[idx].motif_long = MotifClasses.Mi
            else:
                variants[idx].motif_short = 'U'
                variants[idx].motif_long = MotifClasses.U

        return variants

    def _get_id(self, indexs) -> list:
        """
            Given a list of sequence indexes return a list of sequence ids

            :param indexs: A list of sequence indexs
            :type indexs: list

            :return: A list containing sequence ids
        """

        return [self.SEQ_DESCRIPTIONS[x].split('|')[0] for x in indexs]

    def _get_strain(self, indexs) -> list:
        """
            Given a list of sequence indexes return a list of sequence strains

            :param indexs: A list of sequence indexs
            :type indexs: list

            :return: A list containing sequence ids
        """

        return [self.SEQ_DESCRIPTIONS[x].split('|')[1] for x in indexs]

    def _get_country(self, indexs) -> list:
        """
            Given a list of sequence indexes return a list of sequence countries

            :param indexs: A list of sequence indexs
            :type indexs: list

            :return: A list containing sequence ids
        """

        return [self.SEQ_DESCRIPTIONS[x].split('|')[2] for x in indexs]

    def _get_host(self, indexs) -> list:
        """
            Given a list of sequence indexes return a list of sequence hosts

            :param indexs: A list of sequence indexs
            :type indexs: list

            :return: A list containing sequence ids
        """

        return [self.SEQ_DESCRIPTIONS[x].split('|')[3] for x in indexs]
