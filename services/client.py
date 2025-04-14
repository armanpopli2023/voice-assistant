import requests
import numpy as np
import sounddevice as sd
from pathlib import Path
import tempfile
import wave
from datetime import datetime

class VoiceAssistantClient:
    def __init__(self):
        self.stt_url = "http://localhost:8001"
        self.tts_url = "http://localhost:8000"
        self.sample_rate = 16000

    def record_audio(self, duration: float = 5.0):
        """Record audio from microphone."""
        print(f"Recording for {duration} seconds...")
        audio_data = sd.rec(
            int(duration * self.sample_rate),
            samplerate=self.sample_rate,
            channels=1,
            dtype=np.int16
        )
        sd.wait()
        return audio_data

    def play_audio(self, audio_data: np.ndarray, sample_rate: int):
        """Play audio through speakers."""
        sd.play(audio_data, sample_rate)
        sd.wait()

    def detect_wake_word(self, audio_data: np.ndarray) -> bool:
        """Check if wake word is present in audio."""
        response = requests.post(
            f"{self.stt_url}/detect_wake_word",
            json={
                "audio_data": audio_data.tolist(),
                "sample_rate": self.sample_rate
            }
        )
        result = response.json()
        return result["detected"]

    def transcribe(self, audio_data: np.ndarray) -> str:
        """Convert audio to text."""
        response = requests.post(
            f"{self.stt_url}/transcribe",
            json={
                "audio_data": audio_data.tolist(),
                "sample_rate": self.sample_rate
            }
        )
        result = response.json()
        return result["text"]

    def synthesize(self, text: str) -> tuple[np.ndarray, int]:
        """Convert text to speech."""
        response = requests.post(
            f"{self.tts_url}/synthesize",
            json={"text": text}
        )
        result = response.json()
        return np.array(result["audio_data"], dtype=np.int16), result["sample_rate"]

    def run_once(self):
        """Run a single interaction."""
        print("\nWaiting for wake word...")
        
        # Record and check for wake word
        audio_data = self.record_audio()
        if not self.detect_wake_word(audio_data):
            print("No wake word detected. Try again.")
            return
        
        print("Wake word detected! Recording command...")
        
        # Record command
        audio_data = self.record_audio(duration=10.0)
        
        # Transcribe
        text = self.transcribe(audio_data)
        print(f"You said: {text}")
        
        # Generate response (using a simple echo for now)
        response = f"I heard you say: {text}"
        
        # Convert to speech and play
        audio_data, sample_rate = self.synthesize(response)
        self.play_audio(audio_data, sample_rate)

    def run_continuous(self):
        """Run continuously until interrupted."""
        print("\nRunning in continuous mode...")
        print("Press Ctrl+C to stop")
        
        try:
            while True:
                self.run_once()
        except KeyboardInterrupt:
            print("\nStopping voice assistant...")

if __name__ == "__main__":
    client = VoiceAssistantClient()
    client.run_continuous() 