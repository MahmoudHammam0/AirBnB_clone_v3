#!/usr/bin/python3
'''Test module for Review class'''
import unittest
from models.review import Review
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage


class TestUser(unittest.TestCase):
    '''unittest of the Review class'''
    def test_attr(self):
        '''test attributes of Review class'''
        ins = Review()
        self.assertTrue(hasattr(ins, "place_id"))
        self.assertEqual(type(ins.place_id), str)
        self.assertTrue(hasattr(ins, "user_id"))
        self.assertEqual(type(ins.user_id), str)
        self.assertTrue(hasattr(ins, "text"))
        self.assertEqual(type(ins.text), str)

    def test_Review_instance(self):
        '''test Review class with an instance'''
        ins = Review()
        self.assertIsInstance(ins, Review)
        self.assertTrue(issubclass(type(ins), BaseModel))
