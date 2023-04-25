import sqlite3 as sl

con = sl.connect('my-test.db')

with con:
    con.execute("""
        CREATE TABLE USERS (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        );
    """)

    con.execute("""
        CREATE TABLE BOXES (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            color TEXT,
            objects TEXT,
            boxowner INTEGER,
            FOREIGN KEY (boxowner) REFERENCES USERS(id)
        );
    """)

    con.execute("""
        INSERT INTO USERS (username, password) VALUES ('admin', '1337')
    """)

    con.execute("""
        INSERT INTO BOXES (name, color, object, boxowner)
    """)