# 🚀 Guide de Déploiement Complet - Léa Bot WhatsApp

## 📋 ÉTAPE 1 - Vérification Pré-Déploiement

### 🔍 Script de Vérification Automatique
```bash
python deploy_check.py
```

### ✅ Checklist Manuelle
- [ ] Fichier `app_production.py` optimisé (logging, rate limiting)
- [ ] Variables d'environnement documentées (`.env.example`)
- [ ] Configuration Railway complète (`Procfile`, `railway.json`, `nixpacks.toml`)
- [ ] Dépendances à jour (`requirements.txt`)
- [ ] Base de données initialisée
- [ ] Tests locaux réussis

---

## 🚂 ÉTAPE 2 - Déploiement Railway

### 2.1 Connexion GitHub → Railway

1. **Aller sur Railway**
   - URL: https://railway.app
   - Se connecter avec GitHub

2. **Créer un Nouveau Projet**
   - Cliquer "New Project"
   - Sélectionner "Deploy from GitHub repo"
   - Choisir le repository du chatbot
   - Sélectionner la branche `main` ou `production`

### 2.2 Configuration Variables d'Environnement

Dans le dashboard Railway, onglet **"Variables"** :

```env
OPENAI_API_KEY=sk-your-real-openai-key
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your-real-twilio-token
TWILIO_PHONE_NUMBER=whatsapp:+14155238886
```

⚠️ **IMPORTANT** : Utiliser les vraies clés API, pas les exemples !

### 2.3 Déploiement Automatique

Railway détecte automatiquement :
- ✅ `Procfile` → Commande de démarrage
- ✅ `requirements.txt` → Dépendances Python
- ✅ `railway.json` → Configuration déploiement
- ✅ `runtime.txt` → Version Python 3.11
- ✅ `nixpacks.toml` → Build configuration

**Temps de déploiement** : 2-3 minutes

### 2.4 Récupérer l'URL de Production

1. Dans Railway, aller dans **"Settings"**
2. Section **"Domains"** → Cliquer **"Generate Domain"**
3. Noter l'URL : `https://your-app-name.railway.app`

---

## 📱 ÉTAPE 3 - Configuration Twilio

### 3.1 Mise à Jour Webhook WhatsApp

1. **Console Twilio**
   - URL: https://console.twilio.com
   - Aller dans **Messaging** → **Settings** → **WhatsApp sandbox settings**

2. **Configurer Webhook**
   ```
   Webhook URL: https://your-app-name.railway.app/whatsapp
   HTTP Method: POST
   ```

3. **Sauvegarder** la configuration

### 3.2 Test de Connexion

Envoyer au **+1 415 523 8886** :
```
join live-cold
```

---

## 🧪 ÉTAPE 4 - Tests Post-Déploiement

### 4.1 Tests Automatiques

#### ✅ Test 1 : Dashboard Accessible
```bash
curl https://your-app-name.railway.app/
# Doit retourner le HTML du dashboard
```

#### ✅ Test 2 : API Stats
```bash
curl https://your-app-name.railway.app/api/stats
# Doit retourner JSON avec DAU, WAU, etc.
```

#### ✅ Test 3 : Webhook Actif
```bash
curl https://your-app-name.railway.app/whatsapp
# Doit retourner "Webhook WhatsApp actif!"
```

### 4.2 Tests Fonctionnels WhatsApp

#### ✅ Test 4 : Activation Bot
1. Envoyer `join live-cold` au +1 415 523 8886
2. ✅ Doit recevoir message de confirmation

#### ✅ Test 5 : Tracking Aliment
1. Envoyer `50g de poulet`
2. ✅ Doit recevoir analyse nutritionnelle complète

#### ✅ Test 6 : Conversation IA
1. Envoyer `Salut Léa !`
2. ✅ Doit recevoir réponse conversationnelle

#### ✅ Test 7 : Question Nutrition
1. Envoyer `Que manger avant le sport ?`
2. ✅ Doit recevoir conseil nutrition expert

#### ✅ Test 8 : Analyse Image
1. Envoyer photo de repas
2. ✅ Doit analyser et retourner valeurs nutritionnelles

#### ✅ Test 9 : Commandes
1. Envoyer `/aide`
2. ✅ Doit afficher menu d'aide complet

#### ✅ Test 10 : Rate Limiting
1. Envoyer 15 messages rapidement
2. ✅ Doit bloquer après 10 messages avec message d'avertissement

### 4.3 Tests de Performance

#### ✅ Test 11 : Temps de Réponse
- Tracking aliment : < 5 secondes
- Conversation IA : < 3 secondes
- Dashboard : < 2 secondes

#### ✅ Test 12 : Gestion d'Erreurs
1. Envoyer message invalide
2. ✅ Doit retourner message d'erreur utilisateur-friendly

---

## 📊 ÉTAPE 5 - Monitoring Production

### 5.1 Logs Railway

**Accès aux logs** :
1. Dashboard Railway → Onglet **"Deployments"**
2. Cliquer sur le déploiement actuel
3. Voir logs en temps réel

**Logs à surveiller** :
```
✅ Client Twilio initialisé avec succès
✅ Base de données initialisée
📱 Message reçu de whatsapp:+...
🚫 Rate limit dépassé pour whatsapp:+...
```

### 5.2 Métriques Business

**Dashboard KPI** : `https://your-app-name.railway.app/`

Surveiller :
- **DAU** (Daily Active Users)
- **WAU** (Weekly Active Users)
- **Messages traités/jour**
- **Taux d'engagement**

### 5.3 Alertes à Configurer

**Erreurs critiques** :
- Échec connexion OpenAI
- Échec connexion Twilio
- Erreurs base de données
- Dépassement rate limit massif

---

## 🔧 ÉTAPE 6 - Maintenance

### 6.1 Mises à Jour

**Déploiement automatique** :
```bash
git add .
git commit -m "feat: nouvelle fonctionnalité"
git push origin main
# → Railway redéploie automatiquement
```

### 6.2 Rollback

En cas de problème :
1. Dashboard Railway → **"Deployments"**
2. Sélectionner déploiement précédent
3. Cliquer **"Redeploy"**

### 6.3 Scaling

**Augmenter ressources** :
- Railway → **"Settings"** → **"Resources"**
- Ajuster CPU/RAM selon usage

---

## 🚨 DÉPANNAGE

### Problème : Build Failed
**Solution** :
1. Vérifier `requirements.txt`
2. Vérifier `runtime.txt` (Python 3.11.0)
3. Logs Railway pour détails

### Problème : App Crash au Démarrage
**Solution** :
1. Vérifier variables d'environnement
2. Vérifier logs Railway
3. Tester localement avec `python app_production.py`

### Problème : Webhook Twilio Error
**Solution** :
1. Vérifier URL webhook dans Twilio
2. Tester endpoint : `curl https://your-app.railway.app/whatsapp`
3. Vérifier logs Railway pour erreurs

### Problème : Bot Ne Répond Pas
**Solution** :
1. Vérifier clés API OpenAI/Twilio
2. Tester `join live-cold` d'abord
3. Vérifier logs pour erreurs spécifiques

---

## ✅ CHECKLIST FINALE

### Pré-Déploiement
- [ ] Script `deploy_check.py` réussi
- [ ] Variables d'environnement configurées
- [ ] Tests locaux OK

### Déploiement
- [ ] Projet Railway créé et connecté
- [ ] Variables d'environnement Railway configurées
- [ ] Build Railway réussi (vert)
- [ ] URL production générée

### Configuration
- [ ] Webhook Twilio mis à jour
- [ ] Test `join live-cold` réussi
- [ ] Dashboard accessible

### Tests Production
- [ ] 10 tests fonctionnels WhatsApp réussis
- [ ] Tests API réussis
- [ ] Performance acceptable
- [ ] Logs propres

### Monitoring
- [ ] Accès logs Railway configuré
- [ ] Dashboard KPI fonctionnel
- [ ] Alertes configurées (optionnel)

---

## 🎉 SUCCÈS !

**Votre bot WhatsApp Léa est maintenant en production !**

- 🌐 **Dashboard** : https://your-app-name.railway.app
- 📱 **WhatsApp** : +1 415 523 8886 (code: `join live-cold`)
- 📊 **API Stats** : https://your-app-name.railway.app/api/stats
- 🔧 **Logs** : Dashboard Railway

**Prochaines étapes recommandées** :
1. Partager avec utilisateurs test
2. Collecter feedback
3. Monitorer métriques
4. Planifier améliorations
