
import sqlite3
import os

DB_FILE = "mise_digital.db"

if not os.path.exists(DB_FILE):
    print("DB not found")
else:
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Check tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables:", tables)
    
    # Check Usuarios schema
    try:
        cursor.execute("PRAGMA table_info(Usuarios);")
        columns = cursor.fetchall()
        print("Usuarios Schema:", columns)
        
        cursor.execute("SELECT count(*) FROM Usuarios;")
        count = cursor.fetchone()[0]
        print("User Count:", count)
        
        if count > 0:
            cursor.execute("SELECT * FROM Usuarios LIMIT 3;")
            print("Users:", cursor.fetchall())
            
    except Exception as e:
        print("Error checking Usuarios:", e)
        
    conn.close()
