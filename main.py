from modules.speech_recognition_module import listen_for_speech, recognize_speech
from modules.translation_module import translate
from modules.text_to_speech_module import speak_text

def main():
    # Listen for speech until the speaker stops speaking for 4 seconds
    recorded_audio = listen_for_speech(timeout=4, phrase_time_limit=5)
    
    if recorded_audio:
        # Recognize speech
        text = recognize_speech(recorded_audio, language="en-US")  
        
        if text:
            print("Decoded Text: {}".format(text))
            
            # Translate recognized text from English to Hindi
            translated_text = translate(text, 'en', 'hi')
            translated_text = " ".join(translated_text)
            print("Translated Text: {}".format(translated_text))
            
            # Speak translated text
            speak_text(translated_text, lang='hi')
        else:
            print("No recognizable speech detected.")
    else:
        print("No speech detected for 4 seconds. Exiting...")

if __name__ == "__main__":
    main()
