import database as db
import datetime, sqlite3
from sqlite3 import Error

class LogEntry:
    def __init__(self, priority, user_name, log_text, id=None, time=datetime.datetime.now()):
        self.priority = priority
        self.user_name = user_name
        self.log_text = log_text
        self.time = time
        self.id = id

    def getTuple(self):
        return (self.priority, self.user_name, self.log_text, self.time)


class Logger:
    def addLogEntry(self, logEntry):
        """
        Log entry should be a LogEntry object.
        """
        Database = db.Database()
        conn = Database.create_connection()
        with conn:
            c = conn.cursor()
            sql = ''' INSERT INTO Log (priority, user_name, log_text, time) VALUES (?, ?, ?, ?); '''
            logTuple = logEntry.getTuple()
            try:
                c.execute(sql, logTuple)
                conn.commit()
                return c.lastrowid
            except Error as e:
                raise db.DatabaseException()


    def getLogs(self, priority):
        Database = db.Database()
        conn = Database.create_connection()
        with conn:
            c = conn.cursor()
            sql = ''' SELECT * FROM Log WHERE priority BETWEEN 1 AND ?; '''
            priorityTuple = (priority,)
            try:
                c.execute(sql, priorityTuple)
                rows = c.fetchall()
                responseList = []
                if (len(rows) != 0):
                    for row in rows:
                        responseList.append(LogEntry(row[4], row[2], row[3], id=row[0], time=row[1]))
                    return responseList
                else:
                    raise db.EmptyException()
            except Error as e:
                raise db.DatabaseException()

