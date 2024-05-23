# speech_recognition_module.py
import speech_recognition as sr

def listen_for_speech(timeout=4, phrase_time_limit=5):
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source, duration=2)
        print("Listening...")
        
        try:
            recorded_audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            print("Speech detected. Processing...")
            return recorded_audio
        except sr.WaitTimeoutError:
            print("Timeout: No speech detected for {} seconds.".format(timeout))
            return None

def recognize_speech(audio, language="ru-RU"):
    recognizer = sr.Recognizer()
    try:
        text = recognizer.recognize_google(audio, language=language)
        print("Decoded Text: {}".format(text))
        return text
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio.")
    except Exception as ex:
        print("An error occurred: {0}".format(ex))
    return None
