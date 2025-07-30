# 🤖 LUMA Business Pro - Assistant IA Personnel

## 🎯 **Description**

LUMA Business Pro est votre assistant IA personnel ultra-avancé qui combine :

- 🏥 **Surveillance médicale 24/7** avec détection d'épilepsie
- 🧠 **IA hybride** (Claude, GPT-4, Gemini, Mistral local)
- 🏡 **Contrôle domotique** complet (HomeKit, Alexa, IoT)
- 📊 **Analytics business** temps réel (Shopify, emails, KPIs)
- 🎤 **Interface vocale** naturelle avec reconnaissance "Hey Luma"
- 🎨 **Interface Glassmorphism** moderne et accessible

## 🚀 **Installation Rapide**

### **Méthode 1: Installation automatique (recommandée)**

```bash
# 1. Téléchargez tous les fichiers LUMA sur votre Mac
# 2. Ouvrez Terminal et naviguez vers le dossier LUMA
cd ~/Desktop/LUMA-BUSINESS-PRO

# 3. Rendez le script exécutable
chmod +x launch_luma.sh

# 4. Lancez l'installation complète
./launch_luma.sh --install
```

### **Méthode 2: Installation manuelle**

```bash
# 1. Clonez ou téléchargez le projet
mkdir LUMA-BUSINESS-PRO
cd LUMA-BUSINESS-PRO

# 2. Créez l'environnement virtuel Python
python3 -m venv venv
source venv/bin/activate

# 3. Installez les dépendances
pip install -r requirements.txt

# 4. Configurez les variables d'environnement
cp .env.example .env
# Éditez .env avec vos clés API

# 5. Démarrez LUMA
python3 luma_server.py
```

## 📁 **Structure des Fichiers**

```
LUMA-BUSINESS-PRO/
├── luma_interface.html      # Interface web principale
├── luma_server.py          # Serveur backend Python
├── requirements.txt        # Dépendances Python
├── launch_luma.sh         # Script de lancement
├── .env                   # Configuration (à créer)
├── README.md             # Ce guide
└── luma.log             # Logs du système
```

## ⚙️ **Configuration**

### **1. Clés API (obligatoire pour IA complète)**

Éditez le fichier `.env` et ajoutez vos clés :

```bash
# APIs IA
ANTHROPIC_API_KEY=sk-ant-...  # Clé Claude
OPENAI_API_KEY=sk-...         # Clé OpenAI GPT
GEMINI_API_KEY=AIza...        # Clé Google Gemini

# Configuration médicale
MEDICAL_MONITORING=true
EMERGENCY_PHONE=15

# Configuration domotique
HOMEKIT_ENABLED=true
ALEXA_ENABLED=true
```

### **2. Permissions macOS (important !)**

LUMA aura besoin d'autorisations pour :
- 📷 **Caméra** : Surveillance médicale et reconnaissance faciale
- 🎤 **Microphone** : Commandes vocales "Hey Luma"
- 🔔 **Notifications** : Alertes et rappels
- 🔐 **Accessibilité** : Contrôle d'applications (Siri, etc.)

Autorisez ces permissions quand macOS les demande.

### **3. Ollama (IA locale)**

LUMA utilise Ollama pour l'IA locale gratuite :

```bash
# Installation automatique par le script
# Ou installation manuelle :
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull mistral
```

## 🎮 **Utilisation**

### **Démarrage**

```bash
# Démarrage avec menu interactif
./launch_luma.sh

# Ou démarrage direct
./launch_luma.sh --start
```

### **Interface Web**

Ouvrez votre navigateur : **http://127.0.0.1:8080**

### **Commandes Vocales**

- **"Hey Luma"** → Active l'assistant
- **"Mes emails"** → Vérification emails
- **"Mon agenda"** → Consultation planning
- **"Allume les lumières"** → Contrôle domotique
- **"Ventes Shopify"** → Analytics business
- **"Urgence"** → Alerte médicale

### **Interface Chat**

Utilisez l'interface chat pour :
- Questions complexes business
- Création de contenu (posts réseaux sociaux)
- Analyses et stratégies
- Rappels et organisation

## 🏥 **Surveillance Médicale**

### **Fonctionnalités**

- **Monitoring biométrique** : Fréquence cardiaque, température, respiration
- **Détection épilepsie** : Analyse des mouvements et signaux vitaux
- **Alerte automatique** : Appel secours + contacts d'urgence
- **Historique médical** : Suivi des données dans le temps

### **Configuration Urgence**

Modifiez les contacts d'urgence dans `.env` :

```bash
EMERGENCY_CONTACTS='[
  {"name": "SAMU", "number": "15", "type": "emergency"},
  {"name": "Dr. Martin", "number": "+33612345678", "type": "doctor"},
  {"name": "Famille", "number": "+33687654321", "type": "family"}
]'
```

### **Déclenchement Manuel**

- Interface web : Bouton "🚨 APPEL D'URGENCE"
- Vocal : "Hey Luma, urgence !"
- API : `POST /api/emergency/trigger`

## 🏡 **Contrôle Domotique**

### **Appareils Supportés**

- **HomeKit** : Tous les appareils Apple Home
- **Philips Hue** : Éclairage intelligent
- **Alexa** : Contrôle via Echo/Dot
- **Aspirateurs robots** : Roomba, etc.
- **Caméras sécurité** : IP et WiFi
- **Thermostats** : Nest, Ecobee, etc.

### **Scènes Automatiques**

- **🌅 Réveil** : Lumière douce + musique + température optimale
- **🌆 Soirée** : Ambiance chaleureuse + sécurité
- **🌙 Sommeil** : Extinction progressive + surveillance nocturne
- **🚪 Absence** : Mode sécurité + économie d'énergie

### **Commandes Vocales Domotique**

```
"Hey Luma, allume le salon"
"Hey Luma, active la scène soirée" 
"Hey Luma, règle la température à 22 degrés"
"Hey Luma, lance l'aspirateur"
```

## 📊 **Business Analytics**

### **Métriques Suivies**

- **Revenus** : Journaliers, mensuels, objectifs
- **Commandes** : Volume, taux de conversion, panier moyen
- **Clients** : Nouveaux, satisfaction, rétention
- **Inventory** : Stock faible, ruptures
- **Marketing** : Paniers abandonnés, engagement social

### **Intégrations**

- **Shopify** : Ventes et analytics e-commerce
- **Gmail** : Suivi emails clients et prospects
- **Google Analytics** : Trafic web et conversions
- **Réseaux sociaux** : Instagram, LinkedIn, Facebook

### **Recommendations IA**

LUMA analyse vos données et suggère :
- Relancer les paniers abandonnés
- Contacter les clients inactifs
- Créer du contenu pour les produits performants
- Optimiser les campagnes marketing

## 🧠 **Intelligence Artificielle**

### **Modèles Utilisés**

1. **Claude 3.5 Sonnet** : Stratégie, analyses complexes, rédaction
2. **GPT-4** : Conversations naturelles, créativité
3. **Gemini Pro** : Analyse de données, recherche
4. **Mistral (Local)** : Tâches simples, confidentialité

### **Routage Intelligent**

LUMA choisit automatiquement le meilleur modèle :
- **Questions simples** → Mistral local (gratuit)
- **Conversations** → GPT-4 (naturel)
- **Analyses business** → Claude (expert)
- **Créativité** → Gemini (innovant)

### **Apprentissage Personnalisé**

- Mémorisation de vos préférences
- Adaptation à votre style de communication
- Suggestions proactives basées sur vos habitudes
- Amélioration continue des réponses

## 🔧 **API et Intégrations**

### **Endpoints Principaux**

```bash
# Statut système
GET /api/status

# Chat IA
POST /api/ai/chat
{
  "message": "Bonjour LUMA",
  "context": {"user": "Anne-Sophie"}
}

# Contrôle domotique
POST /api/domotic/control
{
  "device": "lights",
  "action": "set_brightness", 
  "value": {"room": "salon", "brightness": 75}
}

# Données médicales
GET /api/medical/status

# Analytics business
GET /api/business/dashboard

# Alerte urgence
POST /api/emergency/trigger
```

### **WebSocket Temps Réel**

```javascript
// Connexion WebSocket pour mises à jour temps réel
const socket = io('http://127.0.0.1:8080');

socket.on('medical_update', (data) => {
  // Mise à jour données médicales
});

socket.on('business_update', (data) => {
  // Mise à jour métriques business
});
```

## 🛠️ **Maintenance et Logs**

### **Logs Système**

```bash
# Voir les logs en temps réel
tail -f luma.log

# Ou via le script
./launch_luma.sh
# → Choix 6: Logs LUMA
```

### **Monitoring Santé**

```bash
# Vérification système
./launch_luma.sh
# → Choix 3: Vérification système
```

### **Sauvegarde**

Sauvegardez régulièrement :
- Fichier `.env` (configuration)
- Fichier `luma.log` (historique)
- Données médicales (si stockées localement)

## 🔒 **Sécurité et Confidentialité**

### **Données Locales**

- **IA locale** : Mistral via Ollama (aucune donnée envoyée)
- **Surveillance médicale** : Traitement 100% local
- **Logs** : Stockés uniquement sur votre Mac

### **Données Cloud**

- **APIs IA** : Claude, GPT, Gemini (selon utilisation)
- **Intégrations** : Shopify, Gmail (avec vos autorisations)
- **Chiffrement** : Toutes les communications sécurisées

### **Contrôle Total**

- Désactivez les modules non souhaités
- Configurez les niveaux de confidentialité
- Contrôlez quelles données sont partagées

## ❓ **Dépannage**

### **Problèmes Courants**

**LUMA ne démarre pas :**
```bash
# Vérifiez Python
python3 --version

# Réinstallez les dépendances
./launch_luma.sh
# → Choix 4: Réinstallation dépendances
```

**Reconnaissance vocale ne fonctionne pas :**
- Vérifiez les permissions microphone dans Préférences Système
- Testez avec "Hey Luma" prononcé clairement
- Vérifiez que PyAudio est installé

**Interface web inaccessible :**
- Vérifiez que le port 8080 est libre
- Essayez http://127.0.0.1:8080 dans le navigateur
- Redémarrez LUMA

**Surveillance médicale inactive :**
- Autorisez l'accès caméra
- Vérifiez que OpenCV est installé
- Contrôlez les logs pour erreurs

### **Support**

- **Logs détaillés** : `luma.log`
- **Mode debug** : Modifiez `LUMA_DEBUG=true` dans `.env`
- **Réinstallation complète** : Supprimez `venv/` et relancez

## 🚀 **Développement Avancé**

### **Extension de LUMA**

LUMA est conçu pour être extensible :

```python
# Ajout de nouveaux modules
class CustomModule:
    def __init__(self, config):
        self.config = config
    
    def process_request(self, data):
        # Votre logique personnalisée
        return result

# Intégration dans le serveur principal
server.add_module('custom', CustomModule(config))
```

### **APIs Personnalisées**

```python
@app.route('/api/custom/endpoint', methods=['POST'])
def custom_endpoint():
    # Votre endpoint personnalisé
    return jsonify(result)
```

## 📈 **Évolutions Futures**

- **IA Vision** : Reconnaissance d'objets et analyse d'images
- **Intégrations étendues** : Plus d'APIs business et domotique
- **ML Personnel** : Modèles entraînés sur vos données
- **Interface 3D** : Visualisations avancées des données
- **Mobile App** : Application iOS/Android native

## 📄 **Licence et Crédits**

LUMA Business Pro - Assistant IA Personnel
Développé avec ❤️ pour optimiser votre productivité et votre sécurité.

**Technologies utilisées :**
- Python 3.8+ & Flask
- OpenCV & NumPy (vision)
- Anthropic Claude, OpenAI GPT, Google Gemini
- Ollama & Mistral (IA locale)
- WebSocket temps réel
- Interface Glassmorphism moderne

---

🤖 **LUMA vous accompagne 24/7 pour un business plus intelligent et une sécurité optimale !** 🚀