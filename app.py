import pygame
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os
import pyttsx3
from langdetect import detect
import pycountry
import threading

# A dictionary containing language codes
all_languages = {
    'afrikaans': 'af', 'albanian': 'sq', 'amharic': 'am', 'arabic': 'ar', 'armenian': 'hy', 'azerbaijani': 'az',
    'basque': 'eu', 'belarusian': 'be', 'bengali': 'bn', 'bosnian': 'bs', 'bulgarian': 'bg', 'catalan': 'ca',
    'cebuano': 'ceb', 'chichewa': 'ny', 'chinese (simplified)': 'zh-cn', 'chinese (traditional)': 'zh-tw',
    'corsican': 'co', 'croatian': 'hr', 'czech': 'cs', 'danish': 'da', 'dutch': 'nl', 'english': 'en',
    'esperanto': 'eo', 'estonian': 'et', 'filipino': 'tl', 'finnish': 'fi', 'french': 'fr', 'frisian': 'fy',
    'galician': 'gl', 'georgian': 'ka', 'german': 'de', 'greek': 'el', 'gujarati': 'gu', 'haitian creole': 'ht',
    'hausa': 'ha', 'hawaiian': 'haw', 'hebrew': 'he', 'hindi': 'hi', 'hmong': 'hmn', 'hungarian': 'hu',
    'icelandic': 'is', 'igbo': 'ig', 'indonesian': 'id', 'irish': 'ga', 'italian': 'it', 'japanese': 'ja',
    'javanese': 'jw', 'kannada': 'kn', 'kazakh': 'kk', 'khmer': 'km', 'korean': 'ko', 'kurdish (kurmanji)': 'ku',
    'kyrgyz': 'ky', 'lao': 'lo', 'latin': 'la', 'latvian': 'lv', 'lithuanian': 'lt', 'luxembourgish': 'lb',
    'macedonian': 'mk', 'malagasy': 'mg', 'malay': 'ms', 'malayalam': 'ml', 'maltese': 'mt', 'maori': 'mi',
    'marathi': 'mr', 'mongolian': 'mn', 'myanmar (burmese)': 'my', 'nepali': 'ne', 'norwegian': 'no', 'odia': 'or',
    'pashto': 'ps', 'persian': 'fa', 'polish': 'pl', 'portuguese': 'pt', 'punjabi': 'pa', 'romanian': 'ro',
    'russian': 'ru', 'samoan': 'sm', 'scots gaelic': 'gd', 'serbian': 'sr', 'sesotho': 'st', 'shona': 'sn',
    'sindhi': 'sd', 'sinhala': 'si', 'slovak': 'sk', 'slovenian': 'sl', 'somali': 'so', 'spanish': 'es',
    'sundanese': 'su', 'swahili': 'sw', 'swedish': 'sv', 'tajik': 'tg', 'tamil': 'ta', 'telugu': 'te', 'thai': 'th',
    'turkish': 'tr', 'ukrainian': 'uk', 'urdu': 'ur', 'uyghur': 'ug', 'uzbek': 'uz', 'vietnamese': 'vi', 'welsh': 'cy',
    'xhosa': 'xh', 'yiddish': 'yi', 'yoruba': 'yo', 'zulu': 'zu'
}

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def getLangCode(lang_name):
    # Check if the input language name exists in the tuple of all_languages
    if lang_name.lower() in all_languages:
        # If found, return its corresponding language code
        return all_languages[lang_name.lower()]
    else:
        # If not found, return None
        return None

def getLangName(lang_code):
    language = pycountry.languages.get(alpha_2=lang_code)
    return language.name

def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You said: {query}\n")
        return query
    except Exception as e:
        print("Please say that again...")
        return None

def select_input_language():
    print("Enter the language you want to translate from: Ex. English, French, Spanish, etc.")
    while True:
        lang = recognize_speech()
        if lang:
            lang_code = getLangCode(lang)
            if lang_code:
                return lang_code
            else:
                print("Language not supported, please try again.")

def select_output_language():
    print("Enter the language you want to translate to: Ex. English, French, Spanish, etc.")
    while True:
        lang = recognize_speech()
        if lang:
            lang_code = getLangCode(lang)
            if lang_code:
                return lang_code
            else:
                print("Language not supported, please try again.")

def translate_text(text, src_lang, dest_lang):
    translator = Translator()
    translation = translator.translate(text, src=src_lang, dest=dest_lang)
    return translation.text

def save_and_play_audio(text, lang_code):
    tts = gTTS(text=text, lang=lang_code, slow=False)
    tts.save("audioCap.mp3")
    play_sound("audioCap.mp3")
    os.remove("audioCap.mp3")

def play_sound(file):
    pygame.mixer.init()
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.stop()
    pygame.mixer.quit()

def handle_speech_input():
    global query
    query = recognize_speech()

if __name__ == "__main__":
    pygame.init()

    print("Welcome to the translator!")
    speak("Welcome to the translator!")

    print("Say the sentence you want to translate once you hear 'Listening'...")
    
    # Start a thread to listen for speech input
    thread = threading.Thread(target=handle_speech_input)
    thread.daemon = True
    thread.start()
    
    # Wait for speech input to be captured
    thread.join()

    # Proceed with language detection and translation
    src_lang = detect(query)
    print("Detected language:", getLangName(src_lang))
    
    dest_lang = select_output_language()
    print("Translating to:", getLangName(dest_lang))

    translated_text = translate_text(query, src_lang, dest_lang)
    print("Translated text:", translated_text)

    save_and_play_audio(translated_text, dest_lang)
