from unittest import TestCase
from mock import patch, MagicMock
import pconf
from pconf import Pconf
from pconf.store.file import File
from pconf.store.env import Env


TEST_FILE_PATH = 'test'
TEST_FILE_RESULT = {'file': 'result'}
TEST_ENV_RESULT = {'env': 'result'}


class TestPconf(TestCase):
    def setUp(self):
        Pconf._Pconf__hierarchy = []

    def test_get_empty_dict_by_default(self):
        self.assertEqual(Pconf.get(), {})

    @patch('pconf.store.file.File', new=MagicMock(), spec=File)
    def test_file(self):
        encoding = 'custom'
        mock_parser = MagicMock()
        Pconf.file(path=TEST_FILE_PATH, encoding=encoding, parser=mock_parser)

        pconf.store.file.File.assert_called_once_with(TEST_FILE_PATH, encoding, mock_parser)
        self.assertEqual(len(Pconf._Pconf__hierarchy), 1)

    @patch('pconf.store.file.File', new=MagicMock(), spec=File)
    def test_file_get(self):
        Pconf.file(path=TEST_FILE_PATH)
        Pconf._Pconf__hierarchy[0].get.return_value = TEST_FILE_RESULT

        results = Pconf.get()

        Pconf._Pconf__hierarchy[0].get.assert_called_once()
        for key in TEST_FILE_RESULT.iterkeys():
            self.assertTrue(key in results)
            self.assertEqual(results[key], TEST_FILE_RESULT[key])

    @patch('pconf.store.env.Env', new=MagicMock(), spec=Env)
    def test_env(self):
        Pconf.env()

        pconf.store.env.Env.assert_called_once()
        self.assertEqual(len(Pconf._Pconf__hierarchy), 1)

    @patch('pconf.store.env.Env', new=MagicMock(), spec=Env)
    def test_env_get(self):
        Pconf.env()
        Pconf._Pconf__hierarchy[0].get.return_value = TEST_ENV_RESULT
        results = Pconf.get()

        Pconf._Pconf__hierarchy[0].get.assert_called_once()
        for key in TEST_ENV_RESULT.iterkeys():
            self.assertTrue(key in results)
            self.assertEqual(results[key], TEST_ENV_RESULT[key])
