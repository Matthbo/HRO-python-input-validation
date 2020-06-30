#!/usr/bin/python3

"""
Super Administrator login
Username: babak
Password: F*s3sj!pg!
"""

from sys import stdin, stdout, stderr
from database import Database, RoleException, UsernameException, PasswordException, DatabaseException, BannedException
from logger import Logger, LogEntry

# The system console which receives all input
class System:
    CITIES = ["Rotterdam", "The Hague", "Utrecht", "Amsterdam", "Groningen", "Maastricht", "Breda", "Eindhoven", "Leeuwarden", "Zwolle"]
    consolePrefix = '> '
    user = None
    wrongLoginCount = 0
    notPermittedCount = 0
    log = Logger()

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
            consoleInput = line.strip().translate(str.maketrans('', '', '\x00')).split(' ')
            command = consoleInput[0]
            args = consoleInput[1:]

            if command == "exit" or command == "stop":
                break

            if self.wrongLoginCount >= 5:
                break

            switcher = {
                'help': self.getHelp,
                'login': self.login,
                'logout': self.logout,
                'new-user': self.new_user,
                'add-client': self.add_client,
                'get-logs': self.get_logs,
            }

            res = switcher.get(command, "Invalid command, type 'help' for all commands")
            
            if isinstance(res, str):
                print(res)
            else:
                res()

            self.prepare_input()

    def login(self):
        if self.user == None:
            username = input("Username: ").lower()
            password = input("Password: ")

            try:
                self.user = self.DB.getUser(username, password)
                self.wrongLoginCount = 0
                self.notPermittedCount = 0
                print(f"Logged in as {self.user.username} ({self.user.ROLE})")
                self.log.addLogEntry(LogEntry(3, username, "[login] User logged in"))
            except Exception as e:
                if isinstance(e, PasswordException) or isinstance(e, UsernameException):
                    self.wrongLoginCount += 1
                    try:
                        self.log.addLogEntry(LogEntry(3, username, "[login] User tried to log in with wrong credentials"))
                        print("Wrong username or password!")
                    except Exception as ex:
                        print(f"Something went wrong. ({type(e).__name__})")
                    if self.wrongLoginCount >= 5:
                        try:
                            print("You are being kicked for login abuse")
                            self.log.addLogEntry(LogEntry(2, username, "[login] User kicked after logging in with wrong credentials 5 times"))
                            print("Closing system...")
                            exit()
                        except Exception as ex:
                            print(f"something went wrong. ({type(ex).__name__})")
                elif isinstance(e, BannedException):
                    try:
                        self.log.addLogEntry(LogEntry(2, username, "[login] Banned user tried to log in"))
                        print("You are banned!")
                    except Exception as ex:
                        print(f"Something went wrong. ({type(ex).__name__})")
                else:
                    try:
                        self.log.addLogEntry(LogEntry(1, username, f"[login] Error occured when trying to log in. ({type(e).__name__})"))
                        print("Something went wrong")
                    except Exception as ex:
                        print(f"Something went wrong ({type(ex).__name__})")
                
        else:
            try:
                self.log.addLogEntry(LogEntry(1, username, "[login] User tried to log in while already being logged in."))
                print(f"Already logged in as {self.user.username} ({self.user.ROLE})")
            except Exception as ex:
                print(f"Something went wrong. ({type(ex).__name__})")
    
    def logout(self):
        if self.user != None:
            try:
                self.log.addLogEntry(LogEntry(3, self.user.username, "[logout] User logged out."))
                self.user = None
                self.notPermittedCount = 0
                print("You are now logged out")
            except Exception as e:
                print(f"Something went wrong. ({type(e).__name__})")
        else:
            try:
                self.log.addLogEntry(LogEntry(1, None, "[logout] User tried to log out while already boing logged out."))
            except Exception as e:
                print(f"Something went wrong. ({type(e).__name__})")
            print("You are already logged out!")

    def new_user(self):
        try:
            if self.user != None and hasattr(self.user, 'new_user'):
                self.user.new_user(self.DB)
            else:
                if self.user != None:
                    self.log.addLogEntry(LogEntry(1, self.user.username, "[new-user] Unauthorized user tried to make a new user"))
                else:
                    self.log.addLogEntry(LogEntry(1, None, "[new-user] Someone without an account tried to make a new user."))

                print("Not allowed!")
                self.checkForBan()
                
        except Exception as e:
            print(f"Something went wrong. ({type(e).__name__})")  
    
    def add_client(self):
        try:
            if self.user != None and hasattr(self.user, 'add_client'):
                self.user.add_client(self.DB, self.CITIES)
            else:
                if self.user != None:
                    self.log.addLogEntry(LogEntry(1, self.user.username, "[add-client] Unauthorized user tried to make a new client"))
                else:
                    self.log.addLogEntry(LogEntry(1, None, "[add-client] Someone without an account tried to make a new user"))

                print("Not allowed!")
                self.checkForBan()
        except Exception as e:
            print(f"Something went wrong. ({type(e).__name__})")

    def get_logs(self):
        try:
            if self.user != None and hasattr(self.user, 'get_logs'):
                self.user.get_logs(self.DB)
            else:
                if self.user != None:
                    self.log.addLogEntry(LogEntry(1, self.user.username, "[get-logs] Unauthorized user tried to get the logs"))
                else:
                    self.log.addLogEntry(LogEntry(1, None, "[get-logs] Someone without an account tried to get the logs"))

                print("Not allowed!")
                self.checkForBan()
        except Exception as e:
            print(f"Something went wrong.1 ({type(e).__name__})\n{e}")

    def getHelp(self):
        if(self.user != None):
            self.user.getHelp()
        else:
            print("Use 'login' to log in, after that you can use 'help' for a list of available commands\nUse 'exit' or 'stop' to exit the system")
    
    def checkForBan(self):
        try:
            self.notPermittedCount += 1
            if self.notPermittedCount >= 4:
                if self.user != None and self.user.ROLE != "Super Administrator":
                    print("You are banned from the system")
                    self.log.addLogEntry(LogEntry(1, self.user.username, "[banned] user got banned"))
                    self.DB.banUser(self.user.username)
                    self.logout()
                elif self.user == None:
                    self.log.addLogEntry(LogEntry(1, None, "[Kicked] Someone with no account got kicked for unauthorized command abuse"))
                    print("You are being kicked for unauthorized command abuse")
                    print("Closing system...")
                    exit()
        except Exception as e:
            print(f"Something went wrong. ({type(e).__name__})")

# Start the application
System()
