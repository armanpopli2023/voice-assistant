import os
from typing import Optional, Dict, Any
from pathlib import Path

def get_settings(env: Optional[str] = None) -> Dict[str, Any]:
    """
    Load settings based on the specified environment.
    
    Args:
        env: Environment name ('development' or 'production'). If None, uses ENV environment variable.
        
    Returns:
        Dictionary containing the settings for the specified environment
    """
    print("Starting get_settings...")
    
    if env is None:
        env = os.getenv('ENV', 'development')
        print(f"Environment not specified, using: {env}")
    
    env = env.lower()
    print(f"Loading settings for environment: {env}")
    
    # Import base settings
    print("Importing base settings...")
    from .base import (
        ROOT_DIR, SAMPLE_RATE, CHANNELS, CHUNK_SIZE, RECORD_SECONDS,
        MEMORY_DIR, MEMORY_FORMAT
    )
    print("Base settings imported successfully")
    
    # Initialize settings with base values
    print("Initializing base settings...")
    settings = {
        'ROOT_DIR': ROOT_DIR,
        'SAMPLE_RATE': SAMPLE_RATE,
        'CHANNELS': CHANNELS,
        'CHUNK_SIZE': CHUNK_SIZE,
        'RECORD_SECONDS': RECORD_SECONDS,
        'MEMORY_DIR': MEMORY_DIR,
        'MEMORY_FORMAT': MEMORY_FORMAT
    }
    print("Base settings initialized")
    
    # Import environment-specific settings
    print("Importing environment-specific settings...")
    if env == 'development':
        print("Loading development settings...")
        from .development import (
            DEBUG, AUDIO_INPUT_DEVICE, AUDIO_OUTPUT_DEVICE,
            WHISPER_MODEL, WHISPER_LANGUAGE, WHISPER_TASK,
            TTS_MODEL, TTS_VOCODER, TTS_SPEAKER, TTS_LANGUAGE,
            OUTPUT_DEVICE
        )
        print("Development settings imported")
        settings.update({
            'DEBUG': DEBUG,
            'AUDIO_INPUT_DEVICE': AUDIO_INPUT_DEVICE,
            'AUDIO_OUTPUT_DEVICE': AUDIO_OUTPUT_DEVICE,
            'WHISPER_MODEL': WHISPER_MODEL,
            'WHISPER_LANGUAGE': WHISPER_LANGUAGE,
            'WHISPER_TASK': WHISPER_TASK,
            'TTS_MODEL': TTS_MODEL,
            'TTS_VOCODER': TTS_VOCODER,
            'TTS_SPEAKER': TTS_SPEAKER,
            'TTS_LANGUAGE': TTS_LANGUAGE,
            'OUTPUT_DEVICE': OUTPUT_DEVICE
        })
        print("Development settings applied")
    elif env == 'production':
        print("Loading production settings...")
        from .production import (
            DEBUG, AUDIO_INPUT_DEVICE, AUDIO_OUTPUT_DEVICE,
            WHISPER_MODEL, WHISPER_LANGUAGE, WHISPER_TASK,
            TTS_MODEL, TTS_VOCODER, TTS_SPEAKER, TTS_LANGUAGE,
            OUTPUT_DEVICE
        )
        print("Production settings imported")
        settings.update({
            'DEBUG': DEBUG,
            'AUDIO_INPUT_DEVICE': AUDIO_INPUT_DEVICE,
            'AUDIO_OUTPUT_DEVICE': AUDIO_OUTPUT_DEVICE,
            'WHISPER_MODEL': WHISPER_MODEL,
            'WHISPER_LANGUAGE': WHISPER_LANGUAGE,
            'WHISPER_TASK': WHISPER_TASK,
            'TTS_MODEL': TTS_MODEL,
            'TTS_VOCODER': TTS_VOCODER,
            'TTS_SPEAKER': TTS_SPEAKER,
            'TTS_LANGUAGE': TTS_LANGUAGE,
            'OUTPUT_DEVICE': OUTPUT_DEVICE
        })
        print("Production settings applied")
    else:
        print(f"Error: Unknown environment: {env}")
        raise ValueError(f"Unknown environment: {env}")
    
    print("Settings loaded successfully")
    print(f"Final settings: {list(settings.keys())}")
    return settings 