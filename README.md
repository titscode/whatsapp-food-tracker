# 🤖 Léa - Chatbot WhatsApp Nutrition

Bot WhatsApp intelligent pour le tracking nutritionnel avec dashboard KPI intégré.

## ✨ Fonctionnalités

### 📱 Bot WhatsApp
- **Tracking nutritionnel** : Analyse des aliments et calcul des calories
- **Conversation IA** : Réponses contextuelles avec GPT-4o
- **Vision IA** : Analyse des photos de repas
- **Persistance** : Sauvegarde des données utilisateur

### 📊 Dashboard KPI
- **Métriques temps réel** : DAU, WAU, engagement
- **Graphiques interactifs** : Historique 14 jours
- **APIs JSON** : `/api/stats`, `/api/dau-history`
- **Interface responsive** : Design moderne

## 🚀 Installation

### Prérequis
- Python 3.8+
- Compte Twilio (WhatsApp Business API)
- Clé API OpenAI (GPT-4o)

### Configuration
1. Cloner le repository
2. Installer les dépendances : `pip install -r requirements.txt`
3. Configurer les variables d'environnement dans `.env`
4. Lancer l'application : `python app_production.py`

### Variables d'environnement
```env
OPENAI_API_KEY=your_openai_key
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
TWILIO_PHONE_NUMBER=your_whatsapp_number
```

## 📖 Utilisation

### Dashboard
- Accéder à `http://localhost:3000`
- Visualiser les métriques en temps réel
- Cliquer sur les cartes pour masquer/afficher

### WhatsApp
- Envoyer `join [code]` pour s'inscrire
- Envoyer des messages alimentaires : "50g de poulet"
- Poser des questions nutritionnelles

## 🛠️ Technologies

- **Backend** : Flask, SQLite
- **IA** : OpenAI GPT-4o + Vision
- **WhatsApp** : Twilio Business API
- **Frontend** : HTML/CSS/JS responsive

## 📊 APIs

- `GET /api/stats` : Statistiques générales
- `GET /api/dau-history` : Historique DAU 14 jours
- `POST /whatsapp` : Webhook WhatsApp

## 🔒 Sécurité

- Variables d'environnement pour les secrets
- .gitignore configuré
- Validation des entrées utilisateur

## 📝 License

MIT License - Voir LICENSE pour plus de détails.
