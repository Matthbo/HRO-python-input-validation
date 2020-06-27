import re

def validate_email(email):
    while not re.match("^[\w.+-]+@[\w.-]+\.\w{2,}$", email):
        print("Invalid email address, it should look like 'person@example.com'")
        email = input("Email: ").translate(str.maketrans('', '', '\x00'))
    else:
        return email

def validate_phone(mobilePhone):
    while not re.match("^\+31-6-[\d]{4}-[\d]{4}$", mobilePhone):
        print("Invalid phone number, it should look like '+31-6-0123-4567'")
        mobilePhone = input("Mobile phone: ").translate(str.maketrans('', '', '\x00'))
    else:
        return mobilePhone

def validate_streethouse(streetHouse):
    while not re.match("^[\w ]+ [\d]+[a-z]?$", streetHouse):
        print("Invalid street & house number: it should look like 'Streetname 12'")
        streetHouse = input("Street & house number: ").translate(str.maketrans('', '', '\x00'))
    else:
        return streetHouse

def validate_zipcode(zipcode):
    while not re.match("^\d{4}[A-Z]{2}$", zipcode):
        print("Invalid zipcode: it should look like '1234AB'")
        zipcode = input("Zipcode: ").upper().translate(str.maketrans('', '', '\x00'))
    else:
        return zipcode

def validate_city(city, cities):
    while not city in cities:
        print("Invalid city, choose from: " + ", ".join(cities))
        city = input("City: ").translate(str.maketrans('', '', '\x00'))
    else:
        return city

def validate_username(username):
    while not re.match("^[a-z]{1}[a-z0-9\.\-\_\']{4,19}$", username):
        print("Given username is invalid:\n"
        + " - The username must be between 5 and 20 characters long\n"
        + " - Start with letter\n"
        + " - Contain only letters, numbers and .-_\' characters")
        username = input("Username: ").lower().translate(str.maketrans('', '', '\x00'))
    else:
        return username


def validate_password(password):
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
        print(
            "Given password is invalid, the password should have: \n"
            + " - at least 8 characters \n"
            + " - a maximum of 30 characters \n"
            + " - can contain letters (a-z), (A-Z), numbers (0-9), Special characters such as ~!@#$%^&*_-+=`|\(){}[]:;'<>,.?/. \n" 
            + " - must have a combination of at least one lowercase letter, one uppercase letter, one digit, and one specialcharacter"
        )
        password = input("Password: ").translate(str.maketrans('', '', '\x00'))
    else:
        return password

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
        username = input('Username: ').lower().translate(str.maketrans('', '', '\x00'))
        username = validate_username(username)

        password = input('Password: ').translate(str.maketrans('', '', '\x00'))
        password = validate_password(password)

        newUser = db.addUser((username, password, "Admin"))
        print(f"Created new user {newUser.username} ({newUser.ROLE})")

# The system administrator
class Admin(User):
    ROLE = "System Administrator"

    def __init__(self, username):
        User.__init__(self, username)
        self.COMMANDS += ",new-user,add-client"

    def new_user(self, db):
        print("Creating a new Advisor")
        username = input('Username: ').lower().translate(str.maketrans('', '', '\x00'))
        username = validate_username(username)

        password = input('Password: ').translate(str.maketrans('', '', '\x00'))
        password = validate_password(password)

        newUser = db.addUser((username, password, "Advisor"))
        print(f"Created new user {newUser.username} ({newUser.ROLE})")

    def add_client(self, db, cities):
        print('Adding a new client')
        fullName = input('Full name: ').translate(str.maketrans('', '', '\x00'))
        
        email = input('Email: ').translate(str.maketrans('', '', '\x00'))
        email = validate_email(email)

        mobilePhone = input('Mobile phone: ').translate(str.maketrans('', '', '\x00'))
        mobilePhone = validate_phone(mobilePhone)

        streetHouseNumber = input('Street & house number: ').translate(str.maketrans('', '', '\x00'))
        streetHouseNumber = validate_streethouse(streetHouseNumber)

        zipcode = input('Zipcode: ').upper().translate(str.maketrans('', '', '\x00'))
        zipcode = validate_zipcode(zipcode)

        print('Available cities: ' + ', '.join(cities))
        city = input('City: ')
        city = validate_city(city, cities)

        newClient = db.addClient((fullName, email, mobilePhone, streetHouseNumber, zipcode, city))
        print(f"Added new client {newClient.fullName} ({newClient.emailAddress})")

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
