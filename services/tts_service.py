from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from pathlib import Path
import tempfile
import numpy as np
import sounddevice as sd
import wave

from utils.tts import CoquiTTS
from config.settings import TTS_MODEL, TTS_SPEAKER

app = FastAPI()
tts = CoquiTTS(model_name=TTS_MODEL, speaker_id=TTS_SPEAKER)

class TTSRequest(BaseModel):
    text: str

@app.post("/synthesize")
async def synthesize(request: TTSRequest):
    try:
        # Create temp file for audio
        temp_dir = tempfile.mkdtemp()
        temp_path = Path(temp_dir) / "output.wav"
        
        # Generate speech
        tts.synthesize(request.text, str(temp_path))
        
        # Read the generated audio
        with wave.open(str(temp_path), 'rb') as wf:
            audio_data = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16)
            sample_rate = wf.getframerate()
        
        # Clean up
        temp_path.unlink()
        
        return {
            "success": True,
            "audio_data": audio_data.tolist(),
            "sample_rate": sample_rate
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 