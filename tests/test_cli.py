import unittest

from spotcrates.cli import parse_cmdline


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