from unittest import TestCase
from mock import patch, MagicMock
from pconf import Pconf


TEST_FILE_PATH = 'test'
TEST_FILE_RESULT = {'file': 'result', 'overlapping': 'file'}
TEST_ENV_RESULT = {'env': 'result', 'overlapping': 'env'}


class TestHierarchy(TestCase):
    def setUp(self):
        Pconf._Pconf__hierarchy = []

    @patch('pconf.store.env.Env')
    @patch('pconf.store.file.File')
    def test_forward(self, mock_file, mock_env):
        mocked_env = MagicMock()
        mocked_env.get.return_value = TEST_ENV_RESULT
        mock_env.return_value = mocked_env

        mocked_file = MagicMock()
        mocked_file.get.return_value = TEST_FILE_RESULT
        mock_file.return_value = mocked_file

        Pconf.env()
        Pconf.file(TEST_FILE_PATH)
        results = Pconf.get()

        self.assertEqual(results['overlapping'], TEST_ENV_RESULT['overlapping'])
        for key in TEST_FILE_RESULT:
            if key == 'overlapping':
                continue
            self.assertTrue(key in results)
            self.assertEqual(results[key], TEST_FILE_RESULT[key])

        for key in TEST_ENV_RESULT:
            if key == 'overlapping':
                continue
            self.assertTrue(key in results)
            self.assertEqual(results[key], TEST_ENV_RESULT[key])

    @patch('pconf.store.env.Env')
    @patch('pconf.store.file.File')
    def test_backward(self, mock_file, mock_env):
        mocked_env = MagicMock()
        mocked_env.get.return_value = TEST_ENV_RESULT
        mock_env.return_value = mocked_env

        mocked_file = MagicMock()
        mocked_file.get.return_value = TEST_FILE_RESULT
        mock_file.return_value = mocked_file

        Pconf.file(TEST_FILE_PATH)
        Pconf.env()
        results = Pconf.get()

        self.assertEqual(results['overlapping'], TEST_FILE_RESULT['overlapping'])
        for key in TEST_FILE_RESULT:
            if key == 'overlapping':
                continue
            self.assertTrue(key in results)
            self.assertEqual(results[key], TEST_FILE_RESULT[key])

        for key in TEST_ENV_RESULT:
            if key == 'overlapping':
                continue
            self.assertTrue(key in results)
            self.assertEqual(results[key], TEST_ENV_RESULT[key])
