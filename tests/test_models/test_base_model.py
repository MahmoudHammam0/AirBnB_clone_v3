#!/usr/bin/python3
""" Unittest for the BaseModel class in the base_model module """
import unittest
from models.base_model import BaseModel
from datetime import datetime


class TestBaseModel(unittest.TestCase):
    """ Tests the BaseModel class """

    def test_init_id(self):
        """ Tests with a custom id """
        model = BaseModel(id=5)
        self.assertEqual(model.id, 5)

    def test_init_id_negative(self):
        """ Tests with a custom negative id """
        model = BaseModel(id=-4)
        self.assertEqual(model.id, -4)

    def test_init_id_float(self):
        """ Tests with a custom float id """
        model = BaseModel(id=654.3)
        self.assertEqual(model.id, 654.3)

    def test_init_name(self):
        """ Tests with a custom instance attribute """
        model = BaseModel(name="first_model")
        self.assertEqual(model.name, "first_model")

    def test_init_created_at(self):
        """ Tests __init__ with a custom updated_at values """
        date = datetime(2024, 1, 13, 11, 58)
        date_str = str(date)
        model = BaseModel(created_at=date_str)
        self.assertEqual(model.created_at, date)

    def test_init_updated_at(self):
        """ Tests __init__ with a custom updated_at values """
        date = datetime(2024, 1, 13, 11, 58)
        date_str = str(date)
        model = BaseModel(updated_at=date_str)
        self.assertEqual(model.updated_at, date)

    def test_init_without_arguments(self):
        """ Tests __init__ without any arguments """
        my_model = BaseModel()

        # Checks if the id is generated
        self.assertTrue(hasattr(my_model, 'id'))
        self.assertIsInstance(my_model.id, str)
        self.assertNotEqual(my_model.id, "")

        # Checks if created_at and updated_at are generated
        self.assertTrue(hasattr(my_model, 'created_at'))
        self.assertTrue(isinstance(my_model.created_at, datetime))

        self.assertTrue(hasattr(my_model, 'updated_at'))
        self.assertTrue(isinstance(my_model.updated_at, datetime))

    def test_str(self):
        """ Tests the string representation of the model with
            custom instances attributes """
        model = BaseModel(id=2, name="model1")
        s = "[BaseModel] (2) {'id': 2, 'name': 'model1'}"
        self.assertEqual(str(model), s)

    def test_str2(self):
        """ Tests the string representation of the model """
        model = BaseModel()
        s = "[BaseModel] ({}) {}".format(model.id, model.__dict__)
        self.assertEqual(str(model), s)

    def test_to_dict(self):
        """ Tests the dictionary representation of the model """
        model = BaseModel()
        expected_dict = model.__dict__.copy()
        expected_dict['created_at'] = expected_dict['created_at'].isoformat()
        expected_dict['updated_at'] = expected_dict['updated_at'].isoformat()
        expected_dict['__class__'] = model.__class__.__name__
        self.assertEqual(model.to_dict(), expected_dict)

    def test_to_dict2(self):
        """ Tests the dictionary representation of the model
            with custom attributes """
        date = datetime(2024, 1, 10, 17, 48)
        date_str = str(date)
        model = BaseModel(number=15, name="test_model",
                          created_at=date_str, updated_at=date_str)
        expected_dict = model.__dict__.copy()
        expected_dict['created_at'] = expected_dict['created_at'].isoformat()
        expected_dict['updated_at'] = expected_dict['updated_at'].isoformat()
        expected_dict['__class__'] = model.__class__.__name__
        self.assertEqual(model.to_dict(), expected_dict)

    def test_save(self):
        """ Tests if save method correctly updates updated_at """
        import time
        my_model = BaseModel()
        initial_updated_at = my_model.updated_at
        time.sleep(1)
        my_model.save()
        self.assertNotEqual(initial_updated_at, my_model.updated_at)
        self.assertTrue(initial_updated_at < my_model.updated_at)
