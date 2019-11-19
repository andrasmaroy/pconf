from unittest import TestCase, skipIf
from mock import patch, mock_open, MagicMock
from pconf.store.file import File
from sys import version_info
from warnings import simplefilter


TEST_FILE_PATH = "test"
TEST_FILE_DICT = {"file": "result"}
TEST_FILE_RAW = '{"file": "result"}'
TEST_FILE_JSON = '{"file": "result"}'
TEST_FILE_JSON_NONE = '{"empty": null}'
TEST_FILE_YAML = """
---
   file: result
"""
TEST_FILE_YAML_NONE = """
---
  empty:
"""
TEST_FILE_LIST = """
---
- item1
- item2
"""
TEST_FILE_INI = """
[DEFAULT]
file=result
"""
TEST_FILE_INI_WITH_SECTION = """
[test]
file=result
"""
TEST_FILE_INI_WITH_SECTION_DICT = {"test": {"file": "result"}}
if version_info.major < 3:
    import __builtin__

    MOCK_OPEN_FUNCTION = "__builtin__.open"
else:
    import builtins

    MOCK_OPEN_FUNCTION = "builtins.open"


def throw_ioerror(*args, **kwargs):
    raise IOError("test")


class TestFile(TestCase):
    @patch(MOCK_OPEN_FUNCTION)
    def test_open_right_file(self, mock_open):
        File(TEST_FILE_PATH)

        mock_open.assert_called_once_with(TEST_FILE_PATH, "r")

    @patch(MOCK_OPEN_FUNCTION, side_effect=throw_ioerror)
    def test_open_nonexistent_file_returns_empty_dict(self, mock_open):
        simplefilter("ignore")
        file_store = File(TEST_FILE_PATH)
        result = file_store.get()

        self.assertEqual(result, {})
        self.assertIsInstance(result, dict)

    @patch(MOCK_OPEN_FUNCTION, mock_open(read_data=TEST_FILE_RAW))
    def test_custom_encoding_without_parser_returns_empty_dict(self):
        file_store = File(TEST_FILE_PATH, encoding="foo")
        result = file_store.get()

        self.assertEqual(result, {})
        self.assertIsInstance(result, dict)

    @patch(MOCK_OPEN_FUNCTION, mock_open(read_data=TEST_FILE_RAW))
    def test_get_raw(self):
        file_store = File(TEST_FILE_PATH)
        result = file_store.get()

        self.assertEqual(result, TEST_FILE_DICT)
        self.assertIsInstance(result, dict)

    @patch(MOCK_OPEN_FUNCTION, mock_open(read_data=TEST_FILE_RAW))
    def test_get_idempotent(self):
        file_store = File(TEST_FILE_PATH)
        result = file_store.get()

        self.assertEqual(result, TEST_FILE_DICT)
        self.assertIsInstance(result, dict)

        result = file_store.get()

        self.assertEqual(result, TEST_FILE_DICT)
        self.assertIsInstance(result, dict)
        if version_info.major < 3:
            __builtin__.open.assert_called_once_with(TEST_FILE_PATH, "r")
        else:
            builtins.open.assert_called_once_with(TEST_FILE_PATH, "r")

    @patch(MOCK_OPEN_FUNCTION, mock_open(read_data=TEST_FILE_RAW))
    def test_get_custom_encoding(self):
        mock_parser = MagicMock()
        mock_parser.return_value = TEST_FILE_DICT
        file_store = File(TEST_FILE_PATH, encoding="custom", parser=mock_parser)
        result = file_store.get()

        mock_parser.assert_called_once_with(TEST_FILE_RAW)
        self.assertEqual(result, TEST_FILE_DICT)
        self.assertIsInstance(result, dict)

    @patch(MOCK_OPEN_FUNCTION, mock_open(read_data=TEST_FILE_JSON))
    def test_get_json(self):
        file_store = File(TEST_FILE_PATH, encoding="json")
        result = file_store.get()

        self.assertEqual(result, TEST_FILE_DICT)
        self.assertIsInstance(result, dict)

    @patch(MOCK_OPEN_FUNCTION, mock_open(read_data=TEST_FILE_JSON_NONE))
    def test_get_json_empty(self):
        file_store = File(TEST_FILE_PATH, encoding="json")
        result = file_store.get()

        self.assertEqual(result, {})

    @patch(MOCK_OPEN_FUNCTION, mock_open(read_data=TEST_FILE_YAML))
    def test_get_yaml(self):
        file_store = File(TEST_FILE_PATH, encoding="yaml")
        result = file_store.get()

        self.assertEqual(result, TEST_FILE_DICT)
        self.assertIsInstance(result, dict)

    @patch(MOCK_OPEN_FUNCTION, mock_open(read_data=TEST_FILE_YAML_NONE))
    def test_get_yaml_empty(self):
        file_store = File(TEST_FILE_PATH, encoding="yaml")
        result = file_store.get()

        self.assertEqual(result, {})

    @patch(MOCK_OPEN_FUNCTION, mock_open(read_data=TEST_FILE_LIST))
    def test_get_yaml_mergekey(self):
        file_store = File(TEST_FILE_PATH, encoding="yaml")
        result = file_store.get()

        self.assertEqual(result, {})

    @patch(MOCK_OPEN_FUNCTION, mock_open(read_data=TEST_FILE_INI))
    def test_get_ini(self):
        file_store = File(TEST_FILE_PATH, encoding="ini")
        result = file_store.get()

        self.assertEqual(result, TEST_FILE_DICT)
        self.assertIsInstance(result, dict)

    @patch(MOCK_OPEN_FUNCTION, mock_open(read_data=TEST_FILE_INI_WITH_SECTION))
    def test_get_ini_with_section(self):
        file_store = File(TEST_FILE_PATH, encoding="ini")
        result = file_store.get()

        self.assertEqual(result, TEST_FILE_INI_WITH_SECTION_DICT)
        self.assertIsInstance(result, dict)

    @patch(MOCK_OPEN_FUNCTION, side_effect=IOError("No such file or directory"))
    def test_non_existent_file(self, mock_open):
        simplefilter("ignore")
        file_store = File(TEST_FILE_PATH, encoding="yaml")
        result = file_store.get()

        self.assertEqual(result, {})

    @skipIf(version_info.major < 3, "Testing for warning not supported in Python2")
    @patch(MOCK_OPEN_FUNCTION, side_effect=throw_ioerror)
    def test_nonexsitent_file_raises_warning(self, mock_open):
        with self.assertWarns(UserWarning):
            File(TEST_FILE_PATH)
