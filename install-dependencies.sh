#!/bin/bash
echo "📦 Installation des dépendances Python..."

# Installation pip si nécessaire
python3 -m ensurepip --upgrade

# Dépendances principales
pip3 install requests
pip3 install schedule 
pip3 install python-dateutil

echo "✅ Dépendances installées !"
echo ""
echo "🚀 Vous pouvez maintenant lancer:"
echo "   ./start-luma.sh"
