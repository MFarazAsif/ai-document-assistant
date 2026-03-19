import sqlite3  # sqlite3 = built into Python, no install needed
import os

# DB_PATH = where the database file will be saved
DB_PATH = "data/assistant.db"

def create_connection():
    # connect() = open or create the database file
    conn = sqlite3.connect(DB_PATH)
    return conn  # return connection object

def create_tables():
    conn = create_connection()
    cursor = conn.cursor()  # cursor = tool to run SQL commands

    # CREATE TABLE = make a new table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY,
            filename TEXT,
            pages INTEGER,
            chunks INTEGER,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY,
            document_id INTEGER,
            question TEXT,
            answer TEXT,
            asked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()   # commit = save changes
    conn.close()    # close = release connection
    print("Tables created")

def save_document(filename, pages, chunks):
    conn = create_connection()
    cursor = conn.cursor()
    # INSERT INTO = add a new row
    cursor.execute("""
        INSERT INTO documents (filename, pages, chunks)
        VALUES (?, ?, ?)
    """, (filename, pages, chunks))  # ? = placeholder, safe from injection
    conn.commit()
    doc_id = cursor.lastrowid  # lastrowid = id of just inserted row
    conn.close()
    return doc_id  # return id so we can link questions to it

def save_question(document_id, question, answer):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO questions (document_id, question, answer)
        VALUES (?, ?, ?)
    """, (document_id, question, answer))
    conn.commit()
    conn.close()

def get_history(document_id):
    conn = create_connection()
    cursor = conn.cursor()
    # SELECT = get rows from table
    cursor.execute("""
        SELECT question, answer, asked_at
        FROM questions
        WHERE document_id = ?
        ORDER BY asked_at DESC
    """, (document_id,))
    rows = cursor.fetchall()  # fetchall = get all results
    conn.close()
    return rows

if __name__ == "__main__":
    create_tables()