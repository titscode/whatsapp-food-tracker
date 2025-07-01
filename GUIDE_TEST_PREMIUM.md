# 🔒 Guide de Test - Système Premium Léa

## 📋 Configuration Actuelle

### ✅ **Ce qui a été configuré :**

1. **Système de Limitation :**
   - ✅ Limite de 30 messages gratuits par utilisateur
   - ✅ Comptage uniquement des messages UTILISATEUR (pas les réponses de Léa)
   - ✅ Pas de comptage pendant l'onboarding
   - ✅ Utilisateurs premium = messages illimités

2. **Lien Stripe Direct :**
   - ✅ Lien configuré : `https://buy.stripe.com/00w4gAgwWePa1LccID3cc02`
   - ✅ Prix : 50 CHF pour 12 mois (4.17 CHF/mois)
   - ✅ Pas de génération dynamique, utilise votre lien direct

3. **Message Premium Optimisé :**
   - ✅ Apparaît AVANT chaque réponse de Léa après 30 messages
   - ✅ Message conçu pour maximiser les conversions
   - ✅ Même message à chaque fois pour cohérence

4. **Commandes de Test :**
   - ✅ `/on30` - Simule dépassement de limite (met compteur à 31)
   - ✅ `/off30` - Remet compteur à 0
   - ✅ `/premium` - Affiche le lien de paiement

## 🧪 **Comment Tester**

### **Test 1 : Commandes de Test**
```
1. Envoyez "/off30" pour remettre à zéro
2. Envoyez "/on30" pour simuler dépassement
3. Envoyez n'importe quel message → Vous verrez le message premium avant la réponse
4. Envoyez "/off30" pour revenir normal
```

### **Test 2 : Limite Naturelle**
```
1. Créez un nouveau numéro de test
2. Envoyez 31 messages différents (pomme, banane, etc.)
3. Au 31ème message → Message premium apparaît avant la réponse
```

### **Test 3 : Lien de Paiement**
```
1. Tapez "/premium" 
2. Vous recevrez le lien Stripe : https://buy.stripe.com/00w4gAgwWePa1LccID3cc02
3. Testez le lien (utilisez une carte de test Stripe)
```

## 💬 **Comptage des Messages**

### ✅ **Messages COMPTÉS :**
- Messages texte utilisateur ("pomme", "j'ai mangé du riz", etc.)
- Photos d'aliments envoyées
- Questions nutrition ("combien de protéines ?")

### ❌ **Messages NON COMPTÉS :**
- Réponses de Léa (jamais comptées)
- Messages pendant l'onboarding
- Commandes spéciales (/aide, /reset, /premium, etc.)
- Messages des utilisateurs premium

## 🚀 **Message Premium Optimisé**

Voici le message qui apparaît AVANT chaque réponse après 30 messages :

```
🏆 *[Nom], passez à la vitesse supérieure !*

Vous avez utilisé vos 30 messages gratuits. Débloquez *Léa Performance* et maximisez vos résultats !

🎯 *Léa Performance - Conçu pour l'excellence :*
• 📊 Score de performance 0-100 pour chaque plat
• 🏅 Classement pour booster votre motivation
• ⚡ Réponses ultra-rapides sans publicité
• 🔥 Messages illimités pendant 12 mois

💎 *Seulement 50 CHF pour 12 mois*
(4.17 CHF/mois - moins qu'un café !)

👆 *DÉBLOQUEZ MAINTENANT :*
https://buy.stripe.com/00w4gAgwWePa1LccID3cc02

🚀 Grimpez dans le classement et atteignez vos objectifs !

---
```

## 🔧 **Commandes de Test Disponibles**

| Commande | Action | Utilisation |
|----------|--------|-------------|
| `/on30` | Met compteur à 31 | Tester expérience premium |
| `/off30` | Remet compteur à 0 | Revenir en mode normal |
| `/premium` | Affiche lien paiement | Tester message premium |
| `/aide` | Menu d'aide | Voir toutes les options |
| `/reset` | Reset données du jour | Remettre nutrition à zéro |

## 📱 **Test en Production**

1. **Déployez sur Railway** (déjà fait)
2. **Testez via WhatsApp** avec votre numéro
3. **Utilisez `/on30`** pour simuler la limite
4. **Envoyez un message** → Vous verrez le message premium
5. **Cliquez sur le lien** → Testez le paiement Stripe

## ✨ **Points Clés**

- ✅ **L'app n'est PAS bloquée** après 30 messages
- ✅ **Message premium apparaît AVANT chaque réponse** de Léa
- ✅ **Même message à chaque fois** pour cohérence
- ✅ **Seuls vos messages sont comptés**, pas les réponses de Léa
- ✅ **Lien direct Stripe** utilisé (pas de génération dynamique)
- ✅ **Commandes de test** pour simuler facilement

## 🎯 **Prêt pour les Clients**

Le système est maintenant opérationnel et prêt pour vos premiers clients premium ! 

**Prochaines étapes :**
1. Testez avec `/on30` et `/off30`
2. Vérifiez le lien Stripe fonctionne
3. Lancez auprès de vos utilisateurs ! 🚀
