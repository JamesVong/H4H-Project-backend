import sqlite3
from werkzeug.security import generate_password_hash


def init_db():
    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()

    with connection:
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY, 
            username TEXT, 
            password TEXT,
            first_name TEXT,
            last_name TEXT,
            email TEXT,
            careers TEXT
            );"""
        )

    # Include our test case
    with connection:
        cursor.execute(
            "REPLACE INTO users (username, password, first_name, last_name, email, careers) VALUES (?, ?, ?, ?, ?, ?)", (
                "HackForHumanity",
                generate_password_hash("HackForHumanity"),
                "John",
                "Smith",
                "John.Smith@scu.edu",
                '["Consulting", "Financial Analyst"]'
            )
        )


init_db()


class User:
    def __init__(self, username, password, first_name, last_name, email, careers):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.careers = careers

    def db_update_career(self):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        with connection:
            cursor.execute('UPDATE users SET careers = ? WHERE username = ?', (self.careers, self.username))

    def db_add_user(self):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        with connection:
            cursor.execute(
                "REPLACE INTO users (username, password, first_name, last_name, email, careers) VALUES (?, ?, ?, ?, ?, ?)",
                (
                    self.username,
                    generate_password_hash(self.password),
                    self.first_name,
                    self.last_name,
                    self.email,
                    self.careers
                )
            )

    @classmethod
    def find_data_by_username(cls, username):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        with connection:
            data = cursor.execute('SELECT * FROM users WHERE username=?', (username,)).fetchone()

        if data:
            return cls(data[1], data[2], data[3], data[4], data[5], data[6])
        return None
