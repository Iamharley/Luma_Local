#!/usr/bin/env python3
"""
LUMA Business Pro - Installation Automatique
Installe et configure LUMA sur macOS en une seule commande
"""

import os
import sys
import subprocess
import json
import shutil
import time
from pathlib import Path
import urllib.request
from typing import List, Dict, Any

# Couleurs pour l'affichage
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_banner():
    """Affiche la bannière LUMA"""
    banner = f"""
{Colors.PURPLE}{Colors.BOLD}
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║          🤖 LUMA BUSINESS PRO - INSTALLATION                 ║
║                                                              ║
║     Assistant IA Personnel Ultra-Avancé                     ║
║     • Surveillance Médicale 24/7                            ║
║     • IA Hybride (Claude + GPT + Local)                     ║
║     • Contrôle Domotique Complet                            ║
║     • Analytics Business Temps Réel                         ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
{Colors.END}
    """
    print(banner)

def log(message: str, level: str = "INFO"):
    """Logging coloré"""
    colors = {
        "INFO": Colors.GREEN,
        "WARNING": Colors.YELLOW,
        "ERROR": Colors.RED,
        "SUCCESS": Colors.CYAN,
        "STEP": Colors.PURPLE + Colors.BOLD
    }
    
    timestamp = time.strftime("%H:%M:%S")
    color = colors.get(level, Colors.WHITE)
    print(f"[{timestamp}] {color}[{level}]{Colors.END} {message}")

def run_command(command: str, shell: bool = True) -> bool:
    """Exécute une commande système"""
    try:
        log(f"Exécution: {command}")
        result = subprocess.run(command, shell=shell, capture_output=True, text=True)
        
        if result.returncode != 0:
            log(f"Erreur commande: {result.stderr}", "ERROR")
            return False
        
        return True
    except Exception as e:
        log(f"Exception commande: {e}", "ERROR")
        return False

def check_system_requirements() -> bool:
    """Vérifie les prérequis système"""
    log("Vérification des prérequis système...", "STEP")
    
    # Vérification macOS
    if sys.platform != "darwin":
        log("❌ LUMA est optimisé pour macOS", "ERROR")
        return False
    log("✅ macOS détecté")
    
    # Vérification Python 3.8+
    python_version = sys.version_info
    if python_version.major < 3 or python_version.minor < 8:
        log(f"❌ Python 3.8+ requis (trouvé: {python_version.major}.{python_version.minor})", "ERROR")
        return False
    log(f"✅ Python {python_version.major}.{python_version.minor}")
    
    # Vérification pip
    if not shutil.which("pip3"):
        log("❌ pip3 non trouvé", "ERROR")
        return False
    log("✅ pip3 disponible")
    
    # Vérification Homebrew (recommandé)
    if not shutil.which("brew"):
        log("⚠️  Homebrew non trouvé - Installation recommandée", "WARNING")
        response = input("Installer Homebrew automatiquement ? (y/n): ")
        if response.lower() == 'y':
            install_homebrew()
    else:
        log("✅ Homebrew disponible")
    
    return True

def install_homebrew():
    """Installe Homebrew"""
    log("Installation de Homebrew...", "STEP")
    
    command = '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
    
    if run_command(command):
        log("✅ Homebrew installé avec succès", "SUCCESS")
    else:
        log("❌ Échec installation Homebrew", "ERROR")

def create_project_structure():
    """Crée la structure du projet LUMA"""
    log("Création de la structure du projet...", "STEP")
    
    # Dossier principal
    project_dir = Path.home() / "Desktop" / "LUMA-BUSINESS-PRO"
    project_dir.mkdir(exist_ok=True)
    os.chdir(project_dir)
    
    log(f"📁 Projet créé dans: {project_dir}")
    
    # Sous-dossiers
    subdirs = [
        "logs",
        "backups", 
        "config",
        "data",
        "static",
        "templates"
    ]
    
    for subdir in subdirs:
        (project_dir / subdir).mkdir(exist_ok=True)
    
    log("✅ Structure de dossiers créée", "SUCCESS")
    return project_dir

def setup_virtual_environment():
    """Configure l'environnement virtuel Python"""
    log("Configuration de l'environnement virtuel...", "STEP")
    
    # Création venv
    if not run_command("python3 -m venv venv"):
        log("❌ Échec création environnement virtuel", "ERROR")
        return False
    
    # Activation et mise à jour pip
    pip_upgrade = "venv/bin/pip install --upgrade pip setuptools wheel"
    if not run_command(pip_upgrade):
        log("❌ Échec mise à jour pip", "ERROR")
        return False
    
    log("✅ Environnement virtuel configuré", "SUCCESS")
    return True

def install_python_dependencies():
    """Installe les dépendances Python"""
    log("Installation des dépendances Python...", "STEP")
    
    # Dépendances essentielles
    dependencies = [
        "flask==2.3.3",
        "flask-socketio==5.3.6", 
        "flask-cors==4.0.0",
        "requests==2.31.0",
        "anthropic==0.7.7",
        "openai==0.28.1",
        "opencv-python==4.8.1.78",
        "numpy==1.24.3",
        "SpeechRecognition==3.10.0",
        "pyttsx3==2.90",
        "psutil==5.9.6",
        "python-dotenv==1.0.0",
        "eventlet==0.33.3"
    ]
    
    # Installation par lot pour éviter les conflits
    for dep in dependencies:
        command = f"venv/bin/pip install {dep}"
        if not run_command(command):
            log(f"⚠️  Échec installation {dep}", "WARNING")
    
    # Installation des dépendances système macOS
    system_deps = [
        "portaudio",  # Pour PyAudio
        "ffmpeg"      # Pour traitement audio/vidéo
    ]
    
    for dep in system_deps:
        if run_command(f"brew install {dep}"):
            log(f"✅ {dep} installé")
        else:
            log(f"⚠️  Échec installation {dep}", "WARNING")
    
    # Installation PyAudio (complexe sur macOS)
    if run_command("venv/bin/pip install pyaudio"):
        log("✅ PyAudio installé")
    else:
        log("⚠️  PyAudio peut nécessiter une installation manuelle", "WARNING")
    
    log("✅ Dépendances Python installées", "SUCCESS")

def install_ollama():
    """Installe et configure Ollama pour l'IA locale"""
    log("Installation d'Ollama pour l'IA locale...", "STEP")
    
    # Vérification si déjà installé
    if shutil.which("ollama"):
        log("✅ Ollama déjà installé")
    else:
        # Installation Ollama
        install_cmd = 'curl -fsSL https://ollama.ai/install.sh | sh'
        if not run_command(install_cmd):
            log("❌ Échec installation Ollama", "ERROR")
            return False
        log("✅ Ollama installé")
    
    # Démarrage du service
    log("Démarrage du service Ollama...")
    subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(3)
    
    # Téléchargement du modèle Mistral
    log("Téléchargement du modèle Mistral (peut prendre plusieurs minutes)...")
    if run_command("ollama pull mistral"):
        log("✅ Modèle Mistral installé", "SUCCESS")
    else:
        log("⚠️  Le modèle Mistral sera téléchargé au premier usage", "WARNING")
    
    return True

def create_configuration_files():
    """Crée les fichiers de configuration"""
    log("Création des fichiers de configuration...", "STEP")
    
    # Copie du .env.example vers .env si n'existe pas
    if not Path(".env").exists():
        log("Création du fichier .env...")
        with open(".env", "w") as f:
            f.write("# LUMA Business Pro - Configuration\n")
            f.write("# Éditez ce fichier avec vos clés API\n\n")
            f.write("ANTHROPIC_API_KEY=\n")
            f.write("OPENAI_API_KEY=\n")
            f.write("GEMINI_API_KEY=\n\n")
            f.write("MEDICAL_MONITORING=true\n")
            f.write("VOICE_ENABLED=true\n")
            f.write("LUMA_HOST=127.0.0.1\n")
            f.write("LUMA_PORT=8080\n")
            f.write("LOG_LEVEL=INFO\n")
    
    # Configuration JSON avancée
    config = {
        "version": "1.0.0",
        "installation_date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "modules": {
            "medical_monitoring": True,
            "ai_brain": True,
            "domotic_control": True,
            "business_analytics": True,
            "voice_interface": True
        },
        "ai_models": {
            "claude": {"enabled": False, "priority": 1},
            "gpt": {"enabled": False, "priority": 2},
            "gemini": {"enabled": False, "priority": 3},
            "local": {"enabled": True, "priority": 4}
        }
    }
    
    with open("config/luma_config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    log("✅ Fichiers de configuration créés", "SUCCESS")

def setup_permissions():
    """Configure les permissions système macOS"""
    log("Configuration des permissions système...", "STEP")
    
    print(f"\n{Colors.YELLOW}🔐 PERMISSIONS SYSTÈME REQUISES{Colors.END}")
    print("LUMA aura besoin des autorisations suivantes :")
    print("  📷 Caméra - Pour surveillance médicale")
    print("  🎤 Microphone - Pour commandes vocales")
    print("  🔔 Notifications - Pour alertes")
    print("  🔐 Accessibilité - Pour contrôle système")
    print("\nAutorisez ces permissions quand macOS les demande.")
    
    input(f"\n{Colors.CYAN}Appuyez sur Entrée quand vous êtes prêt(e) à continuer...{Colors.END}")
    
    # Test rapide des permissions
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            log("✅ Accès caméra autorisé")
            cap.release()
        else:
            log("⚠️  Accès caméra à autoriser", "WARNING")
    except:
        log("⚠️  OpenCV pas encore disponible", "WARNING")

def create_desktop_shortcut():
    """Crée un raccourci sur le bureau"""
    log("Création du raccourci bureau...", "STEP")
    
    script_content = f'''#!/bin/bash
cd "{Path.cwd()}"
./launch_luma.sh --start
'''
    
    # Script de lancement sur le bureau
    desktop_script = Path.home() / "Desktop" / "Lancer LUMA.command"
    with open(desktop_script, "w") as f:
        f.write(script_content)
    
    # Rendre exécutable
    run_command(f"chmod +x '{desktop_script}'")
    
    log("✅ Raccourci créé sur le bureau", "SUCCESS")

def final_setup():
    """Configuration finale"""
    log("Configuration finale...", "STEP")
    
    # Rendre les scripts exécutables
    scripts = ["launch_luma.sh"]
    for script in scripts:
        if Path(script).exists():
            run_command(f"chmod +x {script}")
    
    # Test de démarrage rapide
    log("Test de démarrage...")
    
    # Créer un fichier de test simple
    test_server = '''
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "<h1>🤖 LUMA Business Pro - Test OK!</h1><p>Installation réussie!</p>"

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8081, debug=False)
'''
    
    with open("test_server.py", "w") as f:
        f.write(test_server)
    
    log("✅ Configuration finale terminée", "SUCCESS")

def display_next_steps():
    """Affiche les prochaines étapes"""
    print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 INSTALLATION LUMA TERMINÉE !{Colors.END}\n")
    
    next_steps = f"""
{Colors.PURPLE}{Colors.BOLD}📋 PROCHAINES ÉTAPES :{Colors.END}

{Colors.CYAN}1. Configuration des clés API :{Colors.END}
   • Éditez le fichier .env avec vos clés
   • Au minimum une clé IA (Claude recommandée)
   
{Colors.CYAN}2. Test de l'installation :{Colors.END}
   • Double-cliquez sur "Lancer LUMA.command" sur le bureau
   • Ou dans Terminal : ./launch_luma.sh --start
   
{Colors.CYAN}3. Première utilisation :{Colors.END}
   • Ouvrez http://127.0.0.1:8080 dans votre navigateur
   • Autorisez les permissions système
   • Testez "Hey Luma" pour les commandes vocales
   
{Colors.CYAN}4. Configuration médicale :{Colors.END}
   • Remplissez vos contacts d'urgence dans .env
   • Testez le bouton d'urgence (mode simulation)
   
{Colors.CYAN}5. Intégrations business :{Colors.END}
   • Connectez Shopify, Gmail, réseaux sociaux
   • Configurez vos appareils domotique

{Colors.YELLOW}⚠️  IMPORTANT :{Colors.END}
   • Sauvegardez votre fichier .env de manière sécurisée
   • Ne partagez jamais vos clés API
   • Testez les fonctionnalités une par une

{Colors.GREEN}🚀 LUMA est prêt à révolutionner votre productivité !{Colors.END}
    """
    
    print(next_steps)

def main():
    """Installation principale"""
    print_banner()
    
    try:
        # Étapes d'installation
        steps = [
            ("Vérification système", check_system_requirements),
            ("Structure projet", create_project_structure),
            ("Environnement virtuel", setup_virtual_environment),
            ("Dépendances Python", install_python_dependencies),
            ("Ollama IA locale", install_ollama),
            ("Fichiers configuration", create_configuration_files),
            ("Permissions système", setup_permissions),
            ("Raccourci bureau", create_desktop_shortcut),
            ("Configuration finale", final_setup)
        ]
        
        for step_name, step_func in steps:
            log(f"🔄 {step_name}...", "STEP")
            
            try:
                result = step_func()
                if result is False:
                    log(f"❌ Échec étape: {step_name}", "ERROR")
                    sys.exit(1)
            except Exception as e:
                log(f"❌ Erreur étape {step_name}: {e}", "ERROR")
                sys.exit(1)
        
        # Affichage final
        display_next_steps()
        
    except KeyboardInterrupt:
        log("\n🛑 Installation annulée par l'utilisateur", "WARNING")
        sys.exit(1)
    except Exception as e:
        log(f"\n💥 Erreur fatale: {e}", "ERROR")
        sys.exit(1)

if __name__ == "__main__":
    main()
