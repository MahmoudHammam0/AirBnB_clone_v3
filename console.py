#!/usr/bin/python3
'''console module'''
import cmd
from models.base_model import BaseModel
from models import storage
from sqlalchemy import Column, String, Integer, Float


class HBNBCommand(cmd.Cmd):
    '''simple command interpreter class'''
    prompt = '(hbnb) '

    def do_EOF(self, line):
        '''EOF exit to the program'''
        return True

    def do_quit(self, line):
        '''Quit command to exit the program'''
        return True

    def emptyline(self):
        '''empty line shouldn’t execute anything'''
        pass

    def do_create(self, line):
        '''Creates a new instance of BaseModel, saves it (to the JSON file)'''
        line = line.replace('"', '')
        line = line.replace('(', ' ').replace(')', ' ').replace(',', '')
        args = line.split()
        if not args:
            print("** class name missing **")
        elif args[0] not in storage.classes:
            print("** class doesn't exist **")
        else:
            the_class = storage.classes[args[0]]
            ins = the_class()
            params = args[1:]
            for i in range(len(params)):
                param = params[i].split('=')
                key = param[0]
                value = param[1]
                value = value.replace('_', ' ')
                if key in the_class.__dict__:
                    attr_type = type(getattr(the_class, key))
                    if attr_type in [int, float, str]:
                        value = attr_type(value)
                    else:
                        attr_type = getattr(the_class, key).type
                        if isinstance(attr_type, Integer):
                            value = int(value)
                        elif isinstance(attr_type, Float):
                            value = float(value)
                        elif isinstance(attr_type, String):
                            value = str(value)
                    setattr(ins, key, value)
            ins.save()
            print(ins.id)

    def do_show(self, line):
        '''Prints the string of an instance based on the class name and id'''
        args = line.split()
        if len(args) < 2:
            if len(args) == 0:
                print("** class name missing **")
            elif args[0] not in storage.classes:
                print("** class doesn't exist **")
            elif args[0] in storage.classes:
                print("** instance id missing **")
        elif len(args) == 2:
            key = "{}.{}".format(args[0], args[1])
            obj_dict = storage.all()
            if args[0] not in storage.classes:
                print("** class doesn't exist **")
            elif key not in obj_dict:
                print("** no instance found **")
            else:
                print(obj_dict[key])

    def do_destroy(self, line):
        '''Deletes an instance based on the class name and id'''
        args = line.split()
        if len(args) < 2:
            if len(args) == 0:
                print("** class name missing **")
            elif args[0] not in storage.classes:
                print("** class doesn't exist **")
            elif args[0] in storage.classes:
                print("** instance id missing **")
        elif len(args) == 2:
            key = "{}.{}".format(args[0], args[1])
            obj_dict = storage.all()
            if args[0] not in storage.classes:
                print("** class doesn't exist **")
            elif key not in obj_dict:
                print("** no instance found **")
            else:
                del (storage.all()[key])
                storage.save()

    def do_all(self, line):
        '''Prints all string representation of all instances'''
        the_list = []
        objs_dict = storage.all()
        if line:
            if line not in storage.classes:
                print("** class doesn't exist **")
            else:
                for key, value in objs_dict.items():
                    class_name, x = key.split('.')
                    if class_name == line:
                        the_list.append(str(value))
                print(the_list)
        else:
            for key, value in objs_dict.items():
                the_list.append(str(value))
            print(the_list)

    def do_update(self, line):
        '''Updates an instance by adding or updating attribute'''
        args = line.split()
        obj_dict = storage.all()
        if len(args) < 2:
            if len(args) == 0:
                print("** class name missing **")
            elif args[0] not in storage.classes:
                print("** class doesn't exist **")
            elif args[0] in storage.classes:
                print("** instance id missing **")
        elif len(args) == 2:
            key = "{}.{}".format(args[0], args[1])
            if args[0] not in storage.classes:
                print("** class doesn't exist **")
            elif key not in obj_dict:
                print("** no instance found **")
            else:
                print("** attribute name missing **")
        elif len(args) == 3:
            key = "{}.{}".format(args[0], args[1])
            if args[0] not in storage.classes:
                print("** class doesn't exist **")
            elif key not in obj_dict:
                print("** no instance found **")
            else:
                print("** value missing **")
        else:
            key = "{}.{}".format(args[0], args[1])
            if args[0] not in storage.classes:
                print("** class doesn't exist **")
            elif key not in obj_dict:
                print("** no instance found **")
            else:
                for k, v in storage.all().items():
                    if k == key:
                        args[3] = args[3].strip('"')
                        args[3] = args[3].strip("'")
                        args[2] = args[2].strip('"')
                        args[2] = args[2].strip("'")
                        if args[2] in v.__dict__:
                            attr_type = type(getattr(v, args[2]))
                            args[3] = attr_type(args[3])
                        setattr(v, args[2], args[3])
                        v.save()

    def do_count(self, line):
        '''retrieve the number of instances of a class'''
        count = 0
        for k, v in storage.all().items():
            name, x = k.split('.')
            if line == name:
                count += 1
        print(count)

    def default(self, line):
        ''' Executes the appropiate command (ex: <class name>.command())

            <class name>.all(): prints all the instances of the specified class
            <class name>.show(<id>) : prints the class instance based on its id
            <class name>.destroy(<id>) : destroys the instance based on its id
            <class name>.update(<id>, <attribute name>, <attribute value>) :
                                updates the instance attributes based on its id
            <class name>.update(<id>, <dictionary representation>) : update an
                                instance based on its id with a dictionary
        '''
        commands = {'all': self.do_all, 'show': self.do_show,
                    'count': self.do_count, 'destroy': self.do_destroy,
                    'update': self.do_update}
        parts = line.split('.')
        parts[1] = parts[1].replace('(', ' ').replace(')', '')
        parts[1] = parts[1].replace('"', '').replace(',', '')
        parts[1] = parts[1].replace('{', '').replace('}', '')
        parts[1] = parts[1].replace(':', '').replace("'", '')
        parts[1] = parts[1].split()
        command_name = parts[1][0]
        the_command = None
        for k, v in commands.items():
            if command_name == k:
                the_command = v
        if the_command is not None:
            if len(parts[1]) == 1:
                arg = parts[0]
                the_command(arg)
            elif len(parts[1]) == 2:
                arg = parts[0] + ' ' + parts[1][1]
                the_command(arg)
            elif len(parts[1]) > 2:
                if len(parts[1]) > 4:
                    for i in range(2, len(parts[1]) - 1, 2):
                        key = parts[1][i]
                        value = parts[1][i + 1]
                        arg = (parts[0] + ' ' + parts[1][1] + ' ' +
                               key + ' ' + value)
                        the_command(arg)
                else:
                    arg = (parts[0] + ' ' + parts[1][1] + ' ' +
                           parts[1][2] + ' ' + parts[1][3])
                    the_command(arg)
        else:
            print("** invalid command: <class name>.command() **")


if __name__ == '__main__':
    HBNBCommand().cmdloop()
