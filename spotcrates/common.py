import logging
from collections import defaultdict
from enum import auto, Enum
from itertools import islice
from typing import List, Dict

import pygtrie


class NotFoundException(Exception):
    pass


class InvalidFilterException(Exception):
    pass


def batched(iterable, n):
    "Batch data into lists of length n. The last batch may be shorter."
    # batched('ABCDEFG', 3) --> ABC DEF G
    it = iter(iterable)
    while True:
        batch = list(islice(it, n))
        if not batch:
            return
        yield batch


def get_all_items(spotify, first_page):
    "Collects the 'items' contents from every page in the given result set."
    all_items = []

    all_items.extend(first_page['items'])

    next_page = spotify.next(first_page)
    while next_page:
        all_items.extend(next_page['items'])
        next_page = spotify.next(next_page)

    return all_items


def truncate_long_value(full_value: str, length: int, trim_tail: bool = True) -> str:
    """Returns the given value truncated from the start of the value so that it is at most the given length.

    :param full_value: The value to trim.
    :param length: The maximum length of the returned value.
    :param trim_tail: Whether to trim from the head or tail of the string.
    :return: The value trimmed from the start of the string to be at most the given length.
    """
    if len(full_value) > length:
        if trim_tail:
            return full_value[:length]
        else:
            return full_value[-length:]
    return full_value


class FilterType(Enum):
    CONTAINS = auto()
    EQUALS = auto()
    STARTS = auto()
    ENDS = auto()
    GREATER = auto()
    LESS = auto()
    GREATER_EQUAL = auto()
    LESS_EQUAL = auto()


class FieldName(Enum):
    PLAYLIST_NAME = auto()
    SIZE = auto()
    OWNER = auto()
    PLAYLIST_DESCRIPTION = auto()


class FilterLookup():
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.lookup = FilterLookup._init_lookup()

    def find(self, type_name):
        if not type_name:
            raise NotFoundException(f"Blank/null filter type {type_name}")

        found_type = self.lookup.longest_prefix(type_name)

        if found_type:
            self.logger.debug("Got %s (%s) for %s", found_type.value, found_type.key, type_name)
            return found_type.value
        else:
            raise NotFoundException(f"No filter type for {type_name}")

    @staticmethod
    def _init_lookup():
        lookup = pygtrie.CharTrie()
        lookup['c'] = FilterType.CONTAINS
        lookup['eq'] = FilterType.EQUALS
        lookup['s'] = FilterType.STARTS
        lookup['en'] = FilterType.ENDS
        lookup['g'] = FilterType.GREATER
        lookup['l'] = FilterType.LESS
        lookup['ge'] = FilterType.GREATER_EQUAL
        lookup['leq'] = FilterType.LESS_EQUAL

        return lookup


class FieldLookup():
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.lookup = FieldLookup._init_lookup()

    def find(self, field_name):
        if not field_name:
            raise NotFoundException(f"Blank/null field name {field_name}")

        found_field = self.lookup.longest_prefix(field_name)

        if found_field:
            self.logger.debug("Got %s (%s) for %s", found_field.value, found_field.key, field_name)
            return found_field.value
        else:
            raise NotFoundException(f"No field name for {field_name}")

    @staticmethod
    def _init_lookup():
        lookup = pygtrie.CharTrie()
        lookup['n'] = FieldName.PLAYLIST_NAME
        lookup['p'] = FieldName.PLAYLIST_NAME
        lookup['pl'] = FieldName.PLAYLIST_NAME
        lookup['pn'] = FieldName.PLAYLIST_NAME
        lookup['s'] = FieldName.SIZE
        lookup['ps'] = FieldName.SIZE
        lookup['d'] = FieldName.PLAYLIST_DESCRIPTION
        lookup['pd'] = FieldName.PLAYLIST_DESCRIPTION
        lookup['c'] = FieldName.SIZE
        lookup['s'] = FieldName.SIZE
        lookup['o'] = FieldName.OWNER

        return lookup


class FieldFilter:
    def __init__(self, field, value, filter_type):
        self.filter_lookup = FilterLookup()
        self.field_lookup = FieldLookup()
        self.field = field
        self.value = value
        self.filter_type = self.eval_filter_type(filter_type)

    def eval_field_name(self, field_name):
        field_name_type = type(field_name)
        if field_name_type == FieldName:
            return field_name
        elif field_name_type == str:
            return self.field_lookup.find(field_name_type)
        else:
            raise InvalidFilterException(f"Invalid field name type {field_name_type}")

    def eval_filter_type(self, filter_type):
        filter_type_type = type(filter_type)
        if filter_type_type == FilterType:
            return filter_type
        elif filter_type_type == str:
            return self.filter_lookup.find(filter_type_type)
        else:
            raise InvalidFilterException(f"Invalid filter type {filter_type_type}")


def parse_filters(filters: str) -> Dict[str, List[FieldFilter]]:
    """Returns a dict keyed by field with values being a list of
    name:PoP
    size:gt:22
    name:twin


    :param filters: A str with a comma-separated list of filters
    :return: A map of field names to lower-case "contains" filter strings.
    """
    parsed_filters = defaultdict(list)

    if not filters:
        return parsed_filters

    raw_filters = [raw_filter.strip() for raw_filter in filters.split(",")]
    split_raw_filters = [raw_filter.split(":") for raw_filter in raw_filters]

    for raw_exp in split_raw_filters:
        exp_field_count = len(raw_exp)

        if exp_field_count < 2:
            raise InvalidFilterException(f"Invalid filter expression {':'.join(raw_exp)}")

        stripped_exp = [field.strip() for field in raw_exp]
        if exp_field_count == 2:
            parsed_filters[stripped_exp[0]].append(FieldFilter(stripped_exp[0], stripped_exp[1], FilterType.CONTAINS))
        else:
            parsed_filters[stripped_exp[0]].append(FieldFilter(stripped_exp[0], stripped_exp[2], stripped_exp[1]))

    return parsed_filters


def filter_list(all_items, filters):
    parse_filters(filters)
    filtered_items = []

    pass
