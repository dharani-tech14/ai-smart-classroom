from modules.voice_guidance import VoiceGuidance

class TextToSpeechConverter:

    def __init__(self):

        self.voice = VoiceGuidance()

    def convert(self, text):

        self.voice.speak(text)

    def set_rate(self, rate):

        self.voice.set_speech_rate(rate)

    def set_volume(self, volume):

        self.voice.set_volume(volume)