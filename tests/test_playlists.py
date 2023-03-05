import os
import unittest
from unittest.mock import MagicMock, ANY

from spotcrates.filters import FieldName
from spotcrates.playlists import Playlists, PlaylistResult
from tests.utils import file_json

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
PLAYLIST_LIST = file_json(os.path.join(DATA_DIR, "playlists.json"))
PLAYLIST_NO_DAILY_LIST = file_json(os.path.join(DATA_DIR, "playlists_no_daily.json"))
TRACKS_DAILY1 = file_json(os.path.join(DATA_DIR, "tracks_daily1.json"))
TRACKS_OVERPLAYED = file_json(os.path.join(DATA_DIR, "tracks_overplayed.json"))
TRACKS_TARGET = file_json(os.path.join(DATA_DIR, "tracks_target.json"))


def get_canned_tracks(*args, **kwargs):
    playlist_id = args[0]
    if playlist_id == "37i9dQZF1E37hnawmowyJn":
        return TRACKS_DAILY1
    elif playlist_id == "0y8aCYE2OsnLzzxtqcDGf8":
        return TRACKS_OVERPLAYED
    elif playlist_id == "1JJB9ICuIoE6aD4jg9vgmV":
        return TRACKS_TARGET
    else:
        raise Exception(f"Unhandled tracks ID {playlist_id}")


class DailyAppendTestCase(unittest.TestCase):
    def setUp(self):
        self.spotify = MagicMock()
        self.spotify.next.return_value = None
        self.playlists = Playlists(self.spotify)

    def test_list_all(self):
        self.spotify.current_user_playlists.return_value = {"items": PLAYLIST_LIST}

        playlists = self.playlists.get_all_playlists()

        self.assertEqual(PLAYLIST_LIST, playlists)

    def test_append_daily_mix(self):
        self.spotify.current_user_playlists.return_value = {"items": PLAYLIST_LIST}

        self.spotify.playlist_items.side_effect = get_canned_tracks

        self.playlists.append_daily_mix(randomize=False)

        self.spotify.playlist_add_items.assert_called_with(
            "1JJB9ICuIoE6aD4jg9vgmV", ["3DrlHWCoFqHQYGwE8MWsuv"]
        )

    def test_append_empty_entries(self):
        self.spotify.current_user_playlists.return_value = {"items": [{}, {}, {}]}

        self.spotify.playlist_items.side_effect = get_canned_tracks

        self.playlists.append_daily_mix(randomize=False)

        self.spotify.playlist_add_items.assert_not_called()

    def test_append_daily_mix_missing_target(self):
        self.spotify.current_user_playlists.return_value = {"items": PLAYLIST_LIST}
        self.spotify.me.return_value = {"id": "testuser"}
        self.spotify.user_playlist_create.return_value = {
            "id": "1JJB9ICuIoE6aD4jg9vgmV"
        }

        self.spotify.playlist_items.side_effect = get_canned_tracks

        local_playlists = Playlists(
            self.spotify, {"daily_mix_target": "missing_playlist"}
        )
        local_playlists.append_daily_mix(randomize=False)
        self.spotify.playlist_add_items.assert_called_with(
            "1JJB9ICuIoE6aD4jg9vgmV", ["3DrlHWCoFqHQYGwE8MWsuv"]
        )
        self.spotify.user_playlist_create.assert_called_with(
            "testuser", "missing_playlist", public=False
        )

    # No dailies
    def test_append_daily_mix_no_dailies(self):
        self.spotify.current_user_playlists.return_value = {
            "items": PLAYLIST_NO_DAILY_LIST
        }

        self.spotify.playlist_items.side_effect = get_canned_tracks

        self.playlists.append_daily_mix(randomize=False)

        self.spotify.playlist_add_items.assert_not_called()

    # Paged tracks

    def test_append_daily_mix_paged(self):
        self.spotify.current_user_playlists.return_value = {"items": PLAYLIST_LIST}

        self.spotify.playlist_items.side_effect = get_canned_tracks

        def get_next_page(*args, **kwargs):
            page = args[0]
            if page == TRACKS_TARGET:
                return TRACKS_DAILY1
            else:
                return None

        self.spotify.next.side_effect = get_next_page

        self.playlists.append_daily_mix(randomize=False)

        self.spotify.playlist_add_items.assert_not_called()

    def test_append_daily_mix_paged_tracks(self):
        self.spotify.current_user_playlists.return_value = {"items": PLAYLIST_LIST}

        self.spotify.playlist_items.side_effect = get_canned_tracks

        def get_next_page(*args, **kwargs):
            page = args[0]
            if page == TRACKS_DAILY1:
                return TRACKS_TARGET
            else:
                return None

        self.spotify.next.side_effect = get_next_page

        self.playlists.append_daily_mix(randomize=False)

        self.spotify.playlist_add_items.assert_called_with(
            "1JJB9ICuIoE6aD4jg9vgmV", ["3DrlHWCoFqHQYGwE8MWsuv"]
        )


class ListPlaylistsTestCase(unittest.TestCase):
    def setUp(self):
        self.spotify = MagicMock()
        self.spotify.next.return_value = None
        self.playlists = Playlists(self.spotify)

    def test_list_all(self):
        self.spotify.current_user_playlists.return_value = {"items": PLAYLIST_LIST}

        playlists = self.playlists.list_all_playlists()
        self.assertEqual(6, len(playlists))
        print(playlists)

    def test_filter(self):
        self.spotify.current_user_playlists.return_value = {"items": PLAYLIST_LIST}

        playlists = self.playlists.list_all_playlists(filters="name:eq:Overplayed")
        self.assertEqual(1, len(playlists))
        self.assertEqual("Overplayed", playlists[0][FieldName.PLAYLIST_NAME])
        print(playlists)

    def test_sort(self):
        self.spotify.current_user_playlists.return_value = {"items": PLAYLIST_LIST}

        playlists = self.playlists.list_all_playlists(sort_fields="name:rev")
        self.assertEqual(6, len(playlists))
        self.assertEqual("Your Top Songs 2022", playlists[0][FieldName.PLAYLIST_NAME])
        print(playlists)


class RandomizePlaylistTestCase(unittest.TestCase):
    def setUp(self):
        self.spotify = MagicMock()
        self.spotify.next.return_value = None
        self.playlists = Playlists(self.spotify)

    def test_randomize(self):
        self.spotify.playlist_items.side_effect = get_canned_tracks

        playlist = {'id': '37i9dQZF1E37hnawmowyJn', 'name': 'test_name'}
        result = self.playlists.randomize_playlist(playlist)
        self.assertEqual(PlaylistResult.SUCCESS, result)

        self.spotify.playlist_replace_items.assert_called_with(
            '37i9dQZF1E37hnawmowyJn', ANY)
