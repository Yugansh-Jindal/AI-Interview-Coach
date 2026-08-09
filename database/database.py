import json
import sqlite3
from contextlib import closing

DATABASE_NAME = "interview_coach.db"


def get_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row

    # Enable SQLite foreign keys
    conn.execute("PRAGMA foreign_keys = ON")

    return conn


def initialize_database():
    """
    Creates every table required by the application.

    Safe to call multiple times.
    """

    with closing(get_connection()) as conn:

        cursor = conn.cursor()

        # ----------------------------
        # Users
        # ----------------------------
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

    # ----------------------------
    # Safe Migration
    # ----------------------------

        try:
          cursor.execute("""
          ALTER TABLE users
          ADD COLUMN resume_path TEXT
        """)
        except sqlite3.OperationalError:
            pass

        try:
            cursor.execute("""
        ALTER TABLE users
        ADD COLUMN job_description_path TEXT
        """)
        except sqlite3.OperationalError:
            pass

        # ----------------------------
        # Interviews
        # ----------------------------
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS interviews(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            created_at TEXT DEFAULT (datetime('now','localtime')),

            overall_score REAL,

            resume_skills TEXT,

            job_skills TEXT,

            interview_plan TEXT,

            covered_topics TEXT,

            FOREIGN KEY(user_id)
            REFERENCES users(id)
            ON DELETE CASCADE

        )
        """)

        # ----------------------------
        # Interview Details
        # ----------------------------
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS interview_details(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            interview_id INTEGER NOT NULL,

            question_number INTEGER,

            topic TEXT,

            question TEXT,

            answer TEXT,

            score REAL,

            strengths TEXT,

            weaknesses TEXT,

            suggestions TEXT,

            raw_feedback TEXT,

            FOREIGN KEY(interview_id)
            REFERENCES interviews(id)
            ON DELETE CASCADE

        )
        """)

        conn.commit()


# -------------------------------------------------------
# Save Interview
# -------------------------------------------------------

def save_interview(session, user_id):

    with closing(get_connection()) as conn:

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO interviews(

                user_id,

                overall_score,

                resume_skills,

                job_skills,

                interview_plan,

                covered_topics

            )

            VALUES(?,?,?,?,?,?)
            """,
            (
                user_id,

                session.overall_score,

                json.dumps(session.resume_skills),

                json.dumps(session.job_skills),

                json.dumps(session.interview_plan),

                json.dumps(session.covered_topics),
            ),
        )

        interview_id = cursor.lastrowid
        for index, question in enumerate(session.questions):

            answer = ""

            if index < len(session.answers):
                answer = session.answers[index]

            feedback = {}

            if index < len(session.feedback):
                feedback = session.feedback[index]

            topic = ""

            if index < len(session.covered_topics):
                topic = session.covered_topics[index]

            cursor.execute(
                """
                INSERT INTO interview_details(

                    interview_id,

                    question_number,

                    topic,

                    question,

                    answer,

                    score,

                    strengths,

                    weaknesses,

                    suggestions,

                    raw_feedback

                )

                VALUES(?,?,?,?,?,?,?,?,?,?)
                """,
                (
                    interview_id,

                    index + 1,

                    topic,

                    question,

                    answer,

                    feedback.get("score", 0),

                    json.dumps(
                        feedback.get("strengths", [])
                    ),

                    json.dumps(
                        feedback.get("weaknesses", [])
                    ),

                    json.dumps(
                        feedback.get("suggestions", [])
                    ),

                    feedback.get("raw", ""),
                ),
            )

        conn.commit()

        return interview_id


# -------------------------------------------------------
# Interview History
# -------------------------------------------------------

def get_user_interview(interview_id, user_id):

    with closing(get_connection()) as conn:

        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM interviews
            WHERE id=?
            AND user_id=?
            """,
            (interview_id, user_id),
        )

        interview = cursor.fetchone()

        if interview is None:
            return None

        cursor.execute(
            """
            SELECT *
            FROM interview_details
            WHERE interview_id=?
            ORDER BY question_number
            """,
            (interview_id,),
        )

        details = cursor.fetchall()

        return {
            "interview": dict(interview),
            "details": [dict(row) for row in details]
        }

# -------------------------------------------------------
# Interview Summary
# -------------------------------------------------------

def get_interviews(user_id):

    with closing(get_connection()) as conn:

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                id,
                created_at,
                overall_score
            FROM interviews
            WHERE user_id=?
            ORDER BY created_at DESC
            """,
            (user_id,),
        )

        return [dict(row) for row in cursor.fetchall()]

def get_previous_questions(user_id):

    with closing(get_connection()) as conn:

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT d.question

            FROM interview_details d

            JOIN interviews i
            ON d.interview_id = i.id

            WHERE i.user_id=?
            """,
            (user_id,),
        )

        return [row[0] for row in cursor.fetchall()]


# -------------------------------------------------------
# Delete Interview
# -------------------------------------------------------

def delete_interview(interview_id, user_id):

    with closing(get_connection()) as conn:

        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM interviews

            WHERE id=?
            AND user_id=?
            """,
            (
                interview_id,
                user_id,
            ),
        )

        conn.commit()


# -------------------------------------------------------
# Delete All Interviews For User
# -------------------------------------------------------

def delete_all_interviews(user_id):

    with closing(get_connection()) as conn:

        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM interviews

            WHERE user_id=?
            """,
            (user_id,),
        )

        conn.commit()


# -------------------------------------------------------
# Statistics
# -------------------------------------------------------

def get_average_score(user_id):

    with closing(get_connection()) as conn:

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT AVG(overall_score)

            FROM interviews

            WHERE user_id=?
            """,
            (user_id,),
        )

        score = cursor.fetchone()[0]

        if score is None:
            return 0

        return round(score, 2)

# -------------------------------------------------------
# Analytics
# -------------------------------------------------------

def get_total_interviews(user_id):

    with closing(get_connection()) as conn:

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM interviews
            WHERE user_id=?
            """,
            (user_id,),
        )

        return cursor.fetchone()[0]

    
def get_best_score(user_id):

    with closing(get_connection()) as conn:

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT MAX(overall_score)
            FROM interviews
            WHERE user_id=?
            """,
            (user_id,),
        )

        score = cursor.fetchone()[0]

        if score is None:
            return 0

        return round(score, 2)

def get_total_questions(user_id):

    with closing(get_connection()) as conn:

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)

            FROM interview_details d

            JOIN interviews i
            ON d.interview_id = i.id

            WHERE i.user_id=?
            """,
            (user_id,),
        )

        return cursor.fetchone()[0]

def get_score_history(user_id):

    with closing(get_connection()) as conn:

        cursor = conn.cursor()

        cursor.execute(
        """
        SELECT
            id,
            overall_score

        FROM interviews

        WHERE user_id=?

        ORDER BY created_at
        """,
        (user_id,),
    )

        return [dict(row) for row in cursor.fetchall()]

def get_topic_performance(user_id):

    with closing(get_connection()) as conn:

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                d.topic,
                ROUND(AVG(d.score), 2) AS average_score

            FROM interview_details d

            JOIN interviews i
            ON d.interview_id = i.id

            WHERE i.user_id=?

            GROUP BY d.topic

            ORDER BY average_score DESC
            """,
            (user_id,),
        )

        return [dict(row) for row in cursor.fetchall()]

# -------------------------------------------------------
# Initialize Automatically
# -------------------------------------------------------

initialize_database()

