import mysql.connector
from mysql.connector import Error

class ConnectDb:
    def __init__(self, host='localhost', user='root', \
                 password='', db='login_system'):

        self.host = host
        self.user = user
        self.password = password
        self.db = db

    def connect(self):
        try:
            self.con = mysql.connector.connect(host=self.host, user=self.user, \
                                               password=self.password, database=self.db)
            self.cur = self.con.cursor()
        except Error as e:
            return e
        

    def disconnect(self):
        self.con.close()
    
    def find_user(self, sql, dados):        
        self.connect()
        self.cur.execute(sql, dados)
        res = self.cur.fetchone()
        self.disconnect()
        return res
        
    
    def add_user(self, sql, dados):
        self.connect()
        self.cur.execute(sql, dados)
        self.con.commit()
        self.disconnect()