from unittest import TestCase
from pconf.store.memory import Memory

TEST_DATA = {"test": "memory"}


class TestMemory(TestCase):
    def test_data_stored(self):
        test_memory = Memory(TEST_DATA)
        self.assertEqual(test_memory.get(), TEST_DATA)

    def test_type_check(self):
        with self.assertRaises(TypeError):
            Memory("string")
