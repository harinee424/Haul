import sqlite3

class DB:
    def __init__(self):
        self.connection = sqlite3.connect("haul.db")
        self.cursor = self.connection.cursor() 

        CREATE_TABLE = """
            CREATE TABLE if not exists haul(
                username TEXT not NULL,
                email TEXT not NULL,
                password TEXT not NULL
            );
        """

        self.cursor.execute(CREATE_TABLE)
        self.connection.commit()
        self.connection.close() 
    
    @staticmethod
    def insertValues(username, email, password):
        connection = sqlite3.connect("SQL/haul.db")
        cursor = connection.cursor()
        QUERY = rf"""insert into haul values('{username}', '{email}', '{password}');"""
        cursor.execute(QUERY)
        connection.commit() 
        connection.close()
    
    @staticmethod
    def fetchValues(email, password):
        connection = sqlite3.connect("SQL/haul.db")
        cursor = connection.cursor()
        QUERY = fr"""select * from haul where email='{email}' AND password='{password}';"""
        cursor.execute(QUERY)
        detials =  cursor.fetchall()
        connection.commit() 
        if detials != list():
            return detials
        else:
            return None
    
    @staticmethod
    def listAllDatas():
        connection = sqlite3.connect("haul.db")
        cursor = connection.cursor()
        cursor.execute(r"select * from haul;")
        full_records =  cursor.fetchall()
        connection.commit()
        connection.close()
        return full_records