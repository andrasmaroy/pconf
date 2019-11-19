from .integration_base import IntegrationBase
from pconf import Pconf


class TestIntegrationArgv(IntegrationBase):
    def test_integration_json(self):
        self.maxDiff = None
        # Remove values that are not json encodeable
        IntegrationBase.result.pop("complex")
        IntegrationBase.result.pop("tuple")
        IntegrationBase.result.pop("secret")
        Pconf.file("./tests/integration/example.json", encoding="json")
        config = Pconf.get()
        self.assertEqual(config, IntegrationBase.result)

    def test_integration_yaml(self):
        self.maxDiff = None
        IntegrationBase.result.pop("complex")
        IntegrationBase.result.pop("tuple")
        IntegrationBase.result.pop("secret")
        Pconf.file("./tests/integration/example.yaml", encoding="yaml")
        config = Pconf.get()
        self.assertEqual(config, IntegrationBase.result)
