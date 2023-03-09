import unittest

from spotcrates.cli import parse_cmdline, CommandLookup
from spotcrates.common import NotFoundException


class ArgparseTestCase(unittest.TestCase):
    def test_no_command(self):
        with self.assertRaises(SystemExit) as cm:
            parse_cmdline([])

        self.assertEqual(cm.exception.code, 2)

    def test_command(self):
        args, result_code = parse_cmdline(['test-command'])
        self.assertEqual(0, result_code)
        self.assertEqual('test-command', args.command)
        self.assertFalse(args.randomize)

    def test_random_before(self):
        args, result_code = parse_cmdline(['-r', 'test-command'])
        self.assertEqual(0, result_code)
        self.assertEqual('test-command', args.command)
        self.assertTrue(args.randomize)

    def test_random_after(self):
        args, result_code = parse_cmdline(['test-command', '-r'])
        self.assertEqual(0, result_code)
        self.assertEqual('test-command', args.command)
        self.assertTrue(args.randomize)

    def test_random_after_1arg(self):
        args, result_code = parse_cmdline(['test-command', 'arg1', '-r'])
        self.assertEqual(0, result_code)
        self.assertEqual('test-command', args.command)
        self.assertTrue(args.randomize)
        self.assertSequenceEqual(['arg1'], args.arguments)

    def test_random_after_2args(self):
        args, result_code = parse_cmdline(['test-command', 'arg1', 'arg2', '-r'])
        self.assertEqual(0, result_code)
        self.assertEqual('test-command', args.command)
        self.assertTrue(args.randomize)
        self.assertSequenceEqual(['arg1', 'arg2'], args.arguments)

    def test_random_after_3args(self):
        args, result_code = parse_cmdline(['test-command', 'arg1', 'arg2', 'arg3', '-r'])
        self.assertEqual(0, result_code)
        self.assertEqual('test-command', args.command)
        self.assertTrue(args.randomize)
        self.assertSequenceEqual(['arg1', 'arg2', 'arg3'], args.arguments)


class CommandNameTestCase(unittest.TestCase):
    def setUp(self):
        self.lookup = CommandLookup()

    def test_daily(self):
        self.assertEqual("daily", self.lookup.find("da"))

    def test_list_playlists(self):
        self.assertEqual("list-playlists", self.lookup.find("list"))

    def test_subscriptions(self):
        self.assertEqual("subscriptions", self.lookup.find("subs"))

    def test_randomize(self):
        self.assertEqual("randomize", self.lookup.find("rand"))

    def test_copy(self):
        self.assertEqual("copy", self.lookup.find("copy"))

    def test_commands(self):
        self.assertEqual("commands", self.lookup.find("commands"))

    def test_invalid(self):
        with self.assertRaises(NotFoundException):
            self.lookup.find("zzzinvalid")

    def test_none(self):
        with self.assertRaises(NotFoundException):
            self.lookup.find(None)

    def test_blank(self):
        with self.assertRaises(NotFoundException):
            self.lookup.find("")
