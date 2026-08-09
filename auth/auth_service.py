import sqlite3

from auth.password_utils import (
    hash_password,
    verify_password
)

DATABASE = "interview_coach.db"


class AuthService:

    def __init__(self):
        self.initialize()

    def get_connection(self):
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def initialize(self):

        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT NOT NULL,

        email TEXT UNIQUE NOT NULL,

        password TEXT NOT NULL,

        resume_path TEXT,

        job_description_path TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

        conn.commit()
        conn.close()

    def register_user(
        self,
        name,
        email,
        password
    ):

        conn = self.get_connection()
        cursor = conn.cursor()

        try:

            cursor.execute(
                """
                INSERT INTO users(
                    name,
                    email,
                    password
                )
                VALUES(?,?,?)
                """,
                (
                    name,
                    email,
                    hash_password(password)
                )
            )

            conn.commit()

            return True

        except sqlite3.IntegrityError:

            return False

        finally:

            conn.close()

    def login_user(
        self,
        email,
        password
    ):

        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *

            FROM users

            WHERE email=?
            """,
            (email,)
        )

        user = cursor.fetchone()

        conn.close()

        if user is None:
            return None

        if verify_password(
            password,
            user["password"]
        ):
            return dict(user)

        return None


auth_service = AuthService()