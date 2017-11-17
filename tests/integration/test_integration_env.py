import os
from .integration_base import IntegrationBase
from pconf import Pconf


class TestIntegrationArgv(IntegrationBase):
    def test_integration(self):
        os.environ["BOOL"] = "true"
        os.environ["BOOLSTRING"] = "\"false\""
        os.environ["DICT"] = "{ \"dict\": \"value\", \"list-in-dict\": [ \"nested-list1\", \"nested-list2\" ] }"
        os.environ["FLOAT"] = "1.23"
        os.environ["INT"] = "123"
        os.environ["KEY"] = "value"
        os.environ["LIST"] = "[ \"list1\", \"list2\", { \"dict-in-list\": \"value\" } ]"
        os.environ["STRING_WITH_SPECIALS"] = "Test!@#$%^&*()-_=+[]{};:,<.>/?\\\'\"\`~"
        os.environ["TUPLE"] = "(123, \"string\")"
        os.environ["COMPLEX"] = "1+2j"

        Pconf.env(
                whitelist=[
                    'KEY',
                    'INT',
                    'FLOAT',
                    'COMPLEX',
                    'LIST',
                    'DICT',
                    'TUPLE',
                    'BOOL',
                    'BOOLSTRING',
                    'STRING_WITH_SPECIALS'
                    ],
                parse_values=True,
                to_lower=True,
                convert_underscores=True
                )
        config = Pconf.get()
        self.assertEqual(config, IntegrationBase.result)
