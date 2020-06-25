#!/usr/bin/python

# helpful links:
# Console app recommendations: https://stackoverflow.com/a/39068747
# isinstance: https://pynative.com/python-isinstance-explained-with-examples/

import re
from sys import stdout, stdin, stderr

# Base class for all users
class User:
    def __init__(self, username, password):
        validUsername = self.validate_username(username)
        validPassword = self.validate_username(password)

    def validate_username(self, username):
        # TODO check if username is valid, if not then ask for a new username (until valid)
        pass

    def validate_password(self, password):
        # TODO check if password is valid, if not then ask for a new password (until valid)
        pass

# The super administrator
class SuperAdmin(User):
    def create_admin(self, username, password):
        admin = Admin(username, password)

# The system administrator
class Admin(User):
    def create_advisor(self, username, password):
        advisor = Advisor(username, password)

# The advisor
class Advisor(User):
    pass


class Client:
    # address should be a tuple containing (Street and house number, zipcode, city)
    def __init__(self, fullName, address, emailAddress, mobilePhone):
        # TODO validate address & mobilePhone
        pass

# The system console which receives all input
class System:
    cities = ["Rotterdam", "The Hague", "Utrecht", "Amsterdam", "Groningen", "Maastricht", "Breda", "Eindhoven", "Leeuwarden", "Zwolle"]

    def __init__(self):
        stdout.write('Sup! >:D')

# Start the application
System()
