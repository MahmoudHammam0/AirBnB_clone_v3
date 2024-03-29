#!/usr/bin/python3
""" FileStorage class Module """
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
import json


class FileStorage:
    """ serializes instances to a JSON file and deserializes JSON file
        to instances

        __file_path: string - path to the JSON file (ex: file.json)
        __objects: dictionary - stores all objects by <class name>.id
                                (ex: with id=12121212, the key will be
                                    BaseModel.12121212)"""

    __file_path = "file.json"
    __objects = {}
    classes = {
            'BaseModel': BaseModel,
            'User': User,
            'Place': Place,
            'State': State,
            'City': City,
            'Amenity': Amenity,
            'Review': Review
            }

    def all(self, cls=None):
        """ returns the dictionary __objects """
        if cls is not None:
            new_dict = {}
            for key, value in FileStorage.__objects.items():
                if type(value) is cls:
                    new_dict[key] = value
            return new_dict
        else:
            return FileStorage.__objects

    def new(self, obj):
        """ sets in __objects the obj with key <obj class name>.id
            creates a new object (element) in the objects dictionary

            key = <obj class name>.id
            Value = the object itself
            """
        key = obj.__class__.__name__ + "." + obj.id
        FileStorage.__objects[key] = obj

    def save(self):
        """ serializes __objects to the JSON file (path: __file_path) """
        json_objs = {}
        with open(FileStorage.__file_path, 'w') as file:
            for key, value in FileStorage.__objects.items():
                json_objs[key] = value.to_dict()
            json.dump(json_objs, file)

    def reload(self):
        """ deserializes the JSON file to __objects """
        new_objs = {}
        try:
            with open(FileStorage.__file_path, 'r') as f:
                objs = json.load(f)
            for key, value in objs.items():
                class_name, obj_id = key.split('.')
                the_class = FileStorage.classes[class_name]
                ins = the_class(**value)
                new_objs[key] = ins
            FileStorage.__objects = new_objs
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        '''delete obj from objects if exists'''
        if obj is not None:
            if obj in FileStorage.__objects.values():
                key = obj.__class__.__name__ + "." + obj.id
                del (FileStorage.__objects[key])
                FileStorage.save(self)

    def close(self):
        'deserializing the JSON file to objects'
        self.reload()
