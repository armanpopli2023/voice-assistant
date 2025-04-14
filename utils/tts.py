from TTS.api import TTS
from pathlib import Path
from typing import Optional

from config.settings import TTS_MODEL, TTS_SPEAKER

class CoquiTTS:
    def __init__(self, model_name: str = TTS_MODEL, speaker_id: str = TTS_SPEAKER):
        """Initialize Coqui TTS with specified model."""
        try:
            print(f"Initializing TTS with model: {model_name}")
            self.tts = TTS(model_name=model_name)
            self.speaker_id = speaker_id
            print("TTS initialized successfully!")
        except Exception as e:
            print(f"Error initializing TTS: {e}")
            raise

    def synthesize(self, text: str, output_path: str) -> None:
        """Convert text to speech and save to file."""
        try:
            self.tts.tts_to_file(
                text=text,
                file_path=output_path,
                speaker=self.speaker_id
            )
        except Exception as e:
            print(f"Error in TTS synthesis: {e}")
            raise 