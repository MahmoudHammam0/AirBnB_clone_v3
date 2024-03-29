#!/usr/bin/python3
'''Test module for Place class'''
import unittest
from models.place import Place
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage


class TestUser(unittest.TestCase):
    '''unittest of the Place class'''
    def test_attr(self):
        '''test attributes of Place class'''
        ins = Place()
        self.assertTrue(hasattr(ins, "city_id"))
        self.assertEqual(type(ins.city_id), str)
        self.assertTrue(hasattr(ins, "user_id"))
        self.assertEqual(type(ins.user_id), str)
        self.assertTrue(hasattr(ins, "name"))
        self.assertEqual(type(ins.name), str)
        self.assertTrue(hasattr(ins, "description"))
        self.assertEqual(type(ins.description), str)
        self.assertTrue(hasattr(ins, "number_rooms"))
        self.assertEqual(type(ins.number_rooms), int)
        self.assertTrue(hasattr(ins, "number_bathrooms"))
        self.assertEqual(type(ins.number_bathrooms), int)
        self.assertTrue(hasattr(ins, "max_guest"))
        self.assertEqual(type(ins.max_guest), int)
        self.assertTrue(hasattr(ins, "price_by_night"))
        self.assertEqual(type(ins.price_by_night), int)
        self.assertTrue(hasattr(ins, "latitude"))
        self.assertEqual(type(ins.latitude), float)
        self.assertTrue(hasattr(ins, "longitude"))
        self.assertEqual(type(ins.longitude), float)
        self.assertTrue(hasattr(ins, "amenity_ids"))
        self.assertEqual(type(ins.amenity_ids), list)

    def test_Place_instance(self):
        '''test Place class with an instance'''
        ins = Place()
        self.assertIsInstance(ins, Place)
        self.assertTrue(issubclass(type(ins), BaseModel))
