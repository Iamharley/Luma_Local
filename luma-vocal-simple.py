#!/usr/bin/env python3
import speech_recognition as sr
import pyttsx3
import subprocess
import time

class LumaSimple:
    def __init__(self):
        self.name = "Luma Simple"
        # Synthèse vocale
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 180)
        self.tts_engine.setProperty('volume', 0.8)
        
        # Reconnaissance vocale
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Ajuster pour le bruit ambiant
        with self.microphone as source:
            print("🎤 Calibrage du microphone...")
            self.recognizer.adjust_for_ambient_noise(source, duration=2)
        
    def speak(self, message):
        print(f"🤖 {self.name}: {message}")
        try:
            self.tts_engine.say(message)
            self.tts_engine.runAndWait()
        except:
            subprocess.run(['say', message], check=False)
    
    def listen_once(self):
        """Écoute UNE FOIS avec timeout plus long"""
        try:
            print("🎤 JE VOUS ÉCOUTE... Parlez maintenant !")
            with self.microphone as source:
                # Timeout plus long et phrase plus longue
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=5)
            
            print("🔄 Analyse de ce que vous avez dit...")
            command = self.recognizer.recognize_google(audio, language='fr-FR')
            print(f"✅ J'ai entendu: {command}")
            return command.lower()
            
        except sr.WaitTimeoutError:
            print("⏰ Temps écoulé, je n'ai rien entendu")
            return None
        except sr.UnknownValueError:
            print("❓ J'ai entendu quelque chose mais pas compris")
            return None
        except Exception as e:
            print(f"❌ Erreur: {e}")
            return None
    
    def process_command(self, command):
        """Traite une commande"""
        if "email" in command:
            return "Vérification de vos emails en cours..."
        elif "shopify" in command:
            subprocess.run(['open', 'https://admin.shopify.com'])
            return "Shopify ouvert dans le navigateur"
        elif "bonjour" in command or "salut" in command:
            return "Bonjour ! Comment puis-je vous aider ?"
        elif "test" in command:
            return "Test réussi ! Je vous entends parfaitement !"
        else:
            return f"J'ai entendu: {command}. Dites 'test' pour vérifier que ça marche !"
    
    def start_simple_mode(self):
        """Mode simple sans boucle"""
        self.speak("Bonjour ! Je suis Luma en mode simple.")
        self.speak("Appuyez sur Entrée puis parlez quand je vous le demande.")
        
        while True:
            try:
                input("\n[Appuyez sur ENTRÉE pour parler, ou tapez 'quit' pour arrêter]: ")
                
                if input == 'quit':
                    break
                
                # Écoute une fois
                command = self.listen_once()
                
                if command:
                    if "quit" in command or "au revoir" in command:
                        self.speak("Au revoir !")
                        break
                    
                    # Traite la commande
                    response = self.process_command(command)
                    self.speak(response)
                else:
                    self.speak("Je n'ai pas bien entendu. Réessayons.")
                    
            except KeyboardInterrupt:
                self.speak("Au revoir !")
                break

if __name__ == "__main__":
    assistant = LumaSimple()
    assistant.start_simple_mode()
