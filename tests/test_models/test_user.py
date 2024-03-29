#!/usr/bin/python3
'''Test module for User class'''
import unittest
from models.user import User
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage


class TestUser(unittest.TestCase):
    '''unittest of the User class'''
    def test_attr(self):
        '''test attributes of User class'''
        ins = User()
        self.assertTrue(hasattr(ins, "email"))
        self.assertEqual(type(ins.email), str)
        self.assertTrue(hasattr(ins, "password"))
        self.assertEqual(type(ins.password), str)
        self.assertTrue(hasattr(ins, "first_name"))
        self.assertEqual(type(ins.first_name), str)
        self.assertTrue(hasattr(ins, "last_name"))
        self.assertEqual(type(ins.last_name), str)

    def test_User_instance(self):
        '''test User class with an instance'''
        ins = User()
        self.assertIsInstance(ins, User)
        self.assertTrue(issubclass(type(ins), BaseModel))
