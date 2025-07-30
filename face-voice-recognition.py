#!/usr/bin/env python3
"""
Reconnaissance faciale et vocale pour Luma Business Pro
Créé par Claude pour une interaction naturelle
"""

import cv2
import speech_recognition as sr
import pyttsx3
import face_recognition
import numpy as np
import os
import json
import time
import subprocess
from datetime import datetime

class FaceVoiceAssistant:
    def __init__(self):
        self.name = "Luma Vision"
        self.owner_name = "Anne-Sophie"  # Personnalisable
        self.known_faces = []
        self.known_names = []
        self.face_encodings_file = "known_faces.json"
        
        # Reconnaissance vocale
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Synthèse vocale
        self.tts_engine = pyttsx3.init()
        self.setup_voice()
        
        # État
        self.is_owner_present = False
        self.last_recognition_time = None
        
        # Chargement des visages connus
        self.load_known_faces()
        
    def setup_voice(self):
        """Configure la voix de l'assistant"""
        voices = self.tts_engine.getProperty('voices')
        
        # Cherche une voix féminine française si disponible
        for voice in voices:
            if 'fr' in voice.id.lower() or 'french' in voice.name.lower():
                self.tts_engine.setProperty('voice', voice.id)
                break
        
        # Paramètres vocaux
        self.tts_engine.setProperty('rate', 180)  # Vitesse
        self.tts_engine.setProperty('volume', 0.8)  # Volume
    
    def speak(self, message):
        """Fait parler l'assistant"""
        print(f"🤖 {self.name}: {message}")
        
        # Synthèse vocale Python
        self.tts_engine.say(message)
        self.tts_engine.runAndWait()
        
        # Alternative macOS si problème
        # subprocess.run(['say', '-v', 'Amélie', message])
    
    def listen_for_command(self, timeout=5):
        """Écoute une commande vocale"""
        try:
            with self.microphone as source:
                print("🎤 J'écoute...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
            
            print("🔄 Traitement de la commande...")
            
            # Reconnaissance en français
            command = self.recognizer.recognize_google(audio, language='fr-FR')
            print(f"📝 Commande reconnue: {command}")
            
            return command.lower()
            
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            self.speak("Désolée, je n'ai pas compris")
            return None
        except sr.RequestError as e:
            print(f"Erreur service reconnaissance: {e}")
            return None
    
    def capture_owner_face(self):
        """Capture et enregistre le visage du propriétaire"""
        self.speak(f"Bonjour {self.owner_name} ! Regardez la caméra pour l'enregistrement")
        
        video_capture = cv2.VideoCapture(0)
        
        print("📸 Positionnez-vous face à la caméra...")
        time.sleep(3)
        
        faces_captured = []
        capture_count = 0
        
        while capture_count < 5:  # Capture 5 images
            ret, frame = video_capture.read()
            if not ret:
                continue
                
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)
            
            if face_locations:
                face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
                if face_encodings:
                    faces_captured.append(face_encodings[0].tolist())
                    capture_count += 1
                    print(f"✅ Image {capture_count}/5 capturée")
                    
                    # Affichage avec rectangle
                    for (top, right, bottom, left) in face_locations:
                        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                        cv2.putText(frame, f"Capture {capture_count}/5", (left, top-10), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            
            cv2.imshow('Enregistrement Visage', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        video_capture.release()
        cv2.destroyAllWindows()
        
        if faces_captured:
            self.save_owner_face(faces_captured)
            self.speak("Enregistrement terminé ! Je vous reconnaîtrai maintenant.")
            return True
        else:
            self.speak("Aucun visage détecté. Réessayons.")
            return False
    
    def save_owner_face(self, face_encodings):
        """Sauvegarde les encodages de visage"""
        face_data = {
            'owner_name': self.owner_name,
            'encodings': face_encodings,
            'created_date': datetime.now().isoformat()
        }
        
        with open(self.face_encodings_file, 'w') as f:
            json.dump(face_data, f)
        
        # Recharge les visages connus
        self.load_known_faces()
        
        print(f"✅ Visage de {self.owner_name} enregistré")
    
    def load_known_faces(self):
        """Charge les visages connus"""
        if os.path.exists(self.face_encodings_file):
            try:
                with open(self.face_encodings_file, 'r') as f:
                    face_data = json.load(f)
                
                self.known_names = [face_data['owner_name']]
                self.known_faces = [np.array(encoding) for encoding in face_data['encodings']]
                
                print(f"✅ {len(self.known_faces)} visages chargés")
                
            except Exception as e:
                print(f"Erreur chargement visages: {e}")
                self.known_faces = []
                self.known_names = []
    
    def recognize_face(self, frame):
        """Reconnaît un visage dans une image"""
        if not self.known_faces:
            return None, None
            
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        
        recognized_names = []
        
        for face_encoding in face_encodings:
            # Compare avec les visages connus
            matches = face_recognition.compare_faces(self.known_faces, face_encoding, tolerance=0.6)
            
            name = "Inconnu"
            face_distances = face_recognition.face_distance(self.known_faces, face_encoding)
            
            if matches and len(face_distances) > 0:
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = self.known_names[0]  # Propriétaire
            
            recognized_names.append(name)
        
        return face_locations, recognized_names
    
    def start_monitoring(self):
        """Démarre la surveillance par caméra"""
        self.speak("Surveillance activée. Je vous reconnais maintenant !")
        
        video_capture = cv2.VideoCapture(0)
        
        owner_greeted_today = False
        last_recognition = None
        
        print("👁️ Surveillance active - Appuyez sur 'q' pour arrêter")
        
        while True:
            ret, frame = video_capture.read()
            if not ret:
                continue
            
            # Reconnaissance toutes les 30 frames (optimisation)
            if video_capture.get(cv2.CAP_PROP_POS_FRAMES) % 30 == 0:
                face_locations, names = self.recognize_face(frame)
                
                if face_locations:
                    for (top, right, bottom, left), name in zip(face_locations, names):
                        # Dessine le rectangle
                        color = (0, 255, 0) if name == self.owner_name else (0, 0, 255)
                        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                        cv2.putText(frame, name, (left, top-10), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
                        
                        # Salutation si propriétaire détecté
                        if name == self.owner_name:
                            self.is_owner_present = True
                            current_time = time.time()
                            
                            # Salue une fois par session
                            if not owner_greeted_today or (last_recognition and current_time - last_recognition > 3600):
                                self.greet_owner()
                                owner_greeted_today = True
                            
                            last_recognition = current_time
                        else:
                            self.is_owner_present = False
            
            # Affichage
            cv2.imshow('Luma Vision - Reconnaissance', frame)
            
            # Commandes clavier
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('v'):  # Commande vocale
                if self.is_owner_present:
                    self.process_voice_command()
                else:
                    print("❌ Propriétaire non reconnu")
        
        video_capture.release()
        cv2.destroyAllWindows()
        self.speak("Surveillance arrêtée")
    
    def greet_owner(self):
        """Salue le propriétaire"""
        hour = datetime.now().hour
        
        if 5 <= hour < 12:
            greeting = f"Bonjour {self.owner_name} ! Prête pour une journée productive ?"
        elif 12 <= hour < 18:
            greeting = f"Bon après-midi {self.owner_name} ! Comment puis-je vous aider ?"
        else:
            greeting = f"Bonsoir {self.owner_name} ! Que puis-je faire pour vous ?"
        
        self.speak(greeting)
        
        # Suggestions contextuelles
        suggestions = [
            "Voulez-vous vérifier vos emails ?",
            "Dois-je ouvrir Shopify ?", 
            "Avez-vous des tâches à ajouter ?",
            "Préparer un résumé business ?"
        ]
        
        import random
        suggestion = random.choice(suggestions)
        self.speak(suggestion)
    
    def process_voice_command(self):
        """Traite une commande vocale"""
        self.speak("Je vous écoute")
        
        command = self.listen_for_command()
        
        if command:
            # Import de l'assistant principal
            try:
                from luma_assistant import LumaBusinessPro
                assistant = LumaBusinessPro()
                
                response = assistant.process_command(command)
                self.speak(response)
                
            except ImportError:
                # Commandes de base intégrées
                if "email" in command:
                    self.speak("Vérification des emails en cours")
                    # Code vérification emails
                elif "shopify" in command:
                    self.speak("Ouverture de Shopify")
                    subprocess.run(['open', 'https://admin.shopify.com'])
                elif "rappel" in command or "reminder" in command:
                    self.speak("Rappel créé")
                    # Code création rappel
                else:
                    self.speak(f"Commande reçue: {command}")

# Interface principale
def main():
    assistant = FaceVoiceAssistant()
    
    print("""
🤖 LUMA VISION - Assistant à reconnaissance faciale et vocale

Commandes:
1. Enregistrer votre visage
2. Démarrer la surveillance
3. Test reconnaissance vocale
4. Quitter

    """)
    
    while True:
        choice = input("Votre choix (1-4): ")
        
        if choice == "1":
            assistant.capture_owner_face()
        elif choice == "2":
            assistant.start_monitoring()
        elif choice == "3":
            assistant.speak("Test de reconnaissance vocale")
            command = assistant.listen_for_command()
            if command:
                assistant.speak(f"J'ai compris: {command}")
        elif choice == "4":
            assistant.speak("Au revoir !")
            break
        else:
            print("Choix invalide")

if __name__ == "__main__":
    main()
