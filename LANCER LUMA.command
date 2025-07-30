#!/bin/bash

# Aller dans le bon dossier
cd "$(dirname "$0")"

# Message de bienvenue
echo "🚀 Lancement de LUMA..."

# Lancer l'app
python3 luma_app_simple.py

echo "👋 LUMA fermé. À bientôt !"
