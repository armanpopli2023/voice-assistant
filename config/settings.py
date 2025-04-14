import os
from pathlib import Path

# Project root directory
ROOT_DIR = Path(__file__).parent.parent

# Audio settings
SAMPLE_RATE = 16000  # Sample rate for audio recording
CHANNELS = 1         # Number of audio channels (1 for mono)
CHUNK_SIZE = 1024   # Size of audio chunks for processing
RECORD_SECONDS = 5  # Default recording duration

# Audio device settings
# Set to None to use system default, or specify a device name to use that device
# Example: "MacBook Pro Microphone" or "Arman's iPhone Microphone"
AUDIO_INPUT_DEVICE = "MacBook Pro Microphone"
AUDIO_OUTPUT_DEVICE = None  # None means use system default

# STT settings
WHISPER_MODEL = "base"  # Options: "tiny", "base", "small", "medium", "large"
                        # Smaller models are faster but less accurate
WHISPER_LANGUAGE = "en"  # Language code for transcription
WHISPER_TASK = "transcribe"  # "transcribe" or "translate"

# TTS settings
TTS_MODEL = "tts_models/en/vctk/vits"  # Higher quality multi-speaker model
TTS_VOCODER = "vocoder_models/en/ljspeech/multiband-melgan"  # Better voice quality
TTS_SPEAKER = "p335"  # VCTK speaker ID for more natural voice
TTS_LANGUAGE = "en"  # Language code for TTS

# Output device settings
OUTPUT_DEVICE = None  # None uses default audio device

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