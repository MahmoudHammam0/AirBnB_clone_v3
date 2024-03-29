#!/usr/bin/python3
'''Test module for City class'''
import unittest
from models.city import City
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage


class TestUser(unittest.TestCase):
    '''unittest of the City class'''
    def test_attr(self):
        '''test attributes of City class'''
        ins = City()
        self.assertTrue(hasattr(ins, "state_id"))
        self.assertEqual(type(ins.state_id), str)
        self.assertTrue(hasattr(ins, "name"))
        self.assertEqual(type(ins.name), str)

    def test_City_instance(self):
        '''test City class with an instance'''
        ins = City()
        self.assertIsInstance(ins, City)
        self.assertTrue(issubclass(type(ins), BaseModel))
