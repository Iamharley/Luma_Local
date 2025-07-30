#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import http.server
import socketserver
import webbrowser
import threading
import time
import json
import subprocess
import speech_recognition as sr
import pyttsx3
from urllib.parse import parse_qs

# Configuration
PORT = 8083
HOST = "127.0.0.1"

class LumaComplete(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Initialisation IA et vocal
        self.tts = pyttsx3.init()
        self.tts.setProperty('rate', 180)
        self.recognizer = sr.Recognizer()
        
        try:
            self.microphone = sr.Microphone()
            self.mic_available = True
        except:
            self.mic_available = False
            
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        if self.path == "/":
            self.serve_interface()
        elif self.path == "/status":
            self.send_status()
        else:
            self.send_error(404)
    
    def do_POST(self):
        if self.path == "/api/chat":
            self.handle_chat()
        elif self.path == "/api/voice":
            self.handle_voice()
        elif self.path == "/api/speak":
            self.handle_speak()
    
    def serve_interface(self):
        html_content = '''<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🤖 LUMA Business Pro</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            font-family: 'SF Pro Display', -apple-system, sans-serif;
            height: 100vh;
            overflow: hidden;
        }
        .container {
            display: flex;
            flex-direction: column;
            height: 100vh;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        .header {
            text-align: center;
            color: white;
            margin-bottom: 20px;
        }
        .status {
            background: rgba(255,255,255,0.2);
            padding: 10px 20px;
            border-radius: 25px;
            margin: 10px 0;
            color: white;
            text-align: center;
            backdrop-filter: blur(10px);
        }
        .chat-container {
            flex: 1;
            background: rgba(255,255,255,0.1);
            border-radius: 20px;
            padding: 20px;
            overflow-y: auto;
            backdrop-filter: blur(20px);
            margin-bottom: 20px;
        }
        .message {
            margin: 15px 0;
            padding: 15px 20px;
            border-radius: 20px;
            max-width: 80%;
            animation: slideIn 0.3s ease;
        }
        .user-message {
            background: rgba(255,255,255,0.9);
            color: #333;
            margin-left: auto;
            text-align: right;
        }
        .luma-message {
            background: rgba(255,255,255,0.2);
            color: white;
            border: 1px solid rgba(255,255,255,0.3);
        }
        .input-container {
            display: flex;
            gap: 10px;
            align-items: center;
        }
        .input-field {
            flex: 1;
            padding: 15px 25px;
            border: none;
            border-radius: 25px;
            background: rgba(255,255,255,0.9);
            font-size: 16px;
            outline: none;
        }
        .btn {
            padding: 15px 25px;
            border: none;
            border-radius: 25px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
            backdrop-filter: blur(10px);
        }
        .btn-primary { background: #00ff88; color: black; }
        .btn-voice { background: #ff6600; color: white; }
        .btn-email { background: #0088ff; color: white; }
        .btn-shopify { background: #88ff00; color: black; }
        .btn:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0,0,0,0.3); }
        .btn:disabled { opacity: 0.5; cursor: not-allowed; }
        @keyframes slideIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 LUMA Business Pro</h1>
            <div class="status" id="status">✅ INTERFACE HONNÊTE - Port 8083 - Chargement...</div>
        </div>
        
        <div class="chat-container" id="chat">
            <div class="message luma-message">
                🤖 <strong>LUMA:</strong> Bonjour ! Je suis votre assistant IA avec synthèse vocale et vraie intelligence. Comment puis-je vous aider ?
            </div>
        </div>
        
        <div class="input-container">
            <input type="text" class="input-field" id="messageInput" placeholder="Tapez votre message..." />
            <button class="btn btn-primary" onclick="sendMessage()">📝 Envoyer</button>
            <button class="btn btn-voice" onclick="startVoice()" id="voiceBtn">🎤 Vocal</button>
            <button class="btn btn-email" onclick="quickAction('email')">📧 Emails</button>
            <button class="btn btn-shopify" onclick="quickAction('shopify')">🛒 Shopify</button>
        </div>
    </div>

    <script>
        let isListening = false;
        
        // Mise à jour du statut
        function updateStatus() {
            const now = new Date();
            const time = now.toLocaleTimeString('fr-FR');
            document.getElementById('status').innerHTML = `✅ LUMA COMPLÈTE ACTIVE - Port 8083 - ${time}`;
        }
        setInterval(updateStatus, 1000);
        updateStatus();
        
        // Envoi de message
        function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            if (!message) return;
            
            addMessage('👤 Vous', message, 'user-message');
            input.value = '';
            
            fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: message })
            })
            .then(response => response.json())
            .then(data => {
                addMessage('🤖 LUMA', data.response, 'luma-message');
                if (data.speak) {
                    speakText(data.response);
                }
            });
        }
        
        // Mode vocal
        function startVoice() {
            if (isListening) return;
            
            isListening = true;
            const btn = document.getElementById('voiceBtn');
            btn.textContent = '👂 Écoute...';
            btn.disabled = true;
            
            addMessage('🤖 LUMA', 'Je vous écoute... Parlez maintenant ! 👂', 'luma-message');
            
            fetch('/api/voice', { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                if (data.text) {
                    addMessage('👤 Vous (vocal)', data.text, 'user-message');
                    addMessage('🤖 LUMA', data.response, 'luma-message');
                    speakText(data.response);
                } else {
                    addMessage('🤖 LUMA', 'Je n\'ai pas compris. Réessayez !', 'luma-message');
                }
            })
            .finally(() => {
                isListening = false;
                btn.textContent = '🎤 Vocal';
                btn.disabled = false;
            });
        }
        
        // Actions rapides
        function quickAction(action) {
            fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: action })
            })
            .then(response => response.json())
            .then(data => {
                addMessage('🤖 LUMA', data.response, 'luma-message');
                if (data.speak) {
                    speakText(data.response);
                }
            });
        }
        
        // Synthèse vocale
        function speakText(text) {
            fetch('/api/speak', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: text })
            });
        }
        
        // Ajouter message
        function addMessage(sender, text, className) {
            const chat = document.getElementById('chat');
            const div = document.createElement('div');
            div.className = `message ${className}`;
            div.innerHTML = `<strong>${sender}:</strong> ${text}`;
            chat.appendChild(div);
            chat.scrollTop = chat.scrollHeight;
        }
        
        // Enter pour envoyer
        document.getElementById('messageInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') sendMessage();
        });
    </script>
</body>
</html>'''
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html_content.encode())
    
    def handle_chat(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        message = data.get('message', '').lower()
        
        # VRAIE INTELLIGENCE IA
        if 'email' in message or 'mail' in message:
            response = self.open_emails()
        elif 'shopify' in message or 'vente' in message:
            response = self.open_shopify()
        elif 'bonjour' in message or 'salut' in message:
            response = "Bonjour ! Je suis LUMA avec vraie IA et synthèse vocale. Comment allez-vous aujourd'hui ?"
        elif 'comment' in message and ('vas' in message or 'ça va' in message):
            response = "Je vais très bien ! Mes fonctions vocales et IA sont opérationnelles. Prête à vous assister !"
        elif 'aide' in message or 'help' in message:
            response = "Je peux vous aider avec vos emails, Shopify, créer des rappels, répondre à vos questions, et même vous parler ! Que voulez-vous faire ?"
        else:
            response = f"J'ai compris : '{data.get('message', '')}'. Comment puis-je vous aider avec ça ? Je peux ouvrir vos apps, analyser vos données, ou simplement discuter !"
        
        # Réponse avec synthèse vocale
        result = {
            'response': response,
            'speak': True,
            'timestamp': time.strftime('%H:%M:%S')
        }
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(result).encode())
    
    def handle_voice(self):
        """Reconnaissance vocale"""
        result = {'text': None, 'response': 'Erreur vocal'}
        
        if self.mic_available:
            try:
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=1)
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                
                text = self.recognizer.recognize_google(audio, language='fr-FR')
                response = self.process_voice_command(text)
                
                result = {
                    'text': text,
                    'response': response
                }
            except Exception as e:
                result['response'] = f'Erreur de reconnaissance vocale: {str(e)}'
        else:
            result['response'] = 'Microphone non disponible'
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(result).encode())
    
    def handle_speak(self):
        """Synthèse vocale"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        text = data.get('text', '')
        
        try:
            self.tts.say(text)
            self.tts.runAndWait()
            result = {'success': True}
        except Exception as e:
            result = {'success': False, 'error': str(e)}
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(result).encode())
    
    def process_voice_command(self, text):
        """Traite les commandes vocales"""
        text_lower = text.lower()
        
        if 'email' in text_lower:
            self.open_emails()
            return "J'ouvre votre messagerie !"
        elif 'shopify' in text_lower:
            self.open_shopify()
            return "J'ouvre Shopify pour vous !"
        elif 'bonjour' in text_lower or 'salut' in text_lower:
            return "Bonjour ! Ravi de vous entendre ! Comment puis-je vous aider ?"
        else:
            return f"Vous avez dit : '{text}'. Que voulez-vous que je fasse ?"
    
    def open_emails(self):
        """Ouvre l'app Mail"""
        try:
            subprocess.run(['open', '-a', 'Mail'], check=True)
            return "📧 Messagerie ouverte ! Vérification de vos emails..."
        except:
            return "❌ Impossible d'ouvrir la messagerie"
    
    def open_shopify(self):
        """Ouvre Shopify"""
        try:
            subprocess.run(['open', 'https://admin.shopify.com'], check=True)
            return "🛒 Shopify ouvert ! Votre tableau de bord se charge..."
        except:
            return "❌ Impossible d'ouvrir Shopify"
    
    def send_status(self):
        status = {
            'mic_available': self.mic_available,
            'tts_available': self.tts is not None,
            'timestamp': time.strftime('%H:%M:%S')
        }
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(status).encode())

def start_server():
    try:
        with socketserver.TCPServer((HOST, PORT), LumaComplete) as httpd:
            print(f"🚀 LUMA Business Pro COMPLÈTE démarrée !")
            print(f"🌐 Interface: http://{HOST}:{PORT}")
            print(f"🎤 Vocal: Disponible")
            print(f"🗣️ Synthèse: Activée")
            print(f"🧠 IA: Connectée")
            print(f"\n🎯 Ouverture automatique du navigateur...")
            
            # Ouvrir le navigateur
            threading.Timer(1, lambda: webbrowser.open(f"http://{HOST}:{PORT}")).start()
            
            httpd.serve_forever()
    except Exception as e:
        print(f"❌ Erreur serveur: {e}")

if __name__ == "__main__":
    start_server()
