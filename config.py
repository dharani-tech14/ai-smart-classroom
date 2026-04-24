import os
from dotenv import load_dotenv

load_dotenv()

# App Configuration
APP_NAME = "AI Smart Classroom"
VERSION = "2.0.0"

# Supported Languages
LANGUAGES = {
    "en-IN": "English (India)",
    "ta-IN": "Tamil",
    "hi-IN": "Hindi",
    "te-IN": "Telugu"
}

# Audio Configuration
AUDIO_FORMAT = "wav"
SAMPLE_RATE = 16000
CHUNK_SIZE = 1024

# Database Configuration
DB_PATH = "data/classroom.db"
DB_URL = os.getenv("DATABASE_URL", f"sqlite:///{DB_PATH}")

# NLP Configuration
STOPWORDS = {
    "the", "is", "and", "in", "to", "of", "a", "for", "that", 
    "with", "this", "from", "are", "an", "or", "be", "by", "on"
}

# OCR Configuration
OCR_LANGUAGES = "eng"

# Text-to-Speech Configuration
TTS_RATE = 150
TTS_VOLUME = 0.9

# Paths
DATA_DIR = "data"
UPLOADS_DIR = "data/uploads"
EXPORTS_DIR = "data/exports"

# Ensure directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(UPLOADS_DIR, exist_ok=True)
os.makedirs(EXPORTS_DIR, exist_ok=True)