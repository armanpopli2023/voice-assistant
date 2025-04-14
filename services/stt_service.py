from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from pathlib import Path
import tempfile
import numpy as np
import sounddevice as sd
import wave

from utils.stt import WhisperSTT
from utils.wake_word import WakeWordDetector
from config.settings import (
    WHISPER_MODEL,
    WHISPER_LANGUAGE,
    WHISPER_TASK,
    SAMPLE_RATE
)

app = FastAPI()
stt = WhisperSTT(
    model_name=WHISPER_MODEL,
    language=WHISPER_LANGUAGE,
    task=WHISPER_TASK
)
wake_word = WakeWordDetector()

class AudioRequest(BaseModel):
    audio_data: list
    sample_rate: int

@app.post("/transcribe")
async def transcribe(request: AudioRequest):
    try:
        # Convert audio data to numpy array
        audio_data = np.array(request.audio_data, dtype=np.int16)
        
        # Save to temp file
        temp_dir = tempfile.mkdtemp()
        temp_path = Path(temp_dir) / "input.wav"
        
        with wave.open(str(temp_path), 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(request.sample_rate)
            wf.writeframes(audio_data.tobytes())
        
        # Transcribe
        result = stt.transcribe(str(temp_path))
        
        # Clean up
        temp_path.unlink()
        
        return {
            "success": True,
            "text": result["text"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/detect_wake_word")
async def detect_wake_word(request: AudioRequest):
    try:
        # Convert audio data to numpy array
        audio_data = np.array(request.audio_data, dtype=np.int16)
        
        # Process with wake word detector
        predictions = wake_word.model.predict(audio_data)
        score = predictions["hey_jarvis"]
        
        return {
            "success": True,
            "detected": score > wake_word.confidence_threshold,
            "confidence": float(score)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001) 