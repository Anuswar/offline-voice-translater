# main.py
from modules.speech_recognition_module import listen_for_speech, recognize_speech
from modules.translation_module import translate
from modules.text_to_speech_module import initialize_reader, speak_text

def main():
    reader = initialize_reader()
    
    while True:
        recorded_audio = listen_for_speech(timeout=4, phrase_time_limit=5)
        if recorded_audio:
            text = recognize_speech(recorded_audio, language="ru-RU")
            if text:
                translated_text = translate(text, 'ru')
                translated_text = " ".join(translated_text)
                print("Translated Text: {}".format(translated_text))
                speak_text(reader, translated_text)
            else:
                print("No recognizable speech detected. Retrying...")
        else:
            print("No speech detected for 4 seconds. Exiting...")
            break

if __name__ == "__main__":
    main()
