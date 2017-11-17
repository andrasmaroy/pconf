from pconf import Pconf
from unittest import TestCase


class IntegrationBase(TestCase):
    result = {}

    def setUp(self):
        Pconf._Pconf__hierarchy = []
        IntegrationBase.result = {
                'tuple': (123, 'string'),
                'int': 123,
                'float': 1.23,
                'list': ['list1', 'list2', {'dict_in_list': 'value'}],
                'complex': (1+2j),
                'bool': True,
                'key': 'value',
                'boolstring': 'false',
                'string_with_specials': 'Test!@#$%^&*()-_=+[]{};:,<.>/?\\\'"\\`~',
                'dict': {'dict': 'value', 'list_in_dict': ['nested_list1', 'nested_list2']}
                }
