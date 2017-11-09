from unittest import TestCase
from mock import patch, MagicMock
import pconf
from pconf.store.env import Env


TEST_ENV_BASE_VARS = {'env__var': 'result', 'env__var2': 'second_result', }
TEST_ENV_MATCHED_VARS = {'matched_var': 'match'}
TEST_ENV_WHITELIST_VARS = {'whitelisted_var': 'whitelist'}
TEST_SEPARATED_VARS = {'env': {'var': 'result', 'var2': 'second_result'}}
TEST_ENV_VARS = dict(TEST_ENV_WHITELIST_VARS, **TEST_ENV_MATCHED_VARS)
TEST_SEPARATED_VARS = dict(TEST_SEPARATED_VARS, **TEST_ENV_VARS)
TEST_ENV_VARS = dict(TEST_ENV_VARS, **TEST_ENV_BASE_VARS)
TEST_ENV_TYPED_VARS = {'key': 'value', 'int': '123', 'float': '1.23', 'complex': '1+2j', 'list': "['list1', 'list2', {'dict_in_list': 'value'}]", 'dict': "{'nested_dict': 'nested_value'}", 'tuple': "(123, 'string')", 'bool': 'True', 'boolstring': 'false', 'string_with_specials': 'Test!@#$%^&*()-_=+[]{};:,<.>/?\\\'\"`~'}
TEST_ENV_TYPED_VARS_PARSED = {'key': 'value', 'int': 123, 'float': 1.23, 'complex': 1+2j, 'list': ['list1', 'list2', {'dict_in_list': 'value'}], 'dict': {'nested_dict': 'nested_value'}, 'tuple': (123, 'string'), 'bool': True, 'boolstring': False, 'string_with_specials': 'Test!@#$%^&*()-_=+[]{};:,<.>/?\\\'\"`~'}

TEST_SEPARATOR = '__'
TEST_MATCH = r'^matched'
TEST_WHITELIST = ['whitelisted_var', 'whitelist2']
TEST_PARSE_VALUES = True


class TestEnv(TestCase):
    def test_default_params(self):
        env_store = Env()

        self.assertEqual(env_store.separator, None)
        self.assertEqual(env_store.match, None)
        self.assertEqual(env_store.whitelist, None)
        self.assertEqual(env_store.parse_values, False)

    def test_optional_params(self):
        env_store = Env(separator=TEST_SEPARATOR, match=TEST_MATCH, whitelist=TEST_WHITELIST, parse_values=TEST_PARSE_VALUES)

        self.assertEqual(env_store.separator, TEST_SEPARATOR)
        self.assertEqual(env_store.match, TEST_MATCH)
        self.assertEqual(env_store.whitelist, TEST_WHITELIST)
        self.assertEqual(env_store.parse_values, TEST_PARSE_VALUES)

    @patch('pconf.store.env.os', new=MagicMock())
    def test_get_all_vars(self):
        pconf.store.env.os.environ = TEST_ENV_VARS

        env_store = Env()
        result = env_store.get()

        self.assertEqual(result, TEST_ENV_VARS)
        self.assertIsInstance(result, dict)

    @patch('pconf.store.env.os', new=MagicMock())
    def test_get_idempotent(self):
        pconf.store.env.os.environ = TEST_ENV_VARS

        env_store = Env()
        result = env_store.get()

        self.assertEqual(result, TEST_ENV_VARS)
        self.assertIsInstance(result, dict)

        pconf.store.env.os.environ = TEST_ENV_BASE_VARS
        result = env_store.get()

        self.assertEqual(result, TEST_ENV_VARS)
        self.assertIsInstance(result, dict)

    @patch('pconf.store.env.os', new=MagicMock())
    def test_whitelist(self):
        pconf.store.env.os.environ = TEST_ENV_VARS
        env_store = Env(whitelist=TEST_WHITELIST)
        result = env_store.get()

        self.assertEqual(result, TEST_ENV_WHITELIST_VARS)
        self.assertIsInstance(result, dict)

    @patch('pconf.store.env.os', new=MagicMock())
    def test_match(self):
        pconf.store.env.os.environ = TEST_ENV_VARS
        env_store = Env(match=TEST_MATCH)
        result = env_store.get()

        self.assertEqual(result, TEST_ENV_MATCHED_VARS)
        self.assertIsInstance(result, dict)

    @patch('pconf.store.env.os', new=MagicMock())
    def test_whitelist_and_match(self):
        pconf.store.env.os.environ = TEST_ENV_VARS
        env_store = Env(match=TEST_MATCH, whitelist=TEST_WHITELIST)
        result = env_store.get()

        self.assertEqual(result, dict(TEST_ENV_MATCHED_VARS, **TEST_ENV_WHITELIST_VARS))
        self.assertIsInstance(result, dict)

    @patch('pconf.store.env.os', new=MagicMock())
    def test_separator(self):
        pconf.store.env.os.environ = TEST_ENV_VARS
        env_store = Env(separator=TEST_SEPARATOR)
        result = env_store.get()

        self.assertEqual(result, TEST_SEPARATED_VARS)
        self.assertIsInstance(result, dict)

    @patch('pconf.store.env.os', new=MagicMock())
    def test_parse_values(self):
        pconf.store.env.os.environ = TEST_ENV_TYPED_VARS
        env_store = Env(parse_values=True)
        result = env_store.get()
        self.assertEqual(result, TEST_ENV_TYPED_VARS_PARSED)
