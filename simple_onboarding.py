def handle_simple_onboarding(phone_number, message, user_data):
    """Onboarding complet en 7 étapes pour calculer les objectifs nutritionnels précis"""
    from database import update_user_data
    
    step = user_data.get('onboarding_step', 'start')
    
    if step == 'start':
        # Étape 1 : Accueil
        user_data['onboarding_step'] = 'name'
        update_user_data(phone_number, user_data)
        return "Salut ! Moi c'est Léa 👋\n\nJe vais t'aider à tracker tes aliments et atteindre tes objectifs !\n\nComment tu t'appelles ?"
    
    elif step == 'name':
        # Étape 2 : Nom → Objectif
        user_data['name'] = message.strip()
        user_data['onboarding_step'] = 'goal'
        update_user_data(phone_number, user_data)
        return f"Enchanté {user_data['name']} ! 😊\n\nQuel est ton objectif principal ?\n\nA - Perdre du poids\nB - Prendre du muscle\nC - Maintenir ma forme\n\nRéponds simplement A, B ou C"
    
    elif step == 'goal':
        # Étape 3 : Objectif → Âge
        message_clean = message.strip().upper()
        if message_clean == 'A':
            goal = 'Perdre du poids'
        elif message_clean == 'B':
            goal = 'Prendre du muscle'
        elif message_clean == 'C':
            goal = 'Maintenir ma forme'
        else:
            return "Réponds A, B ou C selon ton objectif ! 😊"
        
        user_data['goal'] = goal
        user_data['onboarding_step'] = 'age'
        update_user_data(phone_number, user_data)
        return f"Super choix ! Objectif : {goal} 🎯\n\nPour personnaliser tes conseils, quel âge as-tu ?"
    
    elif step == 'age':
        # Étape 4 : Âge → Sexe
        try:
            age = int(message.strip())
            if age < 10 or age > 100:
                return "Cet âge me semble étrange... Peux-tu me redonner ton âge ?"
            
            user_data['age'] = age
            user_data['onboarding_step'] = 'gender'
            update_user_data(phone_number, user_data)
            return "Parfait ! Es-tu un homme ou une femme ?\n\nH - Homme\nF - Femme\n\nRéponds H ou F"
            
        except ValueError:
            return "Je n'ai pas compris... Peux-tu me donner ton âge en chiffres ?"
    
    elif step == 'gender':
        # Étape 5 : Sexe → Poids
        message_clean = message.strip().upper()
        if message_clean in ['H', 'HOMME']:
            gender = 'H'
        elif message_clean in ['F', 'FEMME']:
            gender = 'F'
        else:
            return "Réponds H (homme) ou F (femme) ! 😊"
        
        user_data['gender'] = gender
        user_data['onboarding_step'] = 'weight'
        update_user_data(phone_number, user_data)
        return "Merci ! Maintenant, quel est ton poids actuel ?\n\nÉcris juste le nombre en kg (ex: 70)"
    
    elif step == 'weight':
        # Étape 6 : Poids → Activité physique
        try:
            # Extraire le nombre (gérer "70kg", "70 kg", "70")
            import re
            weight_match = re.search(r'(\d+(?:\.\d+)?)', message.strip())
            if not weight_match:
                return "Je n'arrive pas à lire ton poids... Écris juste le nombre (ex: 70)"
            
            weight = float(weight_match.group(1))
            if weight < 30 or weight > 200:
                return "Ce poids me semble étrange... Tu peux vérifier ?"
            
            user_data['weight'] = weight
            user_data['onboarding_step'] = 'activity'
            update_user_data(phone_number, user_data)
            return "Dernière question ! À quelle fréquence tu t'entraînes par semaine ? 💪\n\nA - Jamais (vie sédentaire)\nB - 1-2 fois par semaine\nC - 3-4 fois par semaine\nD - 5-6 fois par semaine\nE - 7+ fois par semaine\n\nRéponds A, B, C, D ou E"
            
        except ValueError:
            return "Je n'arrive pas à lire ton poids... Écris juste le nombre (ex: 70)"
    
    elif step == 'activity':
        # Étape 7 : Activité → Calcul et finalisation
        message_clean = message.strip().upper()
        if message_clean == 'A':
            activity_level = 1.2  # Sédentaire
            activity_text = "Sédentaire"
        elif message_clean == 'B':
            activity_level = 1.375  # Légèrement actif
            activity_text = "1-2 entraînements/semaine"
        elif message_clean == 'C':
            activity_level = 1.55  # Modérément actif
            activity_text = "3-4 entraînements/semaine"
        elif message_clean == 'D':
            activity_level = 1.725  # Très actif
            activity_text = "5-6 entraînements/semaine"
        elif message_clean == 'E':
            activity_level = 1.9  # Extrêmement actif
            activity_text = "7+ entraînements/semaine"
        else:
            return "Réponds A, B, C, D ou E selon ton niveau d'activité ! 😊"
        
        user_data['activity_level'] = activity_level
        user_data['activity_text'] = activity_text
        
        # VALIDATION : Vérifier que tous les champs requis sont présents
        required_fields = ['age', 'weight', 'gender', 'goal']
        missing_fields = [field for field in required_fields if field not in user_data or user_data[field] is None]
        
        if missing_fields:
            print(f"❌ ERREUR VALIDATION: Champs manquants: {missing_fields}")
            print(f"❌ user_data disponible: {list(user_data.keys())}")
            # Essayer de récupérer depuis les champs alternatifs
            if 'gender' not in user_data and 'sex' in user_data:
                user_data['gender'] = user_data['sex']
            if 'goal' not in user_data and 'objective' in user_data:
                user_data['goal'] = user_data['objective']
            
            # Vérifier à nouveau
            missing_fields = [field for field in required_fields if field not in user_data or user_data[field] is None]
            if missing_fields:
                return f"❌ Erreur: Données manquantes ({', '.join(missing_fields)}). Recommencez avec /first_try"
        
        # Calcul précis des objectifs avec formules standards
        try:
            age = user_data['age']
            weight = user_data['weight']
            gender = user_data['gender']
            goal = user_data['goal']
        except KeyError as e:
            print(f"❌ ERREUR ACCÈS DONNÉES: {e}")
            print(f"❌ user_data: {user_data}")
            return f"❌ Erreur technique: {e}. Recommencez avec /first_try"
        
        # Calcul BMR (métabolisme de base) - Formule Mifflin-St Jeor CORRIGÉE
        if gender == 'H':  # Homme
            bmr = 10 * weight + 6.25 * 175 + 5 * age + 5  # Hauteur estimée 175cm
        else:  # Femme
            bmr = 10 * weight + 6.25 * 165 + 5 * age - 161  # Hauteur estimée 165cm
        
        # TDEE (dépense énergétique totale)
        tdee = bmr * activity_level
        
        # Ajustement selon l'objectif - FORMULE CORRIGÉE
        if goal == 'Perdre du poids':
            calories = int(tdee * 0.85)  # Déficit de 15%
            proteins_per_kg = 2.0  # Plus de protéines pour préserver la masse musculaire
        elif goal == 'Prendre du muscle':
            calories = int(tdee * 1.10)  # Surplus de 10% (au lieu de +200 fixe)
            proteins_per_kg = 2.2  # Protéines pour la croissance
        else:  # Maintenir
            calories = int(tdee)  # Maintenance
            proteins_per_kg = 1.8  # Protéines standard
        
        # Calcul des macronutriments
        proteins = int(weight * proteins_per_kg)
        fats = int(calories * 0.25 / 9)  # 25% des calories en lipides
        carbs = int((calories - proteins * 4 - fats * 9) / 4)  # Le reste en glucides
        
        # Sauvegarder les objectifs
        user_data['target_calories'] = calories
        user_data['target_proteins'] = proteins
        user_data['target_fats'] = fats
        user_data['target_carbs'] = carbs
        user_data['onboarding_step'] = 'complete'
        user_data['onboarding_complete'] = True
        update_user_data(phone_number, user_data)
        
        return f"Parfait {user_data['name']} ! 🎉\n\n🎯 *Tes objectifs quotidiens personnalisés :*\n🔥 Calories : {calories} kcal\n💪 Protéines : {proteins}g\n🥑 Lipides : {fats}g\n🍞 Glucides : {carbs}g\n\n📊 *Ton profil :*\n• {age} ans, {activity_text}\n• Objectif : {goal}\n\nMaintenant je peux t'accompagner ! 🚀\n\n📸 Envoie-moi une photo de ton plat\n📝 Ou écris ce que tu manges (ex: \"100g de riz\")\n💬 Pose-moi des questions nutrition\n\nTape /aide pour découvrir toutes mes fonctions !"
    
    # Si on arrive ici, erreur
    user_data['onboarding_complete'] = True
    update_user_data(phone_number, user_data)
    return "Une erreur s'est produite. Tu peux maintenant utiliser l'app normalement !"
