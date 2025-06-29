from flask import Flask, request, jsonify
from twilio.rest import Client as TwilioClient
from dotenv import load_dotenv
import os
import sqlite3
import logging
from datetime import datetime, timedelta
from functools import wraps
import time

# Imports des modules
from database import init_db, get_user_data, update_user_data
from nutrition_improved import analyze_food_request
from utils import send_whatsapp_reply, get_help_message
from config import current_config, get_environment_info, get_environment_display, get_detection_info

# Import de la logique de conversation
from nutrition_chat_improved import (
    is_conversation_message, 
    is_nutrition_question, 
    chat_with_lea_natural, 
    chat_with_nutrition_expert
)

# Charger les variables d'environnement
load_dotenv()

app = Flask(__name__)

# ===== CONFIGURATION LOGGING MULTI-ENVIRONNEMENTS =====
env_info = get_environment_info()
log_level = getattr(logging, env_info['log_level'].upper(), logging.INFO)

logging.basicConfig(
    level=log_level,
    format=f'%(asctime)s - [{env_info["environment"].upper()}] - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Console pour Railway
        logging.FileHandler(f'lea_bot_{env_info["environment"]}.log', encoding='utf-8')  # Fichier par environnement
    ]
)
logger = logging.getLogger(__name__)

# ===== RATE LIMITING CONFIGURABLE =====
user_requests = {}  # {phone_number: [timestamps]}
RATE_LIMIT_WINDOW = current_config.RATE_LIMIT_WINDOW
RATE_LIMIT_MAX_REQUESTS = current_config.RATE_LIMIT_MAX_REQUESTS

def is_rate_limited(phone_number):
    """Vérifie si l'utilisateur dépasse la limite de requêtes"""
    now = time.time()
    
    if phone_number not in user_requests:
        user_requests[phone_number] = []
    
    # Nettoyer les anciennes requêtes (plus de 1 minute)
    user_requests[phone_number] = [
        timestamp for timestamp in user_requests[phone_number] 
        if now - timestamp < RATE_LIMIT_WINDOW
    ]
    
    # Vérifier la limite
    if len(user_requests[phone_number]) >= RATE_LIMIT_MAX_REQUESTS:
        logger.warning(f"Rate limit dépassé pour {phone_number}")
        return True
    
    # Ajouter la requête actuelle
    user_requests[phone_number].append(now)
    return False

# Configuration des clés API depuis config
TWILIO_ACCOUNT_SID = current_config.TWILIO_ACCOUNT_SID
TWILIO_AUTH_TOKEN = current_config.TWILIO_AUTH_TOKEN
TWILIO_PHONE_NUMBER = current_config.TWILIO_PHONE_NUMBER

# Afficher les informations de détection d'environnement
detection_info = get_detection_info()
logger.info(f"[{env_info['environment'].upper()}] 🔍 Détection environnement: {detection_info['detection_method']}")
if detection_info['railway_url']:
    logger.info(f"[{env_info['environment'].upper()}] 🌐 URL Railway: {detection_info['railway_url']}")
logger.info(f"[{env_info['environment'].upper()}] 🎯 Environnement détecté: {detection_info['detected_environment']}")

logger.info(f"[{env_info['environment'].upper()}] 🔑 Twilio configuré: {'Oui' if TWILIO_ACCOUNT_SID else 'Non'}")
logger.info(f"[{env_info['environment'].upper()}] 📊 Base de données: {env_info['database']}")
logger.info(f"[{env_info['environment'].upper()}] 🎯 Code d'activation: {env_info['activation_code']}")

# Initialisation du client Twilio avec gestion d'erreur
try:
    twilio_client = TwilioClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    logger.info("✅ Client Twilio initialisé avec succès")
except Exception as e:
    logger.error(f"❌ Erreur initialisation Twilio: {e}")
    twilio_client = None

# Initialiser la base de données
try:
    init_db()
    logger.info("✅ Base de données initialisée")
except Exception as e:
    logger.error(f"❌ Erreur initialisation DB: {e}")

# ===== FONCTIONS DASHBOARD KPI (INTÉGRÉES DEPUIS SAUVEGARDE) =====

def get_daily_stats():
    """Statistiques business avancées avec DAU, WAU et engagement - INTÉGRÉ"""
    try:
        conn = sqlite3.connect(current_config.DATABASE_NAME)
        cursor = conn.cursor()
        
        # 1. Nouveaux utilisateurs aujourd'hui
        cursor.execute("""
            SELECT COUNT(*) FROM users 
            WHERE DATE(created_at) = DATE('now')
        """)
        new_users_today = cursor.fetchone()[0]
        
        # 2. Messages traités aujourd'hui
        cursor.execute("""
            SELECT COUNT(*) FROM meals 
            WHERE DATE(date) = DATE('now')
        """)
        messages_today = cursor.fetchone()[0]
        
        # 3. DAU - Daily Active Users (utilisateurs qui ont envoyé au moins 1 message aujourd'hui)
        cursor.execute("""
            SELECT COUNT(DISTINCT phone_number) FROM meals 
            WHERE DATE(date) = DATE('now')
        """)
        dau = cursor.fetchone()[0]
        
        # 4. WAU - Weekly Active Users (utilisateurs actifs dans les 7 derniers jours)
        cursor.execute("""
            SELECT COUNT(DISTINCT phone_number) FROM meals 
            WHERE DATE(date) >= DATE('now', '-7 days')
        """)
        wau = cursor.fetchone()[0]
        
        # 5. Messages par utilisateur actif aujourd'hui
        if dau > 0:
            messages_per_user = round(messages_today / dau, 1)
        else:
            messages_per_user = 0
        
        # 6. Total utilisateurs (pour référence)
        cursor.execute("SELECT COUNT(*) FROM users")
        total_users = cursor.fetchone()[0]
        
        conn.close()
        
        stats = {
            'new_users_today': new_users_today,
            'dau': dau,
            'wau': wau,
            'messages_today': messages_today,
            'messages_per_user': messages_per_user,
            'total_users': total_users,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M')
        }
        
        return stats
        
    except Exception as e:
        print(f"Erreur stats: {e}")
        return {}

def get_dau_history_14_days():
    """Récupère l'historique DAU sur 14 jours avec logique de couleur intelligente - INTÉGRÉ"""
    try:
        conn = sqlite3.connect(current_config.DATABASE_NAME)
        cursor = conn.cursor()
        
        dau_history = []
        previous_dau = 0
        
        for i in range(13, -1, -1):  # De J-13 à aujourd'hui
            cursor.execute("""
                SELECT COUNT(DISTINCT phone_number) FROM meals 
                WHERE DATE(date) = DATE('now', '-{} days')
            """.format(i))
            
            dau_count = cursor.fetchone()[0]
            date_obj = datetime.now() - timedelta(days=i)
            
            # Logique de couleur intelligente : comparer avec le jour précédent
            if i == 13:  # Premier jour, pas de comparaison
                is_growth = dau_count > 0
            else:
                is_growth = dau_count > previous_dau
            
            dau_history.append({
                'date': date_obj.strftime('%d/%m'),  # Format français DD/MM
                'dau': dau_count,
                'is_today': i == 0,
                'is_growth': is_growth
            })
            
            previous_dau = dau_count
        
        conn.close()
        return dau_history
        
    except Exception as e:
        print(f"Erreur historique DAU: {e}")
        return []

@app.route('/whatsapp', methods=['POST', 'GET'])
def whatsapp_webhook():
    """Point d'entrée principal pour les messages WhatsApp - VERSION PRODUCTION OPTIMISÉE"""
    if request.method == 'GET':
        return "Webhook WhatsApp actif!", 200
        
    from_number = request.form.get('From')
    text_content = request.form.get('Body', '').strip()
    media_url = request.form.get('MediaUrl0')
    
    # Logging structuré
    logger.info(f"📱 Message reçu de {from_number}")
    logger.info(f"📝 Texte: '{text_content}'")
    logger.info(f"🖼️ Image: {media_url}")
    
    # Vérification rate limiting
    if is_rate_limited(from_number):
        logger.warning(f"🚫 Rate limit dépassé pour {from_number}")
        try:
            send_whatsapp_reply(
                from_number, 
                "⏰ Vous envoyez trop de messages ! Attendez une minute avant de réessayer.", 
                twilio_client, 
                TWILIO_PHONE_NUMBER
            )
        except Exception as e:
            logger.error(f"Erreur envoi message rate limit: {e}")
        return '<Response/>', 429
    
    # Vérification client Twilio
    if not twilio_client:
        logger.error("❌ Client Twilio non initialisé")
        return '<Response/>', 500
    
    try:
        # Récupérer les données utilisateur
        user_data = get_user_data(from_number)
        
        # Créer un utilisateur par défaut si nécessaire
        if not user_data:
            user_data = {
                'onboarding_complete': True,
                'daily_calories': 0,
                'daily_proteins': 0,
                'daily_fats': 0,
                'daily_carbs': 0,
                'meals': []
            }
            update_user_data(from_number, user_data)
        
        # Traitement des commandes spéciales
        if text_content.lower() in ['/aide', '/help', '/?']:
            send_whatsapp_reply(from_number, get_help_message(), twilio_client, TWILIO_PHONE_NUMBER)
            return '<Response/>', 200
        
        if text_content.lower() in ['/reset', '/remise']:
            # Reset des données nutritionnelles du jour
            user_data['daily_calories'] = 0
            user_data['daily_proteins'] = 0
            user_data['daily_fats'] = 0
            user_data['daily_carbs'] = 0
            user_data['meals'] = []
            update_user_data(from_number, user_data)
            send_whatsapp_reply(from_number, "✅ Vos données du jour ont été remises à zéro!", twilio_client, TWILIO_PHONE_NUMBER)
            return '<Response/>', 200
        
        # Commande secrète pour les tests - Reset complet utilisateur
        if text_content.lower() == '/first_try':
            # Supprimer complètement l'utilisateur de la base de données
            from database import delete_user_data
            delete_user_data(from_number)
            
            # Créer un nouvel utilisateur
            user_data = {
                'onboarding_complete': True,
                'daily_calories': 0,
                'daily_proteins': 0,
                'daily_fats': 0,
                'daily_carbs': 0,
                'meals': []
            }
            update_user_data(from_number, user_data)
            send_whatsapp_reply(from_number, "✅ Utilisateur réinitialisé!", twilio_client, TWILIO_PHONE_NUMBER)
            return '<Response/>', 200
        
        # GESTION DES MESSAGES VOCAUX - TEMPORAIREMENT DÉSACTIVÉ
        if not text_content and media_url and 'audio' in request.form.get('MediaContentType0', ''):
            print("🎤 Message vocal détecté - Fonctionnalité temporairement désactivée")
            send_whatsapp_reply(
                from_number, 
                "🎤 Les messages vocaux arrivent bientôt ! En attendant, écris-moi tes aliments en texte (ex: \"50g de poulet\") ou envoie une photo 📷", 
                twilio_client, 
                TWILIO_PHONE_NUMBER
            )
            return '<Response/>', 200
        
        # CLASSIFICATION DES MESSAGES
        if text_content:
            print(f"🔍 Classification du message: '{text_content}'")
            
            # 1. Vérifier si c'est une conversation normale
            if is_conversation_message(text_content):
                print("💬 Message de conversation détecté")
                response = chat_with_lea_natural(text_content, user_data)
                send_whatsapp_reply(from_number, response, twilio_client, TWILIO_PHONE_NUMBER)
                return '<Response/>', 200
            
            # 2. Vérifier si c'est une question nutrition spécifique
            elif is_nutrition_question(text_content):
                print("💬 Question nutrition spécifique détectée")
                response = chat_with_nutrition_expert(text_content, user_data)
                send_whatsapp_reply(from_number, response, twilio_client, TWILIO_PHONE_NUMBER)
                return '<Response/>', 200
            
            # 3. Sinon, c'est du tracking d'aliment
            else:
                print("🍽️ Tracking d'aliment détecté")
        
        # Analyse nutritionnelle (tracking d'aliments)
        print("🔍 Début analyse nutritionnelle...")
        
        # Fonction callback silencieuse pour les logs serveur uniquement
        def silent_debug_callback(message):
            print(f"DEBUG: {message}")  # Log serveur uniquement
        
        food_data = analyze_food_request(text_content, media_url, silent_debug_callback)
        
        if food_data:
            print(f"✅ Analyse réussie - {food_data.get('name', 'Aliment')} détecté")
            
            # Récupérer les données actuelles FRAÎCHES de la base
            current_data = get_user_data(from_number)
            
            # Calculer les nouvelles valeurs en ajoutant aux valeurs actuelles
            new_calories = current_data.get('daily_calories', 0) + food_data['calories']
            new_proteins = current_data.get('daily_proteins', 0) + food_data['proteines']
            new_fats = current_data.get('daily_fats', 0) + food_data['lipides']
            new_carbs = current_data.get('daily_carbs', 0) + food_data['glucides']
            
            # Créer l'objet repas
            new_meal = {
                'name': food_data['name'],
                'time': food_data.get('time', ''),
                'calories': food_data['calories'],
                'proteines': food_data['proteines'],
                'lipides': food_data['lipides'],
                'glucides': food_data['glucides']
            }
            
            # Ajouter le nouveau repas à la liste existante
            current_meals = current_data.get('meals', [])
            updated_meals = current_meals + [new_meal]
            
            # Préparer les données mises à jour
            updated_user_data = current_data.copy()
            updated_user_data.update({
                'daily_calories': new_calories,
                'daily_proteins': new_proteins,
                'daily_fats': new_fats,
                'daily_carbs': new_carbs,
                'meals': updated_meals
            })
            
            # Sauvegarder les données mises à jour
            update_user_data(from_number, updated_user_data)
            
            # Récupérer les données finales pour l'affichage
            user_data = get_user_data(from_number)
            
            response_message = format_response_message(food_data, user_data)
            send_whatsapp_reply(from_number, response_message, twilio_client, TWILIO_PHONE_NUMBER)
        else:
            send_whatsapp_reply(from_number, "😓 Je n'ai pas réussi à identifier cet aliment. Essayez avec un autre nom ou une photo plus claire.", twilio_client, TWILIO_PHONE_NUMBER)
        
        return '<Response/>', 200
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        print(traceback.format_exc())
        send_whatsapp_reply(from_number, "😓 Désolé, je n'arrive pas à analyser votre demande. Réessayez ou tapez /aide.", twilio_client, TWILIO_PHONE_NUMBER)
        return '<Response/>', 200

def format_response_message(food_data, user_data):
    """Formate le message de réponse propre pour la production"""
    message_parts = []
    
    if food_data:
        # Nom principal
        message_parts.append(f"✅ *{food_data['name']}* analysé!")
        
        # Détail des ingrédients si disponible
        if food_data.get('ingredients'):
            message_parts.append(f"\n🍽️ *Ingrédients détectés:*")
            for ing in food_data['ingredients'][:5]:  # Max 5 ingrédients
                message_parts.append(f"• {ing['name']}: {ing['grams']}g ({ing['calories']:.0f} kcal)")
            message_parts.append(f"\n📏 *Poids total estimé:* {food_data.get('total_weight', 0)}g")
        
        # Valeurs nutritionnelles totales
        message_parts.extend([
            f"\n📊 *Valeurs nutritionnelles:*",
            f"🔥 Calories: {food_data['calories']:.0f} kcal",
            f"💪 Protéines: {food_data['proteines']:.1f}g",
            f"🥑 Lipides: {food_data['lipides']:.1f}g",
            f"🍞 Glucides: {food_data['glucides']:.1f}g",
            "",
        ])
    
    message_parts.extend([
        f"📈 *Bilan du jour:*",
        f"🔥 Calories totales: {user_data.get('daily_calories', 0):.0f} kcal",
        f"💪 Protéines: {user_data.get('daily_proteins', 0):.1f}g",
        f"🥑 Lipides: {user_data.get('daily_fats', 0):.1f}g",
        f"🍞 Glucides: {user_data.get('daily_carbs', 0):.1f}g",
        "",
        "💡 Tapez /aide pour plus d'options"
    ])
    
    return "\n".join(message_parts)

@app.route('/', methods=['GET'])
def dashboard_kpi():
    """Dashboard KPI intégré avec bannière d'environnement"""
    stats = get_daily_stats()
    dau_history = get_dau_history_14_days()
    env_display = get_environment_display()
    
    # Générer les données pour le graphique DAU 14 jours avec couleurs optimales (VERSION SAUVEGARDÉE)
    dau_chart_data = ""
    for day in dau_history:
        # Couleurs optimales : vert foncé aujourd'hui, vert clair croissance, gris stagnation/baisse
        if day['is_today']:
            color = "#4CAF50"  # Vert foncé pour aujourd'hui
        elif day['dau'] == 0:
            color = "#e0e0e0"  # Gris pour 0 DAU
        elif day['is_growth']:
            color = "#81C784"  # Vert clair pour croissance (restauré)
        else:
            color = "#e0e0e0"  # Gris pour stagnation/baisse (simplifié)
            
        dau_chart_data += f"""
        <div class="dau-day" style="background-color: {color};">
            <div class="dau-value">{day['dau']}</div>
            <div class="dau-date">{day['date']}</div>
        </div>"""
    
    return f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Léa - Dashboard Production v2.1</title>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                margin: 0;
                padding: 0;
                background: linear-gradient(to bottom, #e8d5ff 0%, #6a4c93 100%);
                color: #333;
                min-height: 100vh;
            }}
            .container {{
                max-width: 1200px;
                margin: 20px auto;
                background: white;
                border-radius: 15px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.15);
                overflow: hidden;
            }}
            .header {{
                background: #4CAF50;
                color: white;
                padding: 30px;
                text-align: center;
                width: 100%;
            }}
            .header h1 {{
                margin: 0 0 15px 0;
                font-size: 2.5em;
                font-weight: 600;
            }}
            .status {{
                background: #2E7D32;
                padding: 12px 25px;
                border-radius: 25px;
                display: inline-block;
                margin-top: 10px;
                font-weight: 600;
                color: white;
            }}
            
            /* KPI Principaux - Ligne du haut */
            .primary-metrics {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
                padding: 30px 30px 15px 30px;
            }}
            
            /* KPI Secondaires - Ligne du bas */
            .secondary-metrics {{
                display: grid;
                grid-template-columns: 1fr 1fr 1fr;
                gap: 20px;
                padding: 15px 30px 30px 30px;
            }}
            
            .metric-card {{
                background: #f8f9fa;
                border-radius: 12px;
                padding: 25px;
                text-align: center;
                border-left: 5px solid;
                transition: all 0.2s ease;
                position: relative;
                cursor: pointer;
            }}
            .metric-card:hover {{
                transform: translateY(-5px);
                box-shadow: 0 10px 25px rgba(0,0,0,0.1);
                background: #f0f1f2;
            }}
            .metric-card.primary {{ border-left-color: #007bff; }}
            .metric-card.success {{ border-left-color: #28a745; }}
            .metric-card.warning {{ border-left-color: #ffc107; }}
            .metric-card.info {{ border-left-color: #17a2b8; }}
            .metric-card.secondary {{ border-left-color: #6c757d; }}
            
            .metric-value {{
                font-size: 2.5em;
                font-weight: bold;
                margin: 10px 0;
                color: #2c3e50;
            }}
            .metric-label {{
                font-size: 1.1em;
                color: #6c757d;
                font-weight: 500;
            }}
            .metric-description {{
                font-size: 0.9em;
                color: #95a5a6;
                margin-top: 8px;
            }}
            
            .hidden-value {{
                color: #bbb;
                font-style: italic;
            }}
            
            /* Graphique DAU 14 jours */
            .dau-chart-section {{
                background: #f8f9fa;
                padding: 30px;
                border-top: 1px solid #e9ecef;
            }}
            .dau-chart-title {{
                text-align: center;
                font-size: 1.3em;
                font-weight: 600;
                color: #2c3e50;
                margin-bottom: 20px;
            }}
            .dau-chart {{
                display: flex;
                justify-content: space-between;
                align-items: end;
                gap: 8px;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background: white;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            .dau-day {{
                flex: 1;
                min-height: 60px;
                border-radius: 6px;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                color: white;
                font-weight: bold;
                text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
                transition: transform 0.2s;
            }}
            .dau-day:hover {{
                transform: scale(1.05);
            }}
            .dau-value {{
                font-size: 1.2em;
                margin-bottom: 5px;
            }}
            .dau-date {{
                font-size: 0.8em;
                opacity: 0.9;
            }}
            
            .info-section {{
                background: #f8f9fa;
                padding: 30px;
                border-top: 1px solid #e9ecef;
            }}
            .info-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 30px;
            }}
            .info-card {{
                background: white;
                border-radius: 10px;
                padding: 25px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.08);
            }}
            .info-card h3 {{
                margin-top: 0;
                color: #2c3e50;
                border-bottom: 2px solid #4CAF50;
                padding-bottom: 10px;
            }}
            .info-list {{
                list-style: none;
                padding: 0;
            }}
            .info-list li {{
                padding: 8px 0;
                border-bottom: 1px solid #f1f3f4;
            }}
            .info-list li:last-child {{
                border-bottom: none;
            }}
            .highlight {{
                background: #e8f5e8;
                padding: 15px;
                border-radius: 8px;
                margin: 20px 0;
                border-left: 4px solid #4CAF50;
            }}
            .timestamp {{
                text-align: center;
                color: #6c757d;
                font-size: 0.9em;
                margin-top: 20px;
            }}
            
            @media (max-width: 768px) {{
                .primary-metrics, .secondary-metrics {{
                    grid-template-columns: 1fr;
                }}
                .dau-chart {{
                    gap: 4px;
                }}
                .dau-value {{
                    font-size: 1em;
                }}
                .dau-date {{
                    font-size: 0.7em;
                }}
            }}
        </style>
        <script>
            // Gestion localStorage pour persistance des KPI masqués
            function toggleMetric(metricId) {{
                const valueElement = document.getElementById(metricId + '-value');
                const isHidden = localStorage.getItem(metricId + '-hidden') === 'true';
                
                if (isHidden) {{
                    // Afficher
                    valueElement.classList.remove('hidden-value');
                    valueElement.textContent = valueElement.dataset.originalValue;
                    localStorage.setItem(metricId + '-hidden', 'false');
                }} else {{
                    // Masquer
                    valueElement.dataset.originalValue = valueElement.textContent;
                    valueElement.classList.add('hidden-value');
                    valueElement.textContent = '---';
                    localStorage.setItem(metricId + '-hidden', 'true');
                }}
            }}
            
            // Restaurer l'état au chargement
            window.addEventListener('DOMContentLoaded', function() {{
                const metrics = ['dau', 'wau', 'new-users', 'messages', 'engagement'];
                metrics.forEach(metricId => {{
                    const valueElement = document.getElementById(metricId + '-value');
                    if (valueElement && localStorage.getItem(metricId + '-hidden') === 'true') {{
                        valueElement.dataset.originalValue = valueElement.textContent;
                        valueElement.classList.add('hidden-value');
                        valueElement.textContent = '---';
                    }}
                }});
            }});
        </script>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🤖 Léa - Dashboard Production v2.1</h1>
                <div class="status">✓ VERSION STABLE + DASHBOARD KPI</div>
            </div>
            
            <!-- KPI Principaux - Ligne du haut -->
            <div class="primary-metrics">
                <div class="metric-card" style="border-left-color: #4CAF50;" onclick="toggleMetric('dau')">
                    <div class="metric-value">
                        <span id="dau-value">{stats.get('dau', 0)}</span>
                    </div>
                    <div class="metric-label">Daily Active Users</div>
                    <div class="metric-description">Utilisateurs actifs aujourd'hui</div>
                </div>
                
                <div class="metric-card" style="border-left-color: #FF9800;" onclick="toggleMetric('wau')">
                    <div class="metric-value">
                        <span id="wau-value">{stats.get('wau', 0)}</span>
                    </div>
                    <div class="metric-label">Weekly Active Users</div>
                    <div class="metric-description">Utilisateurs actifs (7 jours)</div>
                </div>
            </div>
            
            <!-- KPI Secondaires - Ligne du bas -->
            <div class="secondary-metrics">
                <div class="metric-card" style="border-left-color: #2196F3;" onclick="toggleMetric('new-users')">
                    <div class="metric-value">
                        <span id="new-users-value">{stats.get('new_users_today', 0)}</span>
                    </div>
                    <div class="metric-label">Nouveaux</div>
                    <div class="metric-description">Inscriptions aujourd'hui</div>
                </div>
                
                <div class="metric-card" style="border-left-color: #00BCD4;" onclick="toggleMetric('messages')">
                    <div class="metric-value">
                        <span id="messages-value">{stats.get('messages_today', 0)}</span>
                    </div>
                    <div class="metric-label">Messages traités</div>
                    <div class="metric-description">Messages aujourd'hui</div>
                </div>
                
                <div class="metric-card" style="border-left-color: #757575;" onclick="toggleMetric('engagement')">
                    <div class="metric-value">
                        <span id="engagement-value">{stats.get('messages_per_user', 0)}</span>
                    </div>
                    <div class="metric-label">Messages/utilisateur</div>
                    <div class="metric-description">Engagement moyen</div>
                </div>
            </div>
            
            <!-- Graphique DAU 14 jours -->
            <div class="dau-chart-section">
                <div class="dau-chart-title">📊 Historique DAU - 14 derniers jours</div>
                <div class="dau-chart">
                    {dau_chart_data}
                </div>
            </div>
            
            <div class="info-section">
                <div class="info-grid">
                    <div class="info-card">
                        <h3>👥 Informations Utilisateurs</h3>
                        <ul class="info-list">
                            <li><strong>Numéro WhatsApp:</strong> +1 415 523 8886</li>
                            <li><strong>Code d'activation:</strong> join live-cold</li>
                            <li><strong>Message test:</strong> "50g de poulet"</li>
                            <li><strong>Webhook:</strong> /whatsapp</li>
                        </ul>
                    </div>
                    
                    <div class="info-card">
                        <h3>📊 Métriques Business</h3>
                        <ul class="info-list">
                            <li><strong>Total utilisateurs:</strong> {stats.get('total_users', 0)}</li>
                            <li><strong>Taux d'engagement:</strong> {round((stats.get('dau', 0) / max(stats.get('total_users', 1), 1)) * 100, 1)}%</li>
                            <li><strong>Rétention 7j:</strong> {round((stats.get('wau', 0) / max(stats.get('total_users', 1), 1)) * 100, 1)}%</li>
                            <li><strong>Dernière MAJ:</strong> {stats.get('date', 'N/A')}</li>
                        </ul>
                    </div>
                </div>
                
                <div class="highlight">
                    <strong>🍎 Version Stable Restaurée:</strong> Logique de conversation + tracking + dashboard KPI
                </div>
                
                <div class="timestamp">
                    Dashboard mis à jour automatiquement • Version stable d'hier + KPI d'aujourd'hui
                </div>
            </div>
        </div>
    </body>
    </html>
    """

@app.route('/api/stats')
def api_stats():
    """API pour récupérer les statistiques en JSON"""
    return jsonify(get_daily_stats())

@app.route('/api/dau-history')
def api_dau_history():
    """API pour récupérer l'historique DAU en JSON"""
    return jsonify(get_dau_history_14_days())

if __name__ == '__main__':
    print("🚀 Démarrage du serveur Léa (VERSION PRODUCTION)...")
    print("📱 Webhook WhatsApp disponible sur: /whatsapp")
    print("✨ Version production - Messages propres uniquement")
    print("🎤 Messages vocaux temporairement désactivés")
    
    # Port pour Railway (variable d'environnement) ou 3000 en local
    port = int(os.getenv('PORT', 3000))
    print(f"🌐 Serveur démarré sur le port: {port}")
    
    app.run(host='0.0.0.0', port=port, debug=False)
