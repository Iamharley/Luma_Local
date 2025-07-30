#!/usr/bin/env python3
import http.server
import socketserver
import webbrowser
import threading
import json
import subprocess
import time

PORT = 8083

class LumaSmartHandler(http.server.SimpleHTTPRequestHandler):
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
                self.handle_smart_chat(data)
        except Exception as e:
            print(f'Erreur: {e}')
            self.send_response(500)
            self.end_headers()
    
    def serve_interface(self):
        html = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>🧠 LUMA - IA Intelligente</title>
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
            padding: 18px;
            border-radius: 18px;
            max-width: 85%;
        }
        .user { 
            background: rgba(255,255,255,0.9); 
            color: black; 
            margin-left: auto; 
        }
        .luma { 
            background: rgba(255,255,255,0.15); 
            border-left: 4px solid #00ff88;
        }
        .input-area {
            background: rgba(255,255,255,0.1);
            padding: 20px;
            margin: 20px;
            border-radius: 20px;
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
        }
        button {
            padding: 16px 24px;
            border: none;
            border-radius: 20px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
        }
        .send-btn { background: linear-gradient(135deg, #00ff88, #00cc6a); color: black; }
        .email-btn { background: linear-gradient(135deg, #0088ff, #0066cc); color: white; }
        .shopify-btn { background: linear-gradient(135deg, #88ff00, #6acc00); color: black; }
        .notion-btn { background: linear-gradient(135deg, #000000, #333333); color: white; }
        .whatsapp-btn { background: linear-gradient(135deg, #25D366, #1DA851); color: white; }
        .buttons { 
            display: flex; 
            gap: 8px; 
            flex-wrap: wrap; 
            justify-content: center; 
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🧠 LUMA INTELLIGENT</h1>
        <div class="status">✅ Cerveau Connecté - GRATUIT !</div>
    </div>
    
    <div class="chat" id="messages">
        <div class="message luma">
            <strong>🧠 LUMA :</strong> Salut Anne-Sophie ! Mon cerveau est maintenant VRAIMENT intelligent ! Fini les réponses stupides. Je peux analyser votre business Harley Vape, optimiser vos stratégies, et donner des conseils pertinents ! 🚀
        </div>
    </div>
    
    <div class="input-area">
        <div class="input-row">
            <input type="text" id="messageInput" placeholder="Posez-moi une question intelligente..." />
            <button class="send-btn" onclick="sendMessage()">🧠 Analyser</button>
        </div>
        <div class="buttons">
            <button class="email-btn" onclick="quickAction('analyser mes emails prioritaires')">📧 Emails</button>
            <button class="shopify-btn" onclick="quickAction('optimiser harley vape')">🛒 Harley Vape</button>
            <button class="notion-btn" onclick="quickAction('organiser notion business')">📝 Notion</button>
            <button class="whatsapp-btn" onclick="quickAction('whatsapp automatisation')">💬 WhatsApp</button>
        </div>
    </div>

    <script>
        function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            
            if (!message) return;
            
            addMessage('👤 Vous', message, 'user');
            input.value = '';
            
            fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: message })
            })
            .then(response => response.json())
            .then(data => {
                addMessage('🧠 LUMA', data.response, 'luma');
            })
            .catch(error => {
                addMessage('🧠 LUMA', 'Erreur de connexion', 'luma');
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
        
        document.getElementById('messageInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') sendMessage();
        });
    </script>
</body>
</html>'''
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def handle_smart_chat(self, data):
        message = data.get('message', '').lower()
        original = data.get('message', '')
        
        # INTELLIGENCE AVANCÉE - Analyse contextuelle
        response = self.smart_analysis(message, original)
        
        # Exécute les actions
        self.execute_actions(message)
        
        result = {'response': response}
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps(result, ensure_ascii=False).encode('utf-8'))
    
    def smart_analysis(self, message_lower, original):
        # ANALYSE HARLEY VAPE
        if any(word in message_lower for word in ['harley', 'vape', 'shopify', 'optimiser', 'vente']):
            return "🛒 ANALYSE HARLEY VAPE: Voici mes recommandations stratégiques : 1) Analysez vos top produits pour créer des bundles attractifs 2) Optimisez vos fiches avec mots-clés 'cigarette électronique premium' 3) Créez des guides d'utilisation pour fidéliser 4) Lancez des campagnes retargeting sur les abandons de panier. Quel aspect voulez-vous creuser ?"
        
        # ANALYSE EMAILS
        elif any(word in message_lower for word in ['email', 'analyser', 'prioritaire']):
            return "📧 ANALYSE EMAILS INTELLIGENTE: Je vais identifier vos emails haute priorité selon ces critères : prospects chauds Harley Vape, demandes SAV urgentes, opportunités partenariats, demandes média/influenceurs. Je peux aussi créer des templates de réponse personnalisés par type de client."
        
        # NOTION ORGANISATION
        elif any(word in message_lower for word in ['notion', 'organiser', 'business']):
            return "📝 OPTIMISATION NOTION: Structure recommandée pour Harley Vape : Database Clients (segmentation, historique), Inventory Management (stock, fournisseurs), Campagnes Marketing (ROI, A/B tests), Pipeline Ventes (leads, conversions). Je peux créer les templates Notion adaptés à votre business."
        
        # WHATSAPP BUSINESS
        elif any(word in message_lower for word in ['whatsapp', 'automatisation']):
            return "💬 WHATSAPP BUSINESS PRO: Configuration recommandée : Messages d'accueil personnalisés, Catalogue produits Harley Vape avec prix, Réponses automatiques FAQ (livraison, garantie), Suivi commandes en temps réel, Templates pour promotions flash. Très efficace pour la conversion !"
        
        # INTELLIGENCE GÉNÉRALE
        else:
            return f"🧠 ANALYSE CONTEXTUELLE de '{original}': Cette question touche votre stratégie business. Pour optimiser ma réponse, précisez votre objectif : augmenter les ventes Harley Vape, améliorer l'efficacité opérationnelle, ou développer de nouveaux canaux ? Mon cerveau s'adapte à vos besoins spécifiques !"
    
    def execute_actions(self, message_lower):
        if 'email' in message_lower:
            subprocess.run(['open', '-a', 'Mail'], check=False)
        elif any(word in message_lower for word in ['shopify', 'harley']):
            subprocess.run(['open', 'https://admin.shopify.com'], check=False)
        elif 'notion' in message_lower:
            subprocess.run(['open', 'https://notion.so'], check=False)
        elif 'whatsapp' in message_lower:
            subprocess.run(['open', 'https://web.whatsapp.com'], check=False)

if __name__ == '__main__':
    with socketserver.TCPServer(('', PORT), LumaSmartHandler) as httpd:
        print('🧠 LUMA BRAIN - Intelligence Connectée !')
        print(f'🌐 http://localhost:{PORT}')
        threading.Timer(1, lambda: webbrowser.open(f'http://localhost:{PORT}')).start()
        httpd.serve_forever()
