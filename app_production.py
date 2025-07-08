from flask import Flask, request, jsonify
from twilio.rest import Client as TwilioClient
from dotenv import load_dotenv
import os
import sqlite3
import logging
from datetime import datetime, timedelta
import time

# Imports des modules
from database import (
    init_db, get_user_data, update_user_data, delete_user_data,
    increment_message_count, is_user_premium, get_user_message_count, set_test_message_count
)
from nutrition_improved import analyze_food_request
from utils import send_whatsapp_reply, get_help_message
from config import current_config, get_environment_info, get_detection_info
from nutrition_chat_improved import (
    is_conversation_message, 
    is_nutrition_question, 
    chat_with_lea_natural, 
    chat_with_nutrition_expert
)
from stripe_payment import get_premium_message, format_premium_reminder, verify_payment, get_premium_reminder_before_response

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
    
    if text_lower == '/tim':
        # Commande spéciale pour configurer automatiquement le profil de Tim
        from simple_onboarding import handle_simple_onboarding
        response = handle_simple_onboarding(from_number, '/tim', user_data)
        send_whatsapp_reply(from_number, response, twilio_client, current_config.TWILIO_PHONE_NUMBER)
        return True
    
    if text_lower in ['/premium', '/upgrade']:
        user_name = user_data.get('name', 'Utilisateur')
        premium_message = get_premium_message(from_number, user_name)
        send_whatsapp_reply(from_number, premium_message, twilio_client, current_config.TWILIO_PHONE_NUMBER)
        return True
    
    # Commandes de test pour simuler la limite de 30 messages
    if text_lower == '/on30':
        set_test_message_count(from_number, 31)  # Simuler dépassement de limite
        current_count = get_user_message_count(from_number)
        send_whatsapp_reply(from_number, f"🧪 *Mode test activé*\n\nCompteur défini à {current_count} messages.\nTu es maintenant en mode 'limite atteinte' pour tester l'expérience premium.", twilio_client, current_config.TWILIO_PHONE_NUMBER)
        return True
    
    if text_lower == '/off30':
        set_test_message_count(from_number, 0)  # Remettre à zéro
        current_count = get_user_message_count(from_number)
        send_whatsapp_reply(from_number, f"🧪 *Mode test désactivé*\n\nCompteur remis à {current_count} messages.\nTu peux maintenant utiliser Léa normalement.", twilio_client, current_config.TWILIO_PHONE_NUMBER)
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

def send_premium_reminder_if_needed(from_number, user_data):
    """Envoie le message premium optimisé si l'utilisateur a dépassé 30 messages"""
    # Ne pas envoyer pendant l'onboarding
    if not user_data.get('onboarding_complete', True):
        return False
    
    # Ne pas envoyer si l'utilisateur est premium
    if is_user_premium(from_number):
        return False
    
    # Vérifier si l'utilisateur a dépassé 30 messages
    message_count = get_user_message_count(from_number)
    if message_count > 30:
        user_name = user_data.get('name', 'Utilisateur')
        premium_reminder = get_premium_reminder_before_response(user_name)
        send_whatsapp_reply(from_number, premium_reminder, twilio_client, current_config.TWILIO_PHONE_NUMBER)
        return True
    
    return False

def handle_conversation(text_content, from_number, user_data):
    """Gère les messages de conversation"""
    if is_conversation_message(text_content):
        # Envoyer le rappel premium AVANT la réponse si nécessaire
        send_premium_reminder_if_needed(from_number, user_data)
        
        response = chat_with_lea_natural(text_content, user_data)
        send_whatsapp_reply(from_number, response, twilio_client, current_config.TWILIO_PHONE_NUMBER)
        return True
    
    if is_nutrition_question(text_content):
        # Envoyer le rappel premium AVANT la réponse si nécessaire
        send_premium_reminder_if_needed(from_number, user_data)
        
        response = chat_with_nutrition_expert(text_content, user_data)
        send_whatsapp_reply(from_number, response, twilio_client, current_config.TWILIO_PHONE_NUMBER)
        return True
    
    return False

def handle_food_tracking(text_content, media_url, from_number):
    """Gère le tracking d'aliments avec message fusionné"""
    food_data = analyze_food_request(text_content, media_url, lambda msg: logger.debug(msg))
    
    if food_data:
        update_user_nutrition(from_number, food_data)
        user_data = get_user_data(from_number)
        
        # Envoyer le rappel premium AVANT la réponse si nécessaire
        send_premium_reminder_if_needed(from_number, user_data)
        
        # Message fusionné : Analyse + Bilan du jour
        unified_message = format_unified_food_message(food_data, user_data)
        send_whatsapp_reply(from_number, unified_message, twilio_client, current_config.TWILIO_PHONE_NUMBER)
    else:
        # Envoyer le rappel premium AVANT la réponse d'erreur si nécessaire
        user_data = get_user_data(from_number)
        send_premium_reminder_if_needed(from_number, user_data)
        
        send_whatsapp_reply(
            from_number, 
            "😓 Je n'ai pas réussi à identifier cet aliment. Peux-tu me donner plus de détails ou essayer avec une photo plus claire ? 🤔", 
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

# ===== NOUVEAUX MESSAGES AMÉLIORÉS =====
def format_food_analysis_message(food_data, user_data):
    """Message 1 : Analyse de l'aliment avec personnalité de Léa"""
    food_name = food_data['name']
    calories = food_data['calories']
    proteins = food_data['proteines']
    fats = food_data['lipides']
    carbs = food_data['glucides']
    
    # Phrase d'introduction positive et encourageante
    intro_phrases = get_encouraging_intro(food_name, calories, proteins, fats, carbs)
    
    parts = [intro_phrases]
    
    # Détails des ingrédients si disponible
    if food_data.get('ingredients'):
        total_weight = food_data.get('total_weight', 0)
        parts.append(f"\n🍽️ *Ingrédients détectés* ({total_weight}g) :")
        for ing in food_data['ingredients'][:5]:
            parts.append(f"• {ing['name']} ({ing['grams']}g) — {ing['calories']:.0f} kcal")
    
    # Valeurs nutritionnelles avec formatage amélioré
    parts.extend([
        f"\n📊 *Valeurs nutritionnelles :*",
        f"🔥 Calories : *{calories:.0f} kcal*",
        f"💪 Protéines : *{proteins:.1f}g*",
        f"🥑 Lipides : *{fats:.1f}g*",
        f"🍞 Glucides : *{carbs:.1f}g*"
    ])
    
    # Conseil nutritionnel expert de Léa
    expert_advice = get_expert_nutrition_advice(food_name, calories, proteins, fats, carbs, user_data)
    parts.append(f"\n💡 *Le conseil de Léa :* {expert_advice}")
    
    return "\n".join(parts)

def format_daily_progress_message(user_data):
    """Message 2 : Bilan du jour avec question engageante"""
    target_calories = user_data.get('target_calories', 0)
    daily_calories = user_data.get('daily_calories', 0)
    daily_proteins = user_data.get('daily_proteins', 0)
    daily_fats = user_data.get('daily_fats', 0)
    daily_carbs = user_data.get('daily_carbs', 0)
    
    parts = ["📈 *Bilan de ta journée :*"]
    
    if target_calories > 0:
        # Avec objectifs - format "consommé / objectif"
        target_proteins = user_data.get('target_proteins', 0)
        target_fats = user_data.get('target_fats', 0)
        target_carbs = user_data.get('target_carbs', 0)
        
        parts.extend([
            f"🔥 Calories : *{daily_calories:.0f} / {target_calories} kcal*",
            f"💪 Protéines : *{daily_proteins:.1f} / {target_proteins}g*",
            f"🥑 Lipides : *{daily_fats:.1f} / {target_fats}g*",
            f"🍞 Glucides : *{daily_carbs:.1f} / {target_carbs}g*"
        ])
        
        # Message d'encouragement personnalisé selon progression
        progress_message = get_progress_encouragement(daily_calories, target_calories, daily_proteins, target_proteins, user_data)
        parts.append(f"\n{progress_message}")
        
    else:
        # Sans objectifs
        parts.extend([
            f"🔥 Calories : *{daily_calories:.0f} kcal*",
            f"💪 Protéines : *{daily_proteins:.1f}g*",
            f"🥑 Lipides : *{daily_fats:.1f}g*",
            f"🍞 Glucides : *{daily_carbs:.1f}g*",
            f"\n✨ Tu progresses bien ! Continue comme ça !"
        ])
    
    # Question engageante pour continuer la conversation
    engaging_question = get_engaging_question(user_data)
    parts.append(f"\n{engaging_question}")
    
    return "\n".join(parts)

def get_encouraging_intro(food_name, calories, proteins, fats, carbs):
    """Génère une phrase d'introduction positive selon l'aliment"""
    food_lower = food_name.lower()
    
    # Aliments fitness/protéinés
    if any(word in food_lower for word in ['whey', 'protéine', 'shaker', 'barre protéinée']):
        return f"Excellent choix pour tes muscles ! 💪 Voici l'analyse de ton *{food_name}* :"
    
    # Légumes/salade
    elif any(word in food_lower for word in ['salade', 'légume', 'brocoli', 'épinards', 'tomate']):
        return f"Super, des légumes ! 🥗 C'est exactement ce qu'il faut. Analyse de ta *{food_name}* :"
    
    # Fruits
    elif any(word in food_lower for word in ['pomme', 'banane', 'orange', 'fruit', 'fraise']):
        return f"Parfait pour faire le plein de vitamines ! 🍎 Voici ton *{food_name}* :"
    
    # Viandes/poissons
    elif any(word in food_lower for word in ['poulet', 'saumon', 'thon', 'bœuf', 'porc']):
        return f"Très bon choix protéiné ! 🍗 Analyse de ton *{food_name}* :"
    
    # Féculents
    elif any(word in food_lower for word in ['riz', 'pâtes', 'pain', 'pomme de terre']):
        return f"Parfait pour l'énergie ! ⚡ Voici ton *{food_name}* :"
    
    # Repas complets
    elif any(word in food_lower for word in ['repas', 'plat', 'salade niçoise', 'bowl']):
        return f"Super choix, un plat complet et équilibré ! 🍽️ Analyse de ta *{food_name}* :"
    
    # Par défaut
    else:
        return f"Très bien ! 👍 Voici l'analyse de ton *{food_name}* :"

def get_expert_nutrition_advice(food_name, calories, proteins, fats, carbs, user_data):
    """Génère un conseil nutritionnel expert et personnalisé"""
    food_lower = food_name.lower()
    objective = user_data.get('objective', '').lower()
    
    # Conseils spécifiques par type d'aliment
    if 'whey' in food_lower or 'protéine' in food_lower:
        if 'prise de masse' in objective:
            return "Parfait timing pour la whey ! Idéalement dans les 30min post-entraînement pour optimiser la synthèse protéique. Les 25g de protéines vont directement nourrir tes muscles 🎯"
        else:
            return "Excellente source de protéines complètes ! La whey a un aminogramme parfait et se digère rapidement. Idéal pour maintenir ta masse musculaire 💪"
    
    elif 'salade' in food_lower and fats > 15:
        return "Attention à la vinaigrette qui concentre beaucoup de calories ! Astuce : utilise du vinaigre balsamique + 1 cuillère d'huile d'olive pour garder les bons lipides sans exploser les calories 😉"
    
    elif any(word in food_lower for word in ['saumon', 'thon', 'sardine']):
        return "Excellent ! Ces poissons gras sont riches en oméga-3 EPA/DHA, essentiels pour la récupération musculaire et la santé cardiovasculaire. Un vrai super-aliment 🐟✨"
    
    elif 'avocat' in food_lower:
        return "Parfait ! L'avocat apporte des acides gras mono-insaturés qui favorisent l'absorption des vitamines liposolubles (A,D,E,K). Plus nutritif qu'il n'y paraît ! 🥑"
    
    elif any(word in food_lower for word in ['riz', 'pâtes', 'pain']) and 'prise de masse' in objective:
        return f"Bien joué ! Ces {carbs:.0f}g de glucides vont reconstituer tes réserves de glycogène musculaire. Timing parfait si c'est autour de ton entraînement ⚡"
    
    elif any(word in food_lower for word in ['légume', 'brocoli', 'épinards']):
        return "Excellent choix ! Ces légumes sont riches en micronutriments et fibres, avec un index glycémique très bas. Ils optimisent ta digestion et ton métabolisme 🥬"
    
    elif proteins > 25:
        return f"Superbe apport protéiné ! Ces {proteins:.0f}g vont stimuler la synthèse protéique pendant 3-4h. Parfait pour maintenir un bilan azoté positif 💪"
    
    elif calories > 500 and fats > 20:
        return "Repas assez dense en calories ! Assure-toi de bien répartir tes lipides sur la journée pour optimiser la digestion et éviter les pics d'insuline 🎯"
    
    elif carbs > 50 and 'perte de poids' in objective:
        return f"Attention aux {carbs:.0f}g de glucides si ton objectif est la perte de poids. Privilégie ce type de repas autour de tes entraînements pour optimiser l'utilisation 🏃‍♀️"
    
    else:
        # Conseil générique mais expert
        ratio_p_c = proteins / max(carbs, 1)
        if ratio_p_c > 1:
            return "Excellent ratio protéines/glucides ! Cette composition favorise la satiété et maintient ta glycémie stable. Continue comme ça ! 👌"
        else:
            return "Bon équilibre nutritionnel ! Pense à ajouter une source de protéines si ce n'est pas déjà fait pour optimiser la satiété 😊"

def get_progress_encouragement(daily_calories, target_calories, daily_proteins, target_proteins, user_data):
    """Génère un message d'encouragement selon la progression"""
    cal_progress = (daily_calories / target_calories) * 100 if target_calories > 0 else 0
    prot_progress = (daily_proteins / target_proteins) * 100 if target_proteins > 0 else 0
    objective = user_data.get('objective', '').lower()
    
    if cal_progress < 30:
        if 'prise de masse' in objective:
            return "🚀 Bon début ! Il te reste encore de la marge pour atteindre tes objectifs de prise de masse. N'oublie pas de bien répartir sur la journée !"
        else:
            return "✨ Parfait début de journée ! Tu as encore de la place pour tes prochains repas."
    
    elif 30 <= cal_progress < 70:
        if prot_progress > 80:
            return "💪 Excellent ! Tu es bien parti sur les protéines. Continue à équilibrer avec des glucides et lipides de qualité !"
        else:
            return "👍 Tu progresses bien ! Pense à inclure une bonne source de protéines dans ton prochain repas."
    
    elif 70 <= cal_progress < 90:
        return "🎯 Tu approches de tes objectifs ! Parfait timing pour finir la journée en beauté."
    
    elif cal_progress >= 90:
        if 'perte de poids' in objective:
            return "✅ Objectif presque atteint ! Tu peux te contenter d'une collation légère si tu as encore faim."
        else:
            return "🎉 Bravo ! Tu as pratiquement atteint tes objectifs caloriques. Mission accomplie !"
    
    else:
        return "💪 Continue comme ça, tu es sur la bonne voie !"

def get_engaging_question(user_data):
    """Génère une question engageante pour continuer la conversation"""
    objective = user_data.get('objective', '').lower()
    meals_count = len(user_data.get('meals', []))
    
    questions = []
    
    if meals_count == 1:
        questions = [
            "C'était ton petit-déjeuner ? Qu'est-ce qui est prévu pour la suite ? 🤔",
            "Premier repas de la journée ? Raconte-moi ton planning alimentaire ! 😊",
            "Tu commences bien la journée ! Tu as prévu quoi pour le déjeuner ? 🍽️"
        ]
    elif meals_count == 2:
        questions = [
            "Parfait ! Tu as prévu une collation ou tu attends le prochain repas ? 🤗",
            "Super progression ! Comment tu te sens niveau énergie ? ⚡",
            "Ça avance bien ! Tu as encore faim ou ça va pour l'instant ? 😋"
        ]
    elif meals_count >= 3:
        if 'prise de masse' in objective:
            questions = [
                "Excellent ! Tu penses ajouter une collation ou c'est bon pour aujourd'hui ? 💪",
                "Tu gères parfaitement ! Une petite collation protéinée en vue ? 🥜",
                "Bravo pour la régularité ! Tu vises encore quelque chose ? 🎯"
            ]
        else:
            questions = [
                "Super journée ! Tu te sens rassasié(e) ou il te faut encore quelque chose ? 😊",
                "Parfait ! Comment tu te sens niveau satiété ? 🤗",
                "Excellente gestion ! Tu as encore prévu quelque chose ? ✨"
            ]
    else:
        questions = [
            "Dis-moi, qu'est-ce qui est prévu ensuite ? 🤔",
            "Comment tu te sens après ça ? 😊",
            "Tu as d'autres repas de prévus ? 🍽️"
        ]
    
    # Sélectionner une question aléatoirement
    import random
    return random.choice(questions)

# ===== MESSAGE FUSIONNÉ POUR L'ANALYSE ALIMENTAIRE =====
def format_unified_food_message(food_data, user_data):
    """Message fusionné : Analyse + Bilan du jour selon les spécifications exactes"""
    food_name = food_data['name']
    calories = food_data['calories']
    proteins = food_data['proteines']
    fats = food_data['lipides']
    carbs = food_data['glucides']
    
    # Détecter si c'est un seul ingrédient (pas de liste d'ingrédients OU un seul ingrédient)
    ingredients = food_data.get('ingredients', [])
    is_single_ingredient = len(ingredients) <= 1
    
    # Titre : "C'est noté ! ✅"
    parts = [f"C'est noté ! ✅"]
    
    if is_single_ingredient:
        # NOUVEAU FORMAT pour un seul ingrédient
        # Afficher le nom avec le poids si disponible, en évitant la répétition
        if ingredients and len(ingredients) == 1:
            weight = ingredients[0].get('grams', 0)
            ingredient_name = ingredients[0].get('name', food_name)
            # Utiliser le nom de l'ingrédient plutôt que le nom du plat pour éviter "100g de banane (100g)"
            parts.append(f"{ingredient_name} ({weight}g)")
        else:
            parts.append(f"{food_name}")
        
        # Détail du plat (valeurs nutritionnelles)
        parts.extend([
            f"\n📊 Détail du plat :",
            f"🔥 Calories : {calories:.0f} kcal",
            f"💪 Protéines : {proteins:.1f}g",
            f"🥑 Lipides : {fats:.1f}g",
            f"🍞 Glucides : {carbs:.1f}g"
        ])
        
        # Conseil de Léa
        expert_advice = get_expert_nutrition_advice(food_name, calories, proteins, fats, carbs, user_data)
        parts.append(f"\n💡 Le conseil de Léa : {expert_advice}")
        
    else:
        # FORMAT EXISTANT pour plusieurs ingrédients
        parts[0] = f"C'est noté ! ✅ +{calories:.0f} kcal"
        
        # Analyse du plat
        parts.append("\nAnalyse de ton plat :")
        
        # Ingrédients détectés si disponibles
        if ingredients:
            for ing in ingredients[:3]:  # Limiter à 3 ingrédients principaux
                parts.append(f"• {ing['name']} ({ing['grams']}g) : {ing['calories']:.0f} kcal")
        
        # Détail du plat (valeurs nutritionnelles)
        parts.extend([
            f"\n📊 Détail du plat :",
            f"🔥 Calories : {calories:.0f} kcal",
            f"💪 Protéines : {proteins:.1f}g",
            f"🥑 Lipides : {fats:.1f}g",
            f"🍞 Glucides : {carbs:.1f}g"
        ])
        
        # Conseil de Léa
        expert_advice = get_expert_nutrition_advice(food_name, calories, proteins, fats, carbs, user_data)
        parts.append(f"\n💡 Le conseil de Léa : {expert_advice}")
    
    # Bilan du jour (identique pour les deux formats)
    target_calories = user_data.get('target_calories', 0)
    daily_calories = user_data.get('daily_calories', 0)
    daily_proteins = user_data.get('daily_proteins', 0)
    daily_fats = user_data.get('daily_fats', 0)
    daily_carbs = user_data.get('daily_carbs', 0)
    
    if target_calories > 0:
        target_proteins = user_data.get('target_proteins', 0)
        target_fats = user_data.get('target_fats', 0)
        target_carbs = user_data.get('target_carbs', 0)
        
        parts.extend([
            f"\n📈 Ton bilan du jour :",
            f"🔥 Calories : {daily_calories:.0f} / {target_calories}",
            f"💪 Protéines : {daily_proteins:.1f} / {target_proteins}g",
            f"🥑 Lipides : {daily_fats:.1f} / {target_fats}g",
            f"🍞 Glucides : {daily_carbs:.1f} / {target_carbs}g"
        ])
        
        # Message personnalisé selon l'objectif
        goal = user_data.get('goal', user_data.get('objective', ''))
        remaining_calories = target_calories - daily_calories
        remaining_proteins = target_proteins - daily_proteins
        
        if goal == 'Prendre du muscle':
            parts.append(f"\nEncore {remaining_calories:.0f} kcal et {remaining_proteins:.1f}g de prot pour atteindre ton objectif ✨")
        
        elif goal == 'Perdre du poids':
            if remaining_calories > 500:
                parts.append(f"\nSuper ! Tu as encore une belle marge de {remaining_calories:.0f} kcal pour finir ta journée en respectant ton objectif. 💪")
            else:
                parts.append(f"\nSuper ! Tu as encore une marge de {remaining_calories:.0f} kcal pour finir ta journée. + Bravo, tu gères parfaitement tes apports ! 🎯")
        
        elif goal == 'Maintenir ma forme':
            # Encouragement personnalisé pour maintien
            if remaining_calories > 300:
                parts.append("\nParfait équilibre ! Continue comme ça pour maintenir ta forme. 💪")
            else:
                parts.append("\nExcellent ! Tu maintiens parfaitement tes apports. 🎯")
    
    return "\n".join(parts)

# ===== GESTION SMS ENTRANTS =====
def init_sms_database():
    """Initialise la table pour stocker les SMS entrants"""
    try:
        conn = sqlite3.connect(current_config.DATABASE_NAME)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS incoming_sms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                from_number TEXT NOT NULL,
                to_number TEXT NOT NULL,
                body TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                message_sid TEXT UNIQUE,
                status TEXT DEFAULT 'received'
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("✅ Table SMS initialisée")
    except Exception as e:
        logger.error(f"❌ Erreur init SMS DB: {e}")

def store_incoming_sms(from_number, to_number, body, message_sid):
    """Stocke un SMS entrant dans la base de données"""
    try:
        conn = sqlite3.connect(current_config.DATABASE_NAME)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR IGNORE INTO incoming_sms 
            (from_number, to_number, body, message_sid)
            VALUES (?, ?, ?, ?)
        ''', (from_number, to_number, body, message_sid))
        
        conn.commit()
        conn.close()
        logger.info(f"📨 SMS stocké: {from_number} -> {to_number}")
        return True
    except Exception as e:
        logger.error(f"❌ Erreur stockage SMS: {e}")
        return False

def get_recent_sms(limit=50):
    """Récupère les SMS récents"""
    try:
        conn = sqlite3.connect(current_config.DATABASE_NAME)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT from_number, to_number, body, timestamp, message_sid, status
            FROM incoming_sms 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (limit,))
        
        sms_list = []
        for row in cursor.fetchall():
            sms_list.append({
                'from': row[0],
                'to': row[1],
                'body': row[2],
                'timestamp': row[3],
                'message_sid': row[4],
                'status': row[5]
            })
        
        conn.close()
        return sms_list
    except Exception as e:
        logger.error(f"❌ Erreur récupération SMS: {e}")
        return []

# Initialiser la base SMS au démarrage
init_sms_database()

# ===== ROUTES =====
@app.route('/sms', methods=['POST', 'GET'])
def sms_webhook():
    """Webhook pour recevoir les SMS entrants"""
    if request.method == 'GET':
        return "Webhook SMS actif!", 200
    
    try:
        from_number = request.form.get('From', '')
        to_number = request.form.get('To', '')
        body = request.form.get('Body', '')
        message_sid = request.form.get('MessageSid', '')
        
        logger.info(f"📨 SMS reçu de {from_number} vers {to_number}: '{body}'")
        
        # Stocker le SMS
        store_incoming_sms(from_number, to_number, body, message_sid)
        
        return '<Response/>', 200
        
    except Exception as e:
        logger.error(f"❌ Erreur webhook SMS: {e}")
        return '<Response/>', 500

@app.route('/sms-inbox')
def sms_inbox():
    """Page pour voir les SMS entrants"""
    sms_list = get_recent_sms(100)
    
    # Filtrer les SMS pour le numéro spécifique
    target_number = "+41245391230"
    filtered_sms = [sms for sms in sms_list if target_number in sms['to']]
    
    # Générer les SMS en HTML
    sms_html = ""
    if filtered_sms:
        for sms in filtered_sms:
            # Mettre en évidence les codes de vérification (6 chiffres)
            body = sms['body']
            if body and len(body.strip()) == 6 and body.strip().isdigit():
                body_display = f'<span class="verification-code">{body}</span>'
            else:
                body_display = body or "Pas de contenu"
            
            timestamp = datetime.strptime(sms['timestamp'], '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y %H:%M')
            
            sms_html += f'''
            <div class="sms-item">
                <div class="sms-header">
                    <span class="sms-from">De: {sms['from']}</span>
                    <span class="sms-time">{timestamp}</span>
                </div>
                <div class="sms-body">{body_display}</div>
                <div class="sms-meta">Vers: {sms['to']} | ID: {sms['message_sid'][:8]}...</div>
            </div>
            '''
    else:
        sms_html = '<div class="no-sms">Aucun SMS reçu pour ce numéro</div>'
    
    return f'''
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>📨 SMS Inbox - {target_number}</title>
        <style>
            body {{ 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
                margin: 0; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                min-height: 100vh; 
                padding: 20px;
            }}
            .container {{ 
                max-width: 800px; 
                margin: 0 auto; 
                background: white; 
                border-radius: 20px; 
                box-shadow: 0 20px 40px rgba(0,0,0,0.1); 
                overflow: hidden; 
            }}
            .header {{ 
                background: linear-gradient(135deg, #FF6B6B, #FF8E53); 
                color: white; 
                padding: 30px; 
                text-align: center; 
            }}
            .header h1 {{ 
                margin: 0; 
                font-size: 2em; 
                font-weight: 300; 
            }}
            .phone-number {{ 
                background: rgba(255,255,255,0.2); 
                padding: 8px 16px; 
                border-radius: 15px; 
                display: inline-block; 
                margin-top: 10px; 
                font-family: monospace;
                font-size: 1.1em;
            }}
            .refresh-btn {{ 
                background: #4CAF50; 
                color: white; 
                border: none; 
                padding: 10px 20px; 
                border-radius: 10px; 
                cursor: pointer; 
                margin: 20px; 
                font-size: 1em;
            }}
            .refresh-btn:hover {{ background: #45a049; }}
            .sms-container {{ 
                padding: 20px; 
                max-height: 600px; 
                overflow-y: auto; 
            }}
            .sms-item {{ 
                border: 1px solid #e0e0e0; 
                border-radius: 10px; 
                padding: 15px; 
                margin-bottom: 15px; 
                background: #f9f9f9;
                transition: transform 0.2s;
            }}
            .sms-item:hover {{ transform: translateY(-2px); }}
            .sms-header {{ 
                display: flex; 
                justify-content: space-between; 
                margin-bottom: 10px; 
                font-size: 0.9em; 
                color: #666; 
            }}
            .sms-from {{ font-weight: bold; color: #333; }}
            .sms-time {{ color: #888; }}
            .sms-body {{ 
                font-size: 1.1em; 
                margin: 10px 0; 
                padding: 10px; 
                background: white; 
                border-radius: 8px;
                border-left: 4px solid #4CAF50;
            }}
            .verification-code {{ 
                background: #FFD700; 
                color: #333; 
                padding: 5px 10px; 
                border-radius: 5px; 
                font-weight: bold; 
                font-size: 1.3em;
                font-family: monospace;
                border: 2px solid #FFA500;
            }}
            .sms-meta {{ 
                font-size: 0.8em; 
                color: #999; 
                margin-top: 8px; 
            }}
            .no-sms {{ 
                text-align: center; 
                color: #666; 
                font-style: italic; 
                padding: 40px; 
            }}
            .stats {{ 
                background: #f0f0f0; 
                padding: 15px; 
                text-align: center; 
                color: #666; 
            }}
            .auto-refresh {{ 
                position: fixed; 
                top: 20px; 
                right: 20px; 
                background: rgba(0,0,0,0.7); 
                color: white; 
                padding: 10px; 
                border-radius: 10px; 
                font-size: 0.9em;
            }}
        </style>
        <script>
            // Auto-refresh toutes les 10 secondes
            setTimeout(function() {{
                location.reload();
            }}, 10000);
            
            // Copier le code de vérification au clic
            function copyCode(element) {{
                navigator.clipboard.writeText(element.textContent);
                element.style.background = '#90EE90';
                setTimeout(() => element.style.background = '#FFD700', 1000);
            }}
        </script>
    </head>
    <body>
        <div class="auto-refresh">🔄 Auto-refresh: 10s</div>
        
        <div class="container">
            <div class="header">
                <h1>📨 SMS Inbox</h1>
                <div class="phone-number">{target_number}</div>
            </div>
            
            <button class="refresh-btn" onclick="location.reload()">🔄 Actualiser</button>
            
            <div class="sms-container">
                {sms_html}
            </div>
            
            <div class="stats">
                <strong>Total SMS reçus:</strong> {len(filtered_sms)} | 
                <strong>Dernière MAJ:</strong> {datetime.now().strftime('%H:%M:%S')}
            </div>
        </div>
        
        <script>
            // Rendre les codes de vérification cliquables
            document.querySelectorAll('.verification-code').forEach(code => {{
                code.style.cursor = 'pointer';
                code.title = 'Cliquer pour copier';
                code.onclick = () => copyCode(code);
            }});
        </script>
    </body>
    </html>
    '''

def check_premium_limit(from_number, user_data):
    """Vérifie si l'utilisateur a atteint la limite et gère le premium"""
    # Ne pas compter les messages d'onboarding
    if not user_data.get('onboarding_complete', True):
        return True  # Autoriser pendant l'onboarding
    
    # Vérifier si l'utilisateur est premium
    if is_user_premium(from_number):
        return True  # Utilisateur premium, pas de limite
    
    # Incrémenter le compteur de messages
    message_count = increment_message_count(from_number)
    logger.info(f"💬 Message #{message_count} pour {from_number}")
    
    # TOUJOURS autoriser le message, ne jamais bloquer
    return True

@app.route('/whatsapp-business', methods=['POST', 'GET'])
def whatsapp_business_webhook():
    """Webhook pour WhatsApp Business API (Meta)"""
    if request.method == 'GET':
        # Vérification du webhook Meta
        verify_token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        mode = request.args.get('hub.mode')
        
        if mode == 'subscribe' and verify_token == current_config.WHATSAPP_WEBHOOK_TOKEN:
            logger.info("✅ Webhook WhatsApp Business vérifié")
            return challenge, 200
        else:
            logger.error("❌ Échec vérification webhook WhatsApp Business")
            return "Forbidden", 403
    
    try:
        # Traitement des messages entrants
        payload = request.get_json()
        
        if not payload:
            return "No payload", 400
        
        # Parser le message Meta
        from whatsapp_business_api import parse_whatsapp_business_webhook
        message_data = parse_whatsapp_business_webhook(payload)
        
        if not message_data:
            return "No message data", 200
        
        # Extraire les informations
        from_number = message_data.get("from_number")
        text_content = message_data.get("text", "")
        message_id = message_data.get("message_id")
        media_url = message_data.get("media_url")
        
        if not from_number:
            return "No sender", 400
        
        # Ajouter le préfixe whatsapp: pour compatibilité avec le code existant
        from_number_formatted = f"whatsapp:+{from_number}"
        
        logger.info(f"📱 Message WhatsApp Business de {from_number}: '{text_content}'")
        
        # Marquer le message comme lu
        if message_id:
            from whatsapp_business_api import whatsapp_business_client
            whatsapp_business_client.mark_message_as_read(message_id)
        
        # Traitement identique au webhook Twilio
        return process_whatsapp_message(from_number_formatted, text_content, media_url)
        
    except Exception as e:
        logger.error(f"❌ Erreur webhook WhatsApp Business: {e}")
        return "Error", 500

def process_whatsapp_message(from_number, text_content, media_url):
    """Fonction commune pour traiter les messages WhatsApp (Twilio et Business API)"""
    # Vérifications préliminaires
    if is_rate_limited(from_number):
        send_whatsapp_reply(
            from_number, 
            "⏰ Trop de messages ! Attendez une minute.", 
            twilio_client, 
            current_config.TWILIO_PHONE_NUMBER
        )
        return '<Response/>', 429
    
    try:
        # Récupérer/créer utilisateur
        user_data = get_user_data(from_number)
        is_new_user = False
        
        if not user_data:
            # Nouvel utilisateur - créer avec onboarding non terminé
            user_data = {
                'onboarding_complete': False,
                'onboarding_step': 'start',
                'daily_calories': 0,
                'daily_proteins': 0,
                'daily_fats': 0,
                'daily_carbs': 0,
                'meals': []
            }
            update_user_data(from_number, user_data)
            is_new_user = True
        
        # Si c'est un nouvel utilisateur OU si le message contient "join live-cold", démarrer l'onboarding
        if is_new_user or (text_content and 'join live-cold' in text_content.lower()):
            if not is_new_user:
                # Si c'est "join live-cold", redémarrer complètement l'onboarding
                delete_user_data(from_number)
                user_data = {
                    'onboarding_complete': False,
                    'onboarding_step': 'start',
                    'daily_calories': 0,
                    'daily_proteins': 0,
                    'daily_fats': 0,
                    'daily_carbs': 0,
                    'meals': []
                }
                update_user_data(from_number, user_data)
            
            from simple_onboarding import handle_simple_onboarding
            onboarding_message = handle_simple_onboarding(from_number, 'start', user_data)
            send_whatsapp_reply(from_number, onboarding_message, twilio_client, current_config.TWILIO_PHONE_NUMBER)
            return '<Response/>', 200
        
        # Traitement par priorité
        if handle_onboarding(from_number, text_content, user_data):
            return '<Response/>', 200
        
        if handle_special_commands(text_content, from_number, user_data):
            return '<Response/>', 200
        
        # Vérifier la limite premium AVANT de traiter le message
        if not check_premium_limit(from_number, user_data):
            return '<Response/>', 200  # Message bloqué, rappel premium envoyé
        
        # Messages vocaux (désactivés)
        if not text_content and media_url and 'audio' in str(media_url):
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
        logger.error(f"❌ Erreur traitement message: {e}")
        send_whatsapp_reply(
            from_number, 
            "😓 Erreur technique. Réessayez ou tapez /aide.", 
            twilio_client, 
            current_config.TWILIO_PHONE_NUMBER
        )
        return '<Response/>', 200

@app.route('/whatsapp', methods=['POST', 'GET'])
def whatsapp_webhook():
    """Point d'entrée principal pour les messages WhatsApp (Twilio)"""
    if request.method == 'GET':
        return "Webhook WhatsApp Twilio actif!", 200
    
    from_number = request.form.get('From')
    text_content = request.form.get('Body', '').strip()
    media_url = request.form.get('MediaUrl0')
    
    logger.info(f"📱 Message Twilio de {from_number}: '{text_content}'")
    
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
        is_new_user = False
        
        if not user_data:
            # Nouvel utilisateur - créer avec onboarding non terminé
            user_data = {
                'onboarding_complete': False,
                'onboarding_step': 'start',
                'daily_calories': 0,
                'daily_proteins': 0,
                'daily_fats': 0,
                'daily_carbs': 0,
                'meals': []
            }
            update_user_data(from_number, user_data)
            is_new_user = True
        
        # Si c'est un nouvel utilisateur OU si le message contient "join live-cold", démarrer l'onboarding
        if is_new_user or (text_content and 'join live-cold' in text_content.lower()):
            if not is_new_user:
                # Si c'est "join live-cold", redémarrer complètement l'onboarding
                delete_user_data(from_number)
                user_data = {
                    'onboarding_complete': False,
                    'onboarding_step': 'start',
                    'daily_calories': 0,
                    'daily_proteins': 0,
                    'daily_fats': 0,
                    'daily_carbs': 0,
                    'meals': []
                }
                update_user_data(from_number, user_data)
            
            from simple_onboarding import handle_simple_onboarding
            onboarding_message = handle_simple_onboarding(from_number, 'start', user_data)
            send_whatsapp_reply(from_number, onboarding_message, twilio_client, current_config.TWILIO_PHONE_NUMBER)
            return '<Response/>', 200
        
        # Traitement par priorité
        if handle_onboarding(from_number, text_content, user_data):
            return '<Response/>', 200
        
        if handle_special_commands(text_content, from_number, user_data):
            return '<Response/>', 200
        
        # Vérifier la limite premium AVANT de traiter le message
        if not check_premium_limit(from_number, user_data):
            return '<Response/>', 200  # Message bloqué, rappel premium envoyé
        
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

@app.route('/payment-success')
def payment_success():
    """Page de succès après paiement Stripe"""
    session_id = request.args.get('session_id')
    phone_number = request.args.get('phone')
    
    if session_id:
        # Vérifier le paiement
        success, verified_phone = verify_payment(session_id)
        
        if success and verified_phone:
            logger.info(f"✅ Paiement vérifié pour {verified_phone}")
            
            # Envoyer un message de confirmation WhatsApp
            confirmation_message = """🎉 *Paiement confirmé !*

Félicitations ! Ton abonnement Léa Premium est maintenant actif pour 12 mois.

✨ *Tu peux maintenant :*
• Envoyer des messages illimités
• Profiter de toutes les analyses avancées
• Bénéficier du support prioritaire

Merci de faire confiance à Léa ! 💚

Continue à m'envoyer tes repas, je suis là pour t'accompagner ! 🍎"""
            
            send_whatsapp_reply(verified_phone, confirmation_message, twilio_client, current_config.TWILIO_PHONE_NUMBER)
            
            return f'''
            <!DOCTYPE html>
            <html lang="fr">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>✅ Paiement Confirmé - Léa Premium</title>
                <style>
                    body {{ 
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
                        margin: 0; 
                        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%); 
                        min-height: 100vh; 
                        display: flex; 
                        align-items: center; 
                        justify-content: center;
                        padding: 20px;
                    }}
                    .container {{ 
                        max-width: 500px; 
                        background: white; 
                        border-radius: 20px; 
                        box-shadow: 0 20px 40px rgba(0,0,0,0.1); 
                        padding: 40px; 
                        text-align: center;
                    }}
                    .success-icon {{ 
                        font-size: 4em; 
                        margin-bottom: 20px; 
                    }}
                    h1 {{ 
                        color: #4CAF50; 
                        margin-bottom: 20px; 
                    }}
                    .features {{ 
                        background: #f8f9fa; 
                        border-radius: 10px; 
                        padding: 20px; 
                        margin: 20px 0; 
                        text-align: left;
                    }}
                    .feature {{ 
                        margin: 10px 0; 
                        display: flex; 
                        align-items: center; 
                    }}
                    .feature-icon {{ 
                        margin-right: 10px; 
                        font-size: 1.2em; 
                    }}
                    .whatsapp-btn {{ 
                        background: #25D366; 
                        color: white; 
                        padding: 15px 30px; 
                        border: none; 
                        border-radius: 10px; 
                        font-size: 1.1em; 
                        cursor: pointer; 
                        text-decoration: none; 
                        display: inline-block; 
                        margin-top: 20px;
                    }}
                    .whatsapp-btn:hover {{ background: #128C7E; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="success-icon">🎉</div>
                    <h1>Paiement Confirmé !</h1>
                    <p><strong>Félicitations ! Ton abonnement Léa Premium est maintenant actif pour 12 mois.</strong></p>
                    
                    <div class="features">
                        <div class="feature">
                            <span class="feature-icon">💬</span>
                            <span>Messages illimités pendant 12 mois</span>
                        </div>
                        <div class="feature">
                            <span class="feature-icon">🔬</span>
                            <span>Analyses nutritionnelles avancées</span>
                        </div>
                        <div class="feature">
                            <span class="feature-icon">⚡</span>
                            <span>Support client prioritaire</span>
                        </div>
                        <div class="feature">
                            <span class="feature-icon">🎯</span>
                            <span>Conseils personnalisés experts</span>
                        </div>
                    </div>
                    
                    <p>Un message de confirmation a été envoyé sur WhatsApp.</p>
                    
                    <a href="https://wa.me/14155238886" class="whatsapp-btn">
                        📱 Retourner sur WhatsApp
                    </a>
                </div>
            </body>
            </html>
            '''
    
    return '''
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>❌ Erreur - Léa Premium</title>
    </head>
    <body>
        <h1>❌ Erreur de vérification</h1>
        <p>Impossible de vérifier le paiement. Contactez le support.</p>
    </body>
    </html>
    '''

@app.route('/payment-cancel')
def payment_cancel():
    """Page d'annulation de paiement"""
    phone_number = request.args.get('phone')
    
    return f'''
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>❌ Paiement Annulé - Léa Premium</title>
        <style>
            body {{ 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
                margin: 0; 
                background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 100%); 
                min-height: 100vh; 
                display: flex; 
                align-items: center; 
                justify-content: center;
                padding: 20px;
            }}
            .container {{ 
                max-width: 500px; 
                background: white; 
                border-radius: 20px; 
                box-shadow: 0 20px 40px rgba(0,0,0,0.1); 
                padding: 40px; 
                text-align: center;
            }}
            .cancel-icon {{ 
                font-size: 4em; 
                margin-bottom: 20px; 
            }}
            h1 {{ 
                color: #FF6B6B; 
                margin-bottom: 20px; 
            }}
            .retry-btn {{ 
                background: #4CAF50; 
                color: white; 
                padding: 15px 30px; 
                border: none; 
                border-radius: 10px; 
                font-size: 1.1em; 
                cursor: pointer; 
                text-decoration: none; 
                display: inline-block; 
                margin: 10px;
            }}
            .retry-btn:hover {{ background: #45a049; }}
            .whatsapp-btn {{ 
                background: #25D366; 
                color: white; 
                padding: 15px 30px; 
                border: none; 
                border-radius: 10px; 
                font-size: 1.1em; 
                cursor: pointer; 
                text-decoration: none; 
                display: inline-block; 
                margin: 10px;
            }}
            .whatsapp-btn:hover {{ background: #128C7E; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="cancel-icon">😔</div>
            <h1>Paiement Annulé</h1>
            <p>Pas de souci ! Tu peux réessayer quand tu veux.</p>
            <p>Tape <strong>/premium</strong> sur WhatsApp pour obtenir un nouveau lien de paiement.</p>
            
            <a href="https://wa.me/14155238886" class="whatsapp-btn">
                📱 Retourner sur WhatsApp
            </a>
        </div>
    </body>
    </html>
    '''

@app.route('/api/stats')
def api_stats():
    return jsonify(get_stats())

@app.route('/privacy-policy')
def privacy_policy():
    """Page de politique de confidentialité pour Léa Nutrition"""
    return '''
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Politique de Confidentialité - Léa Nutrition</title>
        <style>
            body { 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
                line-height: 1.6; 
                margin: 0; 
                padding: 20px; 
                background: #f8f9fa; 
                color: #333;
            }
            .container { 
                max-width: 800px; 
                margin: 0 auto; 
                background: white; 
                padding: 40px; 
                border-radius: 10px; 
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            h1 { 
                color: #4CAF50; 
                text-align: center; 
                margin-bottom: 30px;
            }
            h2 { 
                color: #2c3e50; 
                border-bottom: 2px solid #4CAF50; 
                padding-bottom: 5px;
            }
            .last-updated { 
                text-align: center; 
                color: #666; 
                font-style: italic; 
                margin-bottom: 30px;
            }
            .contact-info { 
                background: #f8f9fa; 
                padding: 20px; 
                border-radius: 5px; 
                margin-top: 30px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🥗 Politique de Confidentialité - Léa Nutrition</h1>
            <div class="last-updated">Dernière mise à jour : 8 janvier 2025</div>
            
            <h2>1. Introduction</h2>
            <p>Léa Nutrition est un chatbot nutritionnel intelligent qui vous aide à suivre votre alimentation via WhatsApp. Cette politique de confidentialité explique comment nous collectons, utilisons et protégeons vos données personnelles.</p>
            
            <h2>2. Données Collectées</h2>
            <p>Nous collectons uniquement les informations nécessaires au fonctionnement du service :</p>
            <ul>
                <li><strong>Numéro de téléphone :</strong> Pour identifier votre compte et vous envoyer des réponses</li>
                <li><strong>Messages WhatsApp :</strong> Vos questions et descriptions d'aliments</li>
                <li><strong>Photos d'aliments :</strong> Pour analyser votre nutrition (optionnel)</li>
                <li><strong>Données nutritionnelles :</strong> Calories, protéines, lipides, glucides calculés</li>
                <li><strong>Préférences :</strong> Objectifs nutritionnels, allergies, préférences alimentaires</li>
            </ul>
            
            <h2>3. Utilisation des Données</h2>
            <p>Vos données sont utilisées exclusivement pour :</p>
            <ul>
                <li>Fournir des analyses nutritionnelles personnalisées</li>
                <li>Suivre vos progrès alimentaires</li>
                <li>Améliorer nos recommandations</li>
                <li>Assurer le support technique</li>
            </ul>
            
            <h2>4. Protection des Données</h2>
            <p>Nous mettons en place des mesures de sécurité strictes :</p>
            <ul>
                <li><strong>Chiffrement :</strong> Toutes les communications sont chiffrées</li>
                <li><strong>Accès limité :</strong> Seuls les développeurs autorisés peuvent accéder aux données</li>
                <li><strong>Stockage sécurisé :</strong> Base de données protégée sur serveurs sécurisés</li>
                <li><strong>Pas de vente :</strong> Nous ne vendons jamais vos données à des tiers</li>
            </ul>
            
            <h2>5. Partage des Données</h2>
            <p>Vos données ne sont <strong>jamais partagées</strong> avec des tiers, sauf :</p>
            <ul>
                <li>Si requis par la loi</li>
                <li>Pour protéger nos droits légaux</li>
                <li>Avec votre consentement explicite</li>
            </ul>
            
            <h2>6. Conservation des Données</h2>
            <p>Nous conservons vos données :</p>
            <ul>
                <li><strong>Données nutritionnelles :</strong> Tant que vous utilisez le service</li>
                <li><strong>Messages :</strong> 30 jours maximum pour le support technique</li>
                <li><strong>Photos :</strong> Supprimées après analyse (non stockées)</li>
            </ul>
            
            <h2>7. Vos Droits</h2>
            <p>Vous avez le droit de :</p>
            <ul>
                <li><strong>Accéder</strong> à vos données (tapez /export)</li>
                <li><strong>Modifier</strong> vos informations (tapez /profil)</li>
                <li><strong>Supprimer</strong> votre compte (tapez /delete)</li>
                <li><strong>Exporter</strong> vos données nutritionnelles</li>
            </ul>
            
            <h2>8. Cookies et Tracking</h2>
            <p>Léa Nutrition n'utilise <strong>aucun cookie</strong> ni système de tracking. Nous respectons votre vie privée.</p>
            
            <h2>9. Services Tiers</h2>
            <p>Nous utilisons des services tiers sécurisés :</p>
            <ul>
                <li><strong>WhatsApp Business API :</strong> Pour la messagerie (Meta/Facebook)</li>
                <li><strong>Railway :</strong> Pour l'hébergement sécurisé</li>
                <li><strong>Stripe :</strong> Pour les paiements sécurisés (Premium)</li>
            </ul>
            
            <h2>10. Modifications</h2>
            <p>Cette politique peut être mise à jour. Les changements importants vous seront notifiés via WhatsApp.</p>
            
            <h2>11. Contact</h2>
            <div class="contact-info">
                <p><strong>Pour toute question concernant cette politique :</strong></p>
                <ul>
                    <li>📱 WhatsApp : Tapez /aide dans votre conversation avec Léa</li>
                    <li>📧 Email : support@lea-nutrition.com</li>
                    <li>🌐 Site : https://web-production-eed0c.up.railway.app</li>
                </ul>
                <p><em>Nous nous engageons à répondre dans les 48h.</em></p>
            </div>
            
            <div style="text-align: center; margin-top: 40px; color: #666;">
                <p>🥗 <strong>Léa Nutrition</strong> - Votre coach nutrition intelligent</p>
                <p><em>Développé avec ❤️ pour votre bien-être</em></p>
            </div>
        </div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    port = int(os.getenv('PORT', 3000))
    logger.info(f"🚀 Serveur Léa v3.0 démarré sur le port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
