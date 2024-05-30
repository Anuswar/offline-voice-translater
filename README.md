# Real-time Voice Translator 🎙️

Welcome to the GitHub repository for a Real-time Voice Translator! This repository contains the source code for a Python script that translates speech between any given languages by default it set to Russian to English in real-time. Feel free to explore, learn, and contribute.

## ⚙️ Installation

To run this script locally or make contributions, follow these steps:

1. **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/real-time-voice-translator.git
    cd real-time-voice-translator
    ```

2. **Set up a Python virtual environment:**
    ```bash
    # On Windows
    python -m venv venv
    venv\Scripts\activate
    
    # On macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install dependencies from requirements.txt:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the main script:**
    ```bash
    python main.py
    ```

## 🛠️ Technologies Used

- Python
- SpeechRecognition library
- Transformers library for translation
- Pyttsx3 library for text-to-speech

## 📂 Project Structure

The project structure is organized as follows:

- voice_translation_app/: Root directory of the project.
    - **images/**: Directory containing image assets for the application.
        - 01_mic.png: Normal mic button image.
        - 02_mic.png: Pressed mic button image.
    - **main.py**: Main application code containing the Kivy app and logic for voice recognition and translation.
    - **requirements.txt**: List of dependencies required to run the application.
    - **README.md**: Documentation for the project (you are here).
    - **LICENSE.md**: License file detailing the terms under which the code can be used.
    - **buildozer.spec**: Buildozer specification file for packaging the application for Android.

## 🤝 Contributing

Contributions are welcome! If you find any issues, have suggestions, or want to add new features, please open an issue or create a pull request. Follow these steps:

1. **Fork the repository.**
2. **Create a new branch** for your feature or bug fix.
3. **Make your changes and commit them** with descriptive commit messages.
4. **Push your changes to your fork.**
5. **Open a pull request** to the `main` branch of the original repository.

## 📄 License

This project is licensed under the [MIT License](LICENSE.md), which means you are free to use, modify, and distribute the code.
