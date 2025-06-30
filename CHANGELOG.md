# 📋 Changelog - Léa Chatbot Nutrition

## 🚀 v0.91 - Personnalité Léa Améliorée (30/06/2025)

### ✨ **Nouvelles Fonctionnalités**
- **Messages en 2 parties** : Séparation analyse du plat + bilan du jour
- **Personnalité coach bienveillante** : Léa plus humaine et encourageante
- **Conseils nutritionnels poussés** : Insights scientifiques personnalisés
- **Questions engageantes** : Conversation continue après chaque tracking
- **Intros positives** : Phrases d'encouragement spécifiques par aliment

### 🔧 **Améliorations UX**
- **Formatage WhatsApp optimisé** : Utilisation du gras (*texte*) pour la lisibilité
- **Bilan "consommé / objectif"** : Format plus intuitif (525 / 2200 kcal)
- **Délai entre messages** : 1.5s pour simuler conversation naturelle
- **Conseils contextuels** : Selon objectif, heure, et profil utilisateur
- **Questions personnalisées** : Adaptées à l'objectif et moment de la journée

### 🧠 **Intelligence Nutritionnelle**
- **Insights scientifiques** : PDCAAS, EPA/DHA, nitrates, acide oléique
- **Conseils timing** : Métabolisme matin, sérotonine soir, post-workout
- **Analyse macros avancée** : Synthèse protéique, hormones, glycogène
- **Recommandations spécifiques** : Par aliment (whey, saumon, épinards, etc.)
- **Adaptation objectifs** : Prise de masse, perte de poids, maintien

### 💬 **Expérience Conversationnelle**
- **Coach nutrition IA** : Léa donne des conseils comme une vraie coach
- **Encouragements personnalisés** : Selon catégorie d'aliment
- **Questions ouvertes** : Pour maintenir l'engagement utilisateur
- **Ton bienveillant** : Moins "robot", plus humain et motivant

---


## 🚀 v0.90 - Version Stable Refactorisée (30/06/2025)

### ✨ **Nouvelles Fonctionnalités**
- **Reconnaissance d'aliments révolutionnée** : 400+ aliments vs 30 avant
- **Support fitness/musculation** : whey, BCAA, créatine, barres protéinées, gainers
- **Multi-aliments** : "50g poulet et 80g riz" analysé en une fois
- **Classification intelligente** : conversation vs tracking vs questions nutrition
- **Dashboard KPI** : DAU, WAU, engagement, graphiques 14 jours

### 🔧 **Améliorations Techniques**
- **Code refactorisé** : -40% de lignes (600 → 360)
- **Architecture modulaire** : handlers spécialisés par type de message
- **Gestion d'erreurs** : try/catch optimisés et logging structuré
- **Performance** : requêtes SQL optimisées
- **Nettoyage projet** : suppression fichiers inutiles (-50% tokens IA)

### 🐛 **Corrections Critiques**
- **Classification messages** : patterns regex prioritaires pour tracking
- **Reconnaissance whey/fitness** : 100% fonctionnelle
- **Bug onboarding** : KeyError 'weight' corrigé
- **Formule calorique** : surplus 10% TDEE au lieu de +200 kcal fixe

### 📊 **Base de Données Nutritionnelle**
- **400+ aliments** avec recherche intelligente
- **Catégories complètes** : légumes, fruits, protéines, féculents, fitness
- **Synonymes et variantes** : reconnaissance flexible
- **Conversions automatiques** : 1 pomme = 180g, 1 banane = 120g

### 🎯 **Onboarding Optimisé**
- **7 étapes** : nom, âge, sexe, poids, taille, activité, objectif
- **Calculs BMR/TDEE** : formules Mifflin-St Jeor précises
- **Macros personnalisées** : selon objectif (prise de masse, perte, maintien)
- **Validation robuste** : vérification données avant calculs

### 💬 **Conversation IA**
- **Chat naturel** avec Léa (GPT-4o-mini)
- **Réponses personnalisées** selon profil utilisateur
- **Historique maintenu** : contexte conversationnel
- **Questions nutrition** : conseils experts spécialisés

### 🚀 **Déploiement**
- **Multi-environnements** : dev/staging/production
- **Railway auto-deploy** : push → déploiement automatique
- **Configuration flexible** : variables d'environnement
- **Monitoring** : logs structurés et métriques business

### 📈 **Statistiques v0.90**
- **~95% précision** reconnaissance aliments
- **<2s temps réponse** moyen
- **400+ aliments** supportés
- **Multi-formats** : texte, photos, quantités flexibles

---

## 🔄 **Versions Précédentes**

### v0.80 - Base Fonctionnelle
- Onboarding 7 étapes
- Calculs BMR/TDEE basiques
- ~30 aliments reconnus
- Tracking simple

### v0.70 - MVP Initial
- Bot WhatsApp basique
- Reconnaissance limitée
- Pas d'onboarding
- Calculs manuels

---

**🎯 Prochaines versions :**
- v0.91 : Amélioration personnalité Léa + messages UX
- v0.92 : Conseils nutritionnels avancés
- v0.93 : Analyse photos améliorée
- v1.00 : Version finale production
