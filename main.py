import os
import threading
import tkinter as tk
from gtts import gTTS
from tkinter import ttk
import speech_recognition as sr
from playsound import playsound
from deep_translator import GoogleTranslator
from google.transliteration import transliterate_text

# Create an instance of Tkinter frame or window
win = tk.Tk()

# Set the geometry of tkinter frame
win.geometry("700x450")
win.title("Real-Time Voice🎙️ Translator🔊")
icon = tk.PhotoImage(file="icon.png")
win.iconphoto(False, icon)

# Create labels and text boxes for the recognized and translated text
input_label = tk.Label(win, text="Recognized Text ⮯")
input_label.pack(pady=(10, 5))
input_text = tk.Text(win, height=5, width=50)
input_text.pack(pady=(0, 20))

output_label = tk.Label(win, text="Translated Text ⮯")
output_label.pack(pady=(10, 5))
output_text = tk.Text(win, height=5, width=50)
output_text.pack(pady=(0, 20))

# Create the "Run" button
run_button = tk.Button(win, text="Start Translation", command=lambda: run_translator())
run_button.pack(pady=(20, 10))

# Create a dictionary of language names and codes
language_codes = {
    "English": "en", "Hindi": "hi", "Bengali": "bn", "Spanish": "es", "Chinese (Simplified)": "zh-CN", "Russian": "ru", "Japanese": "ja", "Korean": "ko", "German": "de", "French": "fr", "Tamil": "ta", "Telugu": "te", "Kannada": "kn", "Gujarati": "gu", "Punjabi": "pa"
}

language_names = list(language_codes.keys())

# Create dropdown menus for the input and output languages
input_lang_label = tk.Label(win, text="Select Input Language:")
input_lang_label.pack(pady=(10, 5))

input_lang = ttk.Combobox(win, values=language_names)
input_lang.bind("<<ComboboxSelected>>", lambda e: update_input_lang_code(e))
if input_lang.get() == "": input_lang.set("auto")
input_lang.pack(pady=(0, 10))

output_lang_label = tk.Label(win, text="Select Output Language:")
output_lang_label.pack(pady=(10, 5))

output_lang = ttk.Combobox(win, values=language_names)
output_lang.bind("<<ComboboxSelected>>", lambda e: update_output_lang_code(e))
if output_lang.get() == "": output_lang.set("en")
output_lang.pack(pady=(0, 10))

keep_running = False
update_translation_thread = None

def update_input_lang_code(event):
    selected_language_name = event.widget.get()
    selected_language_code = language_codes[selected_language_name]
    input_lang.set(selected_language_code)

def update_output_lang_code(event):
    selected_language_name = event.widget.get()
    selected_language_code = language_codes[selected_language_name]
    output_lang.set(selected_language_code)

def update_translation():
    global keep_running

    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Speak Now!\n")
        audio = r.listen(source)
        
        try:
            speech_text = r.recognize_google(audio)
            speech_text_transliteration = transliterate_text(speech_text, lang_code=input_lang.get()) if input_lang.get() not in ('auto', 'en') else speech_text
            input_text.insert(tk.END, f"{speech_text_transliteration}\n")
            if speech_text.lower() in {'exit', 'stop'}:
                keep_running = False
                return
            
            translated_text = GoogleTranslator(source=input_lang.get(), target=output_lang.get()).translate(text=speech_text_transliteration)
            voice = gTTS(translated_text, lang=output_lang.get())
            voice.save('voice.mp3')
            playsound('voice.mp3')
            os.remove('voice.mp3')

            output_text.insert(tk.END, translated_text + "\n")
            
        except sr.UnknownValueError:
            output_text.insert(tk.END, "Could not understand!\n")
        except sr.RequestError:
            output_text.insert(tk.END, "Could not request from Google!\n")
        
        # Stop after one translation
        keep_running = False
        run_button.config(text="Start Translation")

def run_translator():
    global keep_running, update_translation_thread

    if keep_running:
        keep_running = False
        if update_translation_thread:
            update_translation_thread.join()
        run_button.config(text="Start Translation")
    else:
        keep_running = True
        update_translation_thread = threading.Thread(target=update_translation)
        update_translation_thread.start()
        run_button.config(text="Kill Execution")

# Run the Tkinter event loop
win.mainloop()
