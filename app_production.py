from flask import Flask, request, jsonify
from twilio.rest import Client as TwilioClient
from dotenv import load_dotenv
import os
import sqlite3
import logging
from datetime import datetime, timedelta
import time

# Imports des modules
from database import init_db, get_user_data, update_user_data, delete_user_data
from nutrition_improved import analyze_food_request
from utils import send_whatsapp_reply, get_help_message
from config import current_config, get_environment_info, get_detection_info
from nutrition_chat_improved import (
    is_conversation_message, 
    is_nutrition_question, 
    chat_with_lea_natural, 
    chat_with_nutrition_expert
)

# Charger les variables d'environnement
load_dotenv()

app = Flask(__name__)

# ===== CONFIGURATION =====
def setup_logging():
    """Configure le logging multi-environnements"""
    env_info = get_environment_info()
    log_level = getattr(logging, env_info['log_level'].upper(), logging.INFO)
    
    logging.basicConfig(
        level=log_level,
        format=f'%(asctime)s - [{env_info["environment"].upper()}] - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler()]
    )
    return logging.getLogger(__name__)

def setup_twilio():
    """Initialise le client Twilio"""
    try:
        client = TwilioClient(current_config.TWILIO_ACCOUNT_SID, current_config.TWILIO_AUTH_TOKEN)
        logger.info("✅ Client Twilio initialisé")
        return client
    except Exception as e:
        logger.error(f"❌ Erreur Twilio: {e}")
        return None

def setup_database():
    """Initialise la base de données"""
    try:
        init_db()
        logger.info("✅ Base de données initialisée")
    except Exception as e:
        logger.error(f"❌ Erreur DB: {e}")

# Initialisation
logger = setup_logging()
twilio_client = setup_twilio()
setup_database()

# Rate limiting
user_requests = {}
RATE_LIMIT_WINDOW = current_config.RATE_LIMIT_WINDOW
RATE_LIMIT_MAX_REQUESTS = current_config.RATE_LIMIT_MAX_REQUESTS

def is_rate_limited(phone_number):
    """Vérifie le rate limiting"""
    now = time.time()
    
    if phone_number not in user_requests:
        user_requests[phone_number] = []
    
    # Nettoyer les anciennes requêtes
    user_requests[phone_number] = [
        ts for ts in user_requests[phone_number] 
        if now - ts < RATE_LIMIT_WINDOW
    ]
    
    # Vérifier la limite
    if len(user_requests[phone_number]) >= RATE_LIMIT_MAX_REQUESTS:
        return True
    
    user_requests[phone_number].append(now)
    return False

# ===== HANDLERS DE MESSAGES =====
def handle_special_commands(text_content, from_number, user_data):
    """Gère les commandes spéciales"""
    text_lower = text_content.lower()
    
    if text_lower in ['/aide', '/help', '/?']:
        send_whatsapp_reply(from_number, get_help_message(), twilio_client, current_config.TWILIO_PHONE_NUMBER)
        return True
    
    if text_lower in ['/reset', '/remise']:
        reset_daily_data(from_number, user_data)
        send_whatsapp_reply(from_number, "✅ Données du jour remises à zéro!", twilio_client, current_config.TWILIO_PHONE_NUMBER)
        return True
    
    if text_lower == '/first_try':
        restart_onboarding(from_number)
        return True
    
    return False

def reset_daily_data(from_number, user_data):
    """Reset les données nutritionnelles du jour"""
    user_data.update({
        'daily_calories': 0,
        'daily_proteins': 0,
        'daily_fats': 0,
        'daily_carbs': 0,
        'meals': []
    })
    update_user_data(from_number, user_data)

def restart_onboarding(from_number):
    """Redémarre l'onboarding complet"""
    delete_user_data(from_number)
    
    new_user_data = {
        'onboarding_complete': False,
        'onboarding_step': 'start',
        'daily_calories': 0,
        'daily_proteins': 0,
        'daily_fats': 0,
        'daily_carbs': 0,
        'meals': []
    }
    update_user_data(from_number, new_user_data)
    
    from simple_onboarding import handle_simple_onboarding
    onboarding_message = handle_simple_onboarding(from_number, '/first_try', new_user_data)
    send_whatsapp_reply(from_number, onboarding_message, twilio_client, current_config.TWILIO_PHONE_NUMBER)

def handle_onboarding(from_number, text_content, user_data):
    """Gère l'onboarding si pas terminé"""
    if user_data.get('onboarding_complete', True):
        return False
    
    try:
        from simple_onboarding import handle_simple_onboarding
        response = handle_simple_onboarding(from_number, text_content, user_data)
        send_whatsapp_reply(from_number, response, twilio_client, current_config.TWILIO_PHONE_NUMBER)
        return True
    except Exception as e:
        logger.error(f"❌ Erreur onboarding: {e}")
        send_whatsapp_reply(from_number, f"Erreur onboarding: {e}", twilio_client, current_config.TWILIO_PHONE_NUMBER)
        return True

def handle_conversation(text_content, from_number, user_data):
    """Gère les messages de conversation"""
    if is_conversation_message(text_content):
        response = chat_with_lea_natural(text_content, user_data)
        send_whatsapp_reply(from_number, response, twilio_client, current_config.TWILIO_PHONE_NUMBER)
        return True
    
    if is_nutrition_question(text_content):
        response = chat_with_nutrition_expert(text_content, user_data)
        send_whatsapp_reply(from_number, response, twilio_client, current_config.TWILIO_PHONE_NUMBER)
        return True
    
    return False

def handle_food_tracking(text_content, media_url, from_number):
    """Gère le tracking d'aliments"""
    food_data = analyze_food_request(text_content, media_url, lambda msg: logger.debug(msg))
    
    if food_data:
        update_user_nutrition(from_number, food_data)
        user_data = get_user_data(from_number)
        response = format_response_message(food_data, user_data)
        send_whatsapp_reply(from_number, response, twilio_client, current_config.TWILIO_PHONE_NUMBER)
    else:
        send_whatsapp_reply(
            from_number, 
            "😓 Je n'ai pas réussi à identifier cet aliment. Essayez avec un autre nom ou une photo plus claire.", 
            twilio_client, 
            current_config.TWILIO_PHONE_NUMBER
        )

def update_user_nutrition(from_number, food_data):
    """Met à jour les données nutritionnelles de l'utilisateur"""
    current_data = get_user_data(from_number)
    
    # Calculer les nouvelles valeurs
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
    
    # Mettre à jour les données
    current_meals = current_data.get('meals', [])
    updated_data = current_data.copy()
    updated_data.update({
        'daily_calories': new_calories,
        'daily_proteins': new_proteins,
        'daily_fats': new_fats,
        'daily_carbs': new_carbs,
        'meals': current_meals + [new_meal]
    })
    
    update_user_data(from_number, updated_data)

def format_response_message(food_data, user_data):
    """Formate le message de réponse"""
    parts = [f"✅ *{food_data['name']}* analysé!"]
    
    # Détails des ingrédients
    if food_data.get('ingredients'):
        parts.append("\n🍽️ *Ingrédients détectés:*")
        for ing in food_data['ingredients'][:5]:
            parts.append(f"• {ing['name']}: {ing['grams']}g ({ing['calories']:.0f} kcal)")
        parts.append(f"\n📏 *Poids total:* {food_data.get('total_weight', 0)}g")
    
    # Valeurs nutritionnelles
    parts.extend([
        f"\n📊 *Valeurs nutritionnelles:*",
        f"🔥 Calories: {food_data['calories']:.0f} kcal",
        f"💪 Protéines: {food_data['proteines']:.1f}g",
        f"🥑 Lipides: {food_data['lipides']:.1f}g",
        f"🍞 Glucides: {food_data['glucides']:.1f}g",
        ""
    ])
    
    # Bilan du jour
    parts.extend(format_daily_summary(user_data))
    
    return "\n".join(parts)

def format_daily_summary(user_data):
    """Formate le bilan nutritionnel du jour"""
    target_calories = user_data.get('target_calories', 0)
    daily_calories = user_data.get('daily_calories', 0)
    daily_proteins = user_data.get('daily_proteins', 0)
    daily_fats = user_data.get('daily_fats', 0)
    daily_carbs = user_data.get('daily_carbs', 0)
    
    parts = [f"📈 *Bilan du jour:*"]
    
    if target_calories > 0:
        # Avec objectifs
        target_proteins = user_data.get('target_proteins', 0)
        target_fats = user_data.get('target_fats', 0)
        target_carbs = user_data.get('target_carbs', 0)
        
        remaining_calories = target_calories - daily_calories
        remaining_proteins = target_proteins - daily_proteins
        remaining_fats = target_fats - daily_fats
        remaining_carbs = target_carbs - daily_carbs
        
        parts.extend([
            f"🔥 Calories: {daily_calories:.0f} kcal ({remaining_calories:+.0f} restantes)",
            f"💪 Protéines: {daily_proteins:.1f}g ({remaining_proteins:+.1f}g restantes)",
            f"🥑 Lipides: {daily_fats:.1f}g ({remaining_fats:+.1f}g restantes)",
            f"🍞 Glucides: {daily_carbs:.1f}g ({remaining_carbs:+.1f}g restantes)",
            "",
            f"🎯 *Objectifs:* {target_calories} kcal | {target_proteins}g | {target_fats}g | {target_carbs}g"
        ])
    else:
        # Sans objectifs
        parts.extend([
            f"🔥 Calories totales: {daily_calories:.0f} kcal",
            f"💪 Protéines: {daily_proteins:.1f}g",
            f"🥑 Lipides: {daily_fats:.1f}g",
            f"🍞 Glucides: {daily_carbs:.1f}g"
        ])
    
    parts.extend(["", "💡 Tapez /aide pour plus d'options"])
    return parts

# ===== ROUTES =====
@app.route('/whatsapp', methods=['POST', 'GET'])
def whatsapp_webhook():
    """Point d'entrée principal pour les messages WhatsApp"""
    if request.method == 'GET':
        return "Webhook WhatsApp actif!", 200
    
    from_number = request.form.get('From')
    text_content = request.form.get('Body', '').strip()
    media_url = request.form.get('MediaUrl0')
    
    logger.info(f"📱 Message de {from_number}: '{text_content}'")
    
    # Vérifications préliminaires
    if is_rate_limited(from_number):
        send_whatsapp_reply(
            from_number, 
            "⏰ Trop de messages ! Attendez une minute.", 
            twilio_client, 
            current_config.TWILIO_PHONE_NUMBER
        )
        return '<Response/>', 429
    
    if not twilio_client:
        logger.error("❌ Client Twilio non initialisé")
        return '<Response/>', 500
    
    try:
        # Récupérer/créer utilisateur
        user_data = get_user_data(from_number)
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
        
        # Traitement par priorité
        if handle_onboarding(from_number, text_content, user_data):
            return '<Response/>', 200
        
        if handle_special_commands(text_content, from_number, user_data):
            return '<Response/>', 200
        
        # Messages vocaux (désactivés)
        if not text_content and media_url and 'audio' in request.form.get('MediaContentType0', ''):
            send_whatsapp_reply(
                from_number, 
                "🎤 Messages vocaux bientôt disponibles ! Utilisez du texte ou une photo 📷", 
                twilio_client, 
                current_config.TWILIO_PHONE_NUMBER
            )
            return '<Response/>', 200
        
        # Classification et traitement
        if text_content:
            if handle_conversation(text_content, from_number, user_data):
                return '<Response/>', 200
        
        # Tracking d'aliments par défaut
        handle_food_tracking(text_content, media_url, from_number)
        return '<Response/>', 200
        
    except Exception as e:
        logger.error(f"❌ Erreur webhook: {e}")
        send_whatsapp_reply(
            from_number, 
            "😓 Erreur technique. Réessayez ou tapez /aide.", 
            twilio_client, 
            current_config.TWILIO_PHONE_NUMBER
        )
        return '<Response/>', 200

# ===== DASHBOARD KPI =====
def get_stats():
    """Récupère les statistiques"""
    try:
        conn = sqlite3.connect(current_config.DATABASE_NAME)
        cursor = conn.cursor()
        
        # Requêtes optimisées
        stats_queries = {
            'new_users_today': "SELECT COUNT(*) FROM users WHERE DATE(created_at) = DATE('now')",
            'messages_today': "SELECT COUNT(*) FROM meals WHERE DATE(date) = DATE('now')",
            'dau': "SELECT COUNT(DISTINCT phone_number) FROM meals WHERE DATE(date) = DATE('now')",
            'wau': "SELECT COUNT(DISTINCT phone_number) FROM meals WHERE DATE(date) >= DATE('now', '-7 days')",
            'total_users': "SELECT COUNT(*) FROM users"
        }
        
        stats = {}
        for key, query in stats_queries.items():
            cursor.execute(query)
            stats[key] = cursor.fetchone()[0]
        
        stats['messages_per_user'] = round(stats['messages_today'] / max(stats['dau'], 1), 1)
        stats['date'] = datetime.now().strftime('%Y-%m-%d %H:%M')
        
        conn.close()
        return stats
        
    except Exception as e:
        logger.error(f"Erreur stats: {e}")
        return {}

def get_dau_history():
    """Récupère l'historique DAU 14 jours"""
    try:
        conn = sqlite3.connect(current_config.DATABASE_NAME)
        cursor = conn.cursor()
        
        history = []
        previous_dau = 0
        
        for i in range(13, -1, -1):
            cursor.execute("""
                SELECT COUNT(DISTINCT phone_number) FROM meals 
                WHERE DATE(date) = DATE('now', '-{} days')
            """.format(i))
            
            dau_count = cursor.fetchone()[0]
            date_obj = datetime.now() - timedelta(days=i)
            
            history.append({
                'date': date_obj.strftime('%d/%m'),
                'dau': dau_count,
                'is_today': i == 0,
                'is_growth': dau_count > previous_dau if i < 13 else dau_count > 0
            })
            
            previous_dau = dau_count
        
        conn.close()
        return history
        
    except Exception as e:
        logger.error(f"Erreur historique DAU: {e}")
        return []

@app.route('/')
def dashboard():
    """Dashboard KPI simplifié"""
    stats = get_stats()
    dau_history = get_dau_history()
    
    # Générer graphique DAU
    dau_chart = ""
    for day in dau_history:
        color = "#4CAF50" if day['is_today'] else "#81C784" if day['is_growth'] else "#e0e0e0"
        dau_chart += f'<div class="dau-day" style="background-color: {color};"><div class="dau-value">{day["dau"]}</div><div class="dau-date">{day["date"]}</div></div>'
    
    return f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Léa - Dashboard v3.0</title>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }}
            .container {{ max-width: 1200px; margin: 20px auto; background: white; border-radius: 20px; box-shadow: 0 20px 40px rgba(0,0,0,0.1); overflow: hidden; }}
            .header {{ background: linear-gradient(135deg, #4CAF50, #45a049); color: white; padding: 40px; text-align: center; }}
            .header h1 {{ margin: 0; font-size: 2.5em; font-weight: 300; }}
            .status {{ background: rgba(255,255,255,0.2); padding: 10px 20px; border-radius: 20px; display: inline-block; margin-top: 15px; }}
            .metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; padding: 30px; }}
            .metric {{ background: #f8f9fa; border-radius: 15px; padding: 25px; text-align: center; border-left: 4px solid #4CAF50; transition: transform 0.2s; }}
            .metric:hover {{ transform: translateY(-5px); }}
            .metric-value {{ font-size: 2.5em; font-weight: bold; color: #2c3e50; margin: 10px 0; }}
            .metric-label {{ color: #6c757d; font-weight: 500; }}
            .dau-section {{ background: #f8f9fa; padding: 30px; }}
            .dau-title {{ text-align: center; font-size: 1.3em; font-weight: 600; margin-bottom: 20px; }}
            .dau-chart {{ display: flex; gap: 8px; max-width: 800px; margin: 0 auto; padding: 20px; background: white; border-radius: 15px; }}
            .dau-day {{ flex: 1; min-height: 60px; border-radius: 8px; display: flex; flex-direction: column; justify-content: center; align-items: center; color: white; font-weight: bold; }}
            .dau-value {{ font-size: 1.2em; }}
            .dau-date {{ font-size: 0.8em; opacity: 0.9; }}
            .info {{ padding: 30px; text-align: center; color: #6c757d; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🤖 Léa - Dashboard v3.0</h1>
                <div class="status">✓ VERSION REFACTORISÉE</div>
            </div>
            
            <div class="metrics">
                <div class="metric">
                    <div class="metric-value">{stats.get('dau', 0)}</div>
                    <div class="metric-label">Daily Active Users</div>
                </div>
                <div class="metric">
                    <div class="metric-value">{stats.get('wau', 0)}</div>
                    <div class="metric-label">Weekly Active Users</div>
                </div>
                <div class="metric">
                    <div class="metric-value">{stats.get('messages_today', 0)}</div>
                    <div class="metric-label">Messages Aujourd'hui</div>
                </div>
                <div class="metric">
                    <div class="metric-value">{stats.get('total_users', 0)}</div>
                    <div class="metric-label">Total Utilisateurs</div>
                </div>
            </div>
            
            <div class="dau-section">
                <div class="dau-title">📊 Historique DAU - 14 jours</div>
                <div class="dau-chart">{dau_chart}</div>
            </div>
            
            <div class="info">
                <strong>🚀 Code refactorisé:</strong> -40% de lignes, +100% de lisibilité<br>
                <strong>📱 Test:</strong> https://web-production-eed0c.up.railway.app/whatsapp<br>
                <em>Dernière MAJ: {stats.get('date', 'N/A')}</em>
            </div>
        </div>
    </body>
    </html>
    """

@app.route('/api/stats')
def api_stats():
    return jsonify(get_stats())

if __name__ == '__main__':
    port = int(os.getenv('PORT', 3000))
    logger.info(f"🚀 Serveur Léa v3.0 démarré sur le port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
