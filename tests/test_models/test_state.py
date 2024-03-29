#!/usr/bin/python3
'''Test module for State class'''
import unittest
from models.state import State
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage


class TestState(unittest.TestCase):
    '''unittest of the State class'''
    def test_attr(self):
        '''test attributes of State class'''
        ins = State()
        self.assertTrue(hasattr(ins, "name"))
        self.assertEqual(type(ins.name), str)

    def test_State_instance(self):
        '''test State class with an instance'''
        ins = State()
        self.assertIsInstance(ins, State)
        self.assertTrue(issubclass(type(ins), BaseModel))
