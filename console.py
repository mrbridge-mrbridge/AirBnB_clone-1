#!/usr/bin/python3
"""This module is the entry point of the Airbnb command interpreter"""
import cmd, sys, re, os
from models.base_model import BaseModel
from models.user import User
from models.engine.file_storage import FileStorage
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State

classes = {"Amenity": Amenity,
        "BaseModel": BaseModel,
        "City": City,
        "Place": Place,
        "Review": Review,
        "State": State,
        "User": User}


class HBNBCommand(cmd.Cmd):
    """The class HBNBCommand"""
    prompt = '(hbnb)'

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """EOF command to exit the program"""
        return True

    def emptyline(self):
        """Nothing"""
        pass

    def do_create(self, arg):
        """Create command to create and save new BaseModel
        instance to JSON file and print the id
        Usage: create <class> <key 1>=<value 2> <key 2>=<value 2> ..."""
        
        try:
            if not arg:
                raise SyntaxError()
            cls = arg.split(" ")

            kwargs = {}
            for i in range(1, len(cls)):
                key, value = tuple(cls[i].split("="))
                if value[0] == '"':
                    value = value.strip('"').replace("_", " ")
                else:
                    try:
                        value = eval(value)
                    except (SyntaxError, NameError):
                        continue
                kwargs[key] = value

            if kwargs == {}:
                val = eval(cls[0])()
            else:
                val = eval(cls[0])(**kwargs)
                storage.new(val)
            print(val.id)
            val.save()
        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")


    def do_show(self, arg):
        """Show command prints the string representation of class instance"""
        cls = arg.split(" ")
        dikt = storage.all()
        if len(cls) == 0:
            print("** class name missing **")
            return False

        elif len(cls) == 1:
            print("** instance id missing **")
            return False

        elif cls[0] not in classes:
            print("** class doesn't exist **")
            return False

        elif (cls[0] + "." + cls[1]) not in dikt:
            print("** no instance found **")
            return False

        else:
            print(dikt[cls[0] + "." + cls[1]])

    def do_destroy(self, arg):
        """Destroy command deletes a class instance based on 
        class name and id"""

        cls = arg.split(" ")
        dikt = storage.all()
        if len(cls) == 0:
            print("** class name missing **")
            return False

        elif len(cls) == 1:
            print("** instance id missing **")
            return False

        elif cls[0] not in classes:
            print("** class doesn't exist **")
            return False

        elif (cls[0] + "." + cls[1]) not in dikt:
            print("** no instance found **")
            return False

        else:
            del dikt[(cls[0] + "." + cls[1])]
            storage.save()

    def do_all(self, arg):
        """All command Prints all string representation of all
        instances based or not on the class name"""
        cls = arg.split(" ")
        strg = []

        if len(cls) == 0:
            for v in storage.all().values():
                strg.append(v.__str__())
            print(strg)
        
        if len(cls) > 0:
            if cls[0] in classes:
                for v in storage.all().values():
                    strg.append(v.__str__())
                print(strg)

            elif cls[0] not in classes:
                print("** class doesn't exist **")

    def do_update(self, arg):
        """Update command Updates an instance based on the class
        name and id by adding or updating attribute
        Usage: update <class name> <id> <attribute name> '<attribute value>'
        """
        cls = arg.split(" ")
        dikt = storage.all()
        keyyy = cls[0] + "." + cls[1]


        if len(cls) >= 4:
            if cls[0] not in classes:
                print("** class doesn't exist **")
                return False
            elif cls[0] in classes:
                if keyyy in dikt.keys():
                    setattr(dikt[keyyy], cls[2], cls[3])
                
                else:
                    print("** no instance found **")
                    return False

        if len(cls) == 0:
            print("** class name missing **")
            return False

        if len(cls) == 1:
            print("** instance id missing **")
            return False

        if len(cls) == 2:
            print("** attribute name missing **")
            return False

        if len(cls) == 3:
            print("** value missing **")
            return False
        
if __name__ == '__main__':
    HBNBCommand().cmdloop()
