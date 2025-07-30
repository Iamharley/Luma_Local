#!/usr/bin/env python3
"""
Test complet de LUMA BUSINESS PRO
Vérifie toutes les fonctionnalités principales
"""

import requests
import subprocess
import os
import json
from datetime import datetime

class LumaTester:
    def __init__(self):
        self.tests_passed = 0
        self.tests_total = 0
        
    def test_ollama_connection(self):
        """Test 1: Vérification d'Ollama"""
        print("🧪 Test 1: Connexion Ollama...")
        try:
            response = requests.post('http://localhost:11434/api/generate', 
                                   json={'model': 'mistral', 'prompt': 'Test', 'stream': False})
            if response.status_code == 200:
                print("✅ Ollama fonctionne")
                self.tests_passed += 1
            else:
                print("❌ Ollama ne répond pas")
        except Exception as e:
            print(f"❌ Erreur Ollama: {e}")
        self.tests_total += 1
    
    def test_luma_local_response(self):
        """Test 2: Réponse de Luma Local"""
        print("🧪 Test 2: Réponse Luma Local...")
        try:
            response = requests.post('http://localhost:11434/api/generate',
                                   json={'model': 'mistral', 
                                         'prompt': 'Dis-moi bonjour en français', 
                                         'stream': False})
            if response.status_code == 200:
                result = response.json()
                if 'bonjour' in result['response'].lower() or 'salut' in result['response'].lower():
                    print("✅ Luma Local répond en français")
                    self.tests_passed += 1
                else:
                    print("❌ Luma Local ne répond pas en français")
            else:
                print("❌ Luma Local ne répond pas")
        except Exception as e:
            print(f"❌ Erreur Luma Local: {e}")
        self.tests_total += 1
    
    def test_system_integrations(self):
        """Test 3: Intégrations système"""
        print("🧪 Test 3: Intégrations système...")
        integrations_ok = 0
        total_integrations = 3
        
        # Test AppleScript
        try:
            result = subprocess.run(['osascript', '-e', 'return "test"'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ AppleScript fonctionne")
                integrations_ok += 1
            else:
                print("❌ AppleScript ne fonctionne pas")
        except:
            print("❌ AppleScript non disponible")
        
        # Test say (synthèse vocale)
        try:
            result = subprocess.run(['say', 'test'], capture_output=True)
            if result.returncode == 0:
                print("✅ Synthèse vocale fonctionne")
                integrations_ok += 1
            else:
                print("❌ Synthèse vocale ne fonctionne pas")
        except:
            print("❌ Synthèse vocale non disponible")
        
        # Test Python requests
        try:
            import requests
            print("✅ Module requests disponible")
            integrations_ok += 1
        except:
            print("❌ Module requests manquant")
        
        if integrations_ok >= 2:
            print(f"✅ {integrations_ok}/{total_integrations} intégrations fonctionnent")
            self.tests_passed += 1
        else:
            print(f"❌ Seulement {integrations_ok}/{total_integrations} intégrations fonctionnent")
        self.tests_total += 1
    
    def test_file_structure(self):
        """Test 4: Structure des fichiers"""
        print("🧪 Test 4: Structure des fichiers...")
        required_files = [
            'luma-assistant.py',
            'intelligent-reminders.py',
            'start-luma.sh',
            'README.md'
        ]
        
        missing_files = []
        for file in required_files:
            if not os.path.exists(file):
                missing_files.append(file)
        
        if not missing_files:
            print("✅ Tous les fichiers requis sont présents")
            self.tests_passed += 1
        else:
            print(f"❌ Fichiers manquants: {missing_files}")
        self.tests_total += 1
    
    def test_python_dependencies(self):
        """Test 5: Dépendances Python"""
        print("🧪 Test 5: Dépendances Python...")
        required_modules = ['requests', 'schedule', 'json', 'datetime']
        missing_modules = []
        
        for module in required_modules:
            try:
                __import__(module)
            except ImportError:
                missing_modules.append(module)
        
        if not missing_modules:
            print("✅ Toutes les dépendances Python sont installées")
            self.tests_passed += 1
        else:
            print(f"❌ Modules manquants: {missing_modules}")
        self.tests_total += 1
    
    def run_all_tests(self):
        """Lance tous les tests"""
        print("🚀 DÉMARRAGE DES TESTS LUMA BUSINESS PRO")
        print("=" * 50)
        
        self.test_ollama_connection()
        self.test_luma_local_response()
        self.test_system_integrations()
        self.test_file_structure()
        self.test_python_dependencies()
        
        self.print_results()
    
    def print_results(self):
        """Affiche les résultats"""
        print("\n" + "=" * 50)
        print("📊 RÉSULTATS DES TESTS")
        print("=" * 50)
        
        success_rate = (self.tests_passed / self.tests_total) * 100
        
        print(f"✅ Tests réussis: {self.tests_passed}/{self.tests_total}")
        print(f"📈 Taux de succès: {success_rate:.1f}%")
        
        if success_rate >= 80:
            print("🎉 LUMA BUSINESS PRO est prêt à l'emploi !")
            print("💡 Conseil: Lancez 'python3 luma-assistant.py' pour commencer")
        elif success_rate >= 60:
            print("⚠️  LUMA fonctionne partiellement")
            print("🔧 Vérifiez les erreurs ci-dessus")
        else:
            print("❌ LUMA nécessite des corrections")
            print("🔧 Consultez le README.md pour l'installation")
        
        print("\n🚀 Prochaines étapes:")
        print("1. Lancez: ./start-luma.sh")
        print("2. Puis: python3 luma-assistant.py")
        print("3. Testez: 'aide' pour voir les commandes")

if __name__ == "__main__":
    tester = LumaTester()
    tester.run_all_tests() 