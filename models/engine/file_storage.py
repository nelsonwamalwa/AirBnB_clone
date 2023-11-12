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
    """
    serializes instances to a JSON file and
    deserializes JSON file to instances
    """

    __path = "file.json"
    __object = {}

    def all(self):
        """
        returns the dictionary __objects
        """
        return FileStorage.__object

    def new(self, obj):
        """
        sets in __objects the obj with key <obj class name>.id
        """
        key = "{}.{}".format(type(obj).__name__, obj.id)
        FileStorage.__object[key] = obj

    def save(self):
        """
        serializes __objects to the JSON file (path: __file_path)
        """
        with open(FileStorage.__path, 'w') as f:
            json.dump(
                {k: v.to_dict() for k, v in FileStorage.__object.items()}, f)

    def reload(self):
        """
        deserializes the JSON file to __objects only if the JSON
        file exists; otherwise, does nothing
        """
        current_classes = {
            'BaseModel': BaseModel,
            'User': User,
            'Amenity': Amenity,
            'City': City,
            'State': State,
            'Place': Place,
            'Review': Review
        }

        if not os.path.exists(FileStorage.__path):
            return

        with open(FileStorage.__path, 'r') as f:
            deserialized = None

            try:
                deserialized = json.load(f)
            except json.JSONDecodeError:
                pass

            if deserialized is None:
                return

            FileStorage.__object = {
                k: current_classes[k.split('.')[0]](**v)
                for k, v in deserialized.items()}