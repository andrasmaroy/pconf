from unittest import TestCase
from mock import patch, MagicMock
import pconf
from pconf.store.env import Env


TEST_ENV_VARS = {'env': 'result'}
TEST_SEPARATOR = '__'
TEST_MATCH = 'match'
TEST_WHITELIST = ['whitelist1', 'whitelist2']


@patch('pconf.store.env.os', new=MagicMock())
class TestEnv(TestCase):
    def test_default_params(self):
        env_store = Env()

        self.assertEqual(env_store.separator, ':')
        self.assertEqual(env_store.match, None)
        self.assertEqual(env_store.whitelist, None)

    def test_optional_params(self):
        env_store = Env(separator=TEST_SEPARATOR, match=TEST_MATCH, whitelist=TEST_WHITELIST)

        self.assertEqual(env_store.separator, TEST_SEPARATOR)
        self.assertEqual(env_store.match, TEST_MATCH)
        self.assertEqual(env_store.whitelist, TEST_WHITELIST)

    def test_get_all_vars(self):
        pconf.store.env.os.environ = TEST_ENV_VARS

        env_store = Env()
        result = env_store.get()

        self.assertEqual(result, TEST_ENV_VARS)
        self.assertIsInstance(result, dict)
