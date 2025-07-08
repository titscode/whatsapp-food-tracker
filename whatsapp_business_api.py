import requests
import json
import logging
from typing import Dict, Any, Optional
from config import current_config

logger = logging.getLogger(__name__)

class WhatsAppBusinessAPI:
    """Client pour WhatsApp Business API officielle (Meta)"""
    
    def __init__(self):
        self.access_token = current_config.WHATSAPP_ACCESS_TOKEN
        self.phone_number_id = current_config.WHATSAPP_PHONE_NUMBER_ID
        self.business_account_id = current_config.WHATSAPP_BUSINESS_ACCOUNT_ID
        self.base_url = f"https://graph.facebook.com/v18.0/{self.phone_number_id}"
        
        # Headers pour toutes les requêtes
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
    
    def send_text_message(self, to: str, message: str) -> bool:
        """
        Envoie un message texte via WhatsApp Business API
        
        Args:
            to: Numéro de téléphone destinataire (format: +41774184918)
            message: Contenu du message
            
        Returns:
            bool: True si envoyé avec succès, False sinon
        """
        try:
            # Nettoyer le numéro (enlever whatsapp: si présent)
            clean_to = to.replace("whatsapp:", "").strip()
            
            # Payload pour l'API Meta
            payload = {
                "messaging_product": "whatsapp",
                "to": clean_to,
                "type": "text",
                "text": {
                    "body": message
                }
            }
            
            # Envoyer la requête
            response = requests.post(
                f"{self.base_url}/messages",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                message_id = result.get("messages", [{}])[0].get("id")
                logger.info(f"✅ Message WhatsApp Business envoyé: {message_id}")
                return True
            else:
                logger.error(f"❌ Erreur envoi WhatsApp Business: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Exception envoi WhatsApp Business: {e}")
            return False
    
    def send_media_message(self, to: str, media_url: str, media_type: str = "image", caption: str = "") -> bool:
        """
        Envoie un message avec média via WhatsApp Business API
        
        Args:
            to: Numéro de téléphone destinataire
            media_url: URL du média
            media_type: Type de média (image, video, audio, document)
            caption: Légende optionnelle
            
        Returns:
            bool: True si envoyé avec succès, False sinon
        """
        try:
            clean_to = to.replace("whatsapp:", "").strip()
            
            # Payload pour média
            payload = {
                "messaging_product": "whatsapp",
                "to": clean_to,
                "type": media_type,
                media_type: {
                    "link": media_url
                }
            }
            
            # Ajouter caption si fourni
            if caption and media_type in ["image", "video", "document"]:
                payload[media_type]["caption"] = caption
            
            response = requests.post(
                f"{self.base_url}/messages",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                message_id = result.get("messages", [{}])[0].get("id")
                logger.info(f"✅ Message média WhatsApp Business envoyé: {message_id}")
                return True
            else:
                logger.error(f"❌ Erreur envoi média WhatsApp Business: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Exception envoi média WhatsApp Business: {e}")
            return False
    
    def mark_message_as_read(self, message_id: str) -> bool:
        """
        Marque un message comme lu
        
        Args:
            message_id: ID du message à marquer comme lu
            
        Returns:
            bool: True si marqué avec succès, False sinon
        """
        try:
            payload = {
                "messaging_product": "whatsapp",
                "status": "read",
                "message_id": message_id
            }
            
            response = requests.post(
                f"{self.base_url}/messages",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            return response.status_code == 200
            
        except Exception as e:
            logger.error(f"❌ Erreur marquage lu: {e}")
            return False

def parse_whatsapp_business_webhook(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Parse le payload webhook de WhatsApp Business API
    
    Args:
        payload: Payload JSON du webhook Meta
        
    Returns:
        Dict avec les informations du message ou None si pas un message
    """
    try:
        # Structure du webhook Meta WhatsApp Business
        entry = payload.get("entry", [])
        if not entry:
            return None
        
        changes = entry[0].get("changes", [])
        if not changes:
            return None
        
        value = changes[0].get("value", {})
        messages = value.get("messages", [])
        
        if not messages:
            return None
        
        message = messages[0]
        contacts = value.get("contacts", [{}])
        contact = contacts[0] if contacts else {}
        
        # Extraire les informations du message
        message_data = {
            "message_id": message.get("id"),
            "from_number": message.get("from"),
            "timestamp": message.get("timestamp"),
            "type": message.get("type"),
            "profile_name": contact.get("profile", {}).get("name", ""),
        }
        
        # Contenu selon le type de message
        if message["type"] == "text":
            message_data["text"] = message.get("text", {}).get("body", "")
        
        elif message["type"] == "image":
            image = message.get("image", {})
            message_data["media_id"] = image.get("id")
            message_data["media_url"] = image.get("link")
            message_data["caption"] = image.get("caption", "")
            message_data["mime_type"] = image.get("mime_type")
        
        elif message["type"] == "audio":
            audio = message.get("audio", {})
            message_data["media_id"] = audio.get("id")
            message_data["media_url"] = audio.get("link")
            message_data["mime_type"] = audio.get("mime_type")
        
        elif message["type"] == "video":
            video = message.get("video", {})
            message_data["media_id"] = video.get("id")
            message_data["media_url"] = video.get("link")
            message_data["caption"] = video.get("caption", "")
            message_data["mime_type"] = video.get("mime_type")
        
        elif message["type"] == "document":
            document = message.get("document", {})
            message_data["media_id"] = document.get("id")
            message_data["media_url"] = document.get("link")
            message_data["filename"] = document.get("filename")
            message_data["mime_type"] = document.get("mime_type")
        
        return message_data
        
    except Exception as e:
        logger.error(f"❌ Erreur parsing webhook WhatsApp Business: {e}")
        return None

def verify_webhook_signature(payload: str, signature: str, app_secret: str) -> bool:
    """
    Vérifie la signature du webhook Meta (optionnel mais recommandé)
    
    Args:
        payload: Payload brut du webhook
        signature: Signature X-Hub-Signature-256
        app_secret: Secret de l'application Facebook
        
    Returns:
        bool: True si signature valide, False sinon
    """
    try:
        import hmac
        import hashlib
        
        # Calculer la signature attendue
        expected_signature = hmac.new(
            app_secret.encode('utf-8'),
            payload.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        # Comparer avec la signature reçue (enlever 'sha256=' du début)
        received_signature = signature.replace('sha256=', '') if signature.startswith('sha256=') else signature
        
        return hmac.compare_digest(expected_signature, received_signature)
        
    except Exception as e:
        logger.error(f"❌ Erreur vérification signature: {e}")
        return False

# Fonction utilitaire pour compatibilité avec le code existant
def send_whatsapp_business_reply(to: str, message: str) -> bool:
    """
    Fonction utilitaire pour remplacer send_whatsapp_reply de Twilio
    
    Args:
        to: Numéro destinataire
        message: Message à envoyer
        
    Returns:
        bool: True si envoyé avec succès
    """
    try:
        api = WhatsAppBusinessAPI()
        return api.send_text_message(to, message)
    except Exception as e:
        logger.error(f"❌ Erreur envoi WhatsApp Business reply: {e}")
        return False

# Instance globale pour utilisation dans l'app
whatsapp_business_client = WhatsAppBusinessAPI()
