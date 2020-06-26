#!/usr/bin/python3

"""
Super Administrator login:
Username: Babak
Password: F*s3sj!pg!
"""

# helpful links:
# Console app recommendations: https://stackoverflow.com/a/39068747
# isinstance: https://pynative.com/python-isinstance-explained-with-examples/

from sys import stdin, stdout, stderr
from database import Database, RoleException, UsernameException, PasswordException, DatabaseException

# The system console which receives all input
class System:
    CITIES = ["Rotterdam", "The Hague", "Utrecht", "Amsterdam", "Groningen", "Maastricht", "Breda", "Eindhoven", "Leeuwarden", "Zwolle"]
    consolePrefix = '> '
    user = None

    def __init__(self):
        self.DB = Database()

        print("Welcome to House Construction OS, for a list of commands type 'help'")

        self.command_handler()

        print("Closing system...")

    def prepare_input(self):
        stdout.write(self.consolePrefix)
        stdout.flush()

    def command_handler(self):
        self.prepare_input()

        for line in stdin:
            consoleInput = line.rstrip().split(' ')
            command = consoleInput[0]
            args = consoleInput[1:]

            if command == "exit" or command == "stop":
                break

            switcher = {
                'help': self.getHelp,
                'login': self.login,
                'logout': self.logout,
                'new-user': self.new_user,
            }

            res = switcher.get(command, "Invalid command, type 'help' for all commands")
            
            if isinstance(res, str):
                print(res)
            else:
                res()

            self.prepare_input()

    def login(self):
        if self.user == None:
            username = input("Username: ")
            password = input("Password: ")

            try:
                self.user = self.DB.getUser(username, password)
                print(f"Logged in as {self.user.username} ({self.user.ROLE})")
            except Exception as e:
                if isinstance(e, PasswordException) or isinstance(e, UsernameException):
                    print("Wrong username or password!")
                else:
                    print("Something went wrong")
                
        else:
            print(f"Already logged in as {self.user.username} ({self.user.ROLE})")
    
    def logout(self):
        if self.user != None:
            self.user = None
            print("You are now logged out")
        else:
            print("You are already logged out!")

    def new_user(self):
        if self.user != None and hasattr(self.user, 'new_user'):
            self.user.new_user(self.DB)
        else:
            print("Not allowed!")

    def getHelp(self):
        if(self.user != None):
            self.user.getHelp()
        else:
            print("Use 'login' to log in, after that you can use 'help' for a list of available commands")

# Start the application
System()
