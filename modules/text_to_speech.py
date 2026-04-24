import pyttsx3
import os
from config import TTS_RATE, TTS_VOLUME, EXPORTS_DIR

class TextToSpeechEngine:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', TTS_RATE)
        self.engine.setProperty('volume', TTS_VOLUME)
    
    def speak(self, text):
        """Speak text using system TTS"""
        try:
            self.engine.say(text)
            self.engine.runAndWait()
            return True, "Speech completed"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def text_to_audio_file(self, text, filename=None):
        """Convert text to audio file"""
        try:
            if filename is None:
                filename = f"speech_{len(os.listdir(EXPORTS_DIR))}.mp3"
            
            filepath = os.path.join(EXPORTS_DIR, filename)
            self.engine.save_to_file(text, filepath)
            self.engine.runAndWait()
            return filepath, True, "Audio file created"
        except Exception as e:
            return None, False, f"Error: {str(e)}"
    
    def set_voice(self, voice_id=0):
        """Set TTS voice (0=Male, 1=Female if available)"""
        try:
            voices = self.engine.getProperty('voices')
            if voice_id < len(voices):
                self.engine.setProperty('voice', voices[voice_id].id)
            return True
        except:
            return False
    
    def set_speed(self, rate):
        """Adjust speech speed"""
        try:
            self.engine.setProperty('rate', rate)
            return True
        except:
            return False