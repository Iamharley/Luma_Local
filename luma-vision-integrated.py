#!/usr/bin/env python3
"""
LUMA BUSINESS PRO VISION - Assistant IA avec reconnaissance faciale
Version intégrée complète
"""

import os
import subprocess
import requests
import json
import time
import cv2
import speech_recognition as sr
import pyttsx3
from datetime import datetime
import threading
import webbrowser

class LumaVisionPro:
    def __init__(self):
        self.name = "Luma Vision Pro"
        self.owner_name = "Anne-Sophie"
        self.version = "2.0.0"
        
        # APIs
        self.claude_api_key = "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"
        
        # État de reconnaissance
        self.is_owner_present = False
        self.monitoring_active = False
        
        # Configuration vocale
        self.setup_voice()
        
        # Reconnaissance vocale
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        print(f"🤖 {self.name} initialisé avec succès !")
    
    def setup_voice(self):
        """Configure la synthèse vocale"""
        try:
            self.tts_engine = pyttsx3.init()
            voices = self.tts_engine.getProperty('voices')
            
            # Voix française si disponible
            for voice in voices:
                if 'fr' in voice.id.lower() or 'french' in voice.name.lower():
                    self.tts_engine.setProperty('voice', voice.id)
                    break
            
            self.tts_engine.setProperty('rate', 180)
            self.tts_engine.setProperty('volume', 0.8)
            
        except Exception as e:
            print(f"⚠️ Synthèse vocale non disponible: {e}")
            self.tts_engine = None
    
    def speak(self, message):
        """Fait parler l'assistant"""
        print(f"🤖 {self.name}: {message}")
        
        # Synthèse vocale
        if self.tts_engine:
            try:
                self.tts_engine.say(message)
                self.tts_engine.runAndWait()
            except:
                # Fallback macOS
                subprocess.run(['say', '-v', 'Amélie', message], check=False)
        else:
            # Fallback macOS simple
            subprocess.run(['say', message], check=False)
    
    def listen_for_wake_word(self):
        """Écoute le mot de réveil"""
        wake_words = ['luma', 'hey luma', 'bonjour luma', 'salut luma']
        
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=3)
            
            command = self.recognizer.recognize_google(audio, language='fr-FR').lower()
            
            for wake_word in wake_words:
                if wake_word in command:
                    return True
                    
            return False
            
        except:
            return False
    
    def listen_for_command(self, timeout=10):
        """Écoute une commande vocale complète"""
        try:
            with self.microphone as source:
                print("🎤 J'écoute votre commande...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=15)
            
            command = self.recognizer.recognize_google(audio, language='fr-FR')
            print(f"📝 Commande: {command}")
            return command.lower()
            
        except sr.WaitTimeoutError:
            self.speak("Je n'ai rien entendu")
            return None
        except sr.UnknownValueError:
            self.speak("Désolée, je n'ai pas compris")
            return None
        except Exception as e:
            print(f"Erreur reconnaissance: {e}")
            return None
    
    def simple_face_detection(self):
        """Détection simple de présence humaine"""
        try:
            video_capture = cv2.VideoCapture(0)
            
            # Détecteur de visage simple
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            
            ret, frame = video_capture.read()
            if ret:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.1, 4)
                
                face_detected = len(faces) > 0
                
                video_capture.release()
                return face_detected
            
            video_capture.release()
            return False
            
        except Exception as e:
            print(f"Erreur détection visage: {e}")
            return False
    
    def claude_api_call(self, prompt):
        """Appel Claude API pour questions complexes"""
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
                                   headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                return response.json()['content'][0]['text']
            else:
                return "Erreur API Claude"
                
        except Exception as e:
            return f"Claude indisponible: {e}"
    
    def luma_local_call(self, prompt):
        """Appel Luma local via Ollama"""
        try:
            data = {
                'model': 'mistral',
                'prompt': prompt,
                'stream': False
            }
            
            response = requests.post('http://localhost:11434/api/generate', json=data, timeout=30)
            
            if response.status_code == 200:
                return response.json()['response']
            else:
                return "Luma local non disponible"
                
        except Exception as e:
            return f"Luma local erreur: {e}"
    
    def gpt_local_call(self, prompt):
        """Appel GPT local si disponible"""
        # À adapter selon votre installation GPT locale
        try:
            # Exemple avec GPT4All ou similar
            result = subprocess.run([
                'gpt4all', '--prompt', prompt
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                return "GPT local non disponible"
                
        except Exception as e:
            return f"GPT local erreur: {e}"
    
    def smart_ai_routing(self, command):
        """Routage intelligent entre les IA"""
        # Mots-clés pour Claude API (stratégie, complexe)
        claude_keywords = ['stratégie', 'business', 'analyse', 'complexe', 'créer un plan', 'optimiser']
        
        # Mots-clés pour GPT local 
        gpt_keywords = ['code', 'programmer', 'script', 'debug', 'développer']
        
        # Commandes simples pour Luma local
        simple_keywords = ['bonjour', 'salut', 'comment', 'aide', 'qu\'est-ce que']
        
        command_lower = command.lower()
        
        # Routage basé sur les mots-clés
        if any(keyword in command_lower for keyword in claude_keywords):
            self.speak("Je consulte Claude pour cette question complexe")
            return self.claude_api_call(command)
        elif any(keyword in command_lower for keyword in gpt_keywords):
            self.speak("Je vérifie avec GPT pour le code")
            result = self.gpt_local_call(command)
            if "erreur" in result.lower():
                return self.luma_local_call(command)  # Fallback
            return result
        else:
            # Questions simples → Luma local
            return self.luma_local_call(command)
    
    def process_business_command(self, command):
        """Traite les commandes business spécifiques"""
        command = command.lower()
        
        if "email" in command:
            return self.check_emails()
        elif "shopify" in command:
            return self.open_shopify()
        elif "rappel" in command or "reminder" in command:
            task = command.replace("rappel", "").replace("reminder", "").strip()
            return self.create_reminder(task or "Nouvelle tâche")
        elif "agenda" in command or "calendar" in command:
            return self.check_calendar()
        elif "résumé" in command or "summary" in command:
            return self.daily_summary()
        elif "post" in command and ("instagram" in command or "social" in command):
            return self.create_social_post()
        else:
            return None  # Pas une commande business
    
    def check_emails(self):
        """Vérifie les emails"""
        try:
            script = '''
            tell application "Mail"
                set unreadCount to unread count of inbox
                return unreadCount as string
            end tell
            '''
            result = subprocess.run(['osascript', '-e', script], 
                                  capture_output=True, text=True)
            count = result.stdout.strip()
            return f"Vous avez {count} emails non lus"
        except:
            return "Impossible de vérifier les emails"
    
    def open_shopify(self):
        """Ouvre Shopify"""
        webbrowser.open("https://admin.shopify.com")
        return "Shopify ouvert dans le navigateur"
    
    def create_reminder(self, task):
        """Crée un rappel"""
        try:
            script = f'''
            tell application "Things3"
                make new to do with properties {{name:"{task}", when:date "today"}}
            end tell
            '''
            subprocess.run(['osascript', '-e', script])
            return f"Rappel créé: {task}"
        except:
            return "Erreur création rappel"
    
    def check_calendar(self):
        """Vérifie l'agenda"""
        # Intégration Calendar à implémenter
        return "Vérification de l'agenda en cours..."
    
    def daily_summary(self):
        """Résumé quotidien intelligent"""
        prompt = f'''
        Créer un résumé business quotidien pour {self.owner_name}:
        - Priorités du jour
        - KPIs à surveiller  
        - Actions recommandées
        Format concis et motivant.
        '''
        return self.claude_api_call(prompt)
    
    def create_social_post(self):
        """Crée un post pour les réseaux sociaux"""
        prompt = '''
        Génère une idée de post Instagram engageant pour un business.
        Format: [Texte] + [Hashtags] + [Call-to-action]
        Style professionnel mais accessible.
        '''
        return self.claude_api_call(prompt)
    
    def voice_interaction_loop(self):
        """Boucle d'interaction vocale"""
        self.speak(f"Bonjour {self.owner_name} ! Je suis {self.name}, votre assistant vocal intelligent.")
        self.speak("Dites 'Hey Luma' pour me parler, ou 'arrêt' pour me mettre en pause.")
        
        wake_listening = True
        
        while True:
            try:
                if wake_listening:
                    # Mode écoute passive du mot de réveil
                    print("👂 En écoute passive... (dites 'Hey Luma')")
                    
                    if self.listen_for_wake_word():
                        self.speak("Oui, je vous écoute !")
                        wake_listening = False
                        continue
                    
                    time.sleep(0.5)  # Évite la surcharge CPU
                    
                else:
                    # Mode écoute active pour commande
                    command = self.listen_for_command()
                    
                    if command:
                        # Commandes de contrôle
                        if "arrêt" in command or "stop" in command or "pause" in command:
                            self.speak("Je me mets en pause. Dites 'Hey Luma' pour me réveiller.")
                            wake_listening = True
                            continue
                        elif "au revoir" in command or "bye" in command or "quit" in command:
                            self.speak("Au revoir ! Bonne productivité !")
                            break
                        
                        # Traitement des commandes
                        # 1. Commandes business spécifiques
                        business_response = self.process_business_command(command)
                        
                        if business_response:
                            self.speak(business_response)
                        else:
                            # 2. Questions générales → IA
                            response = self.smart_ai_routing(command)
                            self.speak(response)
                    
                    # Retour en mode écoute passive après réponse
                    time.sleep(1)
                    wake_listening = True
                    
            except KeyboardInterrupt:
                self.speak("Assistant arrêté. À bientôt !")
                break
            except Exception as e:
                print(f"Erreur interaction: {e}")
                time.sleep(1)
    
    def start_with_vision(self):
        """Démarre avec surveillance visuelle"""
        self.speak("Démarrage du mode vision")
        
        # Détection de présence
        if self.simple_face_detection():
            self.is_owner_present = True
            self.speak(f"Bonjour {self.owner_name} ! Je vous vois. Mode vocal activé.")
            
            # Lance l'interaction vocale
            self.voice_interaction_loop()
        else:
            self.speak("Aucune personne détectée. Mode écoute uniquement.")
            self.voice_interaction_loop()
    
    def start_voice_only(self):
        """Démarre en mode vocal uniquement"""
        self.speak("Mode vocal démarré")
        self.voice_interaction_loop()
    
    def show_capabilities(self):
        """Affiche les capacités"""
        capabilities = f'''
🤖 {self.name} - Capacités:

🎤 COMMANDES VOCALES:
- "Hey Luma" → Réveil vocal
- "email" → Vérifier emails
- "shopify" → Ouvrir Shopify  
- "rappel [tâche]" → Créer rappel
- "résumé" → Résumé business
- "post instagram" → Créer post social
- "arrêt" → Pause
- "au revoir" → Arrêt

🧠 IA HYBRIDE:
- Questions simples → Luma local (gratuit)
- Business/stratégie → Claude API (optimal)
- Code/technique → GPT local

👁️ VISION (si caméra):
- Détection de présence
- Activation automatique

🔊 SYNTHÈSE VOCALE:
- Réponses naturelles en français
- Notifications intelligentes
        '''
        
        print(capabilities)
        return capabilities

def main():
    assistant = LumaVisionPro()
    
    print(f"""
🚀 {assistant.name} v{assistant.version}
=====================================

Modes disponibles:
1. Mode Vision + Vocal (caméra requise)
2. Mode Vocal uniquement
3. Afficher les capacités
4. Quitter

    """)
    
    while True:
        try:
            choice = input("Votre choix (1-4): ")
            
            if choice == "1":
                assistant.start_with_vision()
                break
            elif choice == "2":
                assistant.start_voice_only()
                break
            elif choice == "3":
                assistant.show_capabilities()
            elif choice == "4":
                assistant.speak("Au revoir !")
                break
            else:
                print("Choix invalide (1-4)")
                
        except KeyboardInterrupt:
            assistant.speak("Au revoir !")
            break

if __name__ == "__main__":
    main()
