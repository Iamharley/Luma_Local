#!/usr/bin/env python3
"""
LUMA BUSINESS PRO - Assistant IA Hybride
Créé par Claude pour optimiser votre business
"""

import os
import subprocess
import requests
import json
from datetime import datetime
import webbrowser

class LumaBusinessPro:
    def __init__(self):
        self.name = "Luma Business Pro"
        self.version = "1.0.0"
        self.claude_api_key = "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"
        
    def speak(self, message):
        """Fait parler l'assistant"""
        print(f"🤖 {self.name}: {message}")
        os.system(f'say "{message}"')
    
    def claude_api_call(self, prompt):
        """Appel à Claude API pour tâches complexes"""
        try:
            headers = {
                'x-api-key': self.claude_api_key,
                'content-type': 'application/json',
                'anthropic-version': '2023-06-01'
            }
            
            data = {
                'model': 'claude-3-sonnet-20240229',
                'max_tokens': 1000,
                'messages': [{'role': 'user', 'content': prompt}]
            }
            
            response = requests.post('https://api.anthropic.com/v1/messages', 
                                   headers=headers, json=data)
            
            if response.status_code == 200:
                return response.json()['content'][0]['text']
            else:
                return "Erreur API Claude"
                
        except Exception as e:
            return f"Erreur: {e}"
    
    def luma_local_call(self, prompt):
        """Appel à Luma local pour tâches quotidiennes"""
        try:
            data = {
                'model': 'mistral',
                'prompt': prompt,
                'stream': False
            }
            
            response = requests.post('http://localhost:11434/api/generate', json=data)
            
            if response.status_code == 200:
                return response.json()['response']
            else:
                return "Luma local non disponible"
                
        except Exception as e:
            return f"Erreur Luma: {e}"
    
    def check_emails(self):
        """Vérifie les emails via AppleScript"""
        script = '''
        tell application "Mail"
            set unreadCount to unread count of inbox
            return unreadCount as string
        end tell
        '''
        
        try:
            result = subprocess.run(['osascript', '-e', script], 
                                  capture_output=True, text=True)
            return f"Vous avez {result.stdout.strip()} emails non lus"
        except:
            return "Impossible de vérifier les emails"
    
    def create_reminder(self, task, when="today"):
        """Crée un rappel dans Things"""
        script = f'''
        tell application "Things3"
            make new to do with properties {{name:"{task}", when:date "{when}"}}
        end tell
        '''
        
        try:
            subprocess.run(['osascript', '-e', script])
            return f"Rappel créé: {task}"
        except:
            return "Erreur création rappel"
    
    def open_shopify(self):
        """Ouvre Shopify"""
        webbrowser.open("https://admin.shopify.com")
        return "Shopify ouvert dans le navigateur"
    
    def business_summary(self):
        """Résumé business quotidien"""
        prompt = '''Crée un résumé business quotidien avec:
        - Priorités du jour
        - Métriques à surveiller
        - Actions recommandées
        Format concis et actionnable.'''
        
        return self.claude_api_call(prompt)
    
    def process_command(self, command):
        """Traite les commandes utilisateur"""
        command = command.lower()
        
        if "email" in command:
            return self.check_emails()
        elif "rappel" in command or "reminder" in command:
            return self.create_reminder("Nouvelle tâche")
        elif "shopify" in command:
            return self.open_shopify()
        elif "résumé" in command or "summary" in command:
            return self.business_summary()
        elif "aide" in command or "help" in command:
            return self.show_commands()
        else:
            # Utilise Luma local pour questions générales
            return self.luma_local_call(command)
    
    def show_commands(self):
        """Affiche les commandes disponibles"""
        commands = '''
🤖 COMMANDES LUMA BUSINESS PRO:

📧 "email" - Vérifier emails
📝 "rappel [tâche]" - Créer rappel
🛒 "shopify" - Ouvrir Shopify
📊 "résumé" - Résumé business
❓ "aide" - Cette aide

💬 Toute autre question = Luma local
        '''
        return commands
    
    def start(self):
        """Démarre l'assistant"""
        self.speak("Bonjour ! Luma Business Pro est prêt !")
        print(self.show_commands())
        
        while True:
            try:
                user_input = input("\n🎯 Votre commande: ")
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    self.speak("À bientôt ! Bonne productivité !")
                    break
                
                response = self.process_command(user_input)
                print(f"\n✅ Réponse: {response}\n")
                
            except KeyboardInterrupt:
                self.speak("Assistant arrêté. À bientôt !")
                break

if __name__ == "__main__":
    assistant = LumaBusinessPro()
    assistant.start()
