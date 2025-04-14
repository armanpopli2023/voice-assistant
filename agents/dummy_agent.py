from datetime import datetime
from typing import Dict, Any

class DummyAgent:
    """A simple agent that returns predefined responses."""
    
    def __init__(self):
        self.responses = {
            "hello": "Hello! I'm your voice assistant.",
            "how are you": "I'm functioning normally, thank you for asking.",
            "time": self._get_time,
            "help": "I'm a simple assistant. Try saying hello or asking for the time.",
        }

    def process(self, text: str) -> str:
        """
        Process input text and return a response.
        
        Args:
            text: Input text from user
            
        Returns:
            Response text
        """
        text = text.lower().strip()
        
        # Check for exact matches first
        if text in self.responses:
            response = self.responses[text]
            if callable(response):
                return response()
            return response
            
        # Check for partial matches
        for key in self.responses:
            if key in text:
                response = self.responses[key]
                if callable(response):
                    return response()
                return response
        
        return "I'm sorry, I don't understand that yet. I'm just a dummy agent for now!"

    def _get_time(self) -> str:
        """Get current time response."""
        return f"The current time is {datetime.now().strftime('%I:%M %p')}"

    def get_state(self) -> Dict[str, Any]:
        """Get agent state for logging/memory."""
        return {
            "agent_type": "dummy",
            "available_commands": list(self.responses.keys())
        } 