import pyttsx3

class VoiceGuidance:

    def __init__(self):

        self.engine = pyttsx3.init()

        self.engine.setProperty('rate', 150)

        self.engine.setProperty('volume', 1.0)

        self.is_speaking = False

        # Female voice
        voices = self.engine.getProperty('voices')

        for voice in voices:

            name = voice.name.lower()

            if "zira" in name or "female" in name:

                self.engine.setProperty('voice', voice.id)

                break

    def speak(self, text):

        try:

            if self.is_speaking:
                return

            self.is_speaking = True

            self.engine.say(str(text))

            self.engine.runAndWait()

            self.is_speaking = False

        except Exception as e:

            self.is_speaking = False

            print(f"Voice error: {e}")

    def guidance_welcome(self):

        self.speak(
            "Welcome to AI Smart Accessible Learning Dashboard."
        )

    def guidance_action(self, text):

        self.speak(text)

    def set_speech_rate(self, rate):

        self.engine.setProperty('rate', rate)

    def set_volume(self, volume):

        self.engine.setProperty('volume', volume)