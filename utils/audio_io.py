import numpy as np
import sounddevice as sd
import wave
from pathlib import Path
from typing import Optional, Union
import webrtcvad
import struct
from config import get_settings

class AudioIO:
    def __init__(self, device_name: Optional[str] = None):
        """
        Initialize the AudioIO class.
        
        Args:
            device_name: Name of the audio device to use. If None, uses default device.
        """
        self.settings = get_settings()
        self.sample_rate = self.settings['SAMPLE_RATE']
        self.channels = self.settings['CHANNELS']
        self.chunk_size = self.settings['CHUNK_SIZE']
        
        # Set up audio device
        if device_name is None:
            device_name = self.settings['AUDIO_INPUT_DEVICE']
        
        self.device_id = self._get_device_id(device_name)
        if self.device_id is None:
            raise ValueError(f"Audio device '{device_name}' not found")
        
        # Initialize VAD
        self.vad = webrtcvad.Vad(3)  # Aggressiveness mode 3 (most aggressive)
        
    def _get_device_id(self, device_name: Optional[str]) -> Optional[int]:
        """Get the device ID for the given device name."""
        devices = sd.query_devices()
        if device_name is None:
            return sd.default.device[0]  # Return default input device
        
        for i, device in enumerate(devices):
            if device['name'] == device_name and device['max_input_channels'] > 0:
                return i
        return None
        
    def record_audio(self, 
                    max_duration: float = 10.0,
                    silence_duration: float = 0.8) -> np.ndarray:
        """
        Record audio with voice activity detection.
        
        Args:
            max_duration: Maximum recording duration in seconds
            silence_duration: Duration of silence to detect end of speech
            
        Returns:
            numpy.ndarray: Recorded audio data
        """
        print(f"Recording audio (max {max_duration}s)...")
        
        # Calculate number of frames
        max_frames = int(max_duration * self.sample_rate)
        silence_frames = int(silence_duration * self.sample_rate)
        
        # Initialize recording buffer
        audio_buffer = []
        silence_counter = 0
        is_speaking = False
        
        def callback(indata, frames, time, status):
            nonlocal silence_counter, is_speaking
            
            if status:
                print(f"Audio input status: {status}")
            
            # Convert to 16-bit PCM for VAD
            pcm_data = (indata * 32767).astype(np.int16).tobytes()
            
            # Check for voice activity
            is_voice = self.vad.is_speech(pcm_data, self.sample_rate)
            
            if is_voice:
                silence_counter = 0
                is_speaking = True
                audio_buffer.append(indata.copy())
            elif is_speaking:
                silence_counter += frames
                if silence_counter >= silence_frames:
                    raise sd.CallbackStop
                audio_buffer.append(indata.copy())
        
        try:
            with sd.InputStream(samplerate=self.sample_rate,
                              channels=self.channels,
                              device=self.device_id,
                              callback=callback,
                              blocksize=self.chunk_size):
                sd.sleep(int(max_duration * 1000))
        except sd.CallbackStop:
            pass
        
        if not audio_buffer:
            raise RuntimeError("No audio recorded")
        
        # Concatenate audio chunks
        audio_data = np.concatenate(audio_buffer)
        print(f"Recording complete. Duration: {len(audio_data) / self.sample_rate:.2f}s")
        return audio_data
        
    def play_audio(self, audio_data: np.ndarray, sample_rate: Optional[int] = None):
        """
        Play audio data.
        
        Args:
            audio_data: Audio data to play
            sample_rate: Sample rate of the audio data. If None, uses default.
        """
        if sample_rate is None:
            sample_rate = self.sample_rate
            
        print("Playing audio...")
        sd.play(audio_data, sample_rate)
        sd.wait()
        print("Playback complete")
        
    def save_audio(self, audio_data: np.ndarray, file_path: Union[str, Path]):
        """
        Save audio data to a WAV file.
        
        Args:
            audio_data: Audio data to save
            file_path: Path to save the audio file
        """
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        print(f"Saving audio to {file_path}...")
        with wave.open(str(file_path), 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(2)  # 16-bit audio
            wf.setframerate(self.sample_rate)
            wf.writeframes(audio_data.tobytes())
        print("Audio saved successfully") 