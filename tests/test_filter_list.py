import os
import unittest

from spotcrates.filters import filter_list
from tests.test_playlists import file_json

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
TRACKS_DAILY1 = file_json(os.path.join(DATA_DIR, 'tracks_daily1.json'))


class FilterListTestCase(unittest.TestCase):
    # filter_list
    def test_null_filter(self):
        # filters: Dict[FieldName, List[FieldFilter]]
        filter_list(TRACKS_DAILY1, )
