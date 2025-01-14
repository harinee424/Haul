import sqlite3
import db

initialize = db.DB()

connection = sqlite3.connect("haul.db")
cursor = connection.cursor() 

cursor.execute("select * from haul;")
print(cursor.fetchall())