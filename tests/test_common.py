import unittest

from spotcrates.common import FilterLookup, FilterType, NotFoundException, FieldLookup, FieldName


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


class FieldNameTestCase(unittest.TestCase):
    def setUp(self):
        self.lookup = FieldLookup()

    # PLAYLIST NAME                    SIZE   OWNER            DESCRIPTION
    #
    #         lookup['n'] = FieldName.PLAYLIST_NAME
    #         lookup['p'] = FieldName.PLAYLIST_NAME
    #         lookup['pl'] = FieldName.PLAYLIST_NAME
    #         lookup['pn'] = FieldName.PLAYLIST_NAME
    #         lookup['s'] = FieldName.SIZE
    #         lookup['ps'] = FieldName.SIZE
    #         lookup['d'] = FieldName.PLAYLIST_DESCRIPTION
    #         lookup['pd'] = FieldName.PLAYLIST_DESCRIPTION
    #         lookup['o'] = FieldName.OWNER

    def test_name(self):
        self.assertEqual(FieldName.PLAYLIST_NAME, self.lookup.find("name"))

    def test_pname(self):
        self.assertEqual(FieldName.PLAYLIST_NAME, self.lookup.find("pname"))

    def test_playlistname(self):
        self.assertEqual(FieldName.PLAYLIST_NAME, self.lookup.find("playlistname"))

    def test_p(self):
        self.assertEqual(FieldName.PLAYLIST_NAME, self.lookup.find("p"))

    def test_d(self):
        self.assertEqual(FieldName.PLAYLIST_DESCRIPTION, self.lookup.find("d"))

    def test_pd(self):
        self.assertEqual(FieldName.PLAYLIST_DESCRIPTION, self.lookup.find("pd"))

    def test_desc(self):
        self.assertEqual(FieldName.PLAYLIST_DESCRIPTION, self.lookup.find("desc"))

    def test_c(self):
        self.assertEqual(FieldName.SIZE, self.lookup.find("c"))

    def test_s(self):
        self.assertEqual(FieldName.SIZE, self.lookup.find("s"))

    def test_size(self):
        self.assertEqual(FieldName.SIZE, self.lookup.find("size"))

    def test_count(self):
        self.assertEqual(FieldName.SIZE, self.lookup.find("count"))

    def test_o(self):
        self.assertEqual(FieldName.OWNER, self.lookup.find("o"))

    def test_owner(self):
        self.assertEqual(FieldName.OWNER, self.lookup.find("owner"))
