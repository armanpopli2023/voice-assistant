# Voice Assistant

A local-first, modular voice assistant with cloud deployment capabilities.

## 🎯 Project Goals
- Create a privacy-focused voice assistant that runs locally
- Provide modular architecture for easy agent integration
- Support future cloud deployment (AWS Lambda, API Gateway)
- Minimize dependency on external AI services for basic tasks

## 🏗️ Architecture
- Speech-to-Text (STT) using Whisper
- Modular agent system for handling different tasks
- Local Text-to-Speech (TTS) using Coqui/Piper
- Local memory storage with cloud options

## 🚀 Quick Start
1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the assistant:
```bash
python main.py
```

## 📁 Project Structure
```
voice-assistant/
├── main.py                 # Entry point
├── stt/                    # Speech-to-text
│   └── transcriber.py
├── tts/                    # Text-to-speech
│   └── speaker.py
├── agents/                 # Agent modules
│   └── dummy_agent.py
├── memory/                 # Storage/logging
│   └── memory_logger.py
├── config/                 # Configuration
│   └── settings.py
└── utils/                  # Utilities
    └── audio_io.py
```

## 🔄 Pipeline
1. Voice input captured via microphone
2. Speech converted to text using Whisper
3. Text processed by appropriate agent
4. Response converted to speech
5. Audio played back to user

## 🛠️ Future Enhancements
- [ ] Add more specialized agents (Reminders, Spotify, etc.)
- [ ] Implement cloud deployment options
- [ ] Add vector database for long-term memory
- [ ] Integrate with external services (optional) 