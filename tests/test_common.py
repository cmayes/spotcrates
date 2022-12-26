import unittest

from spotcrates.common import truncate_long_value


# truncate_long_value

class TruncateLongValueTestCase(unittest.TestCase):
    def test_default_trunc(self):
        self.assertEqual("some_", truncate_long_value("some_long_string", 5))

    def test_end_trunc(self):
        self.assertEqual("tring", truncate_long_value("some_long_string", 5, trim_tail=False))

    def test_empty(self):
        self.assertEqual("", truncate_long_value("", 5, trim_tail=False))

    def test_null(self):
        self.assertEqual(None, truncate_long_value(None, 5, trim_tail=False))
