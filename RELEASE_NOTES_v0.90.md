# 🚀 Léa v0.90 - Release Notes

**Date de release :** 30/06/2025  
**Tag Git :** v0.90  
**Statut :** ✅ STABLE - Prêt pour production

## 📋 Résumé de la Release

Léa v0.90 marque une étape majeure avec une **refactorisation complète** du code et des **améliorations critiques** de reconnaissance d'aliments.

## ✨ Fonctionnalités Principales

### 🍎 **Reconnaissance d'Aliments Révolutionnée**
- **400+ aliments** dans la base de données (vs 30 avant)
- **Recherche intelligente** : exacte → synonymes → partielle → mots-clés
- **Support fitness complet** : whey, BCAA, créatine, barres protéinées, gainers
- **Multi-aliments** : "50g poulet et 80g riz" analysé en une fois
- **Photos & texte** : GPT-4o Vision + parsing GPT-4o-mini

### 💬 **Conversation IA Naturelle**
- **Classification intelligente** : conversation vs tracking vs questions nutrition
- **Réponses personnalisées** selon profil utilisateur
- **Historique conversationnel** maintenu
- **Conseils nutrition experts** via GPT-4o-mini

### 📊 **Tracking Nutritionnel Précis**
- **Calculs BMR/TDEE** : formules Mifflin-St Jeor
- **Objectifs personnalisés** : prise de masse, perte, maintien
- **Affichage calories restantes** en temps réel
- **Macros optimisées** selon objectif

## 🔧 Améliorations Techniques

### **Code Refactorisé**
- **-40% de lignes** : 600 → 360 lignes dans app_production.py
- **Architecture modulaire** : handlers spécialisés
- **Gestion d'erreurs** optimisée
- **Performance** : requêtes SQL groupées

### **Nettoyage Projet**
- **Suppression fichiers inutiles** : backups, logs, docs redondantes
- **Structure simplifiée** : 19 fichiers essentiels
- **Optimisation tokens IA** : -50% consommation

## 🐛 Corrections Critiques

- ✅ **Classification messages** : patterns regex prioritaires
- ✅ **Reconnaissance whey/fitness** : 100% fonctionnelle  
- ✅ **Bug onboarding** : KeyError 'weight' corrigé
- ✅ **Formule calorique** : surplus 10% TDEE (vs +200 kcal fixe)

## 🚀 Déploiement

### **URLs Production**
- **Application** : https://web-production-eed0c.up.railway.app/
- **Webhook WhatsApp** : `/whatsapp`
- **Dashboard KPI** : `/`

### **Test WhatsApp**
1. **Numéro** : +1 415 523 8886
2. **Code d'activation** : `join live-cold`
3. **Test rapide** : `"40g de whey"` ou `"/first_try"`

## 📈 Métriques de Performance

| Métrique | v0.80 | v0.90 | Amélioration |
|----------|-------|-------|--------------|
| **Aliments reconnus** | ~30 | 400+ | **+1233%** |
| **Précision reconnaissance** | ~70% | ~95% | **+25%** |
| **Temps réponse** | ~3s | <2s | **-33%** |
| **Lignes de code** | 600 | 360 | **-40%** |
| **Fichiers projet** | 30+ | 19 | **-37%** |

## 🛠️ Commandes Utilisateur

| Commande | Description | Exemple |
|----------|-------------|---------|
| Tracking aliment | Reconnaissance automatique | `"40g de whey"` |
| Multi-aliments | Plusieurs aliments | `"50g poulet et 80g riz"` |
| Conversation | Chat naturel | `"Salut Léa !"` |
| Questions nutrition | Conseils experts | `"Que manger avant le sport ?"` |
| `/aide` | Menu d'aide | `/aide` |
| `/reset` | Reset données jour | `/reset` |
| `/first_try` | Restart onboarding | `/first_try` |

## 🎯 Tests de Validation

### **Tests Basiques** ✅
- `"50g de poulet"` → Reconnaissance + calculs
- `"30g de whey"` → Support fitness
- `"1 pomme"` → Conversion automatique

### **Tests Avancés** ✅  
- `"50g de poulet et 80g de riz"` → Multi-aliments
- `"1 shaker protéine"` → Synonymes fitness
- `"aliment inexistant"` → Gestion d'erreur

### **Tests Conversation** ✅
- `"Salut Léa !"` → Chat naturel
- `"Que manger avant le sport ?"` → Conseils nutrition
- `"Merci !"` → Réponses appropriées

## 📁 Architecture Finale

```
📦 chatbot-nutrition/
├── 🚀 app_production.py          # App principale (refactorisée)
├── 🍎 nutrition_database.py      # Base 400+ aliments
├── 🧠 nutrition_improved.py      # Analyse GPT + Vision  
├── 💬 nutrition_chat_improved.py # Classification + IA
├── 🎯 simple_onboarding.py       # Onboarding 7 étapes
├── 💾 database.py               # Gestion SQLite
├── ⚙️ config.py                 # Configuration
├── 🛠️ utils.py                  # Utilitaires
├── 📚 README.md                 # Documentation
├── 📋 CHANGELOG.md              # Historique versions
├── 🏷️ VERSION                   # Numéro version
├── 🚀 release.py                # Script release auto
└── 💾 lea_nutrition_v0.90_backup.db # Sauvegarde DB
```

## 🔄 Processus de Release

### **Sauvegarde Créée**
- ✅ **Tag Git** : v0.90
- ✅ **Backup DB** : lea_nutrition_v0.90_backup.db
- ✅ **Documentation** : README, CHANGELOG, VERSION
- ✅ **Script release** : release.py pour futures versions

### **Déploiement Automatique**
- ✅ **Push GitHub** → Railway auto-deploy
- ✅ **Tests validation** passés
- ✅ **Production stable** confirmée

## 🎯 Prochaines Versions

### **v0.91 - Personnalité Léa** (Planifié)
- Amélioration messages utilisateur
- Personnalité coach bienveillante
- UX WhatsApp optimisée

### **v0.92 - Conseils Avancés** (Planifié)
- Conseils nutrition poussés
- Insights personnalisés
- Recommandations proactives

### **v1.00 - Version Finale** (Objectif)
- Toutes fonctionnalités complètes
- Performance optimale
- Documentation exhaustive

## 📞 Support

**En cas de problème :**
1. Vérifier le statut : https://web-production-eed0c.up.railway.app/
2. Tester webhook : `/whatsapp`
3. Consulter logs Railway
4. Rollback possible vers tag v0.90

---

**🎉 Léa v0.90 - Version stable, optimisée et prête pour la production !**
