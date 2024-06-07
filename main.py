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
win.geometry("400x500")
win.title("Voice Translator")
icon = tk.PhotoImage(file="icon.png")
win.iconphoto(False, icon)

# Function to perform text-to-speech
def speak_text(text, lang):
    try:
        tts = gTTS(text, lang=lang)
        tts.save("temp_audio.mp3")
        playsound("temp_audio.mp3", block=False)
        os.remove("temp_audio.mp3")
    except Exception as e:
        print(f"Error in TTS: {e}")

# Create a scrollable frame for chat messages
chat_canvas = tk.Canvas(win)
chat_scrollbar = tk.Scrollbar(win, orient="vertical", command=chat_canvas.yview)
chat_frame = tk.Frame(chat_canvas)

chat_frame.bind(
    "<Configure>",
    lambda e: chat_canvas.configure(
        scrollregion=chat_canvas.bbox("all")
    )
)

chat_canvas.create_window((0, 0), window=chat_frame, anchor="nw")
chat_canvas.configure(yscrollcommand=chat_scrollbar.set)

chat_canvas.pack(side="top", fill="both", expand=True)
chat_scrollbar.pack(side="right", fill="y")

# Create a dictionary of language names and codes
language_codes = {
    "English": "en", "Hindi": "hi", "Bengali": "bn", "Spanish": "es", "Chinese (Simplified)": "zh-CN", "Russian": "ru", "Japanese": "ja", "Korean": "ko", "German": "de", "French": "fr", "Tamil": "ta", "Telugu": "te", "Kannada": "kn", "Gujarati": "gu", "Punjabi": "pa"
}

language_names = list(language_codes.keys())

# Create the "Start Translation" button
run_button = tk.Button(win, text="Start Translation", command=lambda: run_translator())
run_button.pack(pady=(10, 10))

# Create a frame for language selection and button
control_frame = tk.Frame(win)
control_frame.pack(pady=(10, 5))

input_lang = ttk.Combobox(control_frame, values=language_names, width=15)
if input_lang.get() == "": input_lang.set("English")
input_lang.grid(row=0, column=0, padx=(5, 5), pady=(5, 5))

swap_button = tk.Button(control_frame, text="↔", command=lambda: swap_languages())
swap_button.grid(row=0, column=1, padx=(5, 5), pady=(5, 5))

output_lang = ttk.Combobox(control_frame, values=language_names, width=15)
if output_lang.get() == "": output_lang.set("Hindi")
output_lang.grid(row=0, column=2, padx=(5, 5), pady=(5, 5))

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

def add_message(frame, text, lang, is_input=True):
    msg_frame = tk.Frame(frame, bg="lightgrey" if is_input else "lightblue", padx=5, pady=5)
    msg_frame.pack(anchor="center", pady=5, padx=10)

    text_label = tk.Label(msg_frame, text=text, wraplength=250, justify="left", bg=msg_frame.cget("bg"))
    text_label.pack(side="left", fill="x", expand=True)

    tts_button = tk.Button(msg_frame, text="🔊", command=lambda: speak_text(text, lang))
    tts_button.pack(side="left")

    # Scroll to the end of the chat
    chat_canvas.update_idletasks()
    chat_canvas.yview_moveto(1.0)

def update_translation():
    run_button.config(state=tk.DISABLED)
    run_button.config(text="Listening...")

    with sr.Microphone() as source:
        print("Speak Now!\n")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)  # Adjust for ambient noise
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)  # Timeout and phrase time limit added

        try:
            speech_text = recognizer.recognize_google(audio)
            add_message(chat_frame, speech_text, language_codes[input_lang.get()], is_input=True)
            if speech_text.lower() in {'exit', 'stop'}:
                run_button.config(text="Start Translation", state=tk.NORMAL)
                return

            # Translate from input language to output language
            translated_text = GoogleTranslator(source=language_codes[input_lang.get()], target=language_codes[output_lang.get()]).translate(text=speech_text)
            add_message(chat_frame, translated_text, language_codes[output_lang.get()], is_input=False)
            voice = gTTS(translated_text, lang=language_codes[output_lang.get()], slow=False)
            voice.save('voice.mp3')
            playsound('voice.mp3', block=False)
            os.remove('voice.mp3')
            swap_languages()  # Swap languages after each translation

        except sr.UnknownValueError:
            add_message(chat_frame, "Could not understand!", "en")
        except sr.RequestError:
            add_message(chat_frame, "Could not request from Google!", "en")
        except Exception as e:
            add_message(chat_frame, f"Error: {e}", "en")

    run_button.config(text="Start Translation", state=tk.NORMAL)

def run_translator():
    run_button.config(text="Listening...")
    update_translation_thread = threading.Thread(target=update_translation)
    update_translation_thread.start()

# Run the Tkinter event loop
win.mainloop()
