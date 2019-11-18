from mock import MagicMock, mock_open, patch
from sys import version_info
from unittest import TestCase
from warnings import simplefilter

import pconf
from pconf.store.env import Env


TEST_ENV_BASE_VARS = {'env__var': 'result', 'env__var_2': 'second_result', }
TEST_ENV_MATCHED_VARS = {'matched_var': 'match'}
TEST_ENV_WHITELIST_VARS = {'whitelisted_var': 'whitelist'}
TEST_SEPARATED_VARS = {'env': {'var': 'result', 'var_2': 'second_result'}}
TEST_ENV_VARS = dict(TEST_ENV_WHITELIST_VARS, **TEST_ENV_MATCHED_VARS)
TEST_SEPARATED_VARS = dict(TEST_SEPARATED_VARS, **TEST_ENV_VARS)
TEST_ENV_VARS = dict(TEST_ENV_VARS, **TEST_ENV_BASE_VARS)
TEST_ENV_CONVERTED = {'env--var': 'result', 'env--var-2': 'second_result', 'matched-var': 'match', 'whitelisted-var': 'whitelist'}
TEST_ENV_CONVERTED_SEPARATED = {'env': {'var': 'result', 'var-2': 'second_result'}, 'matched-var': 'match', 'whitelisted-var': 'whitelist'}
TEST_ENV_UPPERCASE = {'ENV__VAR': 'result', 'ENV__VAR_2': 'second_result', 'MATCHED_VAR': 'match', 'WHITELISTED_VAR': 'whitelist'}
TEST_ENV_TYPED_VARS = {'key': 'value', 'int': '123', 'float': '1.23', 'complex': '1+2j', 'list': "['list1', 'list2', {'dict_in_list': 'value'}]", 'dict': "{'nested_dict': 'nested_value'}", 'tuple': "(123, 'string')", 'bool': 'True', 'boolstring': 'false', 'string_with_specials': 'Test!@#$%^&*()-_=+[]{};:,<.>/?\\\'\"`~'}  # noqa: E501
TEST_ENV_TYPED_VARS_PARSED = {'key': 'value', 'int': 123, 'float': 1.23, 'complex': 1+2j, 'list': ['list1', 'list2', {'dict_in_list': 'value'}], 'dict': {'nested_dict': 'nested_value'}, 'tuple': (123, 'string'), 'bool': True, 'boolstring': False, 'string_with_specials': 'Test!@#$%^&*()-_=+[]{};:,<.>/?\\\'\"`~'}  # noqa: E501
TEST_ENV_DOCKER_SECRETS = {'MY_EXAMPLE_SECRET_FILE': '/run/secrets/my_example_secret'}
TEST_ENV_DOCKER_SECRETS_INVALID_POSTFIX = {'MY_EXAMPLE_SECRET': '/run/secrets/my_example_secret'}
TEST_DOCKER_SECRET_CONTENT = 'mysecret'
TEST_DOCKER_SECRETS_RESULT = {'MY_EXAMPLE_SECRET': TEST_DOCKER_SECRET_CONTENT}

TEST_SEPARATOR = '__'
TEST_MATCH = r'^matched'
TEST_WHITELIST = ['whitelisted_var', 'whitelist2']
TEST_PARSE_VALUES = True
TEST_TO_LOWER = True
TEST_CONVERT_UNDERSCORES = True
TEST_DOCKER_SECRETS = list(TEST_ENV_DOCKER_SECRETS.keys())
TEST_DOCKER_SECRETS_INVALID_POSTFIX = ['MY_EXAMPLE_SECRET']
TEST_DOCKER_SECRETS_PATH = str(list(TEST_DOCKER_SECRETS_RESULT.values())[0])

if (version_info.major < 3):
    import __builtin__
    MOCK_OPEN_FUNCTION = '__builtin__.open'
else:
    import builtins
    MOCK_OPEN_FUNCTION = 'builtins.open'


def throw_ioerror(*args, **kwargs):
    raise IOError('test')


class TestEnv(TestCase):
    def test_default_params(self):
        env_store = Env()

        self.assertEqual(env_store.separator, None)
        self.assertEqual(env_store.match, None)
        self.assertEqual(env_store.whitelist, None)
        self.assertEqual(env_store.parse_values, False)
        self.assertEqual(env_store.to_lower, False)
        self.assertEqual(env_store.convert_underscores, False)

    def test_optional_params(self):
        env_store = Env(
                separator=TEST_SEPARATOR,
                match=TEST_MATCH,
                whitelist=TEST_WHITELIST,
                parse_values=TEST_PARSE_VALUES,
                to_lower=TEST_TO_LOWER,
                convert_underscores=TEST_CONVERT_UNDERSCORES
                )

        self.assertEqual(env_store.separator, TEST_SEPARATOR)
        self.assertEqual(env_store.match, TEST_MATCH)
        self.assertEqual(env_store.whitelist, TEST_WHITELIST)
        self.assertEqual(env_store.parse_values, TEST_PARSE_VALUES)
        self.assertEqual(env_store.to_lower, TEST_TO_LOWER)
        self.assertEqual(env_store.convert_underscores, TEST_CONVERT_UNDERSCORES)

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
        env_store = Env(parse_values=TEST_PARSE_VALUES)
        result = env_store.get()
        self.assertEqual(result, TEST_ENV_TYPED_VARS_PARSED)
        self.assertIsInstance(result, dict)

    @patch('pconf.store.env.os', new=MagicMock())
    def test_lowercase_conversion(self):
        pconf.store.env.os.environ = TEST_ENV_UPPERCASE
        env_store = Env(to_lower=TEST_TO_LOWER)
        result = env_store.get()
        self.assertEqual(result, TEST_ENV_VARS)
        self.assertIsInstance(result, dict)

    @patch('pconf.store.env.os', new=MagicMock())
    def test_lowercase_and_separator(self):
        pconf.store.env.os.environ = TEST_ENV_UPPERCASE
        env_store = Env(separator=TEST_SEPARATOR, to_lower=TEST_TO_LOWER)
        result = env_store.get()
        self.assertEqual(result, TEST_SEPARATED_VARS)
        self.assertIsInstance(result, dict)

    @patch('pconf.store.env.os', new=MagicMock())
    def test_convert_underscore_replacement(self):
        pconf.store.env.os.environ = TEST_ENV_VARS
        env_store = Env(convert_underscores=TEST_CONVERT_UNDERSCORES)
        result = env_store.get()
        self.assertEqual(result, TEST_ENV_CONVERTED)
        self.assertIsInstance(result, dict)

    @patch('pconf.store.env.os', new=MagicMock())
    def test_convert_underscore_and_separator(self):
        pconf.store.env.os.environ = TEST_ENV_VARS
        env_store = Env(separator=TEST_SEPARATOR, convert_underscores=TEST_CONVERT_UNDERSCORES)
        result = env_store.get()
        self.assertEqual(result, TEST_ENV_CONVERTED_SEPARATED)
        self.assertIsInstance(result, dict)

    @patch('pconf.store.env.os', new=MagicMock())
    def test_parse_and_split_order(self):
        pconf.store.env.os.environ = TEST_ENV_VARS
        try:
            env_store = Env(separator=TEST_SEPARATOR, parse_values=TEST_PARSE_VALUES)
        except AttributeError:
            self.fail("Parsing environment variables raised AttributeError")
        result = env_store.get()

        self.assertEqual(result, TEST_SEPARATED_VARS)
        self.assertIsInstance(result, dict)

    @patch('pconf.store.env.os', new=MagicMock())
    @patch(MOCK_OPEN_FUNCTION, mock_open(read_data=TEST_DOCKER_SECRETS_PATH))
    def test_docker_secrets(self):
        pconf.store.env.os.environ = TEST_ENV_DOCKER_SECRETS

        env_store = Env(docker_secrets=TEST_DOCKER_SECRETS)
        result = env_store.get()

        self.assertEqual(list(result.keys()), list(TEST_DOCKER_SECRETS_RESULT.keys()))
        self.assertEqual(result, TEST_DOCKER_SECRETS_RESULT)
        self.assertIsInstance(result, dict)

    @patch('pconf.store.env.os', new=MagicMock())
    def test_docker_secrets_invalid_postfix(self):
        pconf.store.env.os.environ = TEST_ENV_DOCKER_SECRETS_INVALID_POSTFIX

        env_store = Env(docker_secrets=TEST_DOCKER_SECRETS_INVALID_POSTFIX)
        result = env_store.get()

        self.assertEqual(result, {})
        self.assertIsInstance(result, dict)

    @patch('pconf.store.env.os', new=MagicMock())
    @patch(MOCK_OPEN_FUNCTION, side_effect=throw_ioerror)
    def test_docker_secrets_nonexistent_file(self, mock_open):
        simplefilter('ignore')
        pconf.store.env.os.environ = TEST_ENV_DOCKER_SECRETS

        env_store = Env(docker_secrets=TEST_DOCKER_SECRETS)
        result = env_store.get()

        self.assertEqual(result, {})
        self.assertIsInstance(result, dict)
