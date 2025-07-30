#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
import speech_recognition as sr
import pyttsx3
import subprocess
import sys

class LumaApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('🤖 LUMA - Votre Assistant IA')
        self.window.geometry('600x500')
        self.window.configure(bg='#1a1a1a')
        
        # Initialisation vocal
        self.recognizer = sr.Recognizer()
        self.tts = pyttsx3.init()
        self.tts.setProperty('rate', 180)
        
        try:
            self.microphone = sr.Microphone()
            self.mic_available = True
        except:
            self.mic_available = False
        
        self.setup_ui()
        
    def setup_ui(self):
        # Titre
        title = tk.Label(self.window, text='🤖 LUMA ASSISTANT', 
                        font=('Arial', 20, 'bold'), 
                        fg='#00ff88', bg='#1a1a1a')
        title.pack(pady=10)
        
        # Status
        status_text = 'Micro disponible ✅' if self.mic_available else 'Micro indisponible ❌'
        self.status = tk.Label(self.window, text=status_text,
                              font=('Arial', 10), 
                              fg='#888', bg='#1a1a1a')
        self.status.pack()
        
        # Chat area
        self.chat_area = scrolledtext.ScrolledText(self.window, 
                                                  width=70, height=20,
                                                  bg='#2a2a2a', fg='white',
                                                  font=('Arial', 11))
        self.chat_area.pack(pady=10, padx=20, fill='both', expand=True)
        
        # Entry et boutons
        input_frame = tk.Frame(self.window, bg='#1a1a1a')
        input_frame.pack(pady=10, padx=20, fill='x')
        
        self.entry = tk.Entry(input_frame, font=('Arial', 12), 
                             bg='#3a3a3a', fg='white', insertbackground='white')
        self.entry.pack(side='left', fill='x', expand=True)
        self.entry.bind('<Return>', self.send_text)
        
        # Boutons
        button_frame = tk.Frame(self.window, bg='#1a1a1a')
        button_frame.pack(pady=5)
        
        tk.Button(button_frame, text='📝 Envoyer', command=self.send_text,
                 bg='#00ff88', fg='black', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        
        if self.mic_available:
            tk.Button(button_frame, text='🎤 Vocal', command=self.start_voice,
                     bg='#ff6600', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        
        tk.Button(button_frame, text='📧 Email', command=lambda: self.quick_command('email'),
                 bg='#0088ff', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        
        tk.Button(button_frame, text='🛒 Shopify', command=lambda: self.quick_command('shopify'),
                 bg='#88ff00', fg='black', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        
        # Message de bienvenue
        self.add_message('🤖 LUMA', 'Bonjour ! Je suis votre assistant IA. Tapez votre question ou utilisez les boutons !')
        
    def add_message(self, sender, message):
        self.chat_area.insert(tk.END, f'{sender}: {message}

')
        self.chat_area.see(tk.END)
        
    def speak(self, text):
        try:
            self.tts.say(text)
            self.tts.runAndWait()
        except:
            pass
            
    def send_text(self, event=None):
        message = self.entry.get().strip()
        if not message:
            return
            
        self.entry.delete(0, tk.END)
        self.add_message('👤 Vous', message)
        
        # Réponse simple
        response = self.process_message(message)
        self.add_message('🤖 LUMA', response)
        
        # Parler la réponse
        threading.Thread(target=self.speak, args=(response,), daemon=True).start()
        
    def process_message(self, message):
        message = message.lower()
        
        if 'bonjour' in message or 'salut' in message:
            return 'Bonjour ! Comment allez-vous ? En quoi puis-je vous aider ?'
        elif 'email' in message:
            self.open_email()
            return 'J\'ouvre votre messagerie !'
        elif 'shopify' in message:
            self.open_shopify()
            return 'J\'ouvre Shopify pour vous !'
        elif 'comment' in message and 'vas' in message:
            return 'Je vais très bien, merci ! Prête à vous aider avec votre business !'
        elif 'aide' in message or 'help' in message:
            return 'Je peux vous aider avec vos emails, Shopify, créer des rappels, ou répondre à vos questions !'
        else:
            return f'Vous avez dit : "{message}". Comment puis-je vous aider avec ça ?'
            
    def quick_command(self, command):
        if command == 'email':
            self.add_message('🤖 LUMA', 'Ouverture de votre messagerie...')
            self.open_email()
        elif command == 'shopify':
            self.add_message('🤖 LUMA', 'Ouverture de Shopify...')
            self.open_shopify()
            
    def open_email(self):
        try:
            subprocess.run(['open', '-a', 'Mail'])
        except:
            pass
            
    def open_shopify(self):
        try:
            subprocess.run(['open', 'https://admin.shopify.com'])
        except:
            pass
            
    def start_voice(self):
        if not self.mic_available:
            messagebox.showerror('Erreur', 'Microphone non disponible')
            return
            
        self.add_message('🤖 LUMA', 'Je vous écoute... 👂')
        threading.Thread(target=self.listen_voice, daemon=True).start()
        
    def listen_voice(self):
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            text = self.recognizer.recognize_google(audio, language='fr-FR')
            self.add_message('👤 Vous (vocal)', text)
            
            response = self.process_message(text)
            self.add_message('🤖 LUMA', response)
            self.speak(response)
            
        except sr.WaitTimeoutError:
            self.add_message('🤖 LUMA', 'Je n\'ai rien entendu. Réessayez !')
        except sr.UnknownValueError:
            self.add_message('🤖 LUMA', 'Je n\'ai pas compris. Pouvez-vous répéter ?')
        except Exception as e:
            self.add_message('🤖 LUMA', f'Erreur vocal: {str(e)}')
            
    def run(self):
        self.window.mainloop()

if __name__ == '__main__':
    app = LumaApp()
    app.run()
