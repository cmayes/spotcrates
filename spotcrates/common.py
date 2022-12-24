import logging
from enum import auto, Enum
from itertools import islice
import pygtrie


class NotFoundException(Exception):
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


class FieldFilter:
    def __init__(self, field, value, filter_type):
        pass


def parse_filters(filters):
    """Returns a dict keyed by field with values being a list of
    name:PoP
    size:gt:22
    name:twin


    :param filters: A str with a comma-separated list of filters
    :return: A map of field names to lower-case "contains" filter strings.
    """
    pass


def filter_list(all_items, filters):
    parse_filters(filters)
    filtered_items = []

    pass
