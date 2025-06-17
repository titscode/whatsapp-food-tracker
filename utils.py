import requests
import tempfile
import os
from datetime import date, datetime

def transcribe_audio(audio_url, account_sid, auth_token, api_key):
    """Transcrit un message audio avec Whisper"""
    try:
        # Télécharger l'audio
        response = requests.get(audio_url, auth=(account_sid, auth_token))
        if response.status_code != 200:
            return None
        
        # Sauvegarder temporairement
        with tempfile.NamedTemporaryFile(suffix='.ogg', delete=False) as tmp_file:
            tmp_file.write(response.content)
            tmp_path = tmp_file.name
        
        # Transcrire
        headers = {"Authorization": f"Bearer {api_key}"}
        
        with open(tmp_path, 'rb') as audio_file:
            files = {
                'file': ('audio.ogg', audio_file, 'audio/ogg'),
                'model': (None, 'whisper-1'),
                'language': (None, 'fr')
            }
            
            response = requests.post(
                "https://api.openai.com/v1/audio/transcriptions",
                headers=headers, files=files
            )
        
        os.unlink(tmp_path)
        
        if response.status_code == 200:
            return response.json().get('text', '')
            
        return None
        
    except Exception as e:
        print(f"❌ Erreur transcription: {e}")
        return None

def send_whatsapp_reply(to, message, twilio_client, twilio_phone_number):
    """Envoie un message WhatsApp avec gestion d'encodage"""
    try:
        # Nettoyer le message des caractères problématiques
        clean_message = message.encode('utf-8', errors='ignore').decode('utf-8')
        
        msg = twilio_client.messages.create(
            body=clean_message,
            from_=twilio_phone_number,
            to=to
        )
        print(f"✅ Message envoyé: {msg.sid}")
    except Exception as e:
        print(f"❌ Erreur envoi: {e}")
        # Fallback sans emojis en cas d'échec
        try:
            fallback_message = ''.join(char for char in message if ord(char) < 128)
            msg = twilio_client.messages.create(
                body=fallback_message,
                from_=twilio_phone_number,
                to=to
            )
            print(f"✅ Message fallback envoyé: {msg.sid}")
        except Exception as e2:
            print(f"❌ Erreur fallback: {e2}")

def get_help_message():
    """Message d'aide"""
    return """🤖 *Léa - Bot WhatsApp Nutrition*

Je suis Léa, je suis là pour t'aider à tracker plus facilement tes calories et atteindre tes objectifs 💪

📱 *Comment m'utiliser:*
• Envoyez une photo de votre repas 📷
• Écrivez le nom d'un aliment (ex: pomme)
• Spécifiez les quantités (ex: 50g de riz)
• 🎤 Envoyez un message vocal (ex: "j'ai mangé un burger")
• 💬 Posez-moi des questions nutrition !

🔥 Je calcule automatiquement vos calories et macronutriments quotidiens!

💬 *Exemples de questions:*
• "Que manger avant mon entraînement ?"
• "Comment augmenter mes protéines ?"
• "J'ai faim à 16h, que me conseilles-tu ?"

⚡ *Commandes disponibles:*
/aide - Afficher cette aide
/reset - Remettre les données à zéro

💡 Données automatiquement remises à zéro chaque jour à minuit."""

def chat_with_lea(question, user, api_key):
    """Chat avec Léa"""
    try:
        context = f"Utilisateur nutrition"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "system",
                    "content": f"Tu es Léa, coach nutrition friendly. Réponds en 2-3 phrases max, tutoie, sois positive et utilise des emojis."
                },
                {"role": "user", "content": question}
            ],
            "max_tokens": 150,
            "temperature": 0.7
        }
        
        response = requests.post("https://api.openai.com/v1/chat/completions", 
                               headers=headers, json=payload)
        
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        
        return "Je n'ai pas compris, reformule ta question 😅"
        
    except:
        return "Oups, petit souci ! Réessaie 😅"
