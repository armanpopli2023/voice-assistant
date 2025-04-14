from .base import *

# Production-specific settings
DEBUG = False

# Audio device settings
AUDIO_INPUT_DEVICE = None  # Use system default
AUDIO_OUTPUT_DEVICE = None  # Use system default

# STT settings
WHISPER_MODEL = "large"  # More accurate model for production
WHISPER_LANGUAGE = "en"
WHISPER_TASK = "transcribe"

# TTS settings
TTS_MODEL = "tts_models/en/vctk/vits"
TTS_VOCODER = "vocoder_models/en/ljspeech/multiband-melgan"
TTS_SPEAKER = "p335"
TTS_LANGUAGE = "en"

# Output device settings
OUTPUT_DEVICE = None  # None uses default audio device 