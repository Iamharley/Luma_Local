# 🤖 LUMA Business Pro - Instructions Cursor

## 🎯 **MISSION**

Implémenter le système **LUMA Business Pro** complet sur le Mac d'Anne-Sophie selon les spécifications techniques fournies par Claude.

## 📁 **FICHIERS À CRÉER**

### **1. Structure des dossiers**
```bash
mkdir -p ~/Desktop/LUMA-BUSINESS-PRO/{logs,backups,config,data,static,templates}
cd ~/Desktop/LUMA-BUSINESS-PRO
```

### **2. Fichiers principaux à créer** ⭐

#### **A. Interface Web - `luma_interface.html`**
- ✅ Interface Glassmorphism complète (déjà fournie par Claude)
- 🎨 Design moderne avec navigation latérale
- 📱 Responsive pour tous écrans
- 🎤 Interface vocale intégrée
- 🏥 Widgets surveillance médicale
- 🏡 Contrôles domotique
- 📊 Dashboard business analytics

#### **B. Serveur Backend - `luma_server.py`**
- ✅ Serveur Flask complet (déjà fourni par Claude)
- 🧠 IA hybride (Claude + GPT + Gemini + Ollama local)
- 🏥 Module surveillance médicale avec OpenCV
- 🏡 Contrôleur domotique (HomeKit, Alexa, IoT)
- 📊 Analytics business (Shopify, Gmail, métriques)
- 🎤 Reconnaissance vocale et synthèse
- ⚡ WebSocket temps réel
- 🚨 Système d'urgence épilepsie

#### **C. Dépendances - `requirements.txt`**
- ✅ Liste complète des packages Python (déjà fournie)
- 🔧 Versions spécifiées pour compatibilité
- 📦 Tous les modules nécessaires

#### **D. Script de lancement - `launch_luma.sh`**
- ✅ Script bash complet (déjà fourni par Claude)
- 🚀 Menu interactif d'installation et démarrage
- ✅ Vérifications système automatiques
- 🔧 Installation des dépendances
- ⚙️ Configuration environnement

#### **E. Configuration - `.env`**
- ✅ Template complet fourni (`.env.example`)
- 🔑 Configuration pour toutes les APIs
- 🏥 Paramètres médicaux d'urgence
- 🏡 Configuration domotique
- 📊 Intégrations business

#### **F. Installation automatique - `install_luma.py`**
- ✅ Script Python d'installation complète (déjà fourni)
- 🔄 Installation automatisée de tous les composants
- ✅ Vérifications et validations
- 🎯 Configuration guidée

#### **G. Documentation - `README.md`**
- ✅ Guide complet d'utilisation (déjà fourni)
- 📖 Instructions détaillées
- 🔧 Dépannage et maintenance

## 🚀 **ÉTAPES D'IMPLÉMENTATION**

### **Phase 1: Création des fichiers (10 min)**
```bash
# 1. Créer la structure
mkdir -p ~/Desktop/LUMA-BUSINESS-PRO
cd ~/Desktop/LUMA-BUSINESS-PRO

# 2. Copier tous les fichiers fournis par Claude :
# - luma_interface.html (Interface complète)
# - luma_server.py (Backend complet)  
# - requirements.txt (Dépendances)
# - launch_luma.sh (Script lancement)
# - install_luma.py (Installation auto)
# - .env.example (Template config)
# - README.md (Documentation)

# 3. Rendre les scripts exécutables
chmod +x launch_luma.sh
chmod +x install_luma.py
```

### **Phase 2: Installation système (15 min)**
```bash
# Option A: Installation automatique (recommandée)
python3 install_luma.py

# Option B: Installation manuelle
./launch_luma.sh --install
```

### **Phase 3: Configuration (10 min)**
```bash
# 1. Copier template de configuration
cp .env.example .env

# 2. Éditez .env avec les vraies clés API d'Anne-Sophie
# Au minimum : ANTHROPIC_API_KEY (clé Claude)

# 3. Configurer contacts d'urgence dans .env
# Remplacer par les vrais contacts médicaux
```

### **Phase 4: Test et validation (10 min)**
```bash
# 1. Démarrer LUMA
./launch_luma.sh --start

# 2. Ouvrir navigateur : http://127.0.0.1:8080

# 3. Tester fonctionnalités de base :
# - Interface se charge correctement
# - Chat IA répond (même en mode dégradé)
# - Reconnaissance vocale "Hey Luma"
# - Widgets s'affichent

# 4. Autoriser permissions macOS :
# - Caméra pour surveillance médicale
# - Microphone pour commandes vocales
# - Notifications pour alertes
```

## ⚙️ **CONFIGURATION PRIORITAIRE**

### **1. Clés API obligatoires**
```bash
# Dans le fichier .env, configurer AU MINIMUM :
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxx  # Clé Claude d'Anne-Sophie

# Optionnel mais recommandé :
OPENAI_API_KEY=sk-xxxxxx               # Si elle en a une
GEMINI_API_KEY=AIza-xxxxxx             # Si elle en a une
```

### **2. Configuration médicale d'urgence**
```bash
# Contacts d'urgence réels d'Anne-Sophie
EMERGENCY_CONTACTS=[
  {"name": "SAMU", "number": "15", "type": "emergency"},
  {"name": "Dr. [Son médecin]", "number": "+33xxxxxxxxx", "type": "doctor"},
  {"name": "[Contact proche]", "number": "+33xxxxxxxxx", "type": "family"}
]

# Informations médicales
MEDICAL_CONDITION=Épilepsie
MEDICATION=[Ses médicaments réels]
```

### **3. Configuration business**
```bash
# Si elle a un store Shopify
SHOPIFY_STORE_URL=[son-store].myshopify.com
SHOPIFY_ACCESS_TOKEN=[sa-clé-shopify]

# Gmail business (optionnel)
GMAIL_CREDENTIALS_FILE=gmail_credentials.json
```

## 🔧 **VÉRIFICATIONS TECHNIQUES**

### **Prérequis système**
- ✅ macOS (testé sur Big Sur+)
- ✅ Python 3.8+ installé
- ✅ Homebrew installé (recommandé)
- ✅ 4GB RAM libre minimum
- ✅ 2GB espace disque

### **Dépendances critiques**
```bash
# Vérifier que ces packages s'installent :
pip install flask anthropic openai opencv-python SpeechRecognition pyttsx3

# Si PyAudio pose problème (fréquent sur macOS) :
brew install portaudio
pip install pyaudio
```

### **Services externes**
- **Ollama** : S'installe automatiquement pour IA locale
- **Modèle Mistral** : Se télécharge au premier usage
- **APIs IA** : Fonctionnent avec les clés fournies

## 🚨 **GESTION D'ERREURS COMMUNES**

### **Erreur 1: PyAudio ne s'installe pas**
```bash
# Solution macOS :
brew install portaudio
export CPPFLAGS=-I/opt/homebrew/include
export LDFLAGS=-L/opt/homebrew/lib
pip install pyaudio
```

### **Erreur 2: OpenCV ne trouve pas la caméra**
```bash
# Vérifier permissions système :
# Préférences Système > Sécurité > Caméra > Autoriser Terminal/Python
```

### **Erreur 3: Port 8080 occupé**
```bash
# Changer port dans .env :
LUMA_PORT=8081
```

### **Erreur 4: Ollama ne démarre pas**
```bash
# Installation manuelle :
curl -fsSL https://ollama.ai/install.sh | sh
ollama serve &
ollama pull mistral
```

## 🎯 **OBJECTIFS DE VALIDATION**

### **✅ Interface fonctionnelle**
- [ ] Page web se charge sur http://127.0.0.1:8080
- [ ] Navigation entre sections fonctionne
- [ ] Design Glassmorphism s'affiche correctement
- [ ] Responsive sur différentes tailles d'écran

### **✅ IA opérationnelle**
- [ ] Chat répond aux messages (même en mode dégradé)
- [ ] Au moins un modèle IA configuré (Claude/GPT/local)
- [ ] Routage intelligent entre modèles
- [ ] Mode vocal "Hey Luma" détecte la voix

### **✅ Surveillance médicale**
- [ ] Widget biométrique affiche des données
- [ ] Bouton d'urgence fonctionnel (mode test)
- [ ] Caméra accède si autorisée
- [ ] Simulation de monitoring active

### **✅ Domotique et business**
- [ ] Widgets domotique interactifs
- [ ] Analytics business s'affichent
- [ ] Contrôles réagissent aux clics
- [ ] Simulation de données fonctionne

## 📞 **SUPPORT ET ASSISTANCE**

### **En cas de problème:**

1. **Vérifier les logs :**
   ```bash
   tail -f luma.log
   ```

2. **Mode debug :**
   ```bash
   # Dans .env :
   LUMA_DEBUG=true
   LOG_LEVEL=DEBUG
   ```

3. **Réinstallation complète :**
   ```bash
   rm -rf venv/
   python3 install_luma.py
   ```

4. **Test minimal :**
   ```bash
   python3 -c "from flask import Flask; app=Flask(__name__); app.run(port=8080)"
   ```

## 🎉 **LIVRAISON FINALE**

### **Anne-Sophie aura :**
- 🤖 **Assistant IA personnel** ultra-avancé
- 🏥 **Surveillance médicale** 24/7 avec alerte épilepsie
- 🏡 **Contrôle domotique** complet et intuitif
- 📊 **Analytics business** temps réel pour son store
- 🎤 **Interface vocale** naturelle "Hey Luma"
- 🎨 **Interface moderne** Glassmorphism accessible
- 🔧 **Système évolutif** et personnalisable

### **Utilisation quotidienne :**
1. **Double-clic** sur "Lancer LUMA.command" (bureau)
2. **Navigation web** : http://127.0.0.1:8080  
3. **Commandes vocales** : "Hey Luma, mes emails ?"
4. **Surveillance automatique** : Mode passif 24/7
5. **Contrôles intuitifs** : Interface tactile moderne

## 🚀 **MISSION ACCOMPLIE !**

LUMA Business Pro sera l'assistant IA personnel le plus avancé qu'Anne-Sophie ait jamais eu :
- **Intelligence** : Hybride Claude + GPT + Local
- **Sécurité** : Surveillance médicale vitale
- **Productivité** : Business analytics + domotique
- **Simplicité** : Interface moderne et vocale
- **Évolutivité** : Plateforme extensible

**🎯 Objectif : Révolutionner sa productivité et assurer sa sécurité !**