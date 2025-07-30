#!/usr/bin/env python3
"""
Système de rappels intelligents pour Luma Business Pro
"""

import schedule
import time
import subprocess
import json
from datetime import datetime, timedelta

class IntelligentReminders:
    def __init__(self):
        self.reminders = []
        self.business_hours = {'start': 9, 'end': 18}
        
    def add_smart_reminder(self, task, priority="normal", context=None):
        """Ajoute un rappel intelligent"""
        reminder = {
            'task': task,
            'priority': priority,
            'context': context,
            'created': datetime.now(),
            'optimal_time': self.calculate_optimal_time(priority),
            'completed': False
        }
        
        self.reminders.append(reminder)
        self.schedule_reminder(reminder)
        
        return reminder
    
    def calculate_optimal_time(self, priority):
        """Calcule le moment optimal pour le rappel"""
        now = datetime.now()
        
        if priority == "urgent":
            return now + timedelta(minutes=5)
        elif priority == "high":
            return now + timedelta(hours=1)
        elif priority == "normal":
            return now + timedelta(hours=4)
        else:  # low
            return now + timedelta(days=1)
    
    def schedule_reminder(self, reminder):
        """Programme le rappel"""
        optimal_time = reminder['optimal_time']
        
        # Programme avec schedule
        schedule.every().day.at(optimal_time.strftime('%H:%M')).do(
            self.send_notification, 
            reminder['task'], 
            reminder['priority']
        )
    
    def send_notification(self, task, priority):
        """Envoie une notification"""
        icon = {
            'urgent': '🚨',
            'high': '⚡',
            'normal': '📋',
            'low': '💡'
        }.get(priority, '📋')
        
        message = f"{icon} Rappel {priority}: {task}"
        
        # Notification système macOS
        subprocess.run([
            'osascript', '-e', 
            f'display notification "{message}" with title "Luma Business Pro"'
        ])
        
        # Notification vocale
        subprocess.run(['say', message])
        
        return True
    
    def check_business_context(self):
        """Vérifie le contexte business actuel"""
        context = {
            'time': datetime.now().strftime('%H:%M'),
            'day': datetime.now().strftime('%A'),
            'emails_pending': self.count_pending_emails(),
            'tasks_today': self.count_today_tasks(),
            'meetings_next': self.get_next_meeting()
        }
        
        return context
    
    def count_pending_emails(self):
        """Compte les emails en attente"""
        try:
            script = '''
            tell application "Mail"
                set unreadCount to unread count of inbox
                return unreadCount as string
            end tell
            '''
            result = subprocess.run(['osascript', '-e', script], 
                                  capture_output=True, text=True)
            return int(result.stdout.strip())
        except:
            return 0
    
    def count_today_tasks(self):
        """Compte les tâches du jour"""
        try:
            script = '''
            tell application "Things3"
                set todayTasks to to dos of list "Today"
                return count of todayTasks
            end tell
            '''
            result = subprocess.run(['osascript', '-e', script], 
                                  capture_output=True, text=True)
            return int(result.stdout.strip())
        except:
            return 0
    
    def get_next_meeting(self):
        """Récupère le prochain RDV"""
        # Intégration avec Calendar à implémenter
        return "Aucun RDV immédiat"
    
    def daily_business_briefing(self):
        """Briefing quotidien intelligent"""
        context = self.check_business_context()
        
        briefing = f'''
🌅 BRIEFING MATINAL - {datetime.now().strftime('%d/%m/%Y')}

📧 Emails: {context['emails_pending']} non lus
📋 Tâches: {context['tasks_today']} programmées aujourd'hui
🗓️ Prochaine réunion: {context['meetings_next']}

💡 Priorités suggérées:
1. Traiter les emails urgents
2. Réviser l'agenda du jour
3. Vérifier les métriques Shopify
4. Préparer le contenu social media

Bonne journée productive ! 🚀
        '''
        
        self.send_notification(briefing, "normal")
        return briefing
    
    def setup_daily_schedule(self):
        """Configure le planning quotidien"""
        # Briefing matinal
        schedule.every().day.at("08:00").do(self.daily_business_briefing)
        
        # Rappel déjeuner
        schedule.every().day.at("12:00").do(
            self.send_notification, 
            "Pause déjeuner - rechargez vos batteries ! 🍽️", 
            "normal"
        )
        
        # Récap fin de journée
        schedule.every().day.at("17:30").do(
            self.send_notification, 
            "Bilan de la journée et préparation de demain 📊", 
            "normal"
        )
        
        print("✅ Planning quotidien configuré")
    
    def run_scheduler(self):
        """Lance le planificateur"""
        self.setup_daily_schedule()
        
        print("🤖 Système de rappels intelligents démarré")
        print("Appuyez sur Ctrl+C pour arrêter")
        
        while True:
            schedule.run_pending()
            time.sleep(60)  # Vérifie chaque minute

if __name__ == "__main__":
    reminder_system = IntelligentReminders()
    
    # Exemples de rappels
    reminder_system.add_smart_reminder(
        "Vérifier les ventes Shopify", 
        "high", 
        "business_metrics"
    )
    
    reminder_system.add_smart_reminder(
        "Poster sur Instagram", 
        "normal", 
        "social_media"
    )
    
    # Lance le système
    reminder_system.run_scheduler()
