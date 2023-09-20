#!/usr/bin/python3
"""Defines the HBNB console."""
import cmd
from shlex import split
from models import storage
from datetime import datetime
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """Contains the functionality for the HBNB console."""

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Amenity",
        "Place",
        "Review"
    }

    def emptyline(self):
        """Ignore empty spaces."""
        pass

    def do_quit(self, line):
        """Quit command to exit the HBNB console."""
        return True

    def do_EOF(self, line):
        """Handles EOF signal to exit the program."""
        print("")
        return True

    def do_create(self, args):
        """Usage: create <class> <key 1>=<value 2> <key 2>=<value 2> ...
        allow for object creation with given parameters.
        """
        try:
            if not args:
                raise SyntaxError()
            list = args.split(" ")

            kwargs = {}
            for j in range(1, len(list)):
                key, value = tuple(list[j].split("="))
                if value[0] == '"':
                    value = value.strip('"').replace("_", " ")
                else:
                    try:
                        value = eval(value)
                    except (SyntaxError, NameError):
                        continue
                kwargs[key] = value

            if kwargs == {}:
                object = eval(list[0])()
            else:
                object = eval(list[0])(**kwargs)
                storage.new(object)
            print(object.id)
            object.save()

        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")

    def do_show(self, args):
        """Method to show an individual object
        Exceptions:
            IndexError: no id given
            SyntaxError: no args given
            KeyError: no valid id provided
            NameError: no object with the name
        """
        try:
            if not args:
                raise SyntaxError()
            list = args.split(" ")
            if list[0] not in self.__classes:
                raise NameError()
            if len(list) < 2:
                raise IndexError()
            objects = storage.all()
            key = list[0] + '.' + list[1]
            if key in objects:
                print(objects[key])
            else:
                raise KeyError()
        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")
        except IndexError:
            print("** instance id missing **")
        except KeyError:
            print("** instance id missing **")

    def do_destroy(self, args):
        """Deletes an instance based on the class name and id
        Exceptions:
            SyntaxError: when there is no args given
            NameError: when there is no object taht has the name
            IndexError: when there is no id given
            KeyError: when there is no valid id given
        """
        try:
            if not args:
                raise SyntaxError()
            list = args.split(" ")
            if list[0] not in self.__classes:
                raise NameError()
            if len(list) < 2:
                raise IndexError()
            objects = storage.all()
            key = list[0] + '.' + list[1]
            if key in objects:
                del objects[key]
                storage.save()
            else:
                raise KeyError()
        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")
        except IndexError:
            print("** instance id missing **")
        except KeyError:
            print("** no instance found **")

    def do_all(self, args):
        """Usage: Shows all objects, or all objects of a class."""
        if not args:
            o = storage.all()
            print([o[k].__str__() for k in o])
            return
        try:
            args = args.split(" ")
            if args[0] not in self.__classes:
                raise NameError()

            o = storage.all(eval(args[0]))
            print([o[k].__str__() for k in o])

        except NameError:
            print("** class doesn't exist **")

    def do_update(self, args):
        """Updates a certain object with new info."""
        try:
            if not args:
                raise SyntaxError()
            list = split(args, " ")
            if list[0] not in self.__classes:
                raise NameError()
            if len(list) < 2:
                raise IndexError()
            objects = storage.all()
            key = list[0] + '.' + list[1]
            if key not in objects:
                raise KeyError()
            if len(list) < 3:
                raise AttributeError()
            if len(list) < 4:
                raise ValueError()
            v = objects[key]
            try:
                v.__dict__[list[2]] = eval(list[3])
            except Exception:
                v.__dict__[list[2]] = list[3]
                v.save()
        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")
        except IndexError:
            print("** instance id missing **")
        except KeyError:
            print("** no instance found **")
        except AttributeError:
            print("** attribute name missing **")
        except ValueError:
            print("** value missing **")

    def count(self, args):
        """Count current number of class instances
        """
        counter = 0
        try:
            list = split(args, " ")
            if list[0] not in self.__classes:
                raise NameError()
            objects = storage.all()
            for key in objects:
                name = key.split('.')
                if name[0] == list[0]:
                    counter += 1
            print(counter)
        except NameError:
            print("** class doesn't exist **")

    def strip_clean(self, args):
        """strips argument and return a string of command
        """
        new_list = []
        new_list.append(args[0])
        try:
            my_dict = eval(
                args[1][args[1].find('{'):args[1].find('}')+1])
        except Exception:
            my_dict = None
        if isinstance(my_dict, dict):
            new_str = args[1][args[1].find('(')+1:args[1].find(')')]
            new_list.append(((new_str.split(", "))[0]).strip('"'))
            new_list.append(my_dict)
            return new_list
        new_str = args[1][args[1].find('(')+1:args[1].find(')')]
        new_list.append(" ".join(new_str.split(", ")))
        return " ".join(i for i in new_list)

    def default(self, args):
        """retrieve all instances of a class and
        retrieve number of instances
        """
        list = args.split('.')
        if len(list) >= 2:
            if list[1] == "all()":
                self.do_all(list[0])
            elif list[1] == "count()":
                self.count(list[0])
            elif list[1][:4] == "show":
                self.do_show(self.strip_clean(list))
            elif list[1][:7] == "destroy":
                self.do_destroy(self.strip_clean(list))
            elif list[1][:6] == "update":
                args = self.strip_clean(list)
                if isinstance(args, list):
                    obj = storage.all()
                    key = args[0] + ' ' + args[1]
                    for k, v in args[2].items():
                        self.do_update(key + ' "{}" "{}"'.format(k, v))
                else:
                    self.do_update(args)
        else:
            cmd.Cmd.default(self, args)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
