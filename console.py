#!/usr/bin/python3
""" The main console """

import cmd


class Mycommand(cmd.Cmd):
    """ Console program class """
    def do_greet(self, line):
        print ('Hello!')
    
    def help_greet(self):
        print("Print greeting to the console")

    def do_EOF(self, line):
        return True


if __name__ == '__main__':
    Mycommand().cmdloop()
