#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import speech_recognition as sr
import pyttsx3
import sys

class LumaVocalFixed:
    def __init__(self):
        print('🎤 Initialisation de Luma Vocal...')
        self.recognizer = sr.Recognizer()
        try:
            self.microphone = sr.Microphone()
            print('✅ Microphone detecte')
        except Exception as e:
            print(f'❌ Erreur microphone: {e}')
            self.microphone = None
            
        self.tts = pyttsx3.init()
        self.tts.setProperty('rate', 200)
        
    def speak(self, text):
        print(f'🗣️ Luma: {text}')
        try:
            self.tts.say(text)
            self.tts.runAndWait()
        except Exception as e:
            print(f'❌ Erreur vocal: {e}')
    
    def listen_once(self):
        if not self.microphone:
            return 'test'
            
        try:
            print('👂 J\'ecoute...')
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            text = self.recognizer.recognize_google(audio, language='fr-FR')
            print(f'👤 Vous avez dit: {text}')
            return text.lower()
            
        except sr.WaitTimeoutError:
            print('⏰ Timeout - rien entendu')
            return None
        except Exception as e:
            print(f'❌ Erreur ecoute: {e}')
            return None
    
    def start_test(self):
        self.speak('Luma Vocal est pret !')
        print('Test vocal termine !')

if __name__ == '__main__':
    assistant = LumaVocalFixed()
    assistant.start_test()
