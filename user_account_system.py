import bcrypt
import sqlite3
from datetime import datetime, timedelta

class UserAccountSystem:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT UNIQUE,
                            password TEXT,
                            password_last_changed TEXT,
                            password_expires_at TEXT,
                            is_2fa_enabled BOOLEAN)''')
        self.conn.commit()

    def register_user(self, username, password):
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        expires_at = (datetime.utcnow() + timedelta(days=90)).strftime('%Y-%m-%d %H:%M:%S')
        try:
            self.cursor.execute("INSERT INTO users (username, password, password_last_changed, password_expires_at, is_2fa_enabled) VALUES (?, ?, ?, ?, ?)", (username, hashed_password, now, expires_at, False))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def authenticate_user(self, username, password):
        self.cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        row = self.cursor.fetchone()
        if row is not None:
            hashed_password = row[2]
            if bcrypt.checkpw(password.encode(), hashed_password):
                return True
        return False

    def delete_user(self, username):
        self.cursor.execute("DELETE FROM users WHERE username=?", (username,))
        self.conn.commit()

    def change_password(self, username, new_password):
        hashed_password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
        now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        expires_at = (datetime.utcnow() + timedelta(days=90)).strftime('%Y-%m-%d %H:%M:%S')
        self.cursor.execute("UPDATE users SET password=?, password_last_changed=?, password_expires_at=? WHERE username=?", (hashed_password, now, expires_at, username))
        self.conn.commit()

    def list_users(self):
        self.cursor.execute("SELECT username FROM users")
        return [row[0] for row in self.cursor.fetchall()]

    def enable_2fa(self, username):
        self.cursor.execute("UPDATE users SET is_2fa_enabled=1 WHERE username=?", (username,))
        self.conn.commit()

    def disable_2fa(self, username):
        self.cursor.execute("UPDATE users SET is_2fa_enabled=0 WHERE username=?", (username,))
        self.conn.commit()

    def is_2fa_enabled(self, username):
        self.cursor.execute("SELECT is_2fa_enabled FROM users WHERE username=?", (username,))
        row = self.cursor.fetchone()
        if row is not None:
            return bool(row[0])
        return False

    def is_password_expired(self, username):
        self.cursor.execute("SELECT password_expires_at FROM users WHERE username=?", (username,))
        row = self.cursor.fetchone()
        if row is not None:
            expires_at = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')
            return datetime.utcnow() > expires_at
        return False

    def is_password_temporary(self, username):
        self.cursor.execute("SELECT password_last_changed FROM users WHERE username=?", (username,))
        row = self.cursor.fetchone()
        if row is not None:
            changed_at = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')
            return (datetime.utcnow() - changed_at) < timedelta(days=7)
        return False