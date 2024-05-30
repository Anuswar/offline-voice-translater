from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import StringProperty
from kivy.uix.label import Label
import threading
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import pygame
import os
from langdetect import detect

class ImageButton(ButtonBehavior, Image):
    source_normal = StringProperty('images/01_mic.png')
    source_pressed = StringProperty('images/02_mic.png')

    def __init__(self, **kwargs):
        super(ImageButton, self).__init__(**kwargs)
        self.source = self.source_normal
        self.bind(on_press=self.on_press_button)
        self.bind(on_release=self.on_release_button)

    def on_press_button(self, *args):
        self.source = self.source_pressed

    def on_release_button(self, *args):
        self.source = self.source_normal
        threading.Thread(target=self.capture_and_translate).start()

    def capture_and_translate(self):
        query = recognize_speech()
        if query:
            src_lang = detect(query)
            dest_lang = app.mainbutton2.text
            dest_lang_code = getLangCode(dest_lang)
            if dest_lang_code:
                translated_text = translate_text(query, src_lang, dest_lang_code)
                save_and_play_audio(translated_text, dest_lang_code)
            else:
                print(f"Error: Destination language '{dest_lang}' is not supported.")

class ArrowLabel(ButtonBehavior, Label):
    pass

class VoiceTranslationApp(App):
    def build(self):
        self.languages = sorted(all_languages.keys())
        layout = FloatLayout()

        # Create the mic button with press effect
        mic_button = ImageButton(size_hint=(None, None), size=(100, 100),
                                 pos_hint={'center_x': 0.5, 'center_y': 0.23})
        layout.add_widget(mic_button)

        # Create the bottom section with dropdown menus
        bottom_layout = BoxLayout(orientation='horizontal', size_hint=(0.8, None), height=50,
                                  pos_hint={'center_x': 0.5, 'y': 0.05}, spacing=20)

        # Create both dropdown menus with the same content
        self.dropdown1 = self.create_dropdown()
        self.dropdown2 = self.create_dropdown()

        self.mainbutton1 = Button(text='English', size_hint=(1, 1))
        self.mainbutton2 = Button(text='Kannada', size_hint=(1, 1))

        self.mainbutton1.bind(on_release=self.dropdown1.open)
        self.dropdown1.bind(on_select=lambda instance, x: setattr(self.mainbutton1, 'text', x))

        self.mainbutton2.bind(on_release=self.dropdown2.open)
        self.dropdown2.bind(on_select=lambda instance, x: setattr(self.mainbutton2, 'text', x))

        # Add the dropdown menus to the bottom layout
        bottom_layout.add_widget(self.mainbutton1)

        # Add the arrow label with switch functionality
        arrow_label = ArrowLabel(text='<->', size_hint=(None, None), size=(50, 50), pos_hint={'center_y': 0.5})
        arrow_label.bind(on_press=self.switch_languages)
        bottom_layout.add_widget(arrow_label)

        bottom_layout.add_widget(self.mainbutton2)

        layout.add_widget(bottom_layout)

        return layout

    def create_dropdown(self):
        dropdown = DropDown()
        for language in self.languages:
            btn = Button(text=language, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            dropdown.add_widget(btn)
        return dropdown

    def switch_languages(self, instance):
        lang1 = self.mainbutton1.text
        lang2 = self.mainbutton2.text
        self.mainbutton1.text = lang2
        self.mainbutton2.text = lang1

def getLangCode(lang_name):
    return all_languages.get(lang_name.lower())

def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Adjusting for ambient noise...")
        r.adjust_for_ambient_noise(source, duration=1)
        r.energy_threshold = 4000  # Adjust this value as needed
        r.pause_threshold = 0.5

        print("Listening...")
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en', show_all=False)
        print(f"You said: {query}\n")
        return query
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None


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

if __name__ == '__main__':
    app = VoiceTranslationApp()
    app.run()
