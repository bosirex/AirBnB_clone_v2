#!/usr/bin/python3
"""Defines the FileStorage class."""
import json
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class FileStorage:
    """This class manages storage of hbnb models in JSON format.
    """

    __file_path = "file.json"
    __objects = {}

    def all(self, clss=None):
        """Returns a dictionary of models currently in storage.
        """
        if clss is not None:
            if type(clss) == str:
                clss = eval(clss)
            cls_dict = {}
            for m, n in self.__objects.items():
                if type(n) == clss:
                    cls_dict[m] = n
            return cls_dict
        return self.__objects

    def new(self, obj):
        """Adds new object to storage dictionary."""
        self.__objects["{}.{}".format(type(obj).__name__, obj.id)] = obj

    def save(self):
        """Saves storage dictionary to file."""
        o_dict = {m: self.__objects[m].to_dict() for m in self.__objects.keys()}
        with open(self.__file_path, "w", encoding="utf-8") as f:
            json.dump(o_dict, f)

    def reload(self):
        """Loads storage dictionary from file."""
        try:
            with open(self.__file_path, "r", encoding="utf-8") as f:
                for m in json.load(f).values():
                    name = m["__class__"]
                    del m["__class__"]
                    self.new(eval(name)(**m))
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """delete obj from __objects."""
        try:
            del self.__objects["{}.{}".format(type(obj).__name__, obj.id)]
        except (AttributeError, KeyError):
            pass

    def close(self):
        """Call the reload function."""
        self.reload()
