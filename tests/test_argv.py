import sys
from unittest import TestCase
from pconf.store.argv import Argv

TEST_ARGV = {'name': '--argv', 'short_name': '-a', 'type': str, 'help': 'help text'}
TEST_ARGV_RESULT = {'argv': 'result'}
TEST_ARGV_BOOL_RESULT = {'argv': True}
TEST_LITERAL_DICT = {'name': '--dict', 'value': "{'key': 'value'}", 'result': {'key': 'value'}}
TEST_LITERAL_LIST = {'name': '--list', 'value': "['list1', 'list2']", 'result': ['list1', 'list2']}
TEST_LITERAL_TUPLE = {'name': '--tuple', 'value': "('tuple1', 'tuple2')", 'result': ('tuple1', 'tuple2')}
TEST_INVALID_KEY = "this is an invalid key, because it doesn't start with dashes"
TEST_DASH_IN_KEY = '--dash-this'
TEST_DASH_IN_KEY_RESULT = {'dash-this': True}


class TestArgv(TestCase):
    def setUp(self):
        sys.argv = [sys.argv[0]]
        Argv.parser = None

    def tearDown(self):
        sys.argv = [sys.argv[0]]
        Argv.parser = None

    def test_args_default_params(self):
        sys.argv.append(TEST_ARGV['name'])
        sys.argv.append(TEST_ARGV_RESULT[TEST_ARGV['name'].replace('--', '')])

        arg_name = TEST_ARGV['name']
        argv_store = Argv(arg_name)
        result = argv_store.get()

        self.assertEqual(result, TEST_ARGV_RESULT)
        self.assertIsInstance(result, dict)

    def test_args_optional_params(self):
        sys.argv.append(TEST_ARGV['short_name'])
        sys.argv.append(TEST_ARGV_RESULT[TEST_ARGV['name'].replace('--', '')])

        arg_name = TEST_ARGV['name']
        arg_short_name = TEST_ARGV['short_name']
        arg_type = TEST_ARGV['type']
        arg_help = TEST_ARGV['help']
        argv_store = Argv(arg_name, arg_short_name, arg_type, arg_help)
        result = argv_store.get()

        self.assertEqual(result, TEST_ARGV_RESULT)
        self.assertIsInstance(result, dict)

    def test_args_optional_params_without_short(self):
        sys.argv.append(TEST_ARGV['name'])
        sys.argv.append(TEST_ARGV_RESULT[TEST_ARGV['name'].replace('--', '')])

        arg_name = TEST_ARGV['name']
        arg_type = TEST_ARGV['type']
        arg_help = TEST_ARGV['help']
        argv_store = Argv(arg_name, type=arg_type, help=arg_help)
        result = argv_store.get()

        self.assertEqual(result, TEST_ARGV_RESULT)
        self.assertIsInstance(result, dict)

    def test_bool_arg(self):
        sys.argv.append(TEST_ARGV['name'])

        arg_name = TEST_ARGV['name']
        arg_type = bool
        argv_store = Argv(arg_name, type=arg_type)
        result = argv_store.get()

        self.assertEqual(result, TEST_ARGV_BOOL_RESULT)
        self.assertIsInstance(result, dict)

    def test_literal_dict(self):
        sys.argv.append(TEST_LITERAL_DICT['name'])
        sys.argv.append(TEST_LITERAL_DICT['value'])
        argv_store = Argv(TEST_LITERAL_DICT['name'], type=type(TEST_LITERAL_DICT['result']))
        result = argv_store.get()

        self.assertEqual(result, {str(TEST_LITERAL_DICT['name']).replace('--', ''): TEST_LITERAL_DICT['result']})

    def test_literal_tuple(self):
        sys.argv.append(TEST_LITERAL_TUPLE['name'])
        sys.argv.append(TEST_LITERAL_TUPLE['value'])
        argv_store = Argv(TEST_LITERAL_TUPLE['name'], type=type(TEST_LITERAL_TUPLE['result']))
        result = argv_store.get()

        self.assertEqual(result, {str(TEST_LITERAL_TUPLE['name']).replace('--', ''): TEST_LITERAL_TUPLE['result']})

    def test_literal_list(self):
        sys.argv.append(TEST_LITERAL_LIST['name'])
        sys.argv.append(TEST_LITERAL_LIST['value'])
        argv_store = Argv(TEST_LITERAL_LIST['name'], type=type(TEST_LITERAL_LIST['result']))
        result = argv_store.get()

        self.assertEqual(result, {str(TEST_LITERAL_LIST['name']).replace('--', ''): TEST_LITERAL_LIST['result']})

    def test_repeated_list(self):
        for value in TEST_LITERAL_LIST['result']:
            sys.argv.append(TEST_LITERAL_LIST['name'])
            sys.argv.append(value)

        argv_store = Argv(TEST_LITERAL_LIST['name'], type='repeated_list')
        result = argv_store.get()

        self.assertEqual(result, {str(TEST_LITERAL_LIST['name']).replace('--', ''): TEST_LITERAL_LIST['result']})

    def test_invalid_name(self):
        with self.assertRaises(ValueError):
            Argv(TEST_INVALID_KEY)

    def test_dash_in_name(self):
        sys.argv.append(TEST_DASH_IN_KEY)

        arg_name = TEST_DASH_IN_KEY
        arg_type = bool
        argv_store = Argv(arg_name, type=arg_type)
        result = argv_store.get()

        self.assertEqual(result, TEST_DASH_IN_KEY_RESULT)
        self.assertIsInstance(result, dict)
