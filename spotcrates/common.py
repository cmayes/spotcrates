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
    """Batch data into lists of length n. The last batch may be shorter."""
    # batched('ABCDEFG', 3) --> ABC DEF G
    it = iter(iterable)
    while True:
        batch = list(islice(it, n))
        if not batch:
            return
        yield batch


def get_all_items(spotify, first_page):
    """Collects the 'items' contents from every page in the given result set."""
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
    if not full_value:
        return full_value

    if len(full_value) > length:
        if trim_tail:
            return full_value[:length]
        else:
            return full_value[-length:]
    return full_value


def test_str_contains(test_val, target_val) -> bool:
    return str(test_val) in str(target_val)


def test_str_equals(test_val, target_val) -> bool:
    return str(test_val) == str(target_val)


def test_str_starts(test_val, target_val) -> bool:
    return str(target_val).startswith(str(test_val))


def test_str_ends(test_val, target_val) -> bool:
    return str(target_val).endswith(str(test_val))


def test_num_greater(test_val, target_val) -> bool:
    return int(target_val) > int(test_val)


def test_num_greater_equal(test_val, target_val) -> bool:
    return int(target_val) >= int(test_val)


def test_num_less(test_val, target_val) -> bool:
    return int(target_val) < int(test_val)


def test_num_less_equal(test_val, target_val) -> bool:
    return int(target_val) <= int(test_val)


class FilterType(Enum):
    def __init__(self, test_func):
        self.test = test_func

    CONTAINS = test_str_contains
    EQUALS = test_str_equals
    STARTS = test_str_starts
    ENDS = test_str_ends
    GREATER = test_num_greater
    LESS = test_num_less
    GREATER_EQUAL = test_num_greater_equal
    LESS_EQUAL = test_num_less_equal


class FieldDataType(Enum):
    STRING = auto()
    NUMERIC = auto()


class FieldName(Enum):
    def __init__(self, data_type):
        self.data_type = data_type

    PLAYLIST_NAME = FieldDataType.STRING
    SIZE = FieldDataType.NUMERIC
    OWNER = FieldDataType.STRING
    PLAYLIST_DESCRIPTION = FieldDataType.STRING


class FilterLookup:
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


class FieldLookup:
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
        self.field = self.eval_field_name(field)
        self.value = value
        self.filter_type = self.eval_filter_type(filter_type)

    def eval_field_name(self, field_name):
        field_name_type = type(field_name)
        if field_name_type == FieldName:
            return field_name
        elif field_name_type == str:
            return self.field_lookup.find(field_name)
        else:
            raise InvalidFilterException(f"Invalid field name type {field_name_type}")

    def eval_filter_type(self, filter_type) -> FilterType:
        filter_type_type = type(filter_type)
        if filter_type_type == FilterType:
            return filter_type
        elif filter_type_type == str:
            return self.filter_lookup.find(filter_type)
        else:
            raise InvalidFilterException(f"Invalid filter type {filter_type_type}")

    def __repr__(self):
        return f"FieldFilter({self.field}, {self.value}, {self.filter_type})"

    def __eq__(self, other):
        if isinstance(other, FieldFilter):
            return self.field == other.field and self.value == other.value \
                and self.filter_type == other.filter_type
        return NotImplemented


def parse_filters(filters: str) -> Dict[FieldName, List[FieldFilter]]:
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
            field_filter = FieldFilter(stripped_exp[0], stripped_exp[1], FilterType.CONTAINS)
        else:
            field_filter = FieldFilter(stripped_exp[0], stripped_exp[2], stripped_exp[1])
        parsed_filters[field_filter.field].append(field_filter)

    return parsed_filters


# TODO: Test filter_list and consider moving filter to separate file
def filter_list(items, filters):
    parsed_filters = parse_filters(filters)

    filtered_items = items
    for field in FieldName:
        field_filters = parsed_filters[field]
        if field_filters:
            for cur_filter in field_filters:
                filter_test = cur_filter.filter_type.test
                test_value = cur_filter.value

                matching_items = []
                for cur_item in filtered_items:
                    if filter_test(test_value, cur_item.get(cur_filter.field)):
                        matching_items.append(cur_item)
                filtered_items = matching_items

    return filtered_items
