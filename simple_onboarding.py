def handle_simple_onboarding(phone_number, message, user_data):
    """Onboarding simple en 5 étapes pour calculer les objectifs nutritionnels"""
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
        return f"Salut {user_data['name']} ! 😊\n\nQuel est ton objectif ?\n\nA - Perdre du poids\nB - Prendre du muscle\nC - Maintenir ma forme\n\nRéponds A, B ou C"
    
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
        return f"Parfait ! Objectif : {goal} 🎯\n\nQuel âge as-tu ?"
    
    elif step == 'age':
        # Étape 4 : Âge → Poids
        try:
            age = int(message.strip())
            if age < 10 or age > 100:
                return "Cet âge me semble étrange... Peux-tu me redonner ton âge ?"
            
            user_data['age'] = age
            user_data['onboarding_step'] = 'weight'
            update_user_data(phone_number, user_data)
            return "Super ! Quel est ton poids actuel (en kg) ?\n\nEx: 70"
            
        except ValueError:
            return "Je n'ai pas compris... Peux-tu me donner ton âge en chiffres ?"
    
    elif step == 'weight':
        # Étape 5 : Poids → Calcul et finalisation
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
            
            # Calcul simple des objectifs
            if user_data['goal'] == 'Perdre du poids':
                calories = int(weight * 22)  # Déficit léger
                proteins = int(weight * 1.8)
            elif user_data['goal'] == 'Prendre du muscle':
                calories = int(weight * 28)  # Surplus léger
                proteins = int(weight * 2.0)
            else:  # Maintenir
                calories = int(weight * 25)  # Maintenance
                proteins = int(weight * 1.6)
            
            fats = int(calories * 0.25 / 9)  # 25% des calories
            carbs = int((calories - proteins * 4 - fats * 9) / 4)  # Le reste
            
            # Sauvegarder les objectifs
            user_data['target_calories'] = calories
            user_data['target_proteins'] = proteins
            user_data['target_fats'] = fats
            user_data['target_carbs'] = carbs
            user_data['onboarding_step'] = 'complete'
            user_data['onboarding_complete'] = True
            update_user_data(phone_number, user_data)
            
            return f"Parfait {user_data['name']} ! 🎉\n\n🎯 *Tes objectifs quotidiens :*\n🔥 Calories : {calories} kcal\n💪 Protéines : {proteins}g\n🥑 Lipides : {fats}g\n🍞 Glucides : {carbs}g\n\nMaintenant tu peux :\n📸 M'envoyer une photo de ton plat\n📝 Écrire ce que tu manges (ex: \"100g de riz\")\n💬 Me poser des questions nutrition\n\nTape /aide pour plus d'options !"
            
        except ValueError:
            return "Je n'arrive pas à lire ton poids... Écris juste le nombre (ex: 70)"
    
    # Si on arrive ici, erreur
    user_data['onboarding_complete'] = True
    update_user_data(phone_number, user_data)
    return "Une erreur s'est produite. Tu peux maintenant utiliser l'app normalement !"
