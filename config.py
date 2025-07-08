import os
from dotenv import load_dotenv

load_dotenv()

def get_environment_info():
    """Détecte l'environnement et retourne les informations appropriées"""
    
    # Récupérer l'URL Railway dès le début
    railway_url = os.getenv('RAILWAY_PUBLIC_DOMAIN', '')
    
    # 1. Vérifier la variable d'environnement explicite
    env_var = os.getenv('ENVIRONMENT', '').lower()
    if env_var in ['production', 'staging', 'development']:
        detected_environment = env_var
        detection_method = f"Variable ENVIRONMENT={env_var}"
    else:
        # 2. Détecter via l'URL Railway
        if railway_url:
            if 'web-production-eed0c' in railway_url:
                detected_environment = 'production'
                detection_method = f"URL Railway: {railway_url}"
            elif 'web-production-1da16' in railway_url:
                detected_environment = 'staging'
                detection_method = f"URL Railway: {railway_url}"
            else:
                detected_environment = 'production'  # Par défaut pour Railway
                detection_method = f"URL Railway inconnue: {railway_url}"
        else:
            # 3. Environnement local
            detected_environment = 'development'
            detection_method = "Pas de Railway détecté (local)"
    
    # Configuration par environnement
    if detected_environment == 'production':
        return {
            'environment': 'production',
            'database': 'lea_nutrition.db',
            'log_level': 'INFO',
            'activation_code': 'live-cold',
            'detection_method': detection_method,
            'railway_url': railway_url,
            'detected_environment': detected_environment
        }
    elif detected_environment == 'staging':
        return {
            'environment': 'staging',
            'database': 'lea_nutrition_staging.db',
            'log_level': 'DEBUG',
            'activation_code': 'test-staging',
            'detection_method': detection_method,
            'railway_url': railway_url,
            'detected_environment': detected_environment
        }
    else:  # development
        return {
            'environment': 'development',
            'database': 'lea_nutrition_dev.db',
            'log_level': 'DEBUG',
            'activation_code': 'dev-local',
            'detection_method': detection_method,
            'railway_url': railway_url,
            'detected_environment': detected_environment
        }

def get_detection_info():
    """Retourne les informations de détection d'environnement"""
    env_info = get_environment_info()
    return {
        'detection_method': env_info['detection_method'],
        'railway_url': env_info['railway_url'],
        'detected_environment': env_info['detected_environment']
    }

def get_environment_display():
    """Retourne les informations d'affichage pour l'environnement"""
    env_info = get_environment_info()
    
    if env_info['environment'] == 'production':
        return {
            'name': 'PRODUCTION',
            'color': '#4CAF50',
            'icon': '🚀',
            'description': 'Environnement de production'
        }
    elif env_info['environment'] == 'staging':
        return {
            'name': 'STAGING',
            'color': '#FF9800',
            'icon': '🧪',
            'description': 'Environnement de test'
        }
    else:
        return {
            'name': 'DEVELOPMENT',
            'color': '#2196F3',
            'icon': '💻',
            'description': 'Environnement de développement'
        }

# Configuration par environnement
class BaseConfig:
    """Configuration de base"""
    # Twilio (legacy - à garder pour transition)
    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
    TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER', 'whatsapp:+14155238886')
    
    # WhatsApp Business API (Meta)
    WHATSAPP_ACCESS_TOKEN = os.getenv('WHATSAPP_ACCESS_TOKEN')
    WHATSAPP_PHONE_NUMBER_ID = os.getenv('WHATSAPP_PHONE_NUMBER_ID')
    WHATSAPP_BUSINESS_ACCOUNT_ID = os.getenv('WHATSAPP_BUSINESS_ACCOUNT_ID')
    WHATSAPP_APP_ID = os.getenv('WHATSAPP_APP_ID')
    WHATSAPP_WEBHOOK_TOKEN = os.getenv('WHATSAPP_WEBHOOK_TOKEN', 'lea-nutrition-webhook-2025')
    USE_WHATSAPP_BUSINESS_API = os.getenv('USE_WHATSAPP_BUSINESS_API', 'false').lower() == 'true'
    
    # OpenAI
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # Rate limiting
    RATE_LIMIT_WINDOW = 60  # 1 minute
    RATE_LIMIT_MAX_REQUESTS = 10  # Max 10 messages par minute
    
    # Port
    PORT = int(os.getenv('PORT', 3000))

class ProductionConfig(BaseConfig):
    """Configuration production"""
    DATABASE_NAME = 'lea_nutrition.db'
    DEBUG = False
    LOG_LEVEL = 'INFO'

class StagingConfig(BaseConfig):
    """Configuration staging"""
    DATABASE_NAME = 'lea_nutrition_staging.db'
    DEBUG = True
    LOG_LEVEL = 'DEBUG'

class DevelopmentConfig(BaseConfig):
    """Configuration développement"""
    DATABASE_NAME = 'lea_nutrition_dev.db'
    DEBUG = True
    LOG_LEVEL = 'DEBUG'

# Sélection de la configuration
env_info = get_environment_info()

if env_info['environment'] == 'production':
    current_config = ProductionConfig()
elif env_info['environment'] == 'staging':
    current_config = StagingConfig()
else:
    current_config = DevelopmentConfig()
