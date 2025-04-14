import openwakeword
import numpy as np
import sounddevice as sd
import webrtcvad
from typing import Optional, Tuple, List
import threading
import queue
import time
import wave
import io

class WakeWordDetector:
    def __init__(self, 
                 wake_word: str = "jarvis",
                 sample_rate: int = 16000,
                 chunk_duration_ms: int = 30,
                 vad_mode: int = 3,
                 confidence_threshold: float = 0.5):
        """Initialize wake word detector with voice activity detection.
        
        Args:
            wake_word: Wake word to detect (default: "jarvis")
            sample_rate: Audio sample rate (default: 16000)
            chunk_duration_ms: Duration of each audio chunk in ms (default: 30)
            vad_mode: VAD aggressiveness mode, 0-3 (default: 3, most aggressive)
            confidence_threshold: Confidence threshold for wake word detection (default: 0.5)
        """
        # Initialize wake word model
        self.model = openwakeword.Model(wakeword_models=["hey_jarvis"])
        self.wake_word = "hey_jarvis"
        self.confidence_threshold = confidence_threshold
        
        # Audio settings
        self.sample_rate = sample_rate
        self.chunk_duration_ms = chunk_duration_ms
        self.chunk_size = int(sample_rate * chunk_duration_ms / 1000)
        
        # Initialize VAD
        self.vad = webrtcvad.Vad(vad_mode)
        
        # Buffers for audio processing
        self.audio_queue = queue.Queue()
        self.is_listening = False
        self.detected_wake_word = False
        
        # Thread for continuous processing
        self.processing_thread = None
        
        # Generate beep sound for feedback
        self.beep_sound = self._generate_beep()

    def _generate_beep(self, frequency: int = 800, duration: float = 0.1) -> np.ndarray:
        """Generate a simple beep sound."""
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        beep = np.sin(2 * np.pi * frequency * t) * 0.3  # 0.3 is volume
        return beep.astype(np.float32)

    def play_beep(self) -> None:
        """Play the beep sound."""
        sd.play(self.beep_sound, self.sample_rate)
        sd.wait()

    def start_listening(self) -> None:
        """Start listening for wake word in background."""
        if self.processing_thread is not None:
            return
            
        self.is_listening = True
        self.detected_wake_word = False
        
        def audio_callback(indata, frames, time, status):
            """Callback for audio stream to process chunks."""
            if status:
                print(f"Audio callback status: {status}")
            if self.is_listening:
                # Convert to int16 for VAD
                audio_chunk = (indata * 32767).astype(np.int16)
                self.audio_queue.put(audio_chunk)

        def process_audio():
            """Process audio chunks in background thread."""
            try:
                with sd.InputStream(
                    samplerate=self.sample_rate,
                    channels=1,
                    dtype=np.float32,
                    blocksize=self.chunk_size,
                    callback=audio_callback
                ):
                    print("Waiting to hear my name...")
                    
                    while self.is_listening:
                        if not self.audio_queue.empty():
                            audio_chunk = self.audio_queue.get()
                            
                            # Check for voice activity
                            is_speech = self.vad.is_speech(
                                audio_chunk.tobytes(),
                                self.sample_rate
                            )
                            
                            if is_speech:
                                # Process with wake word detector
                                predictions = self.model.predict(audio_chunk)
                                score = predictions[self.wake_word]
                                
                                if score > self.confidence_threshold:
                                    print(f"Yes! I heard you! (confidence: {score:.2f})")
                                    self.play_beep()  # Play feedback sound
                                    self.detected_wake_word = True
                                    break
                            
                        time.sleep(0.01)  # Prevent busy waiting
                        
            except Exception as e:
                print(f"Error in audio processing: {e}")
                self.stop_listening()

        self.processing_thread = threading.Thread(target=process_audio)
        self.processing_thread.start()

    def stop_listening(self) -> None:
        """Stop listening for wake word."""
        self.is_listening = False
        if self.processing_thread is not None:
            self.processing_thread.join()
            self.processing_thread = None
        
        # Clear audio queue
        while not self.audio_queue.empty():
            self.audio_queue.get()

    def wait_for_wake_word(self, timeout: Optional[float] = None) -> bool:
        """Wait for wake word to be detected.
        
        Args:
            timeout: Maximum time to wait in seconds (None for no timeout)
            
        Returns:
            True if wake word was detected, False if timeout occurred
        """
        start_time = time.time()
        
        while not self.detected_wake_word:
            if timeout is not None and time.time() - start_time > timeout:
                return False
            time.sleep(0.1)
            
        return True 