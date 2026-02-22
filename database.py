import sqlite3

def connect():
    return sqlite3.connect("database.db")

def create_tables():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pomucky (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nazev TEXT NOT NULL,
        typ TEXT NOT NULL,
        stav TEXT NOT NULL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS studenti (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        jmeno TEXT NOT NULL,
        prijmeni TEXT NOT NULL,
        trida TEXT NOT NULL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vypujcky (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pomucka_id INTEGER,
        student_id INTEGER,
        datum_vypujcky TEXT,
        datum_vraceni TEXT,
        FOREIGN KEY (pomucka_id) REFERENCES pomucky(id),
        FOREIGN KEY (student_id) REFERENCES studenti(id)
    )
    """)
    conn.commit()
    conn.close()
