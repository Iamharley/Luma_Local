#!/bin/bash
echo "🚀 DÉMARRAGE LUMA BUSINESS PRO"
echo "================================"

# Démarrage Ollama
/Applications/Ollama.app/Contents/Resources/ollama serve &

# Ouverture VS Code  
open -a "Visual Studio Code"

echo "✅ Luma Business Pro prêt !"
echo "Lancez: python3 luma-assistant.py"

