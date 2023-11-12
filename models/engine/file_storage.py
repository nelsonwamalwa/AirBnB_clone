#!/usr/bin/python3
"""
Module: file_storage.py defines a `FileStorage` class.
"""
import os
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.review import Review
from models.amenity import Amenity
from models.place import Place


class FileStorage():
    """ serializes instances to a JSON file and deserializes JSON file to instances
    """

    FilePath = "file.json"
    Object = {}

    def all(self):
        """ returns the dictionary __objects """
        return FileStorage.Object

    def new(self, obj):
        """ sets in __objects the obj with key <obj class name>.id """
        key = "{}.{}".format(type(obj).__name__, obj.id)
        FileStorage.Object[key] = obj

    def save(self):
        """ serializes __objects to the JSON file (path: __file_path) """
        with open(FileStorage.FilePath, 'w') as f:
            json.dump(
                {i: j.to_dict() for i, j in FileStorage.Object.items()}, f)

    def reload(self):
        """ Deserializes the JSON file to __objects only if the JSON file exists; otherwise, does nothing """
        CurrentClasses = {
            'BaseModel': BaseModel,
            'User': User,
            'Amenity': Amenity,
            'City': City,
            'State': State,
            'Place': Place,
            'Review': Review
        }

        if not os.path.exists(FileStorage.FilePath):
            return

        with open(FileStorage.FilePath, 'r') as f:
            Deserialized = None

            try:
                Deserialized = json.load(f)
            except json.JSONDecodeError:
                pass

            if Deserialized is None:
                return

            FileStorage.Object = {
                i: CurrentClasses[i.split('.')[0]](**j)
                for i, j in Deserialized.items()}