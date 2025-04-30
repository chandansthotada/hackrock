import sqlite3

def init_db():
    conn = sqlite3.connect('voting_system.db')
    c = conn.cursor()

    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        aadhaar TEXT PRIMARY KEY,
        name TEXT,
        age INTEGER,
        phone TEXT,
        gender TEXT,
        dob TEXT,
        password TEXT
    )
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS votes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        aadhaar TEXT,
        party TEXT,
        time TEXT
    )
    ''')

    conn.commit()
    conn.close()
    print("✅ Database initialized successfully.")

if __name__ == "__main__":
    init_db()
