from unittest import TestCase
from mock import patch, MagicMock
import pconf
from pconf import Pconf
from pconf.store.file import File
from pconf.store.env import Env
from pconf.store.memory import Memory
from pconf.store.argv import Argv


TEST_FILE_PATH = 'test'
TEST_FILE_RESULT = {'file': 'result'}
TEST_ENV_RESULT = {'env': 'result'}
TEST_DEFAULTS = {'defaults': 'result'}
TEST_OVERRIDES = {'overrides': 'result'}
TEST_ARGV = {'name': 'test', 'short_name': 't', 'type': str, 'help': 'help text'}
TEST_ARGV_RESULT = {'test': True, 'argv': 'result'}


class TestPconf(TestCase):
    def setUp(self):
        Pconf._Pconf__hierarchy = []

    def test_get_empty_dict_by_default(self):
        self.assertEqual(Pconf.get(), {})

    @patch('pconf.store.file.File', new=MagicMock(), spec=File)
    def test_file(self):
        Pconf.file(path=TEST_FILE_PATH)

        pconf.store.file.File.assert_called_once_with(TEST_FILE_PATH, None, None)
        self.assertEqual(len(Pconf._Pconf__hierarchy), 1)

    @patch('pconf.store.file.File', new=MagicMock(), spec=File)
    def test_file_optional_params(self):
        encoding = 'custom'
        mock_parser = MagicMock()
        Pconf.file(path=TEST_FILE_PATH, encoding=encoding, parser=mock_parser)

        pconf.store.file.File.assert_called_once_with(TEST_FILE_PATH, encoding, mock_parser)
        self.assertEqual(len(Pconf._Pconf__hierarchy), 1)

    @patch('pconf.store.file.File')
    def test_file_get(self, mock_file):
        mocked_file = MagicMock()
        mocked_file.get.return_value = TEST_FILE_RESULT
        mock_file.return_value = mocked_file

        Pconf.file(path=TEST_FILE_PATH)
        results = Pconf.get()

        mocked_file.get.assert_called_once()
        for key in TEST_FILE_RESULT:
            self.assertTrue(key in results)
            self.assertEqual(results[key], TEST_FILE_RESULT[key])

    @patch('pconf.store.env.Env', new=MagicMock(), spec=Env)
    def test_env(self):
        Pconf.env()

        pconf.store.env.Env.assert_called_once_with(None, None, None, None, None, None)
        self.assertEqual(len(Pconf._Pconf__hierarchy), 1)

    @patch('pconf.store.env.Env', new=MagicMock(), spec=Env)
    def test_env_optional_params(self):
        separator = 'separator'
        match = 'match'
        whitelist = 'whitelist'
        parse_values = True
        to_lower = True
        convert_underscores = True
        Pconf.env(separator, match, whitelist, parse_values, to_lower, convert_underscores)

        pconf.store.env.Env.assert_called_once_with(separator, match, whitelist, parse_values, to_lower, convert_underscores)
        self.assertEqual(len(Pconf._Pconf__hierarchy), 1)

    @patch('pconf.store.env.Env')
    def test_env_get(self, mock_env):
        mocked_env = MagicMock()
        mocked_env.get.return_value = TEST_ENV_RESULT
        mock_env.return_value = mocked_env

        Pconf.env()
        results = Pconf.get()

        mocked_env.get.assert_called_once()
        for key in TEST_ENV_RESULT:
            self.assertTrue(key in results)
            self.assertEqual(results[key], TEST_ENV_RESULT[key])

    @patch('pconf.store.memory.Memory', new=MagicMock(), spec=Memory)
    def test_defaults(self):
        Pconf.defaults(TEST_DEFAULTS)

        pconf.store.memory.Memory.assert_called_once_with(TEST_DEFAULTS)
        self.assertEqual(len(Pconf._Pconf__hierarchy), 1)

    def test_defaults_get(self):
        Pconf.defaults(TEST_DEFAULTS)
        self.assertEqual(Pconf.get(), TEST_DEFAULTS)

    @patch('pconf.store.memory.Memory', new=MagicMock(), spec=Memory)
    def test_overrides(self):
        Pconf.overrides(TEST_OVERRIDES)

        pconf.store.memory.Memory.assert_called_once_with(TEST_OVERRIDES)
        self.assertEqual(len(Pconf._Pconf__hierarchy), 1)

    def test_overrides_get(self):
        Pconf.defaults(TEST_OVERRIDES)
        self.assertEqual(Pconf.get(), TEST_OVERRIDES)

    @patch('pconf.store.argv.Argv', new=MagicMock(), spec=Argv)
    def test_argv(self):
        arg_name = TEST_ARGV['name']
        Pconf.argv(arg_name)

        pconf.store.argv.Argv.assert_called_once_with(arg_name, None, None, None)
        self.assertEqual(len(Pconf._Pconf__hierarchy), 1)

    @patch('pconf.store.argv.Argv', new=MagicMock(), spec=Argv)
    def test_argv_type_optional(self):
        arg_name = TEST_ARGV['name']
        arg_short_name = TEST_ARGV['short_name']
        arg_type = TEST_ARGV['type']
        arg_help = TEST_ARGV['help']
        Pconf.argv(arg_name, arg_short_name, arg_type, arg_help)

        pconf.store.argv.Argv.assert_called_once_with(arg_name, arg_short_name, arg_type, arg_help)
        self.assertEqual(len(Pconf._Pconf__hierarchy), 1)

    @patch('pconf.store.argv.Argv')
    def test_argv_get(self, mock_argv):
        mocked_argv = MagicMock()
        mocked_argv.get.return_value = TEST_ARGV_RESULT
        mock_argv.return_value = mocked_argv

        arg_name = TEST_ARGV['name']
        Pconf.argv(arg_name)
        results = Pconf.get()

        for key in TEST_ARGV_RESULT:
            self.assertTrue(key in results)
            self.assertEqual(results[key], TEST_ARGV_RESULT[key])
