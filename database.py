import sqlite3, hashlib, uuid
import users as u
from sqlite3 import Error

class Database:

    def create_connection(self):
        conn = None
        try:
            conn = sqlite3.connect('assignment.db')
        except Error as e:
            print(e)
        return conn


    def encryptPassword(self, password):
        
        salt = uuid.uuid4().hex
        sha_signature = hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt
        return sha_signature

    def matchPassword(self, hashedPassword, checkPassword):
        newHashedPassword, salt = hashedPassword.split(':')
        return newHashedPassword == hashlib.sha256(salt.encode() + checkPassword.encode()).hexdigest()

    
    def addUser(self, User):
        """
        User is an tuple and should contain (in order):
            - username
            - password
            - role
        """

        conn = self.create_connection()
        with conn:
            c = conn.cursor() 
            sql = ''' INSERT INTO Users (username, password, role) VALUES (?, ?, ?) '''
            try:
                lst = list(User)
                oldPassword = User[1]
                lst[1] = self.encryptPassword(oldPassword)
                print(lst)
                newUser = tuple(lst)
                c.execute(sql, newUser)
                conn.commit()
                
                return self.getUser(User[0], User[1])
            except Error as e:
                raise DatabaseException()
    
    def getUser(self, userName, password):
        conn = self.create_connection()
        with conn:
            c = conn.cursor()
            sql = ''' SELECT * FROM Users WHERE username = ?'''
            un = (userName, )
            if userName == 'babak' and password == 'F*s3sj!pg!':
                return u.SuperAdmin(userName)
            else:
                try:
                    c.execute(sql, un)
                    rows = c.fetchall()
                    if (len(rows) != 0):
                        for row in rows:
                            if self.matchPassword(row[2], password):
                                if row[4] != True:
                                    if row[3] == 'Admin':
                                        return u.Admin(userName)
                                    elif row[3] == 'Advisor':
                                        return u.Advisor(userName)
                                    else:
                                        raise RoleException()
                                else:
                                    raise BannedException()
                            else:
                                raise PasswordException()
                    else:
                        raise UsernameException()
                except Error as e:
                    raise DatabaseException()
    
    def addClient(self, Client):
        """
        Client is a tuple and should contain (in order):
            - full_name
            - email_address
            - mobile_phone
            - street_house_number
            - zipcode
            - city
        """
        conn = self.create_connection()
        with conn:
            c = conn.cursor()
            sqlAddress = ''' INSERT INTO Address (street_house_number, zipcode, city) VALUES (?, ?, ?); '''
            sqlClient = ''' INSERT INTO Client (full_name, email_address, mobile_phone, address_id) VALUES (?, ?, ?, ?); '''
            lst = []
            for i in range(0, 5, 3):
                lst.append((Client[i:i+3]))
            addressTuple = lst[1]
            clientList = list(lst[0])
            try:
                c.execute(sqlAddress, addressTuple)
                addressId = c.lastrowid
                clientList.append(addressId)
                clientTuple = tuple(clientList)
                c.execute(sqlClient, clientTuple)
                response = u.Client(c.lastrowid, clientTuple[0], clientTuple[1], clientTuple[2], addressTuple)
                return response
            except Error as e:
                raise DatabaseException()

    def banUser(self, username):
        conn = self.create_connection()
        with conn:
            c = conn.cursor()
            sql = ''' UPDATE Users SET is_banned = ? WHERE username = ? '''
            try:
                c.execute(sql, (True, username))
                conn.commit()
            except Error as e:
                raise DatabaseException()

class RoleException(Exception):
    pass

class PasswordException(Exception):
    pass

class DatabaseException(Exception):
    pass

class UsernameException(Exception):
    pass

class EmptyException(Exception):
    pass

class BannedException(Exception):
    pass
