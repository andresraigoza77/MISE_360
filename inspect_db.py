
import sqlite3

DB_FILE = "mise_digital.db"

def inspect():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    print("Tables:")
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = c.fetchall()
    print(tables)
    
    for t in tables:
        t_name = t[0]
        print(f"\nSchema for {t_name}:")
        c.execute(f"PRAGMA table_info({t_name})")
        cols = c.fetchall()
        for col in cols:
            print(col)
            
    conn.close()

if __name__ == "__main__":
    inspect()
