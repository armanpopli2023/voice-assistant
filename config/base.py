import os
from pathlib import Path

# Project root directory
ROOT_DIR = Path(__file__).parent.parent

# Audio settings
SAMPLE_RATE = 16000  # Sample rate for audio recording
CHANNELS = 1         # Number of audio channels (1 for mono)
CHUNK_SIZE = 1024   # Size of audio chunks for processing
RECORD_SECONDS = 5  # Default recording duration

# Memory settings
MEMORY_DIR = ROOT_DIR / "memory" / "logs"
MEMORY_FORMAT = "json"  # Options: json, sqlite, vector

# Create necessary directories
MEMORY_DIR.mkdir(parents=True, exist_ok=True)

# Environment variables (if needed)
def load_env_vars():
    """Load environment variables from .env file"""
    from dotenv import load_dotenv
    load_dotenv(ROOT_DIR / ".env") 