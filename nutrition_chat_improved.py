import os
import requests
from dotenv import load_dotenv

load_dotenv()

def is_conversation_message(text):
    """Détermine si le message est une conversation normale (pas tracking d'aliment)"""
    
    # Messages de conversation évidents
    conversation_indicators = [
        # Salutations
        'salut', 'hello', 'hey', 'bonjour', 'bonsoir', 'coucou',
        'ça va', 'comment ça va', 'comment tu vas', 'tu vas bien',
        
        # Politesse
        'merci', 'thanks', 'merci beaucoup', 'super', 'génial', 'parfait',
        'de rien', 's\'il te plaît', 'stp', 'please',
        
        # Expressions courantes
        'oui', 'non', 'ok', 'okay', 'd\'accord', 'bien sûr',
        'yes', 'no', 'yeah', 'yep', 'nope',
        
        # Émotions/réactions
        'cool', 'top', 'nice', 'bien', 'mal', 'triste', 'content',
        'haha', 'lol', 'mdr', '😂', '😊', '😢', '👍', '👌',
        
        # Questions générales
        'comment', 'pourquoi', 'quand', 'où', 'qui', 'quoi',
        
        # Tracking acknowledgment (pas des aliments)
        'je track', 'je tracke', 'j\'ai tracké', 'tracking'
    ]
    
    # Mots-clés d'aliments spécifiques
    food_keywords = [
        # Quantités + aliments
        'grammes', 'kilos', 'litres', 'cuillères', 'morceaux', 'tranches',
        '100g', '50g', '200g', '150g', '300g', 'kg', 'ml',
        
        # Aliments spécifiques
        'poulet', 'bœuf', 'porc', 'poisson', 'saumon', 'thon',
        'riz', 'pâtes', 'pain', 'pomme', 'banane', 'avocat',
        'salade', 'tomate', 'carotte', 'brocoli', 'épinards',
        'yaourt', 'fromage', 'lait', 'œuf', 'œufs',
        'whey', 'whey protéine', 'protéine', 'amandes', 'noix',
        
        # Actions de consommation avec aliments
        'j\'ai mangé', 'j\'ai pris', 'j\'ai bu', 'j\'ai consommé',
        'ce midi j\'ai', 'ce matin j\'ai', 'ce soir j\'ai'
    ]
    
    text_lower = text.lower().strip()
    
    # Si le message est très court (1-2 mots) et contient des indicateurs de conversation
    if len(text.split()) <= 2:
        for indicator in conversation_indicators:
            if indicator in text_lower:
                print(f"💬 Détecté comme CONVERSATION (indicateur court: '{indicator}')")
                return True
    
    # Vérifier les indicateurs de conversation
    conversation_score = sum(1 for indicator in conversation_indicators if indicator in text_lower)
    
    # Vérifier les indicateurs d'aliments
    food_score = sum(1 for keyword in food_keywords if keyword in text_lower)
    
    print(f"🔍 Scores: conversation={conversation_score}, food={food_score}")
    
    # Si c'est clairement de la conversation
    if conversation_score >= 1 and food_score == 0:
        print("💬 Détecté comme CONVERSATION (score conversation > 0, pas d'aliment)")
        return True
    
    # Si c'est clairement du tracking d'aliment
    if food_score >= 2 or any(phrase in text_lower for phrase in ['j\'ai mangé', 'j\'ai pris', 'j\'ai bu']):
        print("🍽️ Détecté comme TRACKING d'aliment")
        return False
    
    # Cas ambigus - privilégier la conversation pour être plus naturel
    if conversation_score >= food_score:
        print("💬 Détecté comme CONVERSATION (privilégier conversation)")
        return True
    
    # Par défaut, si aucun indicateur clair, c'est probablement du tracking
    print("🍽️ Par défaut: TRACKING d'aliment")
    return False

def is_nutrition_question(text):
    """Détermine si le message est une question nutrition spécifique"""
    
    # Questions nutrition spécifiques
    nutrition_questions = [
        'que manger', 'quoi manger', 'comment manger',
        'conseil nutrition', 'aide nutrition', 'recommandation',
        'perdre du poids', 'prendre du muscle', 'maigrir', 'grossir',
        'protéine', 'glucide', 'lipide', 'calorie',
        'avant sport', 'après sport', 'entraînement',
        'fringale', 'faim', 'grignotage', 'collation',
        'régime', 'diet', 'nutrition', 'alimentaire'
    ]
    
    text_lower = text.lower()
    
    # Vérifier si c'est une question nutrition
    nutrition_score = sum(1 for keyword in nutrition_questions if keyword in text_lower)
    
    # Si contient un point d'interrogation ET des mots-clés nutrition
    if '?' in text and nutrition_score >= 1:
        print("💬 Détecté comme QUESTION nutrition spécifique")
        return True
    
    # Si plusieurs mots-clés nutrition
    if nutrition_score >= 2:
        print("💬 Détecté comme QUESTION nutrition spécifique")
        return True
    
    return False

def chat_with_lea_natural(message, user_data):
    """Chat naturel avec Léa comme ChatGPT"""
    try:
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            return "Désolé, je ne peux pas répondre pour le moment ! 😊"
        
        # Construire le contexte utilisateur
        user_context = build_user_context(user_data)
        
        # Récupérer l'historique de conversation
        conversation_history = get_conversation_history(user_data.get('phone_number'))
        
        # Compter les échanges récents pour gérer l'incitation au tracking
        recent_exchanges = len(conversation_history)
        should_encourage_tracking = (recent_exchanges > 0 and recent_exchanges % 4 == 0)  # 1 fois sur 4
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        system_prompt = f"""Tu es Léa, une coach nutrition sympa et naturelle. Tu discutes comme une amie bienveillante.

CONTEXTE UTILISATEUR:
{user_context}

RÈGLES DE CONVERSATION:
1. Sois NATURELLE et SPONTANÉE comme ChatGPT
2. Réponds de manière appropriée au message (salutation → salutation, merci → de rien, etc.)
3. Tutoie toujours, sois chaleureuse mais pas forcée
4. Utilise des emojis avec modération (1-2 max)
5. ÉVITE de forcer le tracking à chaque message
6. Sois concise (1-2 phrases max pour les conversations simples)
7. Adapte ton ton au message reçu

EXEMPLES DE BONNES RÉPONSES:
- "Hey Léa, ça va ?" → "Salut ! Ça va super bien ! Et toi ? 😊"
- "Merci !" → "De rien ! 😊"
- "Tu es géniale" → "Merci, tu es adorable ! 💕"
- "Oui" → "Parfait ! 👍"
- "Non" → "Pas de souci !"

ÉVITE ABSOLUMENT:
- Forcer le tracking dans chaque réponse
- Être trop "commerciale" ou pushy
- Réponses robotiques
- Encouragements forcés au tracking

INCITATION AU TRACKING: {"Ajoute une incitation SUBTILE au tracking à la fin" if should_encourage_tracking else "N'ajoute PAS d'incitation au tracking"}"""

        # Construire les messages avec l'historique
        messages = [{"role": "system", "content": system_prompt}]
        
        # Ajouter l'historique de conversation (max 4 derniers échanges)
        for msg in conversation_history[-4:]:
            messages.append({"role": "user", "content": msg['question']})
            messages.append({"role": "assistant", "content": msg['answer']})
        
        # Ajouter le message actuel
        messages.append({"role": "user", "content": message})

        payload = {
            "model": "gpt-4o-mini",
            "messages": messages,
            "max_tokens": 150,
            "temperature": 0.8
        }
        
        response = requests.post("https://api.openai.com/v1/chat/completions", 
                               headers=headers, json=payload, timeout=15)
        
        if response.status_code == 200:
            answer = response.json()['choices'][0]['message']['content']
            
            # Sauvegarder cet échange dans l'historique
            save_conversation_exchange(user_data.get('phone_number'), message, answer)
            
            return answer
        else:
            return "Oups, petit souci technique ! 😅"
        
    except Exception as e:
        print(f"❌ Erreur chat naturel: {e}")
        return "Désolé, j'ai un petit bug ! Réessaie ? 😊"

def chat_with_nutrition_expert(question, user_data):
    """Chat spécialisé pour les questions nutrition"""
    try:
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            return "Désolé, je ne peux pas répondre aux questions nutrition pour le moment ! 😊"
        
        # Construire le contexte utilisateur
        user_context = build_user_context(user_data)
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        system_prompt = f"""Tu es Léa, experte en nutrition. Tu réponds à une question nutrition spécifique.

CONTEXTE UTILISATEUR:
{user_context}

RÈGLES POUR LES QUESTIONS NUTRITION:
1. Donne des conseils PRÉCIS et ACTIONNABLES
2. Adapte à l'objectif de l'utilisateur
3. Sois concise (2-3 phrases max)
4. Utilise des emojis pertinents
5. Encourage subtilement le tracking à la fin

EXEMPLES:
- "Que manger avant le sport ?" → "30-60 min avant: banane + amandes ou avoine + fruits. Évite les graisses qui ralentissent la digestion ! 🏃‍♀️ N'hésite pas à tracker tes repas pré-workout."
- "Comment prendre du muscle ?" → "Vise 1.6-2g de protéines par kg de poids corporel et mange dans les 2h après ton entraînement ! 💪 Le tracking t'aidera à voir si tu atteins tes objectifs."
"""

        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            "max_tokens": 200,
            "temperature": 0.7
        }
        
        response = requests.post("https://api.openai.com/v1/chat/completions", 
                               headers=headers, json=payload, timeout=15)
        
        if response.status_code == 200:
            answer = response.json()['choices'][0]['message']['content']
            
            # Sauvegarder cet échange dans l'historique
            save_conversation_exchange(user_data.get('phone_number'), question, answer)
            
            return answer
        else:
            return "Oups, petit souci technique ! Peux-tu reformuler ta question ? 😅"
        
    except Exception as e:
        print(f"❌ Erreur chat nutrition: {e}")
        return "Désolé, j'ai un petit problème technique ! 😊"

def build_user_context(user_data):
    """Construit le contexte utilisateur pour personnaliser les réponses"""
    context_parts = []
    
    # Vérifier que user_data existe
    if not user_data:
        return "Utilisateur: Nouveau"
    
    # Informations de base
    name = user_data.get('name')
    if name:
        context_parts.append(f"Nom: {name}")
    
    age = user_data.get('age')
    if age:
        context_parts.append(f"Âge: {age} ans")
    
    sex = user_data.get('sex')
    if sex:
        sex_text = "Homme" if sex == 'H' else "Femme"
        context_parts.append(f"Sexe: {sex_text}")
    
    # Objectif principal
    objective = user_data.get('objective')
    if objective:
        context_parts.append(f"Objectif: {objective}")
    
    # Données nutritionnelles du jour
    daily_calories = user_data.get('daily_calories', 0)
    daily_proteins = user_data.get('daily_proteins', 0)
    
    context_parts.append(f"Calories du jour: {daily_calories:.0f} kcal")
    context_parts.append(f"Protéines du jour: {daily_proteins:.1f}g")
    
    # Nombre de repas trackés
    meals = user_data.get('meals', [])
    meals_count = len(meals)
    context_parts.append(f"Repas trackés aujourd'hui: {meals_count}")
    
    return "\n".join(context_parts) if context_parts else "Utilisateur: Profil en cours de création"

def get_conversation_history(phone_number):
    """Récupère l'historique de conversation pour maintenir le contexte"""
    import sqlite3
    from datetime import date
    
    try:
        conn = sqlite3.connect('lea_nutrition.db')
        conn.row_factory = sqlite3.Row
        
        # Récupérer les conversations du jour
        today = date.today().isoformat()
        
        conversations = conn.execute('''
            SELECT question, answer, timestamp FROM conversation_history 
            WHERE phone_number = ? AND date = ? 
            ORDER BY timestamp ASC
        ''', (phone_number, today)).fetchall()
        
        conn.close()
        
        return [{'question': conv['question'], 'answer': conv['answer']} for conv in conversations]
        
    except Exception as e:
        print(f"❌ Erreur récupération historique: {e}")
        return []

def save_conversation_exchange(phone_number, question, answer):
    """Sauvegarde un échange de conversation"""
    import sqlite3
    from datetime import date, datetime
    
    try:
        conn = sqlite3.connect('lea_nutrition.db')
        
        # Créer la table si elle n'existe pas
        conn.execute('''
            CREATE TABLE IF NOT EXISTS conversation_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phone_number TEXT,
                date DATE,
                timestamp DATETIME,
                question TEXT,
                answer TEXT
            )
        ''')
        
        # Insérer l'échange
        today = date.today().isoformat()
        now = datetime.now().isoformat()
        
        conn.execute('''
            INSERT INTO conversation_history 
            (phone_number, date, timestamp, question, answer)
            VALUES (?, ?, ?, ?, ?)
        ''', (phone_number, today, now, question, answer))
        
        conn.commit()
        conn.close()
        
        print(f"💾 Conversation sauvegardée pour {phone_number}")
        
    except Exception as e:
        print(f"❌ Erreur sauvegarde conversation: {e}")
