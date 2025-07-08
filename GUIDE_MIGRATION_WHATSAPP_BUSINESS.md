# 🚀 Guide de Migration vers WhatsApp Business API

## 📋 Vue d'ensemble

Ce guide détaille la migration complète du chatbot Léa de **Twilio WhatsApp Sandbox** vers **WhatsApp Business API officielle (Meta)** pour obtenir un profil brandé "Léa Nutrition".

## ✅ État Actuel

### Configuration Meta Terminée
- ✅ Application Facebook Developer "Léa Nutrition" créée
- ✅ WhatsApp Business API configuré
- ✅ Profil "Léa Nutrition" avec avatar configuré
- ✅ Numéro +41774184918 vérifié
- ✅ Tous les tokens et IDs récupérés

### Code Développé
- ✅ Module `whatsapp_business_api.py` créé
- ✅ Webhook `/whatsapp-business` implémenté
- ✅ Fonction hybride dans `utils.py`
- ✅ Variables d'environnement ajoutées
- ✅ Script de test créé

## 🔑 Variables d'Environnement

### À Ajouter dans Railway

```bash
# WhatsApp Business API (Meta)
WHATSAPP_ACCESS_TOKEN=EAAPLbERy7sUBPMaq9wF4ONMsDC5y61LWV6OlZCwcbECBncWInSRSyGqToLMwd3mxsEaG6jwuJG0HDkDm7ziHWVc0ooSwX4Gp1mAh6fozjlnp3yPk0S5iBNA3SVN1PGHy8Kfh4ucevSX8l5PJqh5adiJ5PpXaeKwHfyRh5alwgxZCjSHora5qlLAteNapKoRg54frP5KmJo95QfZC0HwEsXswarpB35XHzE1SwF4zN6PdCi8b5VqLE71fraE5AZDZD

WHATSAPP_PHONE_NUMBER_ID=691685597362883
WHATSAPP_BUSINESS_ACCOUNT_ID=1020112836587577
WHATSAPP_APP_ID=1068090795421381
WHATSAPP_WEBHOOK_TOKEN=lea-nutrition-webhook-2025

# Activation (à faire après tests)
USE_WHATSAPP_BUSINESS_API=false
```

### Variables Twilio à Conserver
```bash
# Garder pour transition progressive
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your-twilio-auth-token-here
TWILIO_PHONE_NUMBER=whatsapp:+14155238886
```

## 🚀 Étapes de Déploiement

### 1. Déploiement du Code

```bash
# 1. Commit et push du nouveau code
git add .
git commit -m "feat: Add WhatsApp Business API support with hybrid system"
git push origin main

# 2. Railway déploiera automatiquement
```

### 2. Configuration des Variables Railway

1. Aller sur [Railway Dashboard](https://railway.app/dashboard)
2. Sélectionner le projet Léa
3. Onglet "Variables"
4. Ajouter toutes les variables WhatsApp Business API
5. **NE PAS ENCORE** activer `USE_WHATSAPP_BUSINESS_API=true`

### 3. Configuration Webhook Meta

1. Aller sur [Facebook Developers](https://developers.facebook.com/)
2. Sélectionner l'app "Léa Nutrition"
3. WhatsApp > Configuration
4. Webhook URL : `https://web-production-eed0c.up.railway.app/whatsapp-business`
5. Token de vérification : `lea-nutrition-webhook-2025`
6. Sauvegarder et vérifier

### 4. Tests de Validation

```bash
# Exécuter le script de test
python test_whatsapp_business.py

# Vérifier que tous les tests passent
```

### 5. Activation Progressive

#### Phase 1 : Test en Parallèle
```bash
# Dans Railway, activer temporairement
USE_WHATSAPP_BUSINESS_API=true
```

#### Phase 2 : Test avec Numéro Réel
1. Envoyer un message test au numéro +41774184918
2. Vérifier que le profil "Léa Nutrition" s'affiche
3. Tester l'envoi/réception de messages

#### Phase 3 : Migration Complète
Si tout fonctionne, garder `USE_WHATSAPP_BUSINESS_API=true`

## 🔧 Architecture Technique

### Système Hybride
Le code supporte maintenant les deux APIs en parallèle :

```python
# Fonction hybride dans utils.py
def send_whatsapp_reply(to, message, twilio_client=None, twilio_phone_number=None):
    if USE_WHATSAPP_BUSINESS_API:
        # Essayer WhatsApp Business API
        success = send_whatsapp_business_reply(to, message)
        if success:
            return
        # Fallback vers Twilio si échec
    
    # Utiliser Twilio
    twilio_client.messages.create(...)
```

### Webhooks Parallèles
- `/whatsapp` : Webhook Twilio (existant)
- `/whatsapp-business` : Webhook Meta (nouveau)

### Parsing des Messages
- **Twilio** : `request.form.get('Body')`
- **Meta** : `parse_whatsapp_business_webhook(payload)`

## 📱 Différences Utilisateur

### Avant (Twilio)
- Profil affiché : "Twilio"
- Numéro : +1 415 523 8886
- Pas d'avatar personnalisé

### Après (WhatsApp Business API)
- Profil affiché : "Léa Nutrition" ✨
- Numéro : +41 77 418 49 18
- Avatar Léa personnalisé
- Profil business vérifié

## 🚨 Points d'Attention

### Limitations API Meta
- **1000 messages/jour** en mode développement
- **Validation Meta** requise pour production illimitée
- **Numéro suisse** : vérifier compatibilité continue

### Monitoring
- Surveiller les logs Railway pour erreurs
- Vérifier les métriques d'envoi/réception
- Tester régulièrement le profil brandé

### Rollback Plan
Si problème majeur :
1. `USE_WHATSAPP_BUSINESS_API=false`
2. Retour automatique vers Twilio
3. Pas d'interruption de service

## 🧪 Tests de Validation

### Tests Automatiques
```bash
python test_whatsapp_business.py
```

### Tests Manuels
1. **Profil** : Vérifier "Léa Nutrition" s'affiche
2. **Envoi** : Message depuis l'app vers utilisateur
3. **Réception** : Message utilisateur vers l'app
4. **Fonctionnalités** : Tracking nutrition, conversation, premium

### Tests de Charge
- Envoyer plusieurs messages rapidement
- Vérifier la limite de 1000/jour
- Tester la gestion d'erreurs

## 📊 Métriques de Succès

### Techniques
- ✅ 0 erreur webhook Meta
- ✅ Temps de réponse < 2s
- ✅ 100% messages délivrés

### Business
- ✅ Profil "Léa Nutrition" visible
- ✅ Expérience utilisateur identique
- ✅ Pas de perte d'utilisateurs

## 🎯 Résultat Final

Une fois la migration terminée :

### Pour les Utilisateurs
- Profil professionnel "Léa Nutrition"
- Numéro suisse local (+41)
- Même expérience conversationnelle
- Toutes les fonctionnalités préservées

### Pour le Développement
- API officielle Meta (plus stable)
- Profil brandé professionnel
- Système hybride robuste
- Possibilité d'extensions futures (templates, boutons, etc.)

## 🚀 Commandes de Déploiement

```bash
# 1. Tests locaux
python test_whatsapp_business.py

# 2. Déploiement
git add .
git commit -m "feat: WhatsApp Business API migration ready"
git push origin main

# 3. Configuration Railway
# - Ajouter variables d'environnement
# - Configurer webhook Meta
# - Activer USE_WHATSAPP_BUSINESS_API=true

# 4. Validation
# - Tester profil "Léa Nutrition"
# - Vérifier fonctionnalités
# - Monitorer logs
```

---

**🎉 Migration WhatsApp Business API - Léa Nutrition**
*De Twilio vers un profil brandé professionnel*
