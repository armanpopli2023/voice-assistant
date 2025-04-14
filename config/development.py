from .base import *

# Development-specific settings
DEBUG = True

# Audio device settings
AUDIO_INPUT_DEVICE = "MacBook Pro Microphone"
AUDIO_OUTPUT_DEVICE = None  # None means use system default

# STT settings
WHISPER_MODEL = "base"  # Faster model for development
WHISPER_LANGUAGE = "en"
WHISPER_TASK = "transcribe"

# TTS settings
TTS_MODEL = "tts_models/en/vctk/vits"
TTS_VOCODER = "vocoder_models/en/ljspeech/multiband-melgan"
TTS_SPEAKER = "p335"
TTS_LANGUAGE = "en"

# Output device settings
OUTPUT_DEVICE = None  # None uses default audio device 