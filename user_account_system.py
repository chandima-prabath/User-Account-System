import hashlib
import sqlite3

class UserAccountSystem:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT UNIQUE,
                            password TEXT)''')
        self.conn.commit()

    def register_user(self, username, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        try:
            self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def authenticate_user(self, username, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        self.cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed_password))
        if self.cursor.fetchone() is not None:
            return True
        else:
            return False

    def delete_user(self, username):
        self.cursor.execute("DELETE FROM users WHERE username=?", (username,))
        self.conn.commit()

    def change_password(self, username, new_password):
        hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
        self.cursor.execute("UPDATE users SET password=? WHERE username=?", (hashed_password, username))
        self.conn.commit()

    def list_users(self):
        self.cursor.execute("SELECT username FROM users")
        return self.cursor.fetchall()
