from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty
from kivy.clock import Clock
import threading
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import pygame
import os
import sys

# Set default encoding to utf-8
if sys.version_info[0] < 3:
    reload(sys)
    sys.setdefaultencoding('utf8')
else:
    import importlib
    importlib.reload(sys)

class ImageButton(ButtonBehavior, Image):
    source_normal = StringProperty('images/01_mic.png')
    source_pressed = StringProperty('images/02_mic.png')

    def __init__(self, app, **kwargs):
        super(ImageButton, self).__init__(**kwargs)
        self.app = app
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
            src_lang, dest_lang = self.app.get_selected_languages()
            translated_text = translate_text(query, src_lang, dest_lang)
            
            # Play the audio first before adding the message
            save_and_play_audio(translated_text, dest_lang)

            # Schedule add_message to run on the main thread
            Clock.schedule_once(lambda dt: self.app.add_message(query, 'You', src_lang), 0)
            Clock.schedule_once(lambda dt: self.app.add_message(translated_text, 'Bot', dest_lang), 0)

class ArrowLabel(ButtonBehavior, Label):
    pass

class VoiceTranslationApp(App):
    def build(self):
        self.languages = sorted(all_languages.keys())
        layout = FloatLayout()

        # Create the mic button with press effect
        mic_button = ImageButton(app=self, size_hint=(None, None), size=(100, 100),
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

        # Create the conversation area
        self.conversation_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        self.conversation_layout.bind(minimum_height=self.conversation_layout.setter('height'))

        scroll_view = ScrollView(size_hint=(1, 0.6), pos_hint={'top': 0.9})
        scroll_view.add_widget(self.conversation_layout)

        # Assign an ID to the scroll_view
        layout.ids['scroll_view'] = scroll_view
        layout.add_widget(scroll_view)

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

    def get_selected_languages(self):
        lang1 = self.mainbutton1.text
        lang2 = self.mainbutton2.text
        return all_languages[lang1.lower()], all_languages[lang2.lower()]

    def add_message(self, text, sender, lang):
        if sender == 'You':
            sender_lang = self.mainbutton1.text
        else:
            sender_lang = self.mainbutton1.text  # Use the same language for both messages

        if sender_lang.lower() != lang.lower():
            translation = translate_text(text, lang, sender_lang)
        else:
            translation = text

        bubble_layout = BoxLayout(size_hint_y=None, padding=10)
        bubble_label = Label(text=f"{sender}: {translation}", size_hint_x=None, width=self.conversation_layout.width - 200, text_size=(self.conversation_layout.width - 200, None), halign='left', valign='top')

        # Bind the height of the label to the height of the text
        bubble_label.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
        bubble_layout.add_widget(bubble_label)

        # Add TTS button for original language
        tts_button_original = Button(text="🔊", size_hint_x=None, width=50)
        tts_button_original.bind(on_press=lambda instance, text=translation, lang_code=lang: self.speak_text(text, lang_code))
        bubble_layout.add_widget(tts_button_original)
    
        # Add TTS button for Kannada
        tts_button_kannada = Button(text="🔊 Kannada", size_hint_x=None, width=100)
        tts_button_kannada.bind(on_press=lambda instance, text=text: self.speak_text(text, 'kn'))
        bubble_layout.add_widget(tts_button_kannada)
    
        # Set the height of the bubble layout to match the label's height
        bubble_layout.height = bubble_label.height + 20

        self.conversation_layout.add_widget(bubble_layout)
        # Scroll to the bottom of the ScrollView to show the latest message
        Clock.schedule_once(lambda dt: self.scroll_to_bottom(), 0)

    def scroll_to_bottom(self, *args):
        self.root.ids.scroll_view.scroll_y = 0

    def speak_text(self, text, lang_code):
        save_and_play_audio(text, lang_code)

def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Adjusting for ambient noise...")
        r.adjust_for_ambient_noise(source, duration=1)
        r.energy_threshold = 4000  
        r.pause_threshold = 0.5

        print("Listening...")
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en', show_all=False)
        print(f"You said: {query}\n")
        return query
    except sr.UnknownValueError:
        print("Speech Recognition could not understand audio")
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
    'hausa': 'ha', 'hawaiian': 'haw', 'hebrew': 'he', 'hindi': 'hi', 'hmong': 'hmn', 'hungarian': 'hu', 'icelandic': 'is', 'igbo': 'ig', 'indonesian': 'id', 'irish': 'ga',
    'italian': 'it', 'japanese': 'ja', 'javanese': 'jw', 'kannada': 'kn', 'kazakh': 'kk', 'khmer': 'km', 'korean': 'ko', 'kurdish (kurmanji)': 'ku', 'kyrgyz': 'ky',
    'lao': 'lo', 'latin': 'la', 'latvian': 'lv', 'lithuanian': 'lt', 'luxembourgish': 'lb', 'macedonian': 'mk', 'malagasy': 'mg', 'malay': 'ms', 'malayalam': 'ml',
    'maltese': 'mt', 'maori': 'mi', 'marathi': 'mr', 'mongolian': 'mn', 'myanmar (burmese)': 'my', 'nepali': 'ne', 'norwegian': 'no', 'odia': 'or', 'pashto': 'ps',
    'persian': 'fa', 'polish': 'pl', 'portuguese': 'pt', 'punjabi': 'pa', 'romanian': 'ro', 'russian': 'ru', 'samoan': 'sm', 'scots gaelic': 'gd', 'serbian': 'sr',
    'sesotho': 'st', 'shona': 'sn', 'sindhi': 'sd', 'sinhala': 'si', 'slovak': 'sk', 'slovenian': 'sl', 'somali': 'so', 'spanish': 'es', 'sundanese': 'su',
    'swahili': 'sw', 'swedish': 'sv', 'tajik': 'tg', 'tamil': 'ta', 'telugu': 'te', 'thai': 'th', 'turkish': 'tr', 'ukrainian': 'uk', 'urdu': 'ur', 'uzbek': 'uz',
    'vietnamese': 'vi', 'welsh': 'cy', 'xhosa': 'xh', 'yiddish': 'yi', 'yoruba': 'yo', 'zulu': 'zu'
}

if __name__ == '__main__':
    VoiceTranslationApp().run()
 