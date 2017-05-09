from unittest import TestCase
from mock import patch, MagicMock
import pconf
from pconf.store.env import Env


TEST_ENV_VARS = {'env': 'result'}


@patch('pconf.store.env.os', new=MagicMock())
class TestEnv(TestCase):
    def test_get_all_vars(self):
        pconf.store.env.os.environ = TEST_ENV_VARS

        env_store = Env()
        result = env_store.get()

        self.assertEqual(result, TEST_ENV_VARS)
        self.assertIsInstance(result, dict)
