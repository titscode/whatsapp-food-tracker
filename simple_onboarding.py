def handle_simple_onboarding(phone_number, message, user_data):
    """Onboarding conversationnel et naturel selon les spécifications exactes"""
    from database import update_user_data
    
    step = user_data.get('onboarding_step', 'start')
    
    # Commande spéciale /tim pour remplir automatiquement le profil de Tim
    if message.strip().lower() == '/tim':
        user_data.update({
            'name': 'Tim',
            'goal': 'Prendre du muscle',
            'objective': 'Prendre du muscle',
            'age': 28,
            'gender': 'H',
            'sex': 'H',
            'weight': 70,
            'height': 175,
            'activity_level': 1.725,  # D - 5-6 fois par semaine
            'activity_text': '5-6 entraînements/semaine',
            'onboarding_step': 'complete',
            'onboarding_complete': True
        })
        
        # Calcul des objectifs avec les vraies formules
        age, weight, height, gender, goal, activity_level = 28, 70, 175, 'H', 'Prendre du muscle', 1.725
        
        # BMR avec la vraie taille
        bmr = 10 * weight + 6.25 * height + 5 * age + 5  # Homme
        tdee = bmr * activity_level
        calories = int(tdee * 1.10)  # Surplus de 10% pour prise de muscle
        proteins = int(weight * 2.2)  # 2.2g/kg pour prise de muscle
        fats = int(calories * 0.25 / 9)  # 25% des calories en lipides
        carbs = int((calories - proteins * 4 - fats * 9) / 4)  # Le reste en glucides
        
        user_data.update({
            'target_calories': calories,
            'target_proteins': proteins,
            'target_fats': fats,
            'target_carbs': carbs
        })
        
        update_user_data(phone_number, user_data)
        return f"🚀 *Profil Tim configuré automatiquement !*\n\n🎯 *Tes objectifs quotidiens :*\n🔥 Calories : {calories} kcal\n💪 Protéines : {proteins}g\n🥑 Lipides : {fats}g\n🍞 Glucides : {carbs}g\n\n📊 *Ton profil :*\n• 28 ans, 70kg, 175cm\n• 5-6 entraînements/semaine\n• Objectif : Prendre du muscle\n\nC'est parti ! 🔥\n\n📸 Envoie-moi une photo de ton plat ou écris ce que tu manges !"
    
    if step == 'start':
        # Étape 1 : Intro
        user_data['onboarding_step'] = 'name'
        update_user_data(phone_number, user_data)
        return "Salut ! Moi c'est Léa 👋 Tu t'appelles comment ?"
    
    elif step == 'name':
        # Étape 2 : Confirmation & Age
        user_data['name'] = message.strip()
        user_data['onboarding_step'] = 'age'
        update_user_data(phone_number, user_data)
        return f"Enchanté, {user_data['name']} ! ✌️ T'as quel age ?"
    
    elif step == 'age':
        # Étape 3 : Age → Poids
        try:
            # Extraire le nombre (gérer "28 ans", "28", etc.)
            import re
            age_match = re.search(r'(\d+)', message.strip())
            if not age_match:
                return "Je n'ai pas compris... Peux-tu me donner ton âge en chiffres ?"
            
            age = int(age_match.group(1))
            if age < 10 or age > 100:
                return "Cet âge me semble étrange... Peux-tu me redonner ton âge ?"
            
            user_data['age'] = age
            user_data['onboarding_step'] = 'weight'
            update_user_data(phone_number, user_data)
            return "Tu pèses combien ? (Dis-moi juste le nombre en kg 😉)"
            
        except ValueError:
            return "Je n'ai pas compris... Peux-tu me donner ton âge en chiffres ?"
    
    elif step == 'weight':
        # Étape 4 : Poids → Objectif
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
            user_data['onboarding_step'] = 'goal'
            update_user_data(phone_number, user_data)
            return "Et ça serait quoi ton objectif ?\n\n1 - Perdre du poids 📉\n2 - Prendre du muscle 💪\n3 - Garder la forme ⚡️"
            
        except ValueError:
            return "Je n'arrive pas à lire ton poids... Écris juste le nombre (ex: 70)"
    
    elif step == 'goal':
        # Étape 5 : Objectif → Taille
        message_clean = message.strip()
        if message_clean in ['1', 'perdre du poids', 'perdre', 'maigrir']:
            goal = 'Perdre du poids'
        elif message_clean in ['2', 'prendre du muscle', 'muscle', 'musculation']:
            goal = 'Prendre du muscle'
        elif message_clean in ['3', 'garder la forme', 'maintenir', 'forme']:
            goal = 'Maintenir ma forme'
        else:
            return "Réponds 1, 2 ou 3 selon ton objectif ! 😊"
        
        user_data['goal'] = goal
        user_data['objective'] = goal  # Mapping pour compatibilité
        user_data['onboarding_step'] = 'height'
        update_user_data(phone_number, user_data)
        return "Nickel ! Tu mesures combien ? (En cm, stp)"
    
    elif step == 'height':
        # Étape 6 : Taille → Genre
        try:
            # Extraire le nombre (gérer "175cm", "175 cm", "175", "1m75")
            import re
            height_match = re.search(r'(\d+(?:\.\d+)?)', message.strip())
            if not height_match:
                return "Je n'arrive pas à lire ta taille... Écris juste le nombre en cm (ex: 175)"
            
            height = float(height_match.group(1))
            
            # Gérer les cas où l'utilisateur donne en mètres (ex: 1.75)
            if height < 3:
                height = height * 100  # Convertir en cm
            
            if height < 120 or height > 220:
                return "Cette taille me semble étrange... Tu peux vérifier ? (en cm)"
            
            user_data['height'] = int(height)
            user_data['onboarding_step'] = 'gender'
            update_user_data(phone_number, user_data)
            return "Ok. Et t'es un homme ou une femme ?\n\n👨 Homme (H)\n👩 Femme (F)\n🦄 Ne souhaite pas répondre (N)"
            
        except ValueError:
            return "Je n'arrive pas à lire ta taille... Écris juste le nombre en cm (ex: 175)"
    
    elif step == 'gender':
        # Étape 7 : Genre → Activité
        message_clean = message.strip().upper()
        if message_clean in ['H', 'HOMME']:
            gender = 'H'
        elif message_clean in ['F', 'FEMME']:
            gender = 'F'
        elif message_clean in ['N', 'NE SOUHAITE PAS']:
            gender = 'N'  # Valeur intermédiaire pour les calculs
        else:
            return "Réponds H, F ou N ! 😊"
        
        user_data['gender'] = gender
        user_data['sex'] = gender  # Mapping pour compatibilité
        user_data['onboarding_step'] = 'activity'
        update_user_data(phone_number, user_data)
        return "Et niveau sport, tu te situes où ?\nA - Plutôt canapé 🛋️ (sédentaire)\nB - Tranquille, 1-2 fois / semaine\nC - Régulier, 3-4 fois / semaine\nD - À fond, 5-6 fois / semaine\nE - Machine !  7j/7 et +"
    
    elif step == 'activity':
        # Étape 8 : Activité → Calcul et finalisation
        message_clean = message.strip().upper()
        if message_clean == 'A':
            activity_level = 1.2
            activity_text = "sédentaire"
        elif message_clean == 'B':
            activity_level = 1.375
            activity_text = "1-2 fois/semaine"
        elif message_clean == 'C':
            activity_level = 1.55
            activity_text = "3-4 fois/semaine"
        elif message_clean == 'D':
            activity_level = 1.725
            activity_text = "5-6 fois/semaine"
        elif message_clean == 'E':
            activity_level = 1.9
            activity_text = "7+ fois/semaine"
        else:
            return "Réponds A, B, C, D ou E selon ton niveau d'activité ! 😊"
        
        user_data['activity_level'] = activity_level
        user_data['activity_text'] = activity_text
        user_data['onboarding_step'] = 'confirmation'
        update_user_data(phone_number, user_data)
        
        # Calcul des objectifs
        age = user_data['age']
        weight = user_data['weight']
        height = user_data['height']
        gender = user_data['gender']
        goal = user_data['goal']
        
        # Calcul BMR avec gestion du genre "N" (valeur intermédiaire)
        if gender == 'H':
            bmr = 10 * weight + 6.25 * height + 5 * age + 5
        elif gender == 'F':
            bmr = 10 * weight + 6.25 * height + 5 * age - 161
        else:  # Genre "N" - valeur intermédiaire
            bmr_h = 10 * weight + 6.25 * height + 5 * age + 5
            bmr_f = 10 * weight + 6.25 * height + 5 * age - 161
            bmr = (bmr_h + bmr_f) / 2  # Moyenne entre homme et femme
        
        # TDEE
        tdee = bmr * activity_level
        
        # Ajustement selon l'objectif
        if goal == 'Perdre du poids':
            calories = int(tdee * 0.85)
            proteins_per_kg = 2.0
        elif goal == 'Prendre du muscle':
            calories = int(tdee * 1.10)
            proteins_per_kg = 2.2
        else:  # Maintenir
            calories = int(tdee)
            proteins_per_kg = 1.8
        
        # Calcul des macronutriments
        proteins = int(weight * proteins_per_kg)
        fats = int(calories * 0.25 / 9)
        carbs = int((calories - proteins * 4 - fats * 9) / 4)
        
        # Sauvegarder les objectifs
        user_data['target_calories'] = calories
        user_data['target_proteins'] = proteins
        user_data['target_fats'] = fats
        user_data['target_carbs'] = carbs
        update_user_data(phone_number, user_data)
        
        # Message de confirmation selon le format exact demandé
        gender_text = "homme" if gender == 'H' else "femme" if gender == 'F' else "personne"
        return f"Voilà {user_data['name']}, tout est prêt ! 🚀\n\n🎯 Voici tes objectifs quotidiens :\n🔥 Calories : {calories} kcal\n💪 Protéines : {proteins}g\n🥑 Lipides : {fats}g\n🍞 Glucides : {carbs}g\n\nC'est calculé pour un {gender_text} de {age} ans qui s'entraîne {activity_text} pour {goal.lower()}. On est bon ?"
    
    elif step == 'confirmation':
        # Étape finale : Appel à l'action
        user_data['onboarding_step'] = 'complete'
        user_data['onboarding_complete'] = True
        update_user_data(phone_number, user_data)
        return "Alors, on commence ? Envoie-moi la photo de ton repas, ou dis-moi simplement ce que tu as mangé ce matin. C'est parti ! 💪\n\n/aide pour voir tout ce que je peux faire 😛"
    
    # Si on arrive ici, erreur
    user_data['onboarding_complete'] = True
    update_user_data(phone_number, user_data)
    return "Une erreur s'est produite. Tu peux maintenant utiliser l'app normalement !"
