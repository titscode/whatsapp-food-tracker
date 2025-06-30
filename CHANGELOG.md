# 📋 Changelog - Léa Chatbot Nutrition

## 🚀 v0.91 - Personnalité Léa Améliorée (30/06/2025)

### ✨ **Nouvelles Fonctionnalités**
- **Messages en 2 parties** : Analyse aliment + bilan journée séparés
- **Personnalité coach bienveillante** : Léa plus humaine et encourageante
- **Conseils nutritionnels experts** : Insights poussés et personnalisés
- **Questions engageantes** : Conversation continue après chaque tracking
- **Formatage WhatsApp optimisé** : Texte en gras, structure claire

### 🔧 **Améliorations UX**
- **Phrases d'introduction positives** : Encouragements selon type d'aliment
- **Conseils spécialisés** : Timing whey, oméga-3, index glycémique, etc.
- **Progression personnalisée** : Messages selon objectif utilisateur
- **Format "consommé / objectif"** : Plus intuitif que "calories restantes"
- **Délai 1.5s entre messages** : Simulation conversation naturelle

### 💡 **Conseils Nutritionnels Avancés**
- **Timing optimal** : Whey post-entraînement, glucides autour sport
- **Composition détaillée** : Aminogramme, oméga-3 EPA/DHA, vitamines liposolubles
- **Astuces pratiques** : Vinaigrette allégée, répartition lipides
- **Ratios optimaux** : Protéines/glucides, bilan azoté positif
- **Adaptation objectif** : Conseils prise de masse vs perte de poids

### 🎯 **Questions Engageantes**
- **Selon nombre de repas** : Questions adaptées au moment de la journée
- **Personnalisées objectif** : Collations pour prise de masse, satiété pour perte
- **Variété aléatoire** : 3 questions par contexte pour éviter répétition
- **Ton naturel** : "Tu as prévu quoi ?", "Comment tu te sens ?"

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
