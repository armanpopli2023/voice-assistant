from pathlib import Path
from typing import Optional, Union
from TTS.api import TTS

from config.settings import TTS_MODEL

class Speaker:
    def __init__(self, model_name: str = TTS_MODEL):
        """Initialize TTS model."""
        print(f"Loading TTS model: {model_name}")
        self.tts = TTS(model_name=model_name)
        print("TTS model loaded.")

    def speak(self, text: str, output_path: Optional[Union[str, Path]] = None) -> Optional[Path]:
        """
        Convert text to speech and optionally save to file.
        
        Args:
            text: Text to convert to speech
            output_path: Optional path to save audio file
            
        Returns:
            Path to saved audio file if output_path is provided
        """
        if not text:
            return None

        if output_path:
            output_path = Path(output_path)
            self.tts.tts_to_file(text=text, file_path=str(output_path))
            return output_path
        else:
            # For future: could return audio array for direct playback
            temp_path = Path("temp_tts_output.wav")
            self.tts.tts_to_file(text=text, file_path=str(temp_path))
            return temp_path

    @staticmethod
    def list_available_models() -> list:
        """List all available TTS models."""
        return TTS.list_models() 