# Voice Translator 🎙️

This GitHub repository for a Voice Translator! This repository contains the source code for a Python script that translates speech between any given languages by default it set to English to Hindi. Feel free to explore, learn, and contribute.

## ⚙️ Installation

To run this script locally or make contributions, follow these steps:

1. **Clone the repository:**
    ```bash
    git clone https://github.com/Anuswar/voice-translater-app.git
    cd voice-translater-app
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
    
3. **Build installer containing all the files:**
   - Windows: ```python setup.py bdist_msi```
   - Linux: ```python setup.py bdist_rpm```
   - Mac: ```python setup.py bdist_mac```

4. **Install dependencies from requirements.txt:**
    ```bash
    pip install --upgrade wheel
    
    pip install -r requirements.txt
    ```

5. **Run the main script:**
    ```bash
    python main.py
    ```

## 🛠️ Technologies Used

- Python
- gTTS library for text-to-speech
- PyAudio library for audio I/O
- deep-translator library for translation
- SpeechRecognition library for speech recognition

## 📂 Project Structure

The project structure is organized as follows:

- voice_translation_app/: Root directory of the project.
    - **dist/**: Directory containing built distribution files.
        - voice-translator-2.0.1-win64.msi: Windows installer for version 2.0.1.
    - **build/**: Directory containing build files.
        - bdist.win-amd64/
        - exe.win-amd64-3.10/
        - exe.win-amd64-3.12/
    - **.gitignore**: File specifying intentionally untracked files to ignore.
    - **icon.ico**: Icon file for the executable.
    - **icon.png**: Icon image file.
    - **LICENSE.md**: License file detailing the terms under which the code can be used.
    - **main.py**: Main application code containing the Kivy app and logic for voice recognition and translation.
    - **README.md**: Documentation for the project (you are here).
    - **requirements.txt**: List of dependencies required to run the application.
    - **setup.py**: Script for building the application installer.

## 🤝 Contributing

Contributions are welcome! If you find any issues, have suggestions, or want to add new features, please open an issue or create a pull request. Follow these steps:

1. **Fork the repository.**
2. **Create a new branch** for your feature or bug fix.
3. **Make your changes and commit them** with descriptive commit messages.
4. **Push your changes to your fork.**
5. **Open a pull request** to the `main` branch of the original repository.

## 📄 License

This project is licensed under the [MIT License](LICENSE.md), which means you are free to use, modify, and distribute the code.