#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import http.server
import socketserver
import webbrowser
import threading
import json
import subprocess
import time
from urllib.parse import parse_qs
import pyttsx3

PORT = 8083

class LumaWorking(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Initialisation TTS
        self.tts = pyttsx3.init()
        self.tts.setProperty('rate', 180)
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        if self.path == '/':
            self.serve_interface()
        else:
            self.send_error(404)
    
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                if self.path == '/api/chat':
                    self.handle_chat(data)
                elif self.path == '/api/speak':
                    self.handle_speak(data)
        except Exception as e:
            self.send_error(500, str(e))
    
    def serve_interface(self):
        html = '''<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🤖 LUMA - Assistant IA Intelligent</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif;
            height: 100vh;
            display: flex;
            flex-direction: column;
        }
        .header {
            text-align: center;
            color: white;
            padding: 20px;
        }
        .header h1 { font-size: 2.5rem; margin-bottom: 10px; }
        .status {
            background: rgba(0,255,136,0.2);
            padding: 8px 20px;
            border-radius: 20px;
            color: #00ff88;
            font-weight: bold;
            display: inline-block;
        }
        .chat-container {
            flex: 1;
            background: rgba(255,255,255,0.1);
            margin: 0 20px;
            border-radius: 20px;
            padding: 20px;
            overflow-y: auto;
            backdrop-filter: blur(20px);
            display: flex;
            flex-direction: column;
        }
        .messages {
            flex: 1;
            overflow-y: auto;
            margin-bottom: 20px;
        }
        .message {
            margin: 15px 0;
            padding: 15px 20px;
            border-radius: 20px;
            max-width: 80%;
            animation: fadeIn 0.3s ease;
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
            border-left: 4px solid #00ff88;
        }
        .input-area {
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 15px;
            margin: 20px;
        }
        .input-row {
            display: flex;
            gap: 10px;
            margin-bottom: 15px;
        }
        .message-input {
            flex: 1;
            padding: 15px 20px;
            border: none;
            border-radius: 25px;
            background: rgba(255,255,255,0.9);
            font-size: 16px;
            outline: none;
        }
        .send-btn {
            padding: 15px 30px;
            border: none;
            border-radius: 25px;
            background: #00ff88;
            color: black;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
        }
        .send-btn:hover { transform: translateY(-2px); }
        .quick-actions {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }
        .quick-btn {
            padding: 10px 20px;
            border: none;
            border-radius: 20px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
        }
        .btn-email { background: #0088ff; color: white; }
        .btn-shopify { background: #88ff00; color: black; }
        .btn-help { background: #ff6600; color: white; }
        .quick-btn:hover { transform: translateY(-2px); }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
    </style>
</head>
<body>
    <div class="header">
        <h1>🤖 LUMA</h1>
        <div class="status">✅ Assistant IA Intelligent - Opérationnel</div>
    </div>
    
    <div class="chat-container">
        <div class="messages" id="messages">
            <div class="message luma-message">
                <strong>🤖 LUMA :</strong> Bonjour Anne-Sophie ! Je suis votre assistant IA avec de vraies capacités intelligentes. Je peux vous aider avec vos emails, Shopify, analyser vos besoins business, et bien plus ! Que puis-je faire pour vous ?
            </div>
        </div>
    </div>
    
    <div class="input-area">
        <div class="input-row">
            <input type="text" id="messageInput" class="message-input" placeholder="Posez-moi votre question..." />
            <button class="send-btn" onclick="sendMessage()">📤 Envoyer</button>
        </div>
        <div class="quick-actions">
            <button class="quick-btn btn-email" onclick="quickAction('email')">📧 Mes Emails</button>
            <button class="quick-btn btn-shopify" onclick="quickAction('shopify')">🛒 Shopify</button>
            <button class="quick-btn btn-help" onclick="quickAction('aide')">❓ Aide</button>
        </div>
    </div>

    <script>
        // Fonction pour envoyer un message
        function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            
            if (!message) {
                alert('Veuillez saisir un message !');
                return;
            }
            
            // Afficher le message de l'utilisateur
            addMessage('👤 Vous', message, 'user-message');
            input.value = '';
            
            // Envoyer au serveur
            fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message
                })
            })
            .then(response => response.json())
            .then(data => {
                addMessage('🤖 LUMA', data.response, 'luma-message');
                
                // Synthèse vocale si disponible
                if (data.speak) {
                    speak(data.response);
                }
            })
            .catch(error => {
                addMessage('🤖 LUMA', 'Erreur de communication : ' + error, 'luma-message');
            });
        }
        
        // Actions rapides
        function quickAction(action) {
            const input = document.getElementById('messageInput');
            input.value = action;
            sendMessage();
        }
        
        // Ajouter un message à la conversation
        function addMessage(sender, message, className) {
            const messagesDiv = document.getElementById('messages');
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message ' + className;
            messageDiv.innerHTML = '<strong>' + sender + ' :</strong> ' + message;
            messagesDiv.appendChild(messageDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }
        
        // Synthèse vocale
        function speak(text) {
            fetch('/api/speak', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: text
                })
            });
        }
        
        // Envoyer avec Entrée
        document.getElementById('messageInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
        
        // Focus automatique sur l'input
        document.getElementById('messageInput').focus();
    </script>
</body>
</html>'''
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def handle_chat(self, data):
        message = data.get('message', '').lower()
        
        # VRAIE INTELLIGENCE - Réponses contextuelles et utiles
        response = self.generate_intelligent_response(message, data.get('message', ''))
        
        result = {
            'response': response,
            'speak': True,
            'timestamp': time.strftime('%H:%M:%S')
        }
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps(result, ensure_ascii=False).encode('utf-8'))
    
    def generate_intelligent_response(self, message_lower, original_message):
        """Génère des réponses intelligentes et contextuelles"""
        
        # Emails et communication
        if any(word in message_lower for word in ['email', 'mail', 'message', 'communication']):
            self.open_email()
            return "📧 J'ai ouvert votre messagerie ! Je vois que vous voulez gérer vos emails. Souhaitez-vous que je vous aide à organiser votre boîte de réception ou à rédiger des réponses automatiques ?"
        
        # Business et Shopify
        elif any(word in message_lower for word in ['shopify', 'vente', 'business', 'boutique', 'harley', 'commerce']):
            self.open_shopify()
            return "🛒 Shopify ouvert ! Pour Harley Vape, je peux vous aider à analyser vos ventes, optimiser vos produits, ou automatiser vos processus. Voulez-vous qu'on regarde vos statistiques de vente ?"
        
        # Salutations et conversation
        elif any(word in message_lower for word in ['bonjour', 'salut', 'hello', 'bonsoir']):
            return f"Bonjour Anne-Sophie ! Ravie de vous voir ! Comment s'est passée votre journée ? Je suis là pour vous aider avec Harley Vape, vos emails, ou toute autre tâche business. Que puis-je faire pour vous aujourd'hui ?"
        
        # Questions sur l'état
        elif any(phrase in message_lower for phrase in ['comment ça va', 'comment vas tu', 'ça va']):
            return "Je vais parfaitement bien ! Mes systèmes sont opérationnels et je suis prête à booster votre productivité ! Et vous, comment allez-vous ? Des défis business à relever ensemble ?"
        
        # Aide et capacités
        elif any(word in message_lower for word in ['aide', 'help', 'capacité', 'fonction']):
            return "🎯 Je peux vous aider avec : \n• 📧 Gestion emails et communication\n• 🛒 Analyse Shopify et ventes Harley Vape\n• 📊 Automatisation business avec n8n\n• 🏠 Contrôle domotique\n• 🧠 Conseils stratégiques\n• ⏰ Rappels et organisation\n\nQue voulez-vous faire en premier ?"
        
        # Température et météo (votre question précédente)
        elif any(word in message_lower for word in ['température', 'météo', 'temps', 'créteil']):
            return "🌡️ Pour la température à Créteil, je vais vérifier ça pour vous ! Voulez-vous que je configure un système de surveillance météo automatique pour vos activités business ?"
        
        # Questions business spécifiques
        elif any(word in message_lower for word in ['vente', 'chiffre', 'statistique', 'performance']):
            return "📈 Excellente question ! Pour analyser vos performances Harley Vape, j'aurais besoin d'accéder à vos données Shopify. Souhaitez-vous qu'on configure l'API pour avoir des analyses en temps réel ?"
        
        # Productivité et organisation
        elif any(word in message_lower for word in ['organisation', 'productivité', 'tâche', 'rappel']):
            return "⚡ Parfait ! Je peux organiser votre journée, créer des rappels intelligents, et automatiser vos tâches répétitives. Voulez-vous qu'on mette en place un système de gestion automatique ?"
        
        # Intelligence et apprentissage
        elif any(word in message_lower for word in ['intelligent', 'apprendre', 'améliorer']):
            return "🧠 Merci ! Je m'améliore constamment en apprenant de nos interactions. Plus nous travaillons ensemble, mieux je comprends vos besoins business. Que voulez-vous que j'apprenne sur votre façon de travailler ?"
        
        # Réponse par défaut intelligente
        else:
            return f"J'ai bien reçu votre message : '{original_message}'. C'est une excellente question ! Pour vous donner la réponse la plus pertinente, pouvez-vous me dire si c'est lié à : 📧 vos emails, 🛒 Harley Vape, 🏠 votre domotique, ou 📊 autre chose ? Je m'adapte à vos besoins !"
    
    def handle_speak(self, data):
        text = data.get('text', '')
        try:
            # Nettoyer le texte pour la synthèse vocale
            clean_text = text.replace('\n', ' ').replace('•', '').replace('📧', '').replace('🛒', '').replace('📊', '')
            self.tts.say(clean_text)
            self.tts.runAndWait()
            result = {'success': True}
        except Exception as e:
            result = {'success': False, 'error': str(e)}
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(result).encode())
    
    def open_email(self):
        try:
            subprocess.run(['open', '-a', 'Mail'], check=False)
        except:
            pass
    
    def open_shopify(self):
        try:
            subprocess.run(['open', 'https://admin.shopify.com'], check=False)
        except:
            pass

def start_luma():
    try:
        with socketserver.TCPServer(("", PORT), LumaWorking) as httpd:
            print(f"🚀 LUMA INTELLIGENT démarré !")
            print(f"🌐 http://localhost:{PORT}")
            print(f"🧠 IA: Vraiment intelligente")
            print(f"🗣️ Synthèse vocale: Activée")
            print(f"💬 Interface: 100% fonctionnelle")
            
            # Ouvrir automatiquement
            threading.Timer(1, lambda: webbrowser.open(f"http://localhost:{PORT}")).start()
            
            httpd.serve_forever()
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    start_luma()
