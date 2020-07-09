import re
from logger import Logger, LogEntry

log = Logger()

def validate_email(email, user):
    while not re.match("^[\w.+-]+@[\w.-]+\.\w{2,}$", email):
        try:
            log.addLogEntry(LogEntry(
                2, user, "[validate-email] User tried to create a client with a wrong email address"))
            print("Invalid email address, it should look like 'person@example.com'")
            email = input("Email: ").translate(str.maketrans('', '', '\x00'))
        except Exception as e:
            print(f"Something went wrong. ")
    else:
        return email

def validate_phone(mobilePhone, user):
    while not re.match("^\+31-6-[\d]{4}-[\d]{4}$", mobilePhone):
        try:
            log.addLogEntry(LogEntry(
                2, user, "[validate-phone] User tried to create a client with a wrong phone number"))
            print("Invalid phone number, it should look like '+31-6-0123-4567'")
            mobilePhone = input("Mobile phone: ").translate(
                str.maketrans('', '', '\x00'))
        except Exception as e:
            print(f"Something went wrong. ")
    else:
        return mobilePhone

def validate_streethouse(streetHouse, user):
    while not re.match("^[\w ]+ [\d]+[a-z]?$", streetHouse):
        try:
            log.addLogEntry(LogEntry(
                2, user, "[validate-streethouse] User tried to create a client with a wrong address (street and house number)"))
            print("Invalid street & house number: it should look like 'Streetname 12'")
            streetHouse = input("Street & house number: ").translate(
                str.maketrans('', '', '\x00'))
        except Exception as e:
            print(f"Something went wrong. ")
    else:
        return streetHouse

def validate_zipcode(zipcode, user):
    while not re.match("^\d{4}[A-Z]{2}$", zipcode):
        try:
            log.addLogEntry(LogEntry(
                2, user, "[validate-zipcode] User tried to create a client with a wrong zipcode."))
            print("Invalid zipcode: it should look like '1234AB'")
            zipcode = input("Zipcode: ").upper().translate(
                str.maketrans('', '', '\x00'))
        except Exception as e:
            print(f"Something went wrong. ")
    else:
        return zipcode

def validate_city(city, cities, user):
    while not city in cities:
        try:
            log.addLogEntry(LogEntry(
                2, user, "[validate-city] User tried to create a client with a wrong city."))
            print("Invalid city, choose from: " + ", ".join(cities))
            city = input("City: ").translate(str.maketrans('', '', '\x00'))
        except Exception as e:
            print(f"Something went wrong. ")
    else:
        return city

def validate_priority(priority, user):
    while not re.match("^[123]$", priority):
        try:
            log.addLogEntry(LogEntry(2, user, "[validate-priority] User tried to get logs with a wrong priority."))
            print("Invalid priority, pick either 1, 2 or 3")
            priority = input("Minimum priority: ").translate(str.maketrans('', '', '\x00'))
        except Exception as e:
            print(f"Something went wrong. ")
    else:
        return priority


def validate_username(username, user):
    while not re.match("^[a-z]{1}[a-z0-9\.\-\_\']{4,19}$", username):
        try:
            log.addLogEntry(LogEntry(
                2, user, "[validate-username] User tried to create a user with a wrong username."))
            print("Given username is invalid:\n"
                  + " - The username must be between 5 and 20 characters long\n"
                  + " - Start with letter\n"
                  + " - Contain only letters, numbers and .-_\' characters")
            username = input("Username: ").lower().translate(
                str.maketrans('', '', '\x00'))
        except Exception as e:
            print(f"Something went wrong. ")
    else:
        return username


def validate_password(password, user):
    """
    Password must match:
        - at least 8 characters
        - maximum of 30 characters
        − can contain letters (a-z), (A-Z), numbers (0-9), Special characters such as ~!@#$%^&*_-+=`|\(){}[]:;'<>,.?/.
        − must have a combination of at least one lowercase letter, one uppercase letter, one digit, and one specialcharacter
    """
    while not re.match(
        "^(?=(?:.*[A-Z]){1,})(?=(?:.*[a-z]){1,})(?=(?:.*\d){1,})(?=(?:.*[\~\!\@\#\$\%\^\&\*\_\-\+\=\`\|\\\(\)\{\}\[\]\:\;\'\<\>\,\.\?\/]){1,})([A-Za-z0-9\~\!\@\#\$\%\^\&\*\_\-\+\=\`\|\\\(\)\{\}\[\]\:\;\'\<\>\,\.\?\/]{8,30})$", password
    ):
        try:
            log.addLogEntry(LogEntry(
                2, user, "[validate-password] User tried to create a user with a wrong password."))
            print(
                "Given password is invalid, the password should have: \n"
                + " - at least 8 characters \n"
                + " - a maximum of 30 characters \n"
                + " - can contain letters (a-z), (A-Z), numbers (0-9), Special characters such as ~!@#$%^&*_-+=`|\(){}[]:;'<>,.?/. \n"
                + " - must have a combination of at least one lowercase letter, one uppercase letter, one digit, and one specialcharacter"
            )
            password = input("Password: ").translate(
                str.maketrans('', '', '\x00'))
        except Exception as e:
            print(f"Something has changed. ")
    else:
        return password

# Base class for all users
class User:
    ROLE = None
    COMMANDS = "help,logout,exit,stop"
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
        self.COMMANDS += ",new-user,get-logs"

    def new_user(self, db):
        print("Creating a new System Administrator")
        username = input('Username: ').lower().translate(str.maketrans('', '', '\x00'))
        username = validate_username(username, self.username)

        password = input('Password: ').translate(str.maketrans('', '', '\x00'))
        password = validate_password(password, self.username)

        try:
            log.addLogEntry(LogEntry(3, self.username, f"[new-user] User added with username: {username}"))
            newUser = db.addUser((username, password, "Admin"))
            print(f"Created new user {newUser.username} ({newUser.ROLE})")
        except Exception as e:
            try:
                log.addLogEntry(LogEntry(2, self.username, "[new user] Failed to create user."))
                print('Failed to create user')
            except Exception as ex:
                print(f"Something went wrong. ")

    def get_logs(self, db):
        print("Enter minimum priority of logs to retrieve from 1 to 3 where\n- 1 = important\n- 2 = moderate\n- 3 = info")
        priority = input("Minimum priority: ").translate(str.maketrans('', '', '\x00'))
        priority = validate_priority(priority, self.username)

        try:
            logRows = log.getLogs(priority)
            for entryLog in logRows:
                colour = ["31;40", "33;40", "37;40"]
                print(f"\033[{colour[int(entryLog.priority) - 1]}m{entryLog.time} | {entryLog.user_name } | {entryLog.log_text} \033[0m")
        except Exception as e:
            print("Couldn't retrieve logs (there may be none with the correct priority yet)")

# The system administrator
class Admin(User):
    ROLE = "System Administrator"

    def __init__(self, username):
        User.__init__(self, username)
        self.COMMANDS += ",new-user,add-client"

    def new_user(self, db):
        print("Creating a new Advisor")
        username = input('Username: ').lower().translate(
            str.maketrans('', '', '\x00'))
        username = validate_username(username, self.username)

        password = input('Password: ').translate(str.maketrans('', '', '\x00'))
        password = validate_password(password, self.username)

        try:
            log.addLogEntry(
                LogEntry(3, self.username, f"[new-user] User added with username: {username}"))
            newUser = db.addUser((username, password, "Advisor"))
            print(f"Created new user {newUser.username} ({newUser.ROLE})")
        except Exception as e:
            try:
                log.addLogEntry(LogEntry(2, self.username,
                                         "[new-user] Failed to create user"))
                print('Failed to create user')
            except Exception as ex:
                print(f"Something went wrong. ")

    def add_client(self, db, cities):
        print('Adding a new client')
        fullName = input('Full name: ').translate(
            str.maketrans('', '', '\x00'))

        email = input('Email: ').translate(str.maketrans('', '', '\x00'))
        email = validate_email(email, self.username)

        mobilePhone = input('Mobile phone: ').translate(
            str.maketrans('', '', '\x00'))
        mobilePhone = validate_phone(mobilePhone, self.username)

        streetHouseNumber = input('Street & house number: ').translate(
            str.maketrans('', '', '\x00'))
        streetHouseNumber = validate_streethouse(
            streetHouseNumber, self.username)

        zipcode = input('Zipcode: ').upper().translate(
            str.maketrans('', '', '\x00'))
        zipcode = validate_zipcode(zipcode, self.username)

        print('Available cities: ' + ', '.join(cities))
        city = input('City: ')
        city = validate_city(city, cities, self.username)

        try:
            newClient = db.addClient(
                (fullName, email, mobilePhone, streetHouseNumber, zipcode, city))
            log.addLogEntry(LogEntry(3, self.username,
                                     f"[add-client] Client {fullName} added."))
            print(
                f"Added new client {newClient.fullName} ({newClient.emailAddress})")
        except Exception as e:
            try:
                log.addLogEntry(LogEntry(2, self.username,
                                         "[add-client] Failed to add client."))
                print('Failed to add a new client')
            except Exception as ex:
                print(f"Something went wrong. ")

# The advisor
class Advisor(User):
    ROLE = "Advisor"


class Client:

    def __init__(self, id, fullName, emailAddress, mobilePhone, address):
        self.id = id
        self.fullName = fullName
        self.emailAddress = emailAddress
        self.mobilePhone = mobilePhone
        self.address = address
