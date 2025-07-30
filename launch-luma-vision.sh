#!/bin/bash
echo "🚀 LUMA VISION PRO - Assistant IA avancé"
echo "========================================"

# Démarrage Ollama
/Applications/Ollama.app/Contents/Resources/ollama serve &
sleep 2

echo "✅ Système prêt !"
echo ""
echo "Modes disponibles:"
echo "1. Mode Vision + Vocal"
echo "2. Mode Chat texte"
echo ""

python3 luma-vision-integrated.py

