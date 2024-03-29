#!/usr/bin/python3
""" Unittest for the Amenity class: amenity.py module """
import unittest
from models.amenity import Amenity


class TestAmenity(unittest.TestCase):
    """ Tests the Amenity class

        Inherits from BaseModel, so tests focus only on
        specific attributes/methods introduced in this class

        The attributes/methods inherited from BaseModel are
        covered by the tests for BaseModel in test_base_model.py
    """

    def test_name(self):
        """ Tests the 'name' attribute """
        am = Amenity()
        self.assertTrue(hasattr(am, 'name'))
        self.assertEqual(am.name, "")

    def test_name_custom(self):
        """ Tests 'name' attribute with a custom value """
        am = Amenity(name="amenity01")
        self.assertEqual(am.name, "amenity01")

    def test_name_empty_string(self):
        """ Tests 'name' attribute with and empty string """
        amenity = Amenity(name="")
        self.assertEqual(amenity.name, "")

    def test_name_type(self):
        """ Tests the type of 'name' attribute """
        am = Amenity()
        self.assertIsInstance(am.name, str)

    def test_name_modify(self):
        """ Tests modifying the 'name' attribute """
        am = Amenity(name="first name")
        am.name = "modified name"
        self.assertEqual(am.name, "modified name")
