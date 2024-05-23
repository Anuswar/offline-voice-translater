# text_to_speech_module.py
import pyttsx3

def initialize_reader():
    reader = pyttsx3.init()
    voices = reader.getProperty('voices')
    
    # Selecting a female voice with an American accent
    selected_voice = next((voice for voice in voices if 'en_US' in voice.id and 'female' in voice.id.lower()), None)
    if selected_voice:
        reader.setProperty('voice', selected_voice.id)
    else:
        print("No matching voice found. Using default.")
    
    return reader

def speak_text(reader, text):
    print("Reading the translated text...")
    reader.say(text)
    reader.runAndWait()
