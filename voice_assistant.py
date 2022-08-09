import speech_recognition as sr
import pyttsx3

engine = pyttsx3.init()
r = sr.Recognizer()


def speak(speech):
    if speech is not None:
        engine.setProperty('rate', 190)
        engine.say(speech)
        engine.runAndWait()
    else:
        pass


def listen():
    text = ''
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
            r.energy_threshold = 500
            print('listening...')
            audio = r.listen(source, timeout=4, phrase_time_limit=7)
            text = r.recognize_google(audio)
            print(text)
    except sr.UnknownValueError:
        print('Please try again')
        speak('Please try again')
    except sr.WaitTimeoutError as e:
        print(str(e))
        speak(str(e))
    return text

def listen_once():
    text = ''
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
            r.energy_threshold = 500
            print('listening...')
            audio = r.listen(source, timeout=4, phrase_time_limit=7)
            text = r.recognize_google(audio).lower()
            print(text)
    except Exception:
        pass

    return text








