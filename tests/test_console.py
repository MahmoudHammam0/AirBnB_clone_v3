#!/usr/bin/python3
'''Test module for console'''
import unittest
from console import HBNBCommand
import sys
from io import StringIO
from unittest.mock import patch
import os
from models.engine.file_storage import FileStorage


class TestConsole(unittest.TestCase):
    '''Test class for console module'''
    classes = ['BaseModel', 'User', 'Place', 'State',
               'City', 'Amenity', 'Review']

    def setUp(self):
        '''setup each test'''
        if os.path.isfile("file.json"):
            os.remove("file.json")
        FileStorage._FileStorage__objects = {}

    def test_quit_cmd(self):
        '''test quit command of console'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("quit")
        res = f.getvalue()
        self.assertEqual("", res)
        self.assertTrue(len(res) == 0)

    def test_EOF(self):
        '''test EOF for console'''
        self.assertTrue(HBNBCommand().onecmd("EOF"))

    def test_help(self):
        '''test help for console'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help")
        help_str = '''
Documented commands (type help <topic>):
========================================
EOF  all  count  create  destroy  help  quit  show  update

'''
        self.assertEqual(help_str, f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help quit")
        help_quit = 'Quit command to exit the program\n'
        self.assertEqual(help_quit, f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help EOF")
        help_quit = 'EOF exit to the program\n'
        self.assertEqual(help_quit, f.getvalue())

    def test_emptyline(self):
        '''test empty input line for console'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("\n")
        res = f.getvalue()
        self.assertEqual("", res)

    def test_create(self):
        '''test create command'''
        for class_name in self.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd("create {}".format(class_name))
            class_id = f.getvalue()[:-1]
            self.assertTrue(len(class_id) > 0)
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd("all {}".format(class_name))
            self.assertTrue(class_id in f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create")
        error = f.getvalue()[:-1]
        self.assertEqual(error, "** class name missing **")
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create NotClass")
        error = f.getvalue()[:-1]
        self.assertEqual(error, "** class doesn't exist **")

    def test_show(self):
        '''test show command'''
        for class_name in self.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd("create {}".format(class_name))
            class_id = f.getvalue()[:-1]
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd("show {} {}".format(class_name, class_id))
            res = f.getvalue()[:-1]
            self.assertTrue(class_id in res)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show")
        error = f.getvalue()[:-1]
        self.assertEqual(error, "** class name missing **")
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show NotClass")
        error = f.getvalue()[:-1]
        self.assertEqual(error, "** class doesn't exist **")
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show BaseModel")
        error = f.getvalue()[:-1]
        self.assertEqual(error, "** instance id missing **")
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show BaseModel 564sdg654fg6f4g6")
        error = f.getvalue()[:-1]
        self.assertEqual(error, "** no instance found **")

    def test_class_show_id(self):
        '''test show advanced show command'''
        for class_name in self.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd("create {}".format(class_name))
            class_id = f.getvalue()[:-1]
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd('{}.show("{}")'.format(class_name,
                                                            class_id))
            res = f.getvalue()
            self.assertTrue(class_id in res)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(".show()")
        error = f.getvalue()[:-1]
        self.assertEqual(error, "** class name missing **")
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("NotClass.show()")
        error = f.getvalue()[:-1]
        self.assertEqual(error, "** class doesn't exist **")
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("BaseModel.show()")
        error = f.getvalue()[:-1]
        self.assertEqual(error, "** instance id missing **")
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('BaseModel.show(s5d4g6fg466g4f65g"")')
        error = f.getvalue()[:-1]
        self.assertEqual(error, "** no instance found **")

    def test_destroy(self):
        '''test destroy command'''
        for class_name in self.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd("create {}".format(class_name))
            class_id = f.getvalue()[:-1]
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd("destroy {} {}".format(class_name,
                                                            class_id))
            res = f.getvalue()[:-1]
            self.assertTrue(len(res) == 0)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all")
        self.assertFalse(class_id in f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy")
        error = f.getvalue()[:-1]
        self.assertEqual(error, "** class name missing **")
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy NotClass")
        error = f.getvalue()[:-1]
        self.assertEqual(error, "** class doesn't exist **")
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy BaseModel")
        error = f.getvalue()[:-1]
        self.assertEqual(error, "** instance id missing **")
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy BaseModel 564sdg654fg6f4g6")
        error = f.getvalue()[:-1]
        self.assertEqual(error, "** no instance found **")

    def test_class_destroy_id(self):
        '''test advanced destroy command'''
        for class_name in self.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd("create {}".format(class_name))
            class_id = f.getvalue()[:-1]
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd('{}.destroy("{}")'.format(class_name,
                                                               class_id))
            res = f.getvalue()
            self.assertTrue(len(res) == 0)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all")
        self.assertFalse(class_id in f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(".destroy()")
        error = f.getvalue()[:-1]
        self.assertEqual(error, "** class name missing **")
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("NotClass.destroy()")
        error = f.getvalue()[:-1]
        self.assertEqual(error, "** class doesn't exist **")
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("BaseModel.destroy()")
        error = f.getvalue()[:-1]
        self.assertEqual(error, "** instance id missing **")
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('BaseModel.destroy(s5d4g6fg466g4f65g"")')
        error = f.getvalue()[:-1]
        self.assertEqual(error, "** no instance found **")

    def test_all(self):
        '''test all command'''
        for class_name in self.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd("create {}".format(class_name))
            class_id = f.getvalue()[:-1]
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd("all")
            res = f.getvalue()[:-1]
            self.assertTrue(len(res) > 0)
            self.assertIn(class_id, res)
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd("all {}".format(class_name))
            self.assertTrue(class_id in f.getvalue()[:-1])
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all NotClass")
        error = f.getvalue()[:-1]
        self.assertEqual(error, "** class doesn't exist **")

    def test_class_all(self):
        '''test advanced all command'''
        for class_name in self.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd("create {}".format(class_name))
            class_id = f.getvalue()[:-1]
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd("{}.all()".format(class_name))
            res = f.getvalue()[:-1]
            self.assertTrue(len(res) > 0)
            self.assertIn(class_id, res)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("NotClass.all()")
        error = f.getvalue()[:-1]
        self.assertEqual(error, "** class doesn't exist **")

    def test_class_count(self):
        '''test advanced count command'''
        for class_name in self.classes:
            for x in range(5):
                with patch('sys.stdout', new=StringIO()) as f:
                    HBNBCommand().onecmd("create {}".format(class_name))
                class_id = f.getvalue()[:-1]
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd("{}.count()".format(class_name))
            res = f.getvalue()[:-1]
            self.assertTrue(len(res) > 0)
            self.assertEqual(res, "5")

    def test_update_BaseModel(self):
        '''test update command on BaseModel class'''
        class_name = "BaseModel"
        attr = "foo"
        value = "Bar"
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create {}".format(class_name))
        class_id = f.getvalue()[:-1]
        command = "{}.update('{}', '{}', '{}')".format(class_name, class_id,
                                                       attr, value)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(command)
        res = f.getvalue()
        self.assertEqual(len(res), 0)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('{}.show("{}")'.format(class_name, class_id))
        res = f.getvalue()
        self.assertIn(attr, res)
        self.assertIn(value, res)

    def test_update_City(self):
        '''test update command on City class'''
        class_name = "City"
        attr = "foo"
        value = "Bar"
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create {}".format(class_name))
        class_id = f.getvalue()[:-1]
        command = "{}.update('{}', '{}', '{}')".format(class_name, class_id,
                                                       attr, value)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(command)
        res = f.getvalue()
        self.assertEqual(len(res), 0)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('{}.show("{}")'.format(class_name, class_id))
        res = f.getvalue()
        self.assertIn(attr, res)
        self.assertIn(value, res)

    def test_update_State(self):
        '''test update command on State class'''
        class_name = "State"
        attr = "foo"
        value = "Bar"
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create {}".format(class_name))
        class_id = f.getvalue()[:-1]
        command = "{}.update('{}', '{}', '{}')".format(class_name, class_id,
                                                       attr, value)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(command)
        res = f.getvalue()
        self.assertEqual(len(res), 0)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('{}.show("{}")'.format(class_name, class_id))
        res = f.getvalue()
        self.assertIn(attr, res)
        self.assertIn(value, res)

    def test_update_Amenity(self):
        '''test update command on Amenity class'''
        class_name = "Amenity"
        attr = "foo"
        value = "Bar"
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create {}".format(class_name))
        class_id = f.getvalue()[:-1]
        command = "{}.update('{}', '{}', '{}')".format(class_name, class_id,
                                                       attr, value)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(command)
        res = f.getvalue()
        self.assertEqual(len(res), 0)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('{}.show("{}")'.format(class_name, class_id))
        res = f.getvalue()
        self.assertIn(attr, res)
        self.assertIn(value, res)

    def test_update_User(self):
        '''test update command on User class'''
        class_name = "User"
        attr = "foo"
        value = "Bar"
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create {}".format(class_name))
        class_id = f.getvalue()[:-1]
        command = "{}.update('{}', '{}', '{}')".format(class_name, class_id,
                                                       attr, value)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(command)
        res = f.getvalue()
        self.assertEqual(len(res), 0)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('{}.show("{}")'.format(class_name, class_id))
        res = f.getvalue()
        self.assertIn(attr, res)
        self.assertIn(value, res)

    def test_update_Place(self):
        '''test update command on Place class'''
        class_name = "Place"
        attr = "foo"
        value = "Bar"
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create {}".format(class_name))
        class_id = f.getvalue()[:-1]
        command = "{}.update('{}', '{}', '{}')".format(class_name, class_id,
                                                       attr, value)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(command)
        res = f.getvalue()
        self.assertEqual(len(res), 0)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('{}.show("{}")'.format(class_name, class_id))
        res = f.getvalue()
        self.assertIn(attr, res)
        self.assertIn(value, res)

    def test_update_Review(self):
        '''test update command on Review class'''
        class_name = "Review"
        attr = "foo"
        value = "Bar"
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create {}".format(class_name))
        class_id = f.getvalue()[:-1]
        command = "{}.update('{}', '{}', '{}')".format(class_name, class_id,
                                                       attr, value)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(command)
        res = f.getvalue()
        self.assertEqual(len(res), 0)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('{}.show("{}")'.format(class_name, class_id))
        res = f.getvalue()
        self.assertIn(attr, res)
        self.assertIn(value, res)

    def test_update_BaseModel_2(self):
        '''test update command on BaseModel class'''
        class_name = "BaseModel"
        attr = "foo"
        value = "Bar"
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create {}".format(class_name))
        class_id = f.getvalue()[:-1]
        command = "update {} {} {} {}".format(class_name, class_id,
                                              attr, value)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(command)
        res = f.getvalue()
        self.assertEqual(len(res), 0)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('{}.show("{}")'.format(class_name, class_id))
        res = f.getvalue()
        self.assertIn(attr, res)
        self.assertIn(value, res)

    def test_update_City_2(self):
        '''test update command on City class'''
        class_name = "City"
        attr = "foo"
        value = "Bar"
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create {}".format(class_name))
        class_id = f.getvalue()[:-1]
        command = "update {} {} {} {}".format(class_name, class_id,
                                              attr, value)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(command)
        res = f.getvalue()
        self.assertEqual(len(res), 0)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('{}.show("{}")'.format(class_name, class_id))
        res = f.getvalue()
        self.assertIn(attr, res)
        self.assertIn(value, res)

    def test_update_State_2(self):
        '''test update command on State class'''
        class_name = "State"
        attr = "foo"
        value = "Bar"
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create {}".format(class_name))
        class_id = f.getvalue()[:-1]
        command = "update {} {} {} {}".format(class_name, class_id,
                                              attr, value)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(command)
        res = f.getvalue()
        self.assertEqual(len(res), 0)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('{}.show("{}")'.format(class_name, class_id))
        res = f.getvalue()
        self.assertIn(attr, res)
        self.assertIn(value, res)

    def test_update_Amenity_2(self):
        '''test update command on Amenity class'''
        class_name = "Amenity"
        attr = "foo"
        value = "Bar"
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create {}".format(class_name))
        class_id = f.getvalue()[:-1]
        command = "update {} {} {} {}".format(class_name, class_id,
                                              attr, value)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(command)
        res = f.getvalue()
        self.assertEqual(len(res), 0)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('{}.show("{}")'.format(class_name, class_id))
        res = f.getvalue()
        self.assertIn(attr, res)
        self.assertIn(value, res)

    def test_update_User_2(self):
        '''test update command on User class'''
        class_name = "User"
        attr = "foo"
        value = "Bar"
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create {}".format(class_name))
        class_id = f.getvalue()[:-1]
        command = "update {} {} {} {}".format(class_name, class_id,
                                              attr, value)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(command)
        res = f.getvalue()
        self.assertEqual(len(res), 0)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('{}.show("{}")'.format(class_name, class_id))
        res = f.getvalue()
        self.assertIn(attr, res)
        self.assertIn(value, res)

    def test_update_Place_2(self):
        '''test update command on Place class'''
        class_name = "Place"
        attr = "foo"
        value = "Bar"
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create {}".format(class_name))
        class_id = f.getvalue()[:-1]
        command = "update {} {} {} {}".format(class_name, class_id,
                                              attr, value)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(command)
        res = f.getvalue()
        self.assertEqual(len(res), 0)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('{}.show("{}")'.format(class_name, class_id))
        res = f.getvalue()
        self.assertIn(attr, res)
        self.assertIn(value, res)

    def test_update_Review_2(self):
        '''test update command on Review class'''
        class_name = "Review"
        attr = "foo"
        value = "Bar"
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create {}".format(class_name))
        class_id = f.getvalue()[:-1]
        command = "update {} {} {} {}".format(class_name, class_id,
                                              attr, value)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(command)
        res = f.getvalue()
        self.assertEqual(len(res), 0)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('{}.show("{}")'.format(class_name, class_id))
        res = f.getvalue()
        self.assertIn(attr, res)
        self.assertIn(value, res)

    def test_update_errors(self):
        '''test errors of update command'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")
        class_id = f.getvalue()[:-1]
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update")
        error = f.getvalue()[:-1]
        self.assertEqual(error, "** class name missing **")
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update NotClass")
        error = f.getvalue()[:-1]
        self.assertEqual(error, "** class doesn't exist **")
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update BaseModel")
        error = f.getvalue()[:-1]
        self.assertEqual(error, "** instance id missing **")
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update BaseModel 4d65h43s4d5")
        error = f.getvalue()[:-1]
        self.assertEqual(error, "** no instance found **")
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('update BaseModel {}'.format(class_id))
        error = f.getvalue()[:-1]
        self.assertEqual(error, "** attribute name missing **")
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('update BaseModel {} name'.format(class_id))
        error = f.getvalue()[:-1]
        self.assertEqual(error, "** value missing **")

    def test_update_errors_2(self):
        '''test errors of update command'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")
        class_id = f.getvalue()[:-1]
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(".update()")
        error = f.getvalue()[:-1]
        self.assertEqual(error, "** class name missing **")
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("NotClass.update()")
        error = f.getvalue()[:-1]
        self.assertEqual(error, "** class doesn't exist **")
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("BaseModel.update()")
        error = f.getvalue()[:-1]
        self.assertEqual(error, "** instance id missing **")
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("BaseModel.update(4d65h43s4d5)")
        error = f.getvalue()[:-1]
        self.assertEqual(error, "** no instance found **")
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('BaseModel.update("{}")'.format(class_id))
        error = f.getvalue()[:-1]
        self.assertEqual(error, "** attribute name missing **")
