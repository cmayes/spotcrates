import unittest

from spotcrates.common import FilterLookup, FilterType, NotFoundException


class FilterLookupTestCase(unittest.TestCase):
    def setUp(self):
        self.lookup = FilterLookup()

    def test_contains(self):
        self.assertEqual(FilterType.CONTAINS, self.lookup.find("contains"))

    def test_con(self):
        self.assertEqual(FilterType.CONTAINS, self.lookup.find("con"))

    def test_c(self):
        self.assertEqual(FilterType.CONTAINS, self.lookup.find("c"))

    def test_equ(self):
        self.assertEqual(FilterType.EQUALS, self.lookup.find("equ"))

    def test_st(self):
        self.assertEqual(FilterType.STARTS, self.lookup.find("st"))

    def test_end(self):
        self.assertEqual(FilterType.ENDS, self.lookup.find("end"))

    def test_gr(self):
        self.assertEqual(FilterType.GREATER, self.lookup.find("gr"))

    def test_geq(self):
        self.assertEqual(FilterType.GREATER_EQUAL, self.lookup.find("geq"))

    def test_lt(self):
        self.assertEqual(FilterType.LESS, self.lookup.find("lt"))

    def test_leq(self):
        self.assertEqual(FilterType.LESS_EQUAL, self.lookup.find("leq"))

    def test_invalid(self):
        with self.assertRaises(NotFoundException):
            self.lookup.find("zyzygy")

    def test_none(self):
        with self.assertRaises(NotFoundException):
            self.lookup.find(None)

    def test_blank(self):
        with self.assertRaises(NotFoundException):
            self.lookup.find(None)
