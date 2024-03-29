#!/usr/bin/python3
'''Test module for DBStorage class'''
import os
import unittest
from models.base_model import BaseModel
from models.engine.db_storage import DBStorage
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class TestDBStorage(unittest.TestCase):
    '''Test class for DBStorage'''

    def setUp(self):
        '''class initializations'''
        self.storage = DBStorage()

    @unittest.skipIf(models.storage != 'db', "skip if not database storage")
    def test_get_none(self):
        """ Test get method without input """
        obj = self.storage.get()
        self.assertIsNone(obj)

    @unittest.skipIf(models.storage != 'db', "skip if not database storage")
    def test_get(self):
        """ Test get method with a class & id """
        user = User()
        self.storage.new(user)
        self.storage.save()
        self.storage.reload()
        retrieved_user = self.storage.get(User, user.id)
        self.assertEqual(retrieved_user, user)

    @unittest.skipIf(models.storage != 'db', "skip if not database storage")
    def test_get_nonexistent_obj(self):
        """ Test get method with id that doesn't exist """
        state = self.storage.get(State, -15)
        self.assertIsNone(state)

    @unittest.skipIf(models.storage != 'db', "skip if not database storage")
    def test_get_with_wrong_class(self):
        """ Test get method with wrong class """
        user = User()
        self.storage.new(user)
        self.storage.save()
        self.storage.reload()
        retrieved_user = self.storage.get(City, user.id)
        self.assertIsNone(retrieved_user)

    @unittest.skipIf(models.storage != 'db', "skip if not database storage")
    def test_count_all_classes(self):
        """ Test count method without a specified class """
        number_of_objs = len(self.storage.all())
        count = self.storage.count()
        self.assertEqual(count, number_of_objs)

    @unittest.skipIf(models.storage != 'db', "skip if not database storage")
    def test_count_class(self):
        """ Test count method with a class """
        number_of_objs = len(self.storage.all(User))
        count = self.storage.count(User)
        self.assertEqual(count, number_of_objs)

    @unittest.skipIf(models.storage != 'db', "skip if not database storage")
    def test_count_after_creating_obj(self):
        """ Test count method after creating an object """
        number_of_objs = len(self.storage.all(User))
        user = User()
        self.storage.new(user)
        self.storage.save()
        self.storage.reload()
        count = self.storage.count(User)
        self.assertEqual(count, number_of_objs + 1)

    @unittest.skipIf(models.storage != 'db', "skip if not database storage")
    def test_count_with_wrong_class(self):
        """ Test count method with nonexistent class """
        count = self.storage.count("hi")
        self.assertEqual(count, 0)
