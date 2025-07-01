import stripe
import os
from datetime import datetime, timedelta
from database import set_user_premium
import logging

# Configuration Stripe
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

logger = logging.getLogger(__name__)

def create_payment_link(phone_number, user_name="Utilisateur"):
    """Crée un lien de paiement Stripe pour l'abonnement annuel"""
    try:
        # Prix pour 12 mois (à ajuster selon vos tarifs)
        price_amount = 6000  # 60 CHF en centimes
        
        # Créer une session de checkout Stripe
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'chf',
                    'product_data': {
                        'name': 'Léa Premium - Abonnement 12 mois',
                        'description': 'Accès illimité au coaching nutrition IA Léa pendant 12 mois',
                        'images': ['https://web-production-eed0c.up.railway.app/static/lea-premium.png'],
                    },
                    'unit_amount': price_amount,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=f'https://web-production-eed0c.up.railway.app/payment-success?session_id={{CHECKOUT_SESSION_ID}}&phone={phone_number}',
            cancel_url=f'https://web-production-eed0c.up.railway.app/payment-cancel?phone={phone_number}',
            metadata={
                'phone_number': phone_number,
                'user_name': user_name,
                'subscription_type': '12_months'
            },
            customer_email=None,  # L'utilisateur saisira son email
            billing_address_collection='required',
        )
        
        logger.info(f"💳 Lien de paiement créé pour {phone_number}: {checkout_session.url}")
        return checkout_session.url
        
    except Exception as e:
        logger.error(f"❌ Erreur création lien paiement: {e}")
        return None

def verify_payment(session_id):
    """Vérifie un paiement Stripe et active le premium"""
    try:
        # Récupérer la session de checkout
        session = stripe.checkout.Session.retrieve(session_id)
        
        if session.payment_status == 'paid':
            phone_number = session.metadata.get('phone_number')
            
            if phone_number:
                # Calculer la date d'expiration (12 mois)
                expires_at = datetime.now() + timedelta(days=365)
                expires_at_str = expires_at.isoformat()
                
                # Activer le premium
                set_user_premium(phone_number, session.customer, expires_at_str)
                
                logger.info(f"✅ Premium activé pour {phone_number} jusqu'au {expires_at_str}")
                return True, phone_number
        
        return False, None
        
    except Exception as e:
        logger.error(f"❌ Erreur vérification paiement: {e}")
        return False, None

def get_premium_message(phone_number, user_name=""):
    """Génère le message premium avec lien de paiement direct"""
    # Utiliser le nouveau lien Stripe direct fourni
    payment_link = "https://buy.stripe.com/00w4gAgwWePa1LccID3cc02"
    
    message = f"""🔒 *Limite atteinte !*

Salut {user_name} ! Tu as utilisé tes 30 messages gratuits. 

🌟 *Passe à Léa Performance pour :*
• Messages illimités pendant 12 mois
• Score de performance 0-100 pour chaque plat
• Classement pour booster ta motivation
• Réponses ultra-rapides sans publicité

💰 *Offre spéciale : 50 CHF pour 12 mois*
(soit seulement 4.17 CHF/mois !)

👆 *Clique ici pour débloquer :*
{payment_link}

Merci de faire confiance à Léa ! 💚"""

    return message

def format_premium_reminder():
    """Message de rappel pour les utilisateurs non-premium"""
    return """🔒 *Message premium requis*

Tu as atteint la limite de 30 messages gratuits.

🌟 Passe à Léa Premium pour continuer à profiter de tous mes conseils nutrition !

Tape */premium* pour obtenir ton lien de paiement."""

def get_premium_reminder_before_response(user_name=""):
    """Message premium optimisé qui apparaît avant chaque réponse de Léa après 30 messages"""
    payment_link = "https://buy.stripe.com/00w4gAgwWePa1LccID3cc02"
    
    message = f"""🏆 *{user_name}, passez à la vitesse supérieure !*

Vous avez utilisé vos 30 messages gratuits. Débloquez *Léa Performance* et maximisez vos résultats !

🎯 *Léa Performance - Conçu pour l'excellence :*
• 📊 Score de performance 0-100 pour chaque plat
• 🏅 Classement pour booster votre motivation
• ⚡ Réponses ultra-rapides sans publicité
• 🔥 Messages illimités pendant 12 mois

💎 *Seulement 50 CHF pour 12 mois*
(4.17 CHF/mois - moins qu'un café !)

👆 *DÉBLOQUEZ MAINTENANT :*
{payment_link}

🚀 Grimpez dans le classement et atteignez vos objectifs !

---"""

    return message
