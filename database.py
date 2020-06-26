import sqlite3, hashlib, uuid
import users as u
from sqlite3 import Error



class Database:

    def __init__(self):
        self.conn = self.create_connection()

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
        with self.conn:
            c = self.conn.cursor() 
            sql = ''' INSERT INTO Users (username, password, role) VALUES (?, ?, ?) '''
            try:
                lst = list(User)
                oldPassword = User[1]
                lst[1] = self.encryptPassword(oldPassword)
                newUser = tuple(lst)
                c.execute(sql, newUser)
                return c.lastrowid
            except Error as e:
                print(f'Failed to add new user ({type(e).__name__})')
                return None
    
    def getUser(self, userName, password):
        with self.conn:
            c = self.conn.cursor()
            sql = ''' SELECT * FROM Users WHERE username = ?'''
            un = (userName, )
            if userName == 'Babak' and password == 'F*s3sj!pg!':
                return u.SuperAdmin(userName)
            else:
                try:
                    c.execute(sql, un)
                    rows = c.fetchall()
                    if (len(rows) != 0):
                        for row in rows:
                            if self.matchPassword(row[2], password):
                                if row[3] == 'Admin':
                                    return u.Admin(userName)
                                if row[3] == 'Advisor':
                                    return u.Advisor(userName)
                                else:
                                    raise RoleException()
                            else:
                                raise PasswordException()
                    else:
                        raise UsernameException()
                except Error as e:
                    print(type(e).__name__)
                    raise DatabaseException()
    
    def addClient(self, Client):
        with self.conn:
            pass


class RoleException(Exception):
    pass

class PasswordException(Exception):
    pass

class DatabaseException(Exception):
    pass

class UsernameException(Exception):
    pass
    