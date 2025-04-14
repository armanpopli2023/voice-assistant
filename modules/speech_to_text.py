from typing import Dict, Any, Optional
from pathlib import Path
from utils.stt import WhisperSTT
from config.settings import WHISPER_MODEL, WHISPER_LANGUAGE, WHISPER_TASK

class SpeechToText:
    def __init__(self,
                 model_name: str = WHISPER_MODEL,
                 language: str = WHISPER_LANGUAGE,
                 task: str = WHISPER_TASK):
        """
        Initialize the Speech-to-Text module.
        
        Args:
            model_name: Name of the Whisper model to use
            language: Language code for transcription
            task: Task type (transcribe/translate)
        """
        self.stt_engine = WhisperSTT(
            model_name=model_name,
            language=language,
            task=task
        )

    def transcribe(self, audio_path: str) -> Dict[str, Any]:
        """
        Transcribe audio file to text.
        
        Args:
            audio_path: Path to the audio file
            
        Returns:
            Dict containing transcription results with keys:
            - text: The transcribed text
            - language: Detected language
            - segments: List of transcription segments
        """
        if not Path(audio_path).exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
            
        return self.stt_engine.transcribe(audio_path)

    def get_model_info(self) -> Dict[str, str]:
        """
        Get information about the current STT model configuration.
        
        Returns:
            Dict containing model configuration information
        """
        return {
            "model_name": self.stt_engine.model_name,
            "language": self.stt_engine.language,
            "task": self.stt_engine.task
        } 