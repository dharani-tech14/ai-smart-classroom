import speech_recognition as sr

class SpeechRecognizer:

    def recognize_from_microphone(self):

        recognizer = sr.Recognizer()

        try:
            with sr.Microphone() as source:

                print("Listening...")

                recognizer.adjust_for_ambient_noise(source, duration=1)

                audio = recognizer.listen(source)

                text = recognizer.recognize_google(audio)

                return text

        except sr.UnknownValueError:
            return "Could not understand audio"

        except sr.RequestError:
            return "Internet connection required"

        except Exception as e:
            return f"Error: {e}"