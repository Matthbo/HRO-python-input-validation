def validate_username(username):
    pass

def validate_password(password):
    pass

# Base class for all users
class User:
    ROLE = None
    COMMANDS = "help,logout"
    username = None

    def __init__(self, username):
        self.username = username

    def getHelp(self):
        availableCommands = self.COMMANDS.replace(',', '\n')
        print("Available commands:\n" + availableCommands)

# The super administrator
class SuperAdmin(User):
    ROLE = "Super Administrator"

    def __init__(self, username):
        User.__init__(self, username)
        self.COMMANDS += ",new-user"

    def new_user(self, db):
        print("Creating a new System Administrator")
        username = input('Username: ')



        password = input('Password: ')

        db.addUser((username, password, self.ROLE))

# The system administrator
class Admin(User):
    ROLE = "System Administrator"

    def __init__(self, username):
        User.__init__(self, username)
        self.COMMANDS += ",new-user"

    def new_user(self, db):
        print("Can create Advisor")

# The advisor
class Advisor(User):
    ROLE = "Advisor"

class Client:
    # address should be a tuple containing (Street and house number, zipcode, city)
    def __init__(self, fullName, address, emailAddress, mobilePhone):
        # TODO validate address & mobilePhone
        pass

