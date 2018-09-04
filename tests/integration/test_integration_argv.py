import sys
from .integration_base import IntegrationBase
from pconf import Pconf


class TestIntegrationArgv(IntegrationBase):
    def test_integration(self):
        sys.argv.append("pconf")
        sys.argv.append("--bool")
        sys.argv.append("--boolstring")
        sys.argv.append("false")
        sys.argv.append("--dict")
        sys.argv.append("{ \"dict\": \"value\", \"list-in-dict\": [ \"nested-list1\", \"nested-list2\" ] }")
        sys.argv.append("--float")
        sys.argv.append("1.23")
        sys.argv.append("--int")
        sys.argv.append("123")
        sys.argv.append("--key")
        sys.argv.append("value")
        sys.argv.append("--list")
        sys.argv.append("[ \"list1\", \"list2\", { \"dict-in-list\": \"value\" } ]")
        sys.argv.append("--string-with-specials")
        sys.argv.append("Test!@#$%^&*()-_=+[]{};:,<.>/?\\\'\"\`~")
        sys.argv.append("--tuple")
        sys.argv.append("(123, \"string\")")
        sys.argv.append("--complex")
        sys.argv.append("1+2j")

        Pconf.argv(name="--bool", type=bool)
        Pconf.argv(name="--boolstring")
        Pconf.argv(name="--complex", type=complex)
        Pconf.argv(name="--dict", type=dict)
        Pconf.argv(name="--float", type=float)
        Pconf.argv(name="--int", type=int)
        Pconf.argv(name="--key", type=str)
        Pconf.argv(name="--list", type=list)
        Pconf.argv(name="--string-with-specials")
        Pconf.argv(name="--tuple", type=tuple)

        config = Pconf.get()
        self.assertEqual(config, IntegrationBase.result)
