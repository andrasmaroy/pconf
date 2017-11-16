from unittest import TestCase
from mock import patch, MagicMock
import pconf
from pconf.store.argv import Argv
from argparse import Namespace, SUPPRESS

TEST_ARGV = {'name': 'argv', 'short_name': 'a', 'type': str, 'help': 'help text'}
TEST_ARGV_RESULT = {'argv': 'result'}
TEST_ARGV_NAMESPACE = Namespace(argv='result')
TEST_LITERAL_ARGV = [
        {'dict:': {'key': 'value'}},
        {'list': ['list1', 'list2']},
        {'set': {'set1', 'set2'}},
        {'tuple': ('tuple1', 'tuple2')}
        ]


class TestArgv(TestCase):
    @patch('pconf.store.argv.argparse', new=MagicMock())
    def test_args_default_params(self):
        mock_parser = MagicMock()
        mock_parser.parse_known_args.return_value = (TEST_ARGV_NAMESPACE, [])
        pconf.store.argv.argparse.SUPPRESS = SUPPRESS
        pconf.store.argv.Argv.parser = mock_parser

        arg_name = TEST_ARGV['name']
        argv_store = Argv(arg_name)
        result = argv_store.get()

        mock_parser.add_argument.assert_called_once_with(arg_name, type=None, help=None, default=SUPPRESS)
        mock_parser.parse_known_args.assert_called_once()

        self.assertEqual(result, TEST_ARGV_RESULT)
        self.assertIsInstance(result, dict)

    @patch('pconf.store.argv.argparse', new=MagicMock())
    def test_args_optional_params(self):
        mock_parser = MagicMock()
        mock_parser.parse_known_args.return_value = (TEST_ARGV_NAMESPACE, [])
        pconf.store.argv.argparse.SUPPRESS = SUPPRESS
        pconf.store.argv.Argv.parser = mock_parser

        arg_name = TEST_ARGV['name']
        arg_short_name = TEST_ARGV['short_name']
        arg_type = TEST_ARGV['type']
        arg_help = TEST_ARGV['help']
        argv_store = Argv(arg_name, arg_short_name, arg_type, arg_help)
        result = argv_store.get()

        mock_parser.add_argument.assert_called_once_with(arg_name, arg_short_name, type=arg_type, help=arg_help, default=SUPPRESS)
        mock_parser.parse_known_args.assert_called_once()

        self.assertEqual(result, TEST_ARGV_RESULT)
        self.assertIsInstance(result, dict)

    @patch('pconf.store.argv.argparse', new=MagicMock())
    def test_args_optional_params_without_short(self):
        mock_parser = MagicMock()
        mock_parser.parse_known_args.return_value = (TEST_ARGV_NAMESPACE, [])
        pconf.store.argv.argparse.SUPPRESS = SUPPRESS
        pconf.store.argv.Argv.parser = mock_parser

        arg_name = TEST_ARGV['name']
        arg_type = TEST_ARGV['type']
        arg_help = TEST_ARGV['help']
        argv_store = Argv(arg_name, type=arg_type, help=arg_help)
        result = argv_store.get()

        mock_parser.add_argument.assert_called_once_with(arg_name, type=arg_type, help=arg_help, default=SUPPRESS)
        mock_parser.parse_known_args.assert_called_once()

        self.assertEqual(result, TEST_ARGV_RESULT)
        self.assertIsInstance(result, dict)

    @patch('pconf.store.argv.argparse', new=MagicMock())
    def test_bool_arg(self):
        mock_parser = MagicMock()
        mock_parser.parse_known_args.return_value = (TEST_ARGV_NAMESPACE, [])
        pconf.store.argv.argparse.SUPPRESS = SUPPRESS
        pconf.store.argv.Argv.parser = mock_parser

        arg_name = TEST_ARGV['name']
        arg_type = bool
        argv_store = Argv(arg_name, type=arg_type)
        result = argv_store.get()

        mock_parser.add_argument.assert_called_once_with(arg_name, action='store_true', help=None, default=SUPPRESS)
        mock_parser.parse_known_args.assert_called_once()

        self.assertEqual(result, TEST_ARGV_RESULT)
        self.assertIsInstance(result, dict)

    @patch('pconf.store.argv.argparse', new=MagicMock())
    def test_literal_arg(self):
        mock_parser = MagicMock()
        pconf.store.argv.argparse.SUPPRESS = SUPPRESS
        pconf.store.argv.Argv.parser = mock_parser

        for arg in TEST_LITERAL_ARGV:
            mock_parser.parse_known_args.return_value = (Namespace(**arg), [])
            Argv(list(arg.keys())[0], type=type(list(arg.values())[0]))
            mock_parser.add_argument.assert_called_once_with(
                    list(arg.keys())[0],
                    help=None,
                    default=SUPPRESS,
                    type=pconf.store.argv.literal_eval)
            mock_parser.reset_mock()
