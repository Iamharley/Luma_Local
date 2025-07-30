#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import http.server
import socketserver
import webbrowser
import threading
import json
import subprocess
import time
import requests

PORT = 8083

class LumaBrain(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # TTS
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
    <title>🧠 LUMA - Assistant IA Intelligent</title>
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
            background: linear-gradient(45deg, #00ff88, #00cc6a);
            color: black;
            padding: 12px 25px;
            border-radius: 25px;
            display: inline-block;
            font-weight: bold;
            box-shadow: 0 4px 15px rgba(0,255,136,0.3);
        }
        .chat {
            flex: 1;
            background: rgba(255,255,255,0.1);
            margin: 20px;
            border-radius: 20px;
            padding: 20px;
            overflow-y: auto;
            backdrop-filter: blur(20px);
        }
        .message {
            margin: 15px 0;
            padding: 18px;
            border-radius: 18px;
            max-width: 85%;
            animation: slideIn 0.3s ease;
        }
        .user { 
            background: rgba(255,255,255,0.9); 
            color: black; 
            margin-left: auto; 
            border-left: 4px solid #667eea;
        }
        .luma { 
            background: rgba(255,255,255,0.15); 
            border-left: 4px solid #00ff88;
            border: 1px solid rgba(255,255,255,0.2);
        }
        .input-area {
            background: rgba(255,255,255,0.1);
            padding: 20px;
            margin: 20px;
            border-radius: 20px;
            backdrop-filter: blur(10px);
        }
        .input-row {
            display: flex;
            gap: 12px;
            margin-bottom: 15px;
        }
        #messageInput {
            flex: 1;
            padding: 16px 20px;
            border: none;
            border-radius: 25px;
            font-size: 16px;
            background: rgba(255,255,255,0.95);
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        button {
            padding: 16px 24px;
            border: none;
            border-radius: 20px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
        }
        button:hover { transform: translateY(-2px); }
        .send-btn { background: linear-gradient(135deg, #00ff88, #00cc6a); color: black; }
        .email-btn { background: linear-gradient(135deg, #0088ff, #0066cc); color: white; }
        .shopify-btn { background: linear-gradient(135deg, #88ff00, #6acc00); color: black; }
        .notion-btn { background: linear-gradient(135deg, #000000, #333333); color: white; }
        .whatsapp-btn { background: linear-gradient(135deg, #25D366, #1DA851); color: white; }
        .brain-btn { background: linear-gradient(135deg, #ff00ff, #cc00cc); color: white; }
        .buttons { 
            display: flex; 
            gap: 8px; 
            flex-wrap: wrap; 
            justify-content: center; 
        }
        @keyframes slideIn { 
            from { opacity: 0; transform: translateY(10px); } 
            to { opacity: 1; transform: translateY(0); } 
        }
        .thinking {
            font-style: italic;
            opacity: 0.8;
            color: #00ff88;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🧠 LUMA</h1>
        <div class="status">✅ Assistant IA Intelligent - Cerveau Activé 🧠</div>
    </div>
    
    <div class="chat" id="messages">
        <div class="message luma">
            <strong>🧠 LUMA :</strong> Bonjour Anne-Sophie ! Mon cerveau est maintenant connecté ! Je peux vraiment comprendre vos questions, analyser vos besoins Harley Vape, et donner des réponses intelligentes. Plus de réponses robots ! 🚀
        </div>
    </div>
    
    <div class="input-area">
        <div class="input-row">
            <input type="text" id="messageInput" placeholder="Posez-moi une vraie question intelligente..." />
            <button class="send-btn" onclick="sendMessage()">🧠 Analyser</button>
        </div>
        <div class="buttons">
            <button class="email-btn" onclick="quickAction('analyser mes emails importants')">📧 Emails</button>
            <button class="shopify-btn" onclick="quickAction('optimiser harley vape shopify')">🛒 Harley Vape</button>
            <button class="notion-btn" onclick="quickAction('notion organisation')">📝 Notion</button>
            <button class="whatsapp-btn" onclick="quickAction('whatsapp business')">💬 WhatsApp</button>
            <button class="brain-btn" onclick="quickAction('mode intelligence avancée')">🧠 Cerveau</button>
        </div>
    </div>

    <script>
        let isThinking = false;
        
        function sendMessage() {
            if (isThinking) return;
            
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            
            if (!message) {
                alert('Posez-moi une question !');
                return;
            }
            
            isThinking = true;
            addMessage('👤 Vous', message, 'user');
            input.value = '';
            
            // Indicateur de réflexion
            addMessage('🧠 LUMA', '<span class="thinking">🤔 Je réfléchis avec mon cerveau IA...</span>', 'luma');
            
            fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: message })
            })
            .then(response => response.json())
            .then(data => {
                // Remplacer le message de réflexion
                const messages = document.getElementById('messages');
                const lastMessage = messages.lastElementChild;
                lastMessage.innerHTML = '<strong>🧠 LUMA :</strong> ' + data.response;
                
                if (data.speak) speakText(data.response);
            })
            .catch(error => {
                addMessage('🧠 LUMA', 'Erreur de connexion cerveau : ' + error, 'luma');
            })
            .finally(() => {
                isThinking = false;
            });
        }
        
        function quickAction(action) {
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
        
        document.getElementById('messageInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter' && !isThinking) {
                sendMessage();
            }
        });
        
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
        original = data.get('message', '')
        
        # VRAI CERVEAU - Connexion Ollama (GRATUIT!)
        brain_response = self.ask_brain(original)
        
        if brain_response:
            response = brain_response
        else:
            # Fallback intelligent si Ollama indisponible
            response = self.smart_fallback(message, original)
        
        # Actions
        self.execute_actions(message)
        
        result = {'response': response, 'speak': True}
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps(result, ensure_ascii=False).encode('utf-8'))
    
    def ask_brain(self, question):
        """Connexion au cerveau Ollama (Mistral) - GRATUIT!"""
        try:
            response = requests.post('http://localhost:11434/api/generate',
                json={
                    'model': 'mistral:latest',
                    'prompt': f"Tu es LUMA, l'assistante IA business d'Anne-Sophie qui gère Harley Vape (boutique de cigarettes électroniques). Réponds de manière intelligente, personnalisée et actionnable à cette question: {question}",
                    'stream': False
                },
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                return f"🧠 {result.get('response', '').strip()}"
        except:
            pass
        
        return None
    
    def smart_fallback(self, message_lower, original):
        """Réponses intelligentes si Ollama indisponible"""
        
        if any(word in message_lower for word in ['shopify', 'harley', 'vape', 'vente', 'optimiser']):
            return f"🛒 Analyse Harley Vape: Pour optimiser votre boutique, je recommande d'analyser vos produits bestsellers, optimiser vos fiches produits avec de meilleurs mots-clés, et créer des packs attractifs. Voulez-vous que j'examine vos stats de vente spécifiques ?"
        
        elif any(word in message_lower for word in ['email', 'analyser', 'important']):
            return f"📧 Analyse Emails: Je vais examiner vos emails pour identifier les prospects chauds, les demandes clients urgentes, et les opportunités business. Je peux aussi créer des templates de réponse personnalisés pour Harley Vape."
        
        elif any(word in message_lower for word in ['notion', 'organisation']):
            return f"📝 Intégration Notion: Je peux vous aider à structurer votre workspace Notion avec des databases pour: suivi clients Harley Vape, inventory management, campagnes marketing, et KPIs business. Quelle section voulez-vous organiser en priorité ?"
        
        elif any(word in message_lower for word in ['whatsapp', 'business']):
            return f"💬 WhatsApp Business: Pour Harley Vape, je peux configurer des messages automatiques, catalogues produits, et suivi commandes via WhatsApp. C'est excellent pour le SAV et les ventes directes !"
        
        elif any(word in message_lower for word in ['intelligence', 'cerveau', 'avancée']):
            return f"🧠 Mode Cerveau Activé: Mon intelligence combine analyse prédictive, optimisation SEO, détection tendances marché, et personnalisation client. Je peux analyser vos données Harley Vape pour identifier les opportunités de croissance cachées."
        
        else:
            return f"🤔 Question intéressante: '{original}'. Basé sur mon analyse, cela semble lié à votre stratégie business. Pour vous donner une réponse ultra-pertinente, précisez si c'est pour: optimiser Harley Vape, améliorer votre productivité, ou développer une nouvelle stratégie ?"
    
    def execute_actions(self, message_lower):
        """Exécute les actions demandées"""
        if 'email' in message_lower:
            subprocess.run(['open', '-a', 'Mail'], check=False)
        elif any(word in message_lower for word in ['shopify', 'harley']):
            subprocess.run(['open', 'https://admin.shopify.com'], check=False)
        elif 'notion' in message_lower:
            subprocess.run(['open', 'https://notion.so'], check=False)
        elif 'whatsapp' in message_lower:
            subprocess.run(['open', 'https://web.whatsapp.com'], check=False)
    
    def handle_speak(self, data):
        if self.tts:
            try:
                text = data.get('text', '').replace('🧠', '').replace('🛒', '').replace('📧', '').replace('📝', '').replace('💬', '').replace('🤔', '')
                self.tts.say(text)
                self.tts.runAndWait()
            except:
                pass
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'success': True}).encode())

if __name__ == '__main__':
    with socketserver.TCPServer(('', PORT), LumaBrain) as httpd:
        print('🧠 LUMA BRAIN - Vraie Intelligence Connectée !')
        print('💰 Coût: GRATUIT (Ollama local)')
        print(f'🌐 http://localhost:{PORT}')
        threading.Timer(1, lambda: webbrowser.open(f'http://localhost:{PORT}')).start()
        httpd.serve_forever()
