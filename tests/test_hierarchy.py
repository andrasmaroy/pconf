from unittest import TestCase
from mock import patch, MagicMock
from pconf import Pconf


class TestHierarchy(TestCase):
    def setUp(self):
        Pconf.clear()
        self.TEST_FILE_PATH = "test"
        self.TEST_FILE_RESULT = {
            "file": "result",
            "overlapping": "file",
            "deep": {"stillhere": "stillhere", "overlapping": "file"},
        }
        self.TEST_ENV_RESULT = {
            "env": "result",
            "overlapping": "env",
            "deep": {"overlapping": "env"},
        }

    @patch("pconf.store.env.Env")
    @patch("pconf.store.file.File")
    def test_forward(self, mock_file, mock_env):
        mocked_env = MagicMock()
        mocked_env.get.return_value = self.TEST_ENV_RESULT
        mock_env.return_value = mocked_env

        mocked_file = MagicMock()
        mocked_file.get.return_value = self.TEST_FILE_RESULT
        mock_file.return_value = mocked_file

        Pconf.env()
        Pconf.file(self.TEST_FILE_PATH)
        results = Pconf.get()

        expected = {
            "file": "result",
            "env": "result",
            "overlapping": "env",
            "deep": {"stillhere": "stillhere", "overlapping": "env"},
        }

        self.assertEqual(expected, results)

    @patch("pconf.store.env.Env")
    @patch("pconf.store.file.File")
    def test_double_forward(self, mock_file, mock_env):
        mocked_env = MagicMock()
        mocked_env.get.return_value = self.TEST_ENV_RESULT
        mock_env.return_value = mocked_env

        mocked_file = MagicMock()
        mocked_file.get.return_value = self.TEST_FILE_RESULT
        mock_file.return_value = mocked_file

        Pconf.env()
        Pconf.file(self.TEST_FILE_PATH)
        Pconf.get()
        results = Pconf.get()

        expected = {
            "file": "result",
            "env": "result",
            "overlapping": "env",
            "deep": {"stillhere": "stillhere", "overlapping": "env"},
        }

        self.assertEqual(expected, results)

    @patch("pconf.store.env.Env")
    @patch("pconf.store.file.File")
    def test_backward(self, mock_file, mock_env):
        mocked_env = MagicMock()
        mocked_env.get.return_value = self.TEST_ENV_RESULT
        mock_env.return_value = mocked_env

        mocked_file = MagicMock()
        mocked_file.get.return_value = self.TEST_FILE_RESULT
        mock_file.return_value = mocked_file

        Pconf.file(self.TEST_FILE_PATH)
        Pconf.env()
        results = Pconf.get()

        expected = {
            "file": "result",
            "env": "result",
            "overlapping": "file",
            "deep": {"stillhere": "stillhere", "overlapping": "file"},
        }

        self.assertEqual(expected, results)

    @patch("pconf.store.env.Env")
    @patch("pconf.store.file.File")
    def test_double_backward(self, mock_file, mock_env):
        mocked_env = MagicMock()
        mocked_env.get.return_value = self.TEST_ENV_RESULT
        mock_env.return_value = mocked_env

        mocked_file = MagicMock()
        mocked_file.get.return_value = self.TEST_FILE_RESULT
        mock_file.return_value = mocked_file

        Pconf.file(self.TEST_FILE_PATH)
        Pconf.env()
        Pconf.get()
        results = Pconf.get()

        expected = {
            "file": "result",
            "env": "result",
            "overlapping": "file",
            "deep": {"stillhere": "stillhere", "overlapping": "file"},
        }

        self.assertEqual(expected, results)
