#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import http.server
import socketserver
import webbrowser
import threading
import json
import subprocess
import time

PORT = 8083

class LumaFixed(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.tts = None
        try:
            import pyttsx3
            self.tts = pyttsx3.init()
            self.tts.setProperty('rate', 180)
        except:
            pass
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        if self.path == '/':
            self.serve_interface()
        else:
            self.send_error(404)
    
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            if self.path == '/api/chat':
                self.handle_chat(data)
            elif self.path == '/api/speak':
                self.handle_speak(data)
        except Exception as e:
            self.send_response(500)
            self.end_headers()
    
    def serve_interface(self):
        html = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>🤖 LUMA - Assistant IA</title>
    <style>
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            font-family: -apple-system, sans-serif;
            color: white;
            margin: 0;
            height: 100vh;
            display: flex;
            flex-direction: column;
        }
        .header {
            text-align: center;
            padding: 20px;
        }
        .header h1 { font-size: 3rem; margin: 10px 0; }
        .status {
            background: #00ff88;
            color: black;
            padding: 10px 20px;
            border-radius: 20px;
            display: inline-block;
            font-weight: bold;
        }
        .chat {
            flex: 1;
            background: rgba(255,255,255,0.1);
            margin: 20px;
            border-radius: 20px;
            padding: 20px;
            overflow-y: auto;
        }
        .message {
            margin: 15px 0;
            padding: 15px;
            border-radius: 15px;
            max-width: 80%;
        }
        .user { background: rgba(255,255,255,0.9); color: black; margin-left: auto; }
        .luma { background: rgba(255,255,255,0.2); border-left: 4px solid #00ff88; }
        .input-area {
            background: rgba(255,255,255,0.1);
            padding: 20px;
            margin: 20px;
            border-radius: 15px;
        }
        .input-row {
            display: flex;
            gap: 10px;
            margin-bottom: 15px;
        }
        #messageInput {
            flex: 1;
            padding: 15px;
            border: none;
            border-radius: 20px;
            font-size: 16px;
        }
        button {
            padding: 15px 25px;
            border: none;
            border-radius: 20px;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.2s;
        }
        button:hover { transform: translateY(-2px); }
        .send-btn { background: #00ff88; color: black; }
        .email-btn { background: #0088ff; color: white; }
        .shopify-btn { background: #88ff00; color: black; }
        .help-btn { background: #ff6600; color: white; }
        .buttons { display: flex; gap: 10px; flex-wrap: wrap; justify-content: center; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🤖 LUMA</h1>
        <div class="status">✅ Assistant IA Complet - Synthèse Vocale Activée</div>
    </div>
    
    <div class="chat" id="messages">
        <div class="message luma">
            <strong>🤖 LUMA :</strong> Bonjour Anne-Sophie ! Je suis votre assistante IA complète. Je peux vous aider avec Harley Vape, vos emails, votre organisation et bien plus ! Tapez votre question ou utilisez les boutons.
        </div>
    </div>
    
    <div class="input-area">
        <div class="input-row">
            <input type="text" id="messageInput" placeholder="Tapez votre message..." />
            <button class="send-btn" onclick="sendMessage()">🚀 Envoyer</button>
        </div>
        <div class="buttons">
            <button class="email-btn" onclick="quickAction('mes emails')">📧 Emails</button>
            <button class="shopify-btn" onclick="quickAction('harley vape')">🛒 Harley Vape</button>
            <button class="help-btn" onclick="quickAction('aide')">💡 Aide</button>
        </div>
    </div>

    <script>
        console.log('JavaScript chargé !');
        
        function sendMessage() {
            console.log('sendMessage appelée');
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            
            if (!message) {
                alert('Tapez un message !');
                return;
            }
            
            console.log('Envoi message:', message);
            addMessage('👤 Vous', message, 'user');
            input.value = '';
            
            fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: message })
            })
            .then(response => {
                console.log('Réponse reçue');
                return response.json();
            })
            .then(data => {
                console.log('Data:', data);
                addMessage('🤖 LUMA', data.response, 'luma');
                if (data.speak) speakText(data.response);
            })
            .catch(error => {
                console.error('Erreur:', error);
                addMessage('🤖 LUMA', 'Erreur : ' + error, 'luma');
            });
        }
        
        function quickAction(action) {
            console.log('quickAction:', action);
            document.getElementById('messageInput').value = action;
            sendMessage();
        }
        
        function addMessage(sender, text, className) {
            const chat = document.getElementById('messages');
            const div = document.createElement('div');
            div.className = 'message ' + className;
            div.innerHTML = '<strong>' + sender + ':</strong> ' + text;
            chat.appendChild(div);
            chat.scrollTop = chat.scrollHeight;
        }
        
        function speakText(text) {
            fetch('/api/speak', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: text })
            });
        }
        
        // Entrée pour envoyer
        document.getElementById('messageInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
        
        // Test au chargement
        document.addEventListener('DOMContentLoaded', function() {
            console.log('DOM chargé');
            document.getElementById('messageInput').focus();
        });
        
        console.log('Script terminé');
    </script>
</body>
</html>'''
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def handle_chat(self, data):
        message = data.get('message', '').lower()
        
        if 'harley' in message or 'vape' in message or 'shopify' in message:
            subprocess.run(['open', 'https://admin.shopify.com'], check=False)
            response = "🛒 Shopify Harley Vape ouvert ! Comment puis-je optimiser vos ventes aujourd'hui ?"
        elif 'email' in message:
            subprocess.run(['open', '-a', 'Mail'], check=False)  
            response = "📧 Messagerie ouverte ! Je peux vous aider à organiser vos emails."
        elif 'aide' in message:
            response = "💡 Je peux vous aider avec : Harley Vape (Shopify), vos emails, organisation, stratégies business. Que voulez-vous faire ?"
        elif 'bonjour' in message or 'salut' in message:
            response = "Bonjour Anne-Sophie ! Comment puis-je vous aider avec Harley Vape aujourd'hui ?"
        else:
            response = f"J'ai compris : '{data.get('message', '')}'. Comment puis-je vous aider concrètement ?"
        
        result = {'response': response, 'speak': True}
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps(result, ensure_ascii=False).encode('utf-8'))
    
    def handle_speak(self, data):
        if self.tts:
            try:
                text = data.get('text', '').replace('🛒', '').replace('📧', '').replace('💡', '')
                self.tts.say(text)
                self.tts.runAndWait()
                result = {'success': True}
            except:
                result = {'success': False}
        else:
            result = {'success': False}
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(result).encode())

if __name__ == '__main__':
    with socketserver.TCPServer(('', PORT), LumaFixed) as httpd:
        print('🚀 LUMA FIXED - Interface cliquable !')
        print(f'🌐 http://localhost:{PORT}')
        threading.Timer(1, lambda: webbrowser.open(f'http://localhost:{PORT}')).start()
        httpd.serve_forever()
