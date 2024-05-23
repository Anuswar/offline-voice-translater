from gtts import gTTS
import os
import pygame

def speak_text(text, lang='hi'):
    print("Reading the translated text...")
    tts = gTTS(text=text, lang=lang, slow=False)
    tts.save("translated_text.mp3")
    
    # Initialize pygame mixer
    pygame.mixer.init()
    
    # Load and play the audio file
    pygame.mixer.music.load("translated_text.mp3")
    pygame.mixer.music.play()
    
    # Wait for the audio to finish playing
    while pygame.mixer.music.get_busy():
        continue
    
    # Quit the mixer
    pygame.mixer.quit()
    
    # Remove the audio file
    os.remove("translated_text.mp3")
