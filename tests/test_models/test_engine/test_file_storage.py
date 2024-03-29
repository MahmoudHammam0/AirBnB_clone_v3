#!/usr/bin/python3
'''Test module for FileStorage class'''
import json
import os
import unittest
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class TestFileStorage(unittest.TestCase):
    '''Test class for FileStorage'''
    def setUp(self):
        '''class initializations'''
        self.storage = FileStorage()
        self.new_ins = BaseModel()

    def tearDown(self):
        '''clean up'''
        FileStorage._FileStorage__objects = {}
        if os.path.isfile(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test_class_name(self):
        '''test class name'''
        self.assertEqual(self.storage.__class__.__name__, "FileStorage")

    def test_all(self):
        '''Test all method of FileStorage'''
        the_dict = self.storage.all()
        self.assertIsInstance(the_dict, dict)

    def test_new(self):
        '''test new method of FileStorage'''
        user = User()
        city = City()
        amen = Amenity()
        rev = Review()
        pl = Place()
        state = State()
        self.storage.new(self.new_ins)
        self.storage.new(user)
        self.storage.new(city)
        self.storage.new(amen)
        self.storage.new(rev)
        self.storage.new(pl)
        self.storage.new(state)
        self.assertNotEqual(self.storage.all(), {})
        key = self.new_ins.__class__.__name__ + "." + self.new_ins.id
        self.assertTrue(key in self.storage.all())
        self.assertTrue(self.new_ins in self.storage.all().values())
        self.assertTrue("User" + "." + user.id in self.storage.all())
        self.assertTrue(user in self.storage.all().values())
        self.assertTrue("City" + "." + city.id in self.storage.all())
        self.assertTrue(city in self.storage.all().values())
        self.assertTrue("Amenity" + "." + amen.id in self.storage.all())
        self.assertTrue(amen in self.storage.all().values())
        self.assertTrue("Review" + "." + rev.id in self.storage.all())
        self.assertTrue(rev in self.storage.all().values())
        self.assertTrue("Place" + "." + pl.id in self.storage.all())
        self.assertTrue(pl in self.storage.all().values())
        self.assertTrue("State" + "." + state.id in self.storage.all())
        self.assertTrue(state in self.storage.all().values())

    def test_save(self):
        '''test save method of FileStorage'''
        self.storage.save()
        with open(FileStorage._FileStorage__file_path, 'r') as f:
            content = f.read()
        self.assertTrue(type(content) is str)
        content = json.loads(content)
        self.assertTrue(type(content) is dict)
        self.assertTrue(os.path.isfile(FileStorage._FileStorage__file_path))

    def test_save_with_all_classes(self):
        '''test save method with different classes'''
        user = User()
        city = City()
        amen = Amenity()
        rev = Review()
        pl = Place()
        state = State()
        self.storage.new(self.new_ins)
        self.storage.new(user)
        self.storage.new(city)
        self.storage.new(amen)
        self.storage.new(rev)
        self.storage.new(pl)
        self.storage.new(state)
        self.storage.save()
        with open(FileStorage._FileStorage__file_path, 'r') as f:
            content = f.read()
        self.assertTrue("BaseModel" + "." + self.new_ins.id in content)
        self.assertTrue("User" + "." + user.id in content)
        self.assertTrue("City" + "." + city.id in content)
        self.assertTrue("Amenity" + "." + amen.id in content)
        self.assertTrue("Review" + "." + rev.id in content)
        self.assertTrue("Place" + "." + pl.id in content)
        self.assertTrue("State" + "." + state.id in content)

    def test_all_dict_value_types(self):
        '''test type of values of dictionary returned by all method'''
        self.storage.new(self.new_ins)
        key = self.new_ins.__class__.__name__ + "." + self.new_ins.id
        value = self.storage.all()[key]
        self.assertIsInstance(self.new_ins, type(value))

    def type_of_FileStorage(self):
        '''test the type of FileStorage class'''
        self.assertEqual(type(self.Storage), FileStorage)

    def test_reload(self):
        '''test reload method of FileStorage class'''
        user = User()
        city = City()
        amen = Amenity()
        rev = Review()
        pl = Place()
        state = State()
        self.storage.new(self.new_ins)
        self.storage.new(user)
        self.storage.new(city)
        self.storage.new(amen)
        self.storage.new(rev)
        self.storage.new(pl)
        self.storage.new(state)
        self.storage.save()
        self.storage.reload()
        obj_dict = self.storage.all()
        self.assertTrue("BaseModel" + "." + self.new_ins.id in obj_dict)
        self.assertTrue("User" + "." + user.id in obj_dict)
        self.assertTrue("City" + "." + city.id in obj_dict)
        self.assertTrue("Amenity" + "." + amen.id in obj_dict)
        self.assertTrue("Review" + "." + rev.id in obj_dict)
        self.assertTrue("Place" + "." + pl.id in obj_dict)
        self.assertTrue("State" + "." + state.id in obj_dict)

    def test_save_str_arg(self):
        '''test save method with string argument'''
        with self.assertRaises(TypeError):
            self.storage.save("string")

    def test_FileStorage_str_arg(self):
        '''test FileStorage class init with string'''
        with self.assertRaises(TypeError):
            FileStorage("Hello")

    def test_all_str_arg(self):
        '''test all method with string argument'''
        with self.assertRaises(TypeError):
            self.storage.all("007")

    def test_attr(self):
        '''test attributes of FileStorage'''

        self.assertTrue(hasattr(FileStorage, "_FileStorage__file_path"))
        self.assertTrue(hasattr(FileStorage, "_FileStorage__objects"))
        self.assertTrue(hasattr(FileStorage, "classes"))

    def test_new_with_no_arg(self):
        '''test new method without argument'''
        with self.assertRaises(TypeError):
            self.storage.new()

    def test_new_with_more_arg(self):
        '''test new method with more than 1 argument'''
        with self.assertRaises(TypeError):
            self.storage.new(BaseModel(), User(), City())

    def test_reload_str_arg(self):
        '''test reload method with string argument'''
        with self.assertRaises(TypeError):
            self.storage.reload("RELOAD")

    def test_get_none(self):
        '''test get method without input'''
        obj = self.storage.get()
        self.assertIsNone(obj)

    def test_get(self):
        '''tests get method with a class & id'''
        user = User()
        self.storage.new(user)
        self.storage.save()
        self.storage.reload()
        retrieved_user = self.storage.get(User, user.id)
        self.assertEqual(retrieved_user, user)

    def test_get_nonexistent_obj(self):
        '''tests get method with id that doesn't exist'''
        state = self.storage.get(State, -15.2)
        self.assertIsNone(state)

    def test_get_with_wrong_class(self):
        '''test get method with wrong class'''
        User
        retrieved_user = self.storage.get(City, user.id)
        self.assertIsNone(retrieved_user)

    def test_count_all_classes(self):
        '''tests count method without a specified class'''
        number_of_objs = len(self.storage.all())
        count = self.storage.count()
        self.assertEqual(count, number_of_objs)

    def test_count_class(self):
        '''test count method with a class'''
        number_of_objs = len(self.storage.all(User))
        count = self.storage.count(User)
        self.assertEqual(count, number_of_objs)

    def test_count_after_creating_obj(self):
        '''tests count method after creating an object'''
        number_of_objs = len(self.storage.all(User))
        user = User()
        self.storage.new(user)
        self.storage.save()
        self.storage.reload()
        count = self.storage.count(User)
        self.assertEqual(count, number_of_objs + 1)

    def test_count_with_wrong_class(self):
        '''tests count method with nonexistent class'''
        count = self.storage.count("hi")
        self.assertEqual(count, 0)
