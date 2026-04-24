import sqlite3
import json
from datetime import datetime
from config import DB_PATH, DATA_DIR
import os

os.makedirs(DATA_DIR, exist_ok=True)

class DatabaseManager:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.init_db()
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def init_db(self):
        """Initialize database with required tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE,
                disability_type TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                lecture_title TEXT,
                subject TEXT,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                duration INTEGER,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # Transcripts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transcripts (
                id INTEGER PRIMARY KEY,
                session_id INTEGER,
                full_text TEXT,
                keywords TEXT,
                summary TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES sessions(id)
            )
        ''')
        
        # Notes table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY,
                session_id INTEGER,
                note_text TEXT,
                highlights TEXT,
                timestamp TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES sessions(id)
            )
        ''')
        
        # OCR Records table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ocr_records (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                image_name TEXT,
                extracted_text TEXT,
                confidence REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_user(self, name, email, disability_type):
        """Add a new user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                'INSERT INTO users (name, email, disability_type) VALUES (?, ?, ?)',
                (name, email, disability_type)
            )
            conn.commit()
            user_id = cursor.lastrowid
            return user_id
        except sqlite3.IntegrityError:
            return None
        finally:
            conn.close()
    
    def create_session(self, user_id, lecture_title, subject):
        """Create a new lecture session"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO sessions (user_id, lecture_title, subject) VALUES (?, ?, ?)',
            (user_id, lecture_title, subject)
        )
        conn.commit()
        session_id = cursor.lastrowid
        conn.close()
        return session_id
    
    def save_transcript(self, session_id, full_text, keywords, summary):
        """Save transcript for a session"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''INSERT INTO transcripts (session_id, full_text, keywords, summary) 
               VALUES (?, ?, ?, ?)''',
            (session_id, full_text, json.dumps(keywords), summary)
        )
        conn.commit()
        conn.close()
    
    def save_notes(self, session_id, note_text, highlights, timestamp):
        """Save notes for a session"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''INSERT INTO notes (session_id, note_text, highlights, timestamp) 
               VALUES (?, ?, ?, ?)''',
            (session_id, note_text, json.dumps(highlights), timestamp)
        )
        conn.commit()
        conn.close()
    
    def save_ocr_record(self, user_id, image_name, extracted_text, confidence):
        """Save OCR extraction record"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''INSERT INTO ocr_records (user_id, image_name, extracted_text, confidence) 
               VALUES (?, ?, ?, ?)''',
            (user_id, image_name, extracted_text, confidence)
        )
        conn.commit()
        conn.close()
    
    def get_user_sessions(self, user_id):
        """Get all sessions for a user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM sessions WHERE user_id = ? ORDER BY date DESC',
            (user_id,)
        )
        sessions = cursor.fetchall()
        conn.close()
        return sessions
    
    def get_session_transcript(self, session_id):
        """Get transcript for a session"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM transcripts WHERE session_id = ?', (session_id,))
        transcript = cursor.fetchone()
        conn.close()
        return transcript