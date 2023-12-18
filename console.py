#!/usr/bin/python3
"""This module defines the entry point of the command interpreter.

It defines one class, `HBNBCommand()`, which sub-classes the `cmd.Cmd` class.
This module defines abstractions that allows us to manipulate a powerful
storage system (FileStorage / DB). This abstraction will also allow us to
change the type of storage easily without updating all of our codebase.

It allows us to interactively and non-interactively:
    - create a data model
    - manage (create, update, destroy, etc) objects via a console / interpreter
    - store and persist objects to a file (JSON file)

usage example:

    $ ./console
    (hbnb)

    (hbnb) help
    Documented commands (type help <topic>):
    ========================================
    EOF  create  help  quit

    (hbnb)
    (hbnb) quit
    $
"""
import re
import cmd
import json
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.review import Review
from models.amenity import Amenity
from models.place import Place

CurrentClasses = {'BaseModel': BaseModel, 'User': User,
                   'Amenity': Amenity, 'City': City, 'State': State,
                   'Place': Place, 'Review': Review}


class HBNBCommand(cmd.Cmd):
    """The command interpreter.

    This class represent the command interpreter, and the control center
    of this project. It defines function handlers for all commands inputted
    in the console and calls the appropriate storage engine APIs to manipulate
    application data / models.

    The  sub-classes Python's `cmd.Cmd` class which provides a simple framework
    for writing line-oriented command interpreters.
    """
    intro = """
    ============= HBNB THE CONSOLE =============
    |  ||        ||||||||           ||||||||   |
    |  ||        ||    ||           ||    ||   |
    |  ||||||||  ||||||    |||||||  ||||||     |
    |  ||    ||  ||    ||  ||   ||  ||    ||   |
    |  ||    ||  ||||||||  ||   ||  ||||||||   |
    ============================================
"""
    prompt = "(hbnb) "

    def precmd(self, line):
        """ Defines instructions to execute before <line> is interpreted. """
        if not line:
            return '\n'

        pattern = re.compile(r"(\w+)\.(\w+)\((.*)\)")
        MatchList = pattern.findall(line)
        if not MatchList:
            return super().precmd(line)

        MatchTuple = MatchList[0]
        if not MatchTuple[2]:
            if MatchTuple[1] == "count":
                ObjectInstances = storage.all()
                print(len([
                    j for _, j in ObjectInstances.items()
                    if type(j).__name__ == MatchTuple[0]]))
                return "\n"
            return "{} {}".format(MatchTuple[1], MatchTuple[0])
        else:
            args = MatchTuple[2].split(", ")
            if len(args) == 1:
                return "{} {} {}".format(
                    MatchTuple[1], MatchTuple[0],
                    re.sub("[\"\']", "", MatchTuple[2]))
            else:
                MatchJson = re.findall(r"{.*}", MatchTuple[2])
                if (MatchJson):
                    return "{} {} {} {}".format(
                        MatchTuple[1], MatchTuple[0],
                        re.sub("[\"\']", "", args[0]),
                        re.sub("\'", "\"", MatchJson[0]))
                return "{} {} {} {} {}".format(
                    MatchTuple[1], MatchTuple[0],
                    re.sub("[\"\']", "", args[0]),
                    re.sub("[\"\']", "", args[1]), args[2])

    def do_help(self, arg):
        """ To get help on a command, type help <topic>. """
        return super().do_help(arg)

    def do_EOF(self, line):
        """ Built-In EOF command to catch errors when necessary. """
        print("")
        return True

    def do_quit(self, arg):
        """ Quit command to exit the program. """
        return True

    def emptyline(self):
        """ Override default `empty line + return` behaviour. """
        pass

    def do_create(self, arg):
        """Creates a new instance.
        """
        args = arg.split()
        if not validate_classname(args):
            return

        NewObject = CurrentClasses[args[0]]()
        NewObject.save()
        print(NewObject.id)

    def do_show(self, arg):
        """ Show the string representation of an instance. """
        args = arg.split()
        if not validate_classname(args, CheckId=True):
            return

        ObjectInstances = storage.all()
        key = "{}.{}".format(args[0], args[1])
        RequestInstance = ObjectInstances.get(key, None)
        if RequestInstance is None:
            print("** no instance found **")
            return
        print(RequestInstance)

    def do_destroy(self, arg):
        """ Destory instance based on the class name and id. """
        args = arg.split()
        if not validate_classname(args, CheckId=True):
            return

        ObjectInstances = storage.all()
        key = "{}.{}".format(args[0], args[1])
        RequestInstance = ObjectInstances.get(key, None)
        if RequestInstance is None:
            print("** no instance found **")
            return

        del ObjectInstances[key]
        storage.save()

    def do_all(self, arg):
        """Do print string representation of all instances. """
        args = arg.split()
        AllObject = storage.all()

        if len(args) < 1:
            print(["{}".format(str(j)) for _, j in AllObject.items()])
            return
        if args[0] not in CurrentClasses.keys():
            print("** class doesn't exist **")
            return
        else:
            print(["{}".format(str(j))
                  for _, j in AllObject.items() if type(j).__name__ == args[0]])
            return

    def do_update(self, arg: str):
        """ Do update of instance based on the class name and id."""
        args = arg.split(maxsplit=3)
        if not validate_classname(args, CheckId=True):
            return

        ObjectInstances = storage.all()
        key = "{}.{}".format(args[0], args[1])
        RequestInstance = ObjectInstances.get(key, None)
        if RequestInstance is None:
            print("** no instance found **")
            return

        MatchJson = re.findall(r"{.*}", arg)
        if MatchJson:
            payload = None
            try:
                payload: dict = json.loads(MatchJson[0])
            except Exception:
                print("** invalid syntax")
                return
            for i, j in payload.items():
                setattr(RequestInstance, i, j)
            storage.save()
            return
        if not validate_attrs(args):
            return
        FistAttribute = re.findall(r"^[\"\'](.*?)[\"\']", args[3])
        if FistAttribute:
            setattr(RequestInstance, args[2], FistAttribute[0])
        else:
            ValueList = args[3].split()
            setattr(RequestInstance, args[2], parse_str(ValueList[0]))
        storage.save()


def validate_classname(args, CheckId=False):
    """Runs Validation on args classname entry. """
    if len(args) < 1:
        print("** class name missing **")
        return False
    if args[0] not in CurrentClasses.keys():
        print("** class doesn't exist **")
        return False
    if len(args) < 2 and CheckId:
        print("** instance id missing **")
        return False
    return True


def validate_attrs(args):
    """Runs validations on args classname attributes and values."""
    if len(args) < 3:
        print("** attribute name missing **")
        return False
    if len(args) < 4:
        print("** value missing **")
        return False
    return True


def is_float(x):
    """Checks for float value passed in the function `is_float`"""
    try:
        a = float(x)
    except (TypeError, ValueError):
        return False
    else:
        return True


def is_int(x):
    """Checks for integer value passed in the function `is_int`"""
    try:
        a = float(x)
        b = int(a)
    except (TypeError, ValueError):
        return False
    else:
        return a == b


def parse_str(arg):
    """ Parse through `args` to integer, float or string. """
    parsed = re.sub("\"", "", arg)

    if is_int(parsed):
        return int(parsed)
    elif is_float(parsed):
        return float(parsed)
    else:
        return arg


if __name__ == "__main__":
    HBNBCommand().cmdloop()
