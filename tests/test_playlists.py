import json
import os
import unittest
from unittest.mock import Mock

from spotcrates.playlists import Playlists

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
PLAYLIST_LIST_FILE = os.path.join(DATA_DIR, 'playlists.json')


class PlaylistTestCase(unittest.TestCase):

    def setUp(self):
        with open(PLAYLIST_LIST_FILE, 'r') as myfile:
            self.playlist_list = json.load(myfile)

    def test_list_all(self):
        spotify = Mock()
        spotify.current_user_playlists.return_value = {'items': self.playlist_list}

        playlists = Playlists(spotify)
        playlists.get_all_playlists()
        self.assertEqual(self.playlist_list, playlists.get_all_playlists())


