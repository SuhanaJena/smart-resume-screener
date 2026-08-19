import sqlite3


DATABASE_NAME = "resume_screener.db"


# ==========================================
# DATABASE CONNECTION
# ==========================================

def get_connection():
    return sqlite3.connect(DATABASE_NAME)


# ==========================================
# CREATE TABLE
# ==========================================

def create_table():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS candidates (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            candidate_name TEXT,

            filename TEXT UNIQUE,

            match_score INTEGER,

            candidate_summary TEXT,

            matching_skills TEXT,

            missing_skills TEXT,

            education TEXT,

            experience TEXT,

            strengths TEXT,

            recommendations TEXT,

            justification TEXT

        )
        """
    )

    connection.commit()
    connection.close()


# ==========================================
# SAVE / UPDATE CANDIDATE
# ==========================================

def save_candidate(candidate):

    connection = get_connection()
    cursor = connection.cursor()

    # Check whether this resume already exists
    cursor.execute(
        """
        SELECT id
        FROM candidates
        WHERE filename = ?
        """,
        (
            candidate.get("filename"),
        )
    )

    existing_candidate = cursor.fetchone()

    # ======================================
    # UPDATE EXISTING CANDIDATE
    # ======================================

    if existing_candidate:

        cursor.execute(
            """
            UPDATE candidates

            SET
                candidate_name = ?,
                match_score = ?,
                candidate_summary = ?,
                matching_skills = ?,
                missing_skills = ?,
                education = ?,
                experience = ?,
                strengths = ?,
                recommendations = ?,
                justification = ?

            WHERE filename = ?
            """,

            (
                candidate.get("candidate_name"),

                candidate.get("match_score"),

                candidate.get("candidate_summary"),

                ", ".join(
                    candidate.get(
                        "matching_skills",
                        []
                    )
                ),

                ", ".join(
                    candidate.get(
                        "missing_skills",
                        []
                    )
                ),

                ", ".join(
                    candidate.get(
                        "education",
                        []
                    )
                ),

                ", ".join(
                    candidate.get(
                        "experience",
                        []
                    )
                ),

                ", ".join(
                    candidate.get(
                        "strengths",
                        []
                    )
                ),

                ", ".join(
                    candidate.get(
                        "recommendations",
                        []
                    )
                ),

                candidate.get(
                    "justification"
                ),

                candidate.get(
                    "filename"
                )
            )
        )

    # ======================================
    # INSERT NEW CANDIDATE
    # ======================================

    else:

        cursor.execute(
            """
            INSERT INTO candidates (

                candidate_name,

                filename,

                match_score,

                candidate_summary,

                matching_skills,

                missing_skills,

                education,

                experience,

                strengths,

                recommendations,

                justification

            )

            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,

            (
                candidate.get(
                    "candidate_name"
                ),

                candidate.get(
                    "filename"
                ),

                candidate.get(
                    "match_score"
                ),

                candidate.get(
                    "candidate_summary"
                ),

                ", ".join(
                    candidate.get(
                        "matching_skills",
                        []
                    )
                ),

                ", ".join(
                    candidate.get(
                        "missing_skills",
                        []
                    )
                ),

                ", ".join(
                    candidate.get(
                        "education",
                        []
                    )
                ),

                ", ".join(
                    candidate.get(
                        "experience",
                        []
                    )
                ),

                ", ".join(
                    candidate.get(
                        "strengths",
                        []
                    )
                ),

                ", ".join(
                    candidate.get(
                        "recommendations",
                        []
                    )
                ),

                candidate.get(
                    "justification"
                )
            )
        )

    connection.commit()
    connection.close()


# ==========================================
# GET ALL CANDIDATES
# ==========================================

def get_all_candidates():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT

            id,

            candidate_name,

            filename,

            match_score,

            candidate_summary,

            matching_skills,

            missing_skills,

            education,

            experience,

            strengths,

            recommendations,

            justification

        FROM candidates

        ORDER BY match_score DESC
        """
    )

    candidates = cursor.fetchall()

    connection.close()

    return candidates


# ==========================================
# CLEAR ALL CANDIDATES
# ==========================================

def clear_candidates():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM candidates"
    )

    connection.commit()
    connection.close()
