import sys
import os
from pathlib import Path
import tempfile
from typing import Optional, Dict, Any
import numpy as np
from datetime import datetime
import wave

print("Starting main.py...")

# Add project root to Python path
project_root = Path(__file__).parent.absolute()
sys.path.append(str(project_root))
print(f"Project root: {project_root}")

from utils.audio_io import AudioIO
from utils.stt import WhisperSTT
from utils.tts import CoquiTTS
from utils.wake_word import WakeWordDetector
from agents.dummy_agent import DummyAgent
from config import get_settings

class VoiceAssistant:
    def __init__(self, env: Optional[str] = None):
        """
        Initialize the voice assistant with all necessary components.
        
        Args:
            env: Environment name ('development' or 'production'). If None, uses ENV environment variable.
        """
        print("\nInitializing Voice Assistant...")
        print(f"Environment: {env}")
        
        # Load settings for the specified environment
        print("Loading settings...")
        self.settings = get_settings(env)
        print("Settings loaded successfully")
        
        # Initialize components
        print("Initializing audio I/O...")
        self.audio_io = AudioIO(device_name=self.settings['AUDIO_INPUT_DEVICE'])
        print("Audio I/O initialized")
        
        print("Initializing wake word detector...")
        self.wake_word = WakeWordDetector()
        print("Wake word detector initialized")
        
        print("Initializing STT...")
        self.stt = WhisperSTT(
            model_name=self.settings['WHISPER_MODEL'],
            language=self.settings['WHISPER_LANGUAGE'],
            task=self.settings['WHISPER_TASK']
        )
        print("STT initialized")
        
        print("Initializing TTS...")
        self.tts = CoquiTTS(
            model_name=self.settings['TTS_MODEL'],
            speaker_id=self.settings['TTS_SPEAKER']
        )
        print("TTS initialized")
        
        print("Initializing agent...")
        self.agent = DummyAgent()
        print("Agent initialized")
        
        # Create temp directory for audio files
        print("Creating temporary directory...")
        self.temp_dir = tempfile.mkdtemp()
        print(f"Temporary directory created at: {self.temp_dir}")

    def process_audio(self, audio_data: np.ndarray) -> Dict[str, Any]:
        """Process audio data through the entire pipeline."""
        try:
            # 1. Save audio to temporary file
            print("\n2. Saving audio to temporary file...")
            temp_audio_path = Path(self.temp_dir) / f"temp_audio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
            self.audio_io.save_audio(audio_data, temp_audio_path)
            print(f"   Saved to: {temp_audio_path}")

            # 2. Transcribe audio
            print("3. Transcribing audio...")
            transcription = self.stt.transcribe(str(temp_audio_path))
            print(f"   You said: {transcription['text']}")

            # 3. Process with agent
            print("4. Processing with agent...")
            response = self.agent.process(transcription['text'])
            print(f"   Assistant response: {response}")

            # 4. Convert response to speech
            print("5. Converting response to speech...")
            temp_tts_path = Path(self.temp_dir) / f"temp_tts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
            self.tts.synthesize(response, str(temp_tts_path))
            print(f"   Generated audio at: {temp_tts_path}")

            # 5. Play response
            print("6. Playing response...")
            with wave.open(str(temp_tts_path), 'rb') as wf:
                audio_data = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16)
                self.audio_io.play_audio(audio_data, wf.getframerate())

            # 6. Clean up
            print("7. Cleaning up temporary files...")
            temp_audio_path.unlink()
            temp_tts_path.unlink()

            return {
                "transcription": transcription,
                "response": response,
                "success": True
            }

        except Exception as e:
            print(f"Error in processing pipeline: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def run_once(self):
        """Run a single iteration of the voice assistant."""
        print("\nRunning single test iteration...")
        
        try:
            # Start wake word detection
            print("Starting wake word detection...")
            self.wake_word.start_listening()
            print("Say 'Jarvis' to start...")
            
            # Wait for wake word
            print("Waiting for wake word...")
            if not self.wake_word.wait_for_wake_word(timeout=30):
                print("No wake word detected. Try again.")
                return
            
            # Stop wake word detection
            print("Wake word detected, stopping detection...")
            self.wake_word.stop_listening()
            
            # Record command with VAD
            print("\n1. Recording command...")
            audio_data = self.audio_io.record_audio(
                max_duration=10.0,
                silence_duration=0.8
            )
            print("Command recorded successfully")
            
            # Process the audio through the pipeline
            print("Processing audio...")
            result = self.process_audio(audio_data)
            
            if result["success"]:
                print("\nCommand processed successfully!")
            else:
                print("\nCommand processing failed. Check the error message above.")

        except Exception as e:
            print(f"\nError during test: {e}")

    def run_continuous(self):
        """Run the voice assistant continuously."""
        print("\nRunning in continuous mode...")
        print("Press Ctrl+C to stop")
        
        try:
            while True:
                self.run_once()
        except KeyboardInterrupt:
            print("\nStopping voice assistant...")
            self.wake_word.stop_listening()

if __name__ == "__main__":
    print("Starting voice assistant...")
    # Get environment from command line or use default
    env = sys.argv[1] if len(sys.argv) > 1 else None
    print(f"Using environment: {env}")
    
    assistant = VoiceAssistant(env=env)
    assistant.run_continuous()  # Run in continuous mode by default 