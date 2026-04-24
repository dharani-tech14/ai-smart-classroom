import speech_recognition as sr
from config import LANGUAGES
import streamlit as st

class SpeechRecognitionEngine:
    def __init__(self):
        self.recognizer = sr.Recognizer()
    
    def recognize_from_file(self, audio_file, language="en-IN"):
        """Convert audio file to text"""
        try:
            with sr.AudioFile(audio_file) as source:
                audio = self.recognizer.record(source)
            
            text = self.recognizer.recognize_google(audio, language=language)
            return text, True, "Success"
        except sr.UnknownValueError:
            return "", False, "Could not understand audio"
        except sr.RequestError as e:
            return "", False, f"API Error: {str(e)}"
        except Exception as e:
            return "", False, f"Error: {str(e)}"
    
    def recognize_from_microphone(self, language="en-IN", timeout=30):
        """Real-time microphone input"""
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source, timeout=timeout)
            
            text = self.recognizer.recognize_google(audio, language=language)
            return text, True, "Success"
        except sr.UnknownValueError:
            return "", False, "Could not understand audio"
        except sr.RequestError as e:
            return "", False, f"API Error: {str(e)}"
        except Exception as e:
            return "", False, f"Error: {str(e)}"