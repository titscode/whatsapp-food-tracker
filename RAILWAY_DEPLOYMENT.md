# 🚀 Guide de Déploiement Railway - Léa Bot WhatsApp

## 📋 **Variables d'Environnement Nécessaires**

### **🔑 Clés API Obligatoires**
```env
OPENAI_API_KEY=sk-your-openai-key-here
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your-twilio-auth-token
TWILIO_PHONE_NUMBER=whatsapp:+14155238886
```

### **⚙️ Variables Railway (Automatiques)**
- `PORT` : Géré automatiquement par Railway
- `RAILWAY_ENVIRONMENT` : production

---

## 🚀 **Instructions de Déploiement**

### **1. Connecter GitHub à Railway**
1. Aller sur [railway.app](https://railway.app)
2. Se connecter avec GitHub
3. Cliquer sur "New Project"
4. Sélectionner "Deploy from GitHub repo"
5. Choisir le repository : `titscode/whatsapp-food-tracker`
6. Sélectionner la branche : `production-clean`

### **2. Configuration des Variables d'Environnement**
1. Dans le dashboard Railway, aller dans l'onglet "Variables"
2. Ajouter les 4 variables obligatoires :
   ```
   OPENAI_API_KEY = sk-your-key...
   TWILIO_ACCOUNT_SID = ACxxxxxxxx...
   TWILIO_AUTH_TOKEN = your-token...
   TWILIO_PHONE_NUMBER = whatsapp:+14155238886
   ```
3. Cliquer sur "Save" pour chaque variable

### **3. Déploiement Automatique**
- Railway détecte automatiquement les fichiers :
  - `Procfile` : Commande de démarrage
  - `requirements.txt` : Dépendances Python
  - `railway.json` : Configuration Railway
- Le déploiement se lance automatiquement
- Attendre 2-3 minutes pour le build complet

### **4. Récupérer l'URL de Production**
1. Dans le dashboard Railway, aller dans "Settings"
2. Section "Domains" → Cliquer sur "Generate Domain"
3. Noter l'URL générée : `https://your-app-name.railway.app`

---

## 🔧 **Configuration Twilio Finale**

### **Mise à jour du Webhook WhatsApp**
1. Aller sur [console.twilio.com](https://console.twilio.com)
2. Messaging → Settings → WhatsApp sandbox settings
3. Remplacer l'URL webhook par :
   ```
   https://your-app-name.railway.app/whatsapp
   ```
4. Sauvegarder la configuration

### **Test de Fonctionnement**
1. Envoyer `join live-cold` au +1 415 523 8886
2. Tester avec : "50g de poulet"
3. Vérifier la réponse du bot

---

## 📊 **URLs de Production**

### **🌐 Endpoints Disponibles**
- **Dashboard KPI** : `https://your-app-name.railway.app/`
- **Webhook WhatsApp** : `https://your-app-name.railway.app/whatsapp`
- **API Stats** : `https://your-app-name.railway.app/api/stats`
- **API DAU History** : `https://your-app-name.railway.app/api/dau-history`

---

## 🔍 **Monitoring et Logs**

### **Logs Railway**
- Dans le dashboard Railway, onglet "Deployments"
- Cliquer sur le déploiement actuel
- Voir les logs en temps réel

### **Métriques Disponibles**
- CPU et RAM usage
- Requêtes par minute
- Temps de réponse
- Erreurs 4xx/5xx

---

## 🛠️ **Dépannage**

### **Problèmes Courants**
1. **Build Failed** : Vérifier `requirements.txt`
2. **App Crash** : Vérifier les variables d'environnement
3. **Webhook Error** : Vérifier l'URL Twilio
4. **Database Error** : SQLite se crée automatiquement

### **Commandes de Debug**
```bash
# Voir les logs
railway logs

# Redéployer
git push origin production-clean

# Variables d'environnement
railway variables
```

---

## ✅ **Checklist de Déploiement**

- [ ] Repository connecté à Railway
- [ ] Variables d'environnement configurées
- [ ] Build réussi (vert dans Railway)
- [ ] URL de production générée
- [ ] Webhook Twilio mis à jour
- [ ] Test WhatsApp fonctionnel
- [ ] Dashboard accessible
- [ ] APIs JSON opérationnelles

---

## 🎯 **Post-Déploiement**

### **Surveillance**
- Monitorer les logs Railway
- Vérifier les métriques dashboard
- Tester régulièrement le bot WhatsApp

### **Mises à jour**
- Push sur `production-clean` → Déploiement automatique
- Variables d'environnement modifiables via Railway
- Rollback possible via l'interface Railway

**🎉 Votre bot WhatsApp Léa est maintenant en production sur Railway !**
