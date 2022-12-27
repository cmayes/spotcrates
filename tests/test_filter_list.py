import os
import unittest

from spotcrates.filters import filter_list, FieldName
from tests.utils import load_playlist_listing_file

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
PLAYLISTS = load_playlist_listing_file(os.path.join(DATA_DIR, 'playlists.json'))


class FilterListTestCase(unittest.TestCase):
    # filter_list
    def test_empty_filter(self):
        self.assertEqual(PLAYLISTS, filter_list(PLAYLISTS, ""))

    def test_null_filter(self):
        self.assertEqual(PLAYLISTS, filter_list(PLAYLISTS, None))

    def test_implicit_contains(self):
        filtered_list = filter_list(PLAYLISTS, "na:Songs")

        self.assertEqual(2, len(filtered_list))

        for playlist in filtered_list:
            self.assertTrue("Songs" in playlist[FieldName.PLAYLIST_NAME])

    def test_implicit_contains_caseless(self):
        filtered_list = filter_list(PLAYLISTS, "na:sOnGs")

        self.assertEqual(2, len(filtered_list))

        for playlist in filtered_list:
            self.assertTrue("Songs" in playlist[FieldName.PLAYLIST_NAME])

    def test_explicit_contains_caseless(self):
        playlists = PLAYLISTS
        # filters: Dict[FieldName, List[FieldFilter]]
        filtered_list = filter_list(playlists, "pname:con:sOnGs")

        self.assertEqual(2, len(filtered_list))

        for playlist in filtered_list:
            self.assertTrue("Songs" in playlist[FieldName.PLAYLIST_NAME])

    def test_equals(self):
        playlists = PLAYLISTS
        # filters: Dict[FieldName, List[FieldFilter]]
        filtered_list = filter_list(playlists, "na:eq:Now")

        self.assertEqual(1, len(filtered_list))

        for playlist in filtered_list:
            self.assertTrue("Now" == playlist[FieldName.PLAYLIST_NAME])

    def test_starts(self):
        playlists = PLAYLISTS
        # filters: Dict[FieldName, List[FieldFilter]]
        filtered_list = filter_list(playlists, "na:sta:your")

        self.assertEqual(2, len(filtered_list))

        for playlist in filtered_list:
            self.assertTrue(str(playlist[FieldName.PLAYLIST_NAME]).startswith("Your"))

    def test_ends(self):
        playlists = PLAYLISTS
        # filters: Dict[FieldName, List[FieldFilter]]
        filtered_list = filter_list(playlists, "desc:ends:MoRe")

        self.assertEqual(1, len(filtered_list))

        for playlist in filtered_list:
            self.assertTrue(str(playlist[FieldName.PLAYLIST_DESCRIPTION]).endswith("more"))

    def test_greater(self):
        playlists = PLAYLISTS
        # filters: Dict[FieldName, List[FieldFilter]]
        filtered_list = filter_list(playlists, "size:greater:300")

        self.assertEqual(2, len(filtered_list))

        for playlist in filtered_list:
            self.assertTrue(int(playlist[FieldName.SIZE]) > 300)

    def test_less(self):
        playlists = PLAYLISTS
        # filters: Dict[FieldName, List[FieldFilter]]
        filtered_list = filter_list(playlists, "size:lt:300")

        self.assertEqual(4, len(filtered_list))

        for playlist in filtered_list:
            self.assertTrue(int(playlist[FieldName.SIZE]) < 300)

    def test_greater_equal(self):
        playlists = PLAYLISTS
        # filters: Dict[FieldName, List[FieldFilter]]
        filtered_list = filter_list(playlists, "size:geq:101")

        self.assertEqual(3, len(filtered_list))

        for playlist in filtered_list:
            self.assertTrue(int(playlist[FieldName.SIZE]) >= 101)

    def test_less_equal(self):
        playlists = PLAYLISTS
        # filters: Dict[FieldName, List[FieldFilter]]
        filtered_list = filter_list(playlists, "size:leq:100")

        self.assertEqual(3, len(filtered_list))

        for playlist in filtered_list:
            self.assertTrue(int(playlist[FieldName.SIZE]) <= 100)
