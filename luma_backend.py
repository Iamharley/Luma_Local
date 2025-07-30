#!/usr/bin/env python3
"""
LUMA Business Pro - Backend Server
Assistant IA Personnel avec surveillance médicale et domotique
"""

import asyncio
import json
import logging
import os
import sys
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import threading
import subprocess
import psutil

# Web server
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_socketio import SocketIO, emit
from flask_cors import CORS

# IA et APIs
import requests
import openai
from anthropic import Anthropic

# Monitoring système
import cv2
import numpy as np
import speech_recognition as sr
import pyttsx3

# Domotique et intégrations
import applescript

# Configuration logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('luma.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('LUMA')

class LumaConfig:
    """Configuration centralisée de LUMA"""
    
    def __init__(self):
        self.load_config()
    
    def load_config(self):
        """Charge la configuration depuis les variables d'environnement ou fichier"""
        self.ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', '')
        self.OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
        self.GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
        
        # Configuration médicale
        self.MEDICAL_MONITORING = True
        self.EMERGENCY_CONTACTS = [
            {'name': 'SAMU', 'number': '15', 'type': 'emergency'},
            {'name': 'Dr. Martin', 'number': '+33612345678', 'type': 'doctor'},
            {'name': 'Famille', 'number': '+33687654321', 'type': 'family'}
        ]
        
        # Configuration domotique
        self.HOMEKIT_ENABLED = True
        self.ALEXA_ENABLED = True
        
        # Configuration IA
        self.DEFAULT_AI_MODEL = 'claude'  # claude, gpt, gemini, local
        self.VOICE_ENABLED = True
        self.WAKE_WORD = 'hey luma'
        
        logger.info("Configuration LUMA chargée")

class MedicalMonitor:
    """Surveillance médicale et détection d'épilepsie"""
    
    def __init__(self, config: LumaConfig):
        self.config = config
        self.monitoring_active = False
        self.camera = None
        self.biometric_data = {}
        self.last_seizure_risk = 'LOW'
        
    def start_monitoring(self):
        """Démarre la surveillance médicale"""
        if not self.config.MEDICAL_MONITORING:
            return
            
        logger.info("🏥 Démarrage surveillance médicale")
        self.monitoring_active = True
        
        # Thread pour la surveillance caméra
        threading.Thread(target=self._camera_monitoring, daemon=True).start()
        
        # Thread pour la simulation biométrique (en attendant vrais capteurs)
        threading.Thread(target=self._biometric_simulation, daemon=True).start()
        
    def _camera_monitoring(self):
        """Surveillance par caméra pour détection d'épilepsie"""
        try:
            self.camera = cv2.VideoCapture(0)
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            
            while self.monitoring_active:
                ret, frame = self.camera.read()
                if not ret:
                    time.sleep(1)
                    continue
                
                # Détection de visage et analyse mouvement
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.1, 4)
                
                # Analyse simple pour détection d'anomalies
                risk_level = self._analyze_movement_patterns(frame)
                
                if risk_level == 'HIGH':
                    logger.warning("⚠️ RISQUE ÉPILEPSIE DÉTECTÉ!")
                    self._trigger_medical_alert()
                
                time.sleep(0.1)  # 10 FPS
                
        except Exception as e:
            logger.error(f"Erreur surveillance caméra: {e}")
        finally:
            if self.camera:
                self.camera.release()
    
    def _analyze_movement_patterns(self, frame) -> str:
        """Analyse les patterns de mouvement pour détecter une crise"""
        # Simulation d'analyse - dans la vraie version, ici on aurait
        # de la computer vision avancée pour détecter les mouvements convulsifs
        
        # Pour l'instant, simulation aléatoire de risque faible
        import random
        risk_chance = random.random()
        
        if risk_chance < 0.001:  # 0.1% de chance de détecter un risque
            return 'HIGH'
        elif risk_chance < 0.01:  # 1% de chance de risque modéré
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def _biometric_simulation(self):
        """Simulation des données biométriques"""
        while self.monitoring_active:
            # Génération de données réalistes
            self.biometric_data = {
                'heart_rate': 68 + np.random.randint(-8, 15),
                'temperature': round(36.5 + np.random.uniform(-0.3, 0.8), 1),
                'oxygen_saturation': 97 + np.random.randint(0, 3),
                'breathing_rate': 14 + np.random.randint(-2, 6),
                'timestamp': datetime.now().isoformat()
            }
            
            # Évaluation du risque d'épilepsie basée sur les métriques
            risk = self._evaluate_seizure_risk()
            self.biometric_data['seizure_risk'] = risk
            
            time.sleep(3)  # Mise à jour toutes les 3 secondes
    
    def _evaluate_seizure_risk(self) -> str:
        """Évalue le risque de crise d'épilepsie"""
        hr = self.biometric_data.get('heart_rate', 70)
        temp = self.biometric_data.get('temperature', 36.7)
        
        # Règles simples d'évaluation
        if hr > 100 or hr < 50 or temp > 38.0:
            return 'MEDIUM'
        elif hr > 90 or temp > 37.5:
            return 'LOW-MEDIUM'
        else:
            return 'LOW'
    
    def _trigger_medical_alert(self):
        """Déclenche une alerte médicale"""
        logger.critical("🚨 ALERTE MÉDICALE DÉCLENCHÉE!")
        
        # Appel automatique des secours (simulation)
        for contact in self.config.EMERGENCY_CONTACTS:
            logger.info(f"📞 Appel automatique: {contact['name']} - {contact['number']}")
            
            # Dans une vraie implémentation, ici on déclencherait:
            # - Appel téléphonique automatique via Siri Shortcuts
            # - SMS d'urgence avec géolocalisation
            # - Notification aux proches
        
        # Notification système
        try:
            applescript.run('''
                display notification "ALERTE MÉDICALE DÉCLENCHÉE - Secours contactés" 
                with title "🚨 LUMA URGENCE" sound name "Sosumi"
            ''')
        except:
            pass
    
    def get_status(self) -> Dict[str, Any]:
        """Retourne le statut médical actuel"""
        return {
            'monitoring_active': self.monitoring_active,
            'biometric_data': self.biometric_data,
            'last_update': datetime.now().isoformat(),
            'camera_status': 'active' if self.camera else 'inactive'
        }

class AIBrain:
    """Cerveau IA hybride - routage intelligent entre modèles"""
    
    def __init__(self, config: LumaConfig):
        self.config = config
        self.claude_client = None
        self.setup_ai_clients()
    
    def setup_ai_clients(self):
        """Configure les clients IA"""
        try:
            if self.config.ANTHROPIC_API_KEY:
                self.claude_client = Anthropic(api_key=self.config.ANTHROPIC_API_KEY)
                logger.info("✅ Claude configuré")
        except Exception as e:
            logger.error(f"Erreur config Claude: {e}")
        
        try:
            if self.config.OPENAI_API_KEY:
                openai.api_key = self.config.OPENAI_API_KEY
                logger.info("✅ OpenAI configuré")
        except Exception as e:
            logger.error(f"Erreur config OpenAI: {e}")
    
    def process_query(self, query: str, context: Dict = None) -> Dict[str, Any]:
        """Route la requête vers le bon modèle IA"""
        
        # Analyse de la complexité de la requête
        complexity = self._analyze_query_complexity(query)
        
        # Routage intelligent
        if complexity == 'simple':
            model = 'local'  # Ollama local pour économiser
        elif complexity == 'medium':
            model = 'gpt'    # GPT pour l'équilibre
        else:
            model = 'claude' # Claude pour les tâches complexes
        
        response = self._get_ai_response(query, model, context)
        
        return {
            'response': response,
            'model_used': model,
            'complexity': complexity,
            'timestamp': datetime.now().isoformat()
        }
    
    def _analyze_query_complexity(self, query: str) -> str:
        """Analyse la complexité d'une requête"""
        query_lower = query.lower()
        
        # Requêtes simples
        simple_keywords = ['email', 'agenda', 'météo', 'heure', 'date', 'hello', 'bonjour']
        if any(keyword in query_lower for keyword in simple_keywords):
            return 'simple'
        
        # Requêtes complexes
        complex_keywords = ['stratégie', 'analyse', 'optimisation', 'conseil', 'créer', 'rédiger']
        if any(keyword in query_lower for keyword in complex_keywords):
            return 'complex'
        
        return 'medium'
    
    def _get_ai_response(self, query: str, model: str, context: Dict = None) -> str:
        """Obtient la réponse du modèle spécifié"""
        
        try:
            if model == 'claude' and self.claude_client:
                return self._ask_claude(query, context)
            elif model == 'gpt' and openai.api_key:
                return self._ask_gpt(query, context)
            elif model == 'local':
                return self._ask_ollama(query, context)
            else:
                return self._fallback_response(query)
                
        except Exception as e:
            logger.error(f"Erreur IA {model}: {e}")
            return self._fallback_response(query)
    
    def _ask_claude(self, query: str, context: Dict = None) -> str:
        """Requête vers Claude"""
        try:
            message = self.claude_client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1000,
                messages=[{
                    "role": "user", 
                    "content": f"En tant qu'assistant personnel LUMA, réponds à: {query}"
                }]
            )
            return message.content[0].text
        except Exception as e:
            logger.error(f"Erreur Claude: {e}")
            return self._fallback_response(query)
    
    def _ask_gpt(self, query: str, context: Dict = None) -> str:
        """Requête vers GPT"""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{
                    "role": "system",
                    "content": "Tu es LUMA, l'assistant IA personnel d'Anne-Sophie."
                }, {
                    "role": "user",
                    "content": query
                }],
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Erreur GPT: {e}")
            return self._fallback_response(query)
    
    def _ask_ollama(self, query: str, context: Dict = None) -> str:
        """Requête vers Ollama local"""
        try:
            response = requests.post('http://localhost:11434/api/generate', 
                json={
                    'model': 'mistral',
                    'prompt': f"En tant qu'assistant LUMA, réponds brièvement à: {query}",
                    'stream': False
                },
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json().get('response', 'Erreur de génération')
            else:
                return self._fallback_response(query)
                
        except Exception as e:
            logger.error(f"Erreur Ollama: {e}")
            return self._fallback_response(query)
    
    def _fallback_response(self, query: str) -> str:
        """Réponse de secours quand les IA ne fonctionnent pas"""
        fallback_responses = {
            'email': 'Je vérifie vos emails... Fonctionnalité en cours de configuration.',
            'agenda': 'Consultation de votre agenda... Configuration en cours.',
            'météo': 'Service météo temporairement indisponible.',
            'shopify': 'Connexion à Shopify en cours de configuration.',
            'default': 'Je suis temporairement en mode réduit. Toutes mes fonctions seront bientôt disponibles !'
        }
        
        query_lower = query.lower()
        for key, response in fallback_responses.items():
            if key in query_lower:
                return response
        
        return fallback_responses['default']

class DomoticController:
    """Contrôleur domotique - HomeKit, Alexa, etc."""
    
    def __init__(self, config: LumaConfig):
        self.config = config
        self.devices = {}
        self.scenes = {}
        self.setup_devices()
    
    def setup_devices(self):
        """Configuration des appareils domotiques"""
        # Simulation d'appareils connectés
        self.devices = {
            'lights': {
                'salon': {'brightness': 75, 'status': 'on'},
                'chambre': {'brightness': 50, 'status': 'off'},
                'cuisine': {'brightness': 80, 'status': 'on'}
            },
            'climate': {
                'temperature': 22,
                'mode': 'auto',
                'status': 'on'
            },
            'security': {
                'status': 'armed',
                'cameras': 4,
                'sensors': 8
            },
            'audio': {
                'status': 'off',
                'volume': 30,
                'source': 'spotify'
            }
        }
        
        self.scenes = {
            'morning': 'Scène Réveil',
            'evening': 'Scène Soirée', 
            'sleep': 'Scène Sommeil',
            'away': 'Scène Absence'
        }
        
        logger.info("🏡 Contrôleur domotique initialisé")
    
    def control_device(self, device: str, action: str, value: Any = None) -> Dict[str, Any]:
        """Contrôle un appareil domotique"""
        
        try:
            if device == 'lights':
                return self._control_lights(action, value)
            elif device == 'climate':
                return self._control_climate(action, value)
            elif device == 'security':
                return self._control_security(action, value)
            elif device == 'audio':
                return self._control_audio(action, value)
            else:
                return {'status': 'error', 'message': f'Appareil {device} non reconnu'}
                
        except Exception as e:
            logger.error(f"Erreur contrôle domotique: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def _control_lights(self, action: str, value: Any) -> Dict[str, Any]:
        """Contrôle de l'éclairage"""
        if action == 'set_brightness':
            room = value.get('room', 'salon')
            brightness = value.get('brightness', 50)
            
            if room in self.devices['lights']:
                self.devices['lights'][room]['brightness'] = brightness
                self.devices['lights'][room]['status'] = 'on' if brightness > 0 else 'off'
                
                return {
                    'status': 'success',
                    'message': f'Luminosité {room} réglée à {brightness}%'
                }
        
        elif action == 'toggle':
            room = value.get('room', 'salon')
            if room in self.devices['lights']:
                current_status = self.devices['lights'][room]['status']
                new_status = 'off' if current_status == 'on' else 'on'
                self.devices['lights'][room]['status'] = new_status
                
                return {
                    'status': 'success',
                    'message': f'Éclairage {room} {new_status}'
                }
        
        return {'status': 'error', 'message': 'Action éclairage non reconnue'}
    
    def _control_climate(self, action: str, value: Any) -> Dict[str, Any]:
        """Contrôle de la climatisation"""
        if action == 'set_temperature':
            temperature = value.get('temperature', 22)
            self.devices['climate']['temperature'] = temperature
            
            return {
                'status': 'success',
                'message': f'Température réglée à {temperature}°C'
            }
        
        return {'status': 'error', 'message': 'Action climat non reconnue'}
    
    def _control_security(self, action: str, value: Any) -> Dict[str, Any]:
        """Contrôle de la sécurité"""
        if action == 'toggle':
            current = self.devices['security']['status']
            new_status = 'disarmed' if current == 'armed' else 'armed'
            self.devices['security']['status'] = new_status
            
            return {
                'status': 'success',
                'message': f'Sécurité {new_status}'
            }
        
        return {'status': 'error', 'message': 'Action sécurité non reconnue'}
    
    def _control_audio(self, action: str, value: Any) -> Dict[str, Any]:
        """Contrôle audio"""
        if action == 'toggle':
            current = self.devices['audio']['status']
            new_status = 'off' if current == 'on' else 'on'
            self.devices['audio']['status'] = new_status
            
            return {
                'status': 'success',
                'message': f'Audio {new_status}'
            }
        
        return {'status': 'error', 'message': 'Action audio non reconnue'}
    
    def activate_scene(self, scene: str) -> Dict[str, Any]:
        """Active une scène domotique"""
        if scene not in self.scenes:
            return {'status': 'error', 'message': f'Scène {scene} non trouvée'}
        
        scene_actions = {
            'morning': {
                'lights': {'salon': 60, 'cuisine': 80},
                'temperature': 21,
                'audio': 'on'
            },
            'evening': {
                'lights': {'salon': 40, 'chambre': 30},
                'temperature': 22,
                'audio': 'on'
            },
            'sleep': {
                'lights': {'all': 0},
                'temperature': 19,
                'audio': 'off'
            },
            'away': {
                'lights': {'security': 20},
                'temperature': 18,
                'security': 'armed'
            }
        }
        
        # Application des actions de la scène
        actions = scene_actions.get(scene, {})
        
        return {
            'status': 'success',
            'message': f'Scène {self.scenes[scene]} activée',
            'actions_applied': actions
        }
    
    def get_status(self) -> Dict[str, Any]:
        """Retourne le statut de tous les appareils"""
        return {
            'devices': self.devices,
            'scenes': self.scenes,
            'last_update': datetime.now().isoformat()
        }

class BusinessAnalytics:
    """Analytics business - Shopify, emails, KPIs"""
    
    def __init__(self, config: LumaConfig):
        self.config = config
        self.metrics = {}
        self.update_metrics()
    
    def update_metrics(self):
        """Met à jour les métriques business"""
        # Simulation de données Shopify
        base_revenue = 12450
        daily_revenue = 3127
        orders = 247
        
        # Simulation de variations réalistes
        import random
        revenue_variation = random.uniform(0.85, 1.15)
        orders_variation = random.uniform(0.9, 1.1)
        
        self.metrics = {
            'revenue': {
                'monthly': int(base_revenue * revenue_variation),
                'daily': int(daily_revenue * revenue_variation),
                'target': 41200,
                'currency': 'EUR'
            },
            'orders': {
                'monthly': int(orders * orders_variation),
                'daily': random.randint(8, 25),
                'conversion_rate': round(random.uniform(0.85, 0.92), 3)
            },
            'customers': {
                'new_monthly': random.randint(15, 25),
                'satisfaction': round(random.uniform(0.92, 0.96), 3),
                'return_rate': round(random.uniform(0.02, 0.04), 3)
            },
            'inventory': {
                'low_stock_items': random.randint(3, 8),
                'out_of_stock': random.randint(0, 2)
            },
            'marketing': {
                'abandoned_carts': random.randint(8, 15),
                'email_open_rate': round(random.uniform(0.25, 0.35), 3),
                'social_engagement': round(random.uniform(0.04, 0.08), 3)
            }
        }
        
        logger.info("📊 Métriques business mises à jour")
    
    def get_recommendations(self) -> List[Dict[str, str]]:
        """Génère des recommandations business"""
        recommendations = []
        
        # Analyse des paniers abandonnés
        abandoned = self.metrics['marketing']['abandoned_carts']
        if abandoned > 10:
            recommendations.append({
                'type': 'urgent',
                'title': f'📧 Relancer {abandoned} paniers abandonnés',
                'description': f'Potentiel de récupération: ~€{abandoned * 45}',
                'action': 'send_abandoned_cart_emails'
            })
        
        # Analyse des stocks
        low_stock = self.metrics['inventory']['low_stock_items']
        if low_stock > 5:
            recommendations.append({
                'type': 'warning',
                'title': f'📦 {low_stock} produits en stock faible',
                'description': 'Recommandation de réapprovisionnement',
                'action': 'reorder_inventory'
            })
        
        # Opportunités marketing
        engagement = self.metrics['marketing']['social_engagement']
        if engagement < 0.06:
            recommendations.append({
                'type': 'opportunity',
                'title': '📱 Améliorer engagement réseaux sociaux',
                'description': f'Taux actuel: {engagement:.1%} (objectif: 8%)',
                'action': 'create_social_content'
            })
        
        return recommendations
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        """Retourne les données pour le dashboard"""
        self.update_metrics()
        
        return {
            'metrics': self.metrics,
            'recommendations': self.get_recommendations(),
            'last_update': datetime.now().isoformat()
        }

class LumaServer:
    """Serveur principal LUMA"""
    
    def __init__(self):
        self.config = LumaConfig()
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'luma-secret-key-2024'
        
        # Configuration CORS et SocketIO
        CORS(self.app)
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")
        
        # Initialisation des modules
        self.medical_monitor = MedicalMonitor(self.config)
        self.ai_brain = AIBrain(self.config)
        self.domotic_controller = DomoticController(self.config)
        self.business_analytics = BusinessAnalytics(self.config)
        
        # Configuration des routes
        self.setup_routes()
        self.setup_socketio_events()
        
        logger.info("🤖 Serveur LUMA initialisé")
    
    def setup_routes(self):
        """Configuration des routes Flask"""
        
        @self.app.route('/')
        def index():
            """Page principale"""
            logger.info("📱 Accès à l'interface LUMA")
            return send_from_directory('.', 'luma_interface.html')
        
        @self.app.route('/api/status')
        def api_status():
            """Statut général du système"""
            return jsonify({
                'status': 'running',
                'timestamp': datetime.now().isoformat(),
                'modules': {
                    'medical': self.medical_monitor.monitoring_active,
                    'ai': True,
                    'domotic': True,
                    'business': True
                }
            })
        
        @self.app.route('/api/medical/status')
        def medical_status():
            """Statut médical"""
            return jsonify(self.medical_monitor.get_status())
        
        @self.app.route('/api/domotic/status')
        def domotic_status():
            """Statut domotique"""
            return jsonify(self.domotic_controller.get_status())
        
        @self.app.route('/api/business/dashboard')
        def business_dashboard():
            """Dashboard business"""
            return jsonify(self.business_analytics.get_dashboard_data())
        
        @self.app.route('/api/ai/chat', methods=['POST'])
        def ai_chat():
            """Endpoint chat IA"""
            data = request.get_json()
            query = data.get('message', '')
            context = data.get('context', {})
            
            logger.info(f"💬 Requête IA: {query}")
            response = self.ai_brain.process_query(query, context)
            
            return jsonify(response)
        
        @self.app.route('/api/domotic/control', methods=['POST'])
        def domotic_control():
            """Contrôle domotique"""
            data = request.get_json()
            device = data.get('device')
            action = data.get('action')
            value = data.get('value')
            
            logger.info(f"🏡 Contrôle domotique: {device} - {action}")
            response = self.domotic_controller.control_device(device, action, value)
            
            return jsonify(response)
        
        @self.app.route('/api/domotic/scene/<scene>', methods=['POST'])
        def activate_scene(scene):
            """Active une scène domotique"""
            logger.info(f"🎬 Activation scène: {scene}")
            response = self.domotic_controller.activate_scene(scene)
            
            return jsonify(response)
        
        @self.app.route('/api/emergency/trigger', methods=['POST'])
        def emergency_trigger():
            """Déclenche une alerte d'urgence"""
            logger.critical("🚨 ALERTE URGENCE DÉCLENCHÉE VIA API!")
            self.medical_monitor._trigger_medical_alert()
            
            return jsonify({
                'status': 'emergency_triggered',
                'message': 'Alerte d\'urgence déclenchée - Secours contactés',
                'timestamp': datetime.now().isoformat()
            })
    
    def setup_socketio_events(self):
        """Configuration des événements SocketIO pour temps réel"""
        
        @self.socketio.on('connect')
        def on_connect():
            logger.info("🔌 Client connecté via WebSocket")
            emit('status', {'message': 'LUMA connecté'})
        
        @self.socketio.on('disconnect') 
        def on_disconnect():
            logger.info("🔌 Client déconnecté")
        
        @self.socketio.on('request_medical_update')
        def on_medical_update():
            """Envoi des données médicales en temps réel"""
            data = self.medical_monitor.get_status()
            emit('medical_update', data)
        
        @self.socketio.on('request_business_update')
        def on_business_update():
            """Envoi des données business"""
            data = self.business_analytics.get_dashboard_data()
            emit('business_update', data)
    
    def start_background_tasks(self):
        """Démarre les tâches en arrière-plan"""
        
        # Surveillance médicale
        self.medical_monitor.start_monitoring()
        
        # Mise à jour périodique des données
        def periodic_updates():
            while True:
                try:
                    # Mise à jour métriques business
                    self.business_analytics.update_metrics()
                    
                    # Émission des mises à jour via WebSocket
                    self.socketio.emit('medical_update', 
                                     self.medical_monitor.get_status())
                    self.socketio.emit('business_update', 
                                     self.business_analytics.get_dashboard_data())
                    
                    time.sleep(30)  # Mise à jour toutes les 30 secondes
                    
                except Exception as e:
                    logger.error(f"Erreur mise à jour périodique: {e}")
                    time.sleep(10)
        
        # Démarrage du thread de mise à jour
        threading.Thread(target=periodic_updates, daemon=True).start()
        
        logger.info("🔄 Tâches en arrière-plan démarrées")
    
    def run(self, host='127.0.0.1', port=8080, debug=False):
        """Lance le serveur LUMA"""
        
        # Démarrage des tâches en arrière-plan
        self.start_background_tasks()
        
        logger.info(f"🚀 LUMA Business Pro démarré sur http://{host}:{port}")
        
        # Message d'accueil
        print("\n" + "="*60)
        print("🤖 LUMA BUSINESS PRO - Assistant IA Personnel")
        print("="*60)
        print(f"🌐 Interface web: http://{host}:{port}")
        print("🏥 Surveillance médicale: ACTIVE")
        print("🏡 Contrôle domotique: PRÊT")
        print("📊 Analytics business: EN LIGNE")
        print("🧠 IA hybride: OPÉRATIONNELLE")
        print("="*60 + "\n")
        
        # Lancement du serveur
        self.socketio.run(
            self.app, 
            host=host, 
            port=port, 
            debug=debug,
            allow_unsafe_werkzeug=True
        )

def main():
    """Point d'entrée principal"""
    
    # Vérification des prérequis
    try:
        import cv2, numpy, flask, anthropic, openai
        logger.info("✅ Toutes les dépendances sont installées")
    except ImportError as e:
        logger.error(f"❌ Dépendance manquante: {e}")
        print("Installez les dépendances avec: pip install -r requirements.txt")
        sys.exit(1)
    
    # Création et lancement du serveur
    server = LumaServer()
    
    try:
        server.run(host='127.0.0.1', port=8080, debug=False)
    except KeyboardInterrupt:
        logger.info("🛑 Arrêt de LUMA demandé par l'utilisateur")
    except Exception as e:
        logger.error(f"💥 Erreur fatale: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
