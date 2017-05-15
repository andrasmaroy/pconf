from unittest import TestCase
from mock import patch, mock_open, MagicMock
from pconf.store.file import File
import __builtin__


TEST_FILE_PATH = 'test'
TEST_FILE_DICT = {'file': 'result'}
TEST_FILE_RAW = '{"file": "result"}'
TEST_FILE_JSON = '{"file": "result"}'


def throw_ioerror(*args, **kwargs):
    raise IOError('test')


class TestFile(TestCase):
    @patch('__builtin__.open')
    def test_open_right_file(self, mock_open):
        File(TEST_FILE_PATH)

        mock_open.assert_called_once_with(TEST_FILE_PATH, 'r')

    @patch('__builtin__.open', side_effect=throw_ioerror)
    def test_open_nonexistent_file_returns_empty_dict(self, mock_open):
        file_store = File(TEST_FILE_PATH)
        result = file_store.get()

        self.assertEqual(result, {})
        self.assertIsInstance(result, dict)

    @patch('__builtin__.open'.format(__name__), side_effect=throw_ioerror)
    def test_custom_encoding_without_parser_returns_empty_dict(self, mock_open):
        file_store = File(TEST_FILE_PATH, encoding='foo')
        result = file_store.get()

        self.assertEqual(result, {})
        self.assertIsInstance(result, dict)

    @patch('__builtin__.open', mock_open(read_data=TEST_FILE_RAW))
    def test_get_raw(self):
        file_store = File(TEST_FILE_PATH)
        result = file_store.get()

        self.assertEqual(result, TEST_FILE_DICT)
        self.assertIsInstance(result, dict)

    @patch('__builtin__.open', mock_open(read_data=TEST_FILE_RAW))
    def test_get_idempotent(self):
        file_store = File(TEST_FILE_RAW)
        result = file_store.get()

        self.assertEqual(result, TEST_FILE_DICT)
        self.assertIsInstance(result, dict)

        result = file_store.get()

        self.assertEqual(result, TEST_FILE_DICT)
        self.assertIsInstance(result, dict)
        __builtin__.open.assert_called_once()

    @patch('__builtin__.open', mock_open(read_data=TEST_FILE_RAW))
    def test_get_custom_encoding(self):
        mock_parser = MagicMock()
        mock_parser.return_value = TEST_FILE_DICT
        file_store = File(TEST_FILE_PATH, encoding='custom', parser=mock_parser)
        result = file_store.get()

        mock_parser.assert_called_once_with(TEST_FILE_RAW)
        self.assertEqual(result, TEST_FILE_DICT)
        self.assertIsInstance(result, dict)

    @patch('__builtin__.open', mock_open(read_data=TEST_FILE_JSON))
    def test_get_json(self):
        file_store = File(TEST_FILE_PATH, encoding='json')
        result = file_store.get()

        self.assertEqual(result, TEST_FILE_DICT)
        self.assertIsInstance(result, dict)
