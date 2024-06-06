import os
import threading
import tkinter as tk
from tkinter import ttk
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
from deep_translator import GoogleTranslator

# Create an instance of Tkinter frame or window
win = tk.Tk()

# Set the geometry of tkinter frame
win.geometry("700x450")
win.title("Voice Translator")
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

# Create the "Start Translation" button
run_button = tk.Button(win, text="Start Translation", command=lambda: run_translator())
run_button.pack(pady=(20, 10))

# Create a dictionary of language names and codes
language_codes = {
    "English": "en", "Hindi": "hi", "Bengali": "bn", "Spanish": "es", "Chinese (Simplified)": "zh-CN", "Russian": "ru", "Japanese": "ja", "Korean": "ko", "German": "de", "French": "fr", "Tamil": "ta", "Telugu": "te", "Kannada": "kn", "Gujarati": "gu", "Punjabi": "pa"
}

language_names = list(language_codes.keys())

# Create dropdown menus for the input and output languages
frame = tk.Frame(win)
frame.pack(pady=(10, 5))

input_lang_label = tk.Label(frame, text="Input Language:")
input_lang_label.grid(row=0, column=0, padx=(10, 5), pady=(10, 5))

input_lang = ttk.Combobox(frame, values=language_names)
if input_lang.get() == "": input_lang.set("English")
input_lang.grid(row=1, column=0, padx=(10, 5), pady=(0, 10))

swap_button = tk.Button(frame, text="↔", command=lambda: swap_languages())
swap_button.grid(row=1, column=1, padx=(0, 5), pady=(0, 10))

output_lang_label = tk.Label(frame, text="Output Language:")
output_lang_label.grid(row=0, column=2, padx=(5, 10), pady=(10, 5))

output_lang = ttk.Combobox(frame, values=language_names)
if output_lang.get() == "": output_lang.set("Hindi")
output_lang.grid(row=1, column=2, padx=(5, 10), pady=(0, 10))

# Initialize Speech Recognizer
recognizer = sr.Recognizer()
recognizer.energy_threshold = 300  # Adjust energy threshold for ambient noise
recognizer.pause_threshold = 0.6   # Adjust pause threshold for quicker response
recognizer.phrase_threshold = 0.3  # Adjust phrase threshold for faster recognition of short phrases

# Variable to track the current input and output languages
current_input_lang = "English"
current_output_lang = "Hindi"

def swap_languages():
    global current_input_lang, current_output_lang
    # Swap input and output languages
    input_lang_val = input_lang.get()
    input_lang.set(output_lang.get())
    output_lang.set(input_lang_val)
    current_input_lang, current_output_lang = current_output_lang, current_input_lang

def update_translation():
    run_button.config(state=tk.DISABLED)
    run_button.config(text="Listening...")

    with sr.Microphone() as source:
        print("Speak Now!\n")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)  # Adjust for ambient noise
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)  # Timeout and phrase time limit added

        try:
            speech_text = recognizer.recognize_google(audio)
            input_text.insert(tk.END, f"{speech_text}\n")
            if speech_text.lower() in {'exit', 'stop'}:
                run_button.config(text="Start Translation", state=tk.NORMAL)
                return

            # Translate from input language to output language
            translated_text = GoogleTranslator(source=language_codes[input_lang.get()], target=language_codes[output_lang.get()]).translate(text=speech_text)
            output_text.insert(tk.END, translated_text + "\n")
            voice = gTTS(translated_text, lang=language_codes[output_lang.get()], slow=False)
            voice.save('voice.mp3')
            playsound('voice.mp3', block=False)
            os.remove('voice.mp3')
            swap_languages()  # Swap languages after each translation

        except sr.UnknownValueError:
            output_text.insert(tk.END, "Could not understand!\n")
        except sr.RequestError:
            output_text.insert(tk.END, "Could not request from Google!\n")
        except Exception as e:
            output_text.insert(tk.END, f"Error: {e}\n")

    run_button.config(text="Start Translation", state=tk.NORMAL)

def run_translator():
    run_button.config(text="Listening...")
    update_translation_thread = threading.Thread(target=update_translation)
    update_translation_thread.start()

# Run the Tkinter event loop
win.mainloop()
