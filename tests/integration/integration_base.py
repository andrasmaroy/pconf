from pconf import Pconf
from unittest import TestCase


class IntegrationBase(TestCase):
    result = {}

    def setUp(self):
        Pconf.clear()
        IntegrationBase.result = {
                'tuple': (123, 'string'),
                'int': 123,
                'float': 1.23,
                'list': ['list1', 'list2', {'dict-in-list': 'value'}],
                'complex': (1+2j),
                'bool': True,
                'key': 'value',
                'boolstring': 'false',
                'string-with-specials': 'Test!@#$%^&*()-_=+[]{};:,<.>/?\\\'"\\`~',
                'dict': {'dict': 'value', 'list-in-dict': ['nested-list1', 'nested-list2']}
                }
