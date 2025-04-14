import whisper
from pathlib import Path
from typing import Union

from config.settings import WHISPER_MODEL, LANGUAGE

class Transcriber:
    def __init__(self, model_name: str = WHISPER_MODEL):
        """Initialize Whisper model."""
        print(f"Loading Whisper model: {model_name}")
        self.model = whisper.load_model(model_name)
        print("Whisper model loaded.")

    def transcribe(self, audio_path: Union[str, Path]) -> str:
        """
        Transcribe audio file to text.
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Transcribed text
        """
        result = self.model.transcribe(
            str(audio_path),
            language=LANGUAGE,
            fp16=False  # Use float32 for better compatibility
        )
        return result["text"].strip()

    @staticmethod
    def is_valid_audio_file(file_path: Union[str, Path]) -> bool:
        """Check if file exists and has valid audio extension."""
        file_path = Path(file_path)
        valid_extensions = {".wav", ".mp3", ".m4a", ".ogg"}
        return file_path.exists() and file_path.suffix.lower() in valid_extensions 