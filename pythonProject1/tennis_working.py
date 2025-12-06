# Tennis System 
import sqlite3 
 
print("Tennis system started") 
conn = sqlite3.connect("test.db") 
print("Database connected") 
conn.close() 
print("Done") 
