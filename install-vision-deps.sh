#!/bin/bash

echo "🎤👁️ Installation des dépendances Vision et Voix"
echo "================================================"

# Mise à jour pip
python3 -m pip install --upgrade pip

echo "📦 Installation reconnaissance faciale..."
pip3 install opencv-python
pip3 install face-recognition
pip3 install dlib

echo "🎤 Installation reconnaissance vocale..."
pip3 install SpeechRecognition
pip3 install pyttsx3
pip3 install pyaudio

# Pour macOS
echo "🔊 Installation support audio macOS..."
brew install portaudio || echo "Homebrew requis pour PortAudio"

echo ""
echo "✅ Installation terminée !"
echo ""
echo "🚀 Vous pouvez maintenant lancer:"
echo "   python3 face-voice-recognition.py"
echo ""
echo "📝 Note: Autorisez l'accès caméra et micro quand demandé"

