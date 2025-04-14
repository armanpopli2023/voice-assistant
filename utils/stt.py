import whisper
from pathlib import Path
from typing import Dict, Any, Optional

from config.settings import WHISPER_MODEL, WHISPER_LANGUAGE, WHISPER_TASK

class WhisperSTT:
    def __init__(self, 
                 model_name: str = WHISPER_MODEL,
                 language: str = WHISPER_LANGUAGE,
                 task: str = WHISPER_TASK):
        """Initialize Whisper STT with specified model and settings."""
        try:
            print(f"Loading Whisper model: {model_name}")
            self.model = whisper.load_model(model_name)
            self.language = language
            self.task = task
            print("Whisper model loaded successfully!")
        except Exception as e:
            print(f"Error loading Whisper model: {e}")
            raise

    def transcribe(self, audio_path: str) -> Dict[str, Any]:
        """Transcribe audio file to text."""
        try:
            # Verify audio file exists
            if not Path(audio_path).exists():
                raise FileNotFoundError(f"Audio file not found: {audio_path}")

            # Transcribe with Whisper
            result = self.model.transcribe(
                audio_path,
                language=self.language,
                task=self.task,
                fp16=False  # Force CPU mode
            )

            return {
                "text": result["text"].strip(),
                "language": result["language"],
                "segments": result["segments"]
            }

        except Exception as e:
            print(f"Error in transcription: {e}")
            raise 