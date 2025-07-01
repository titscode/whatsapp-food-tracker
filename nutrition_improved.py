import requests
import base64
import re
import os
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def analyze_food_request(text_content, media_url, debug_callback=None):
    """Point d'entrée principal pour l'analyse nutritionnelle"""
    try:
        if media_url:
            # Analyse d'image
            return analyze_image_openai(
                media_url, 
                os.getenv('TWILIO_ACCOUNT_SID'),
                os.getenv('TWILIO_AUTH_TOKEN'),
                os.getenv('OPENAI_API_KEY')
            )
        elif text_content:
            # Analyse de texte améliorée
            return analyze_text_improved(text_content, debug_callback)
        else:
            return None
    except Exception as e:
        # Utiliser logging au lieu de print
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"❌ Erreur analyze_food_request: {e}")
        if debug_callback:
            debug_callback(f"❌ DEBUG: Erreur analyze_food_request: {str(e)}")
        return None

def clean_json_content(content):
    """Nettoie le contenu JSON pour éviter les erreurs de parsing"""
    # Enlever les balises markdown si présentes
    if content.startswith('```json'):
        content = content.replace('```json', '').replace('```', '').strip()
    elif content.startswith('```'):
        content = content.replace('```', '').strip()
    
    # Nettoyer les espaces et retours à la ligne problématiques
    content = content.strip()
    
    # Remplacer les apostrophes courbes par des apostrophes droites
    content = content.replace(''', "'").replace(''', "'")
    content = content.replace('"', '"').replace('"', '"')
    
    # S'assurer que les chaînes sont bien échappées
    # Mais ne pas toucher aux guillemets qui délimitent les chaînes JSON
    lines = content.split('\n')
    cleaned_lines = []
    for line in lines:
        # Garder seulement les lignes non vides
        if line.strip():
            cleaned_lines.append(line.strip())
    
    return '\n'.join(cleaned_lines)

def parse_food_text_with_gpt(text, debug_callback=None):
    """Utilise GPT pour parser intelligemment le texte alimentaire - VERSION AMÉLIORÉE"""
    import logging
    logger = logging.getLogger(__name__)
    logger.debug(f"🔍 DEBUG GPT: Début parsing pour '{text}'")
    
    try:
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            logger.error("❌ DEBUG GPT: Clé API manquante")
            if debug_callback:
                debug_callback("❌ DEBUG GPT: Clé API manquante")
            return None
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        # Prompt amélioré pour éviter les ambiguïtés
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "system",
                    "content": """Tu es un expert en nutrition qui parse les descriptions d'aliments.

RÈGLE ABSOLUE : Retourne TOUJOURS un JSON avec la structure {"aliments": [...]} même pour un seul aliment.

FORMAT UNIQUE À UTILISER :
{
  "aliments": [
    {"aliment": "nom", "quantite": nombre, "unite": "g/ml/pieces", "poids_estime": nombre_en_grammes}
  ]
}

EXEMPLES :
- "50g de poulet" → {"aliments": [{"aliment": "poulet", "quantite": 50, "unite": "g", "poids_estime": 50}]}
- "50g de poulet et 80g d'orange" → {"aliments": [{"aliment": "poulet", "quantite": 50, "unite": "g", "poids_estime": 50}, {"aliment": "orange", "quantite": 80, "unite": "g", "poids_estime": 80}]}
- "une pomme et deux bananes" → {"aliments": [{"aliment": "pomme", "quantite": 1, "unite": "pieces", "poids_estime": 180}, {"aliment": "banane", "quantite": 2, "unite": "pieces", "poids_estime": 240}]}
- "150ml de lait" → {"aliments": [{"aliment": "lait", "quantite": 150, "unite": "ml", "poids_estime": 150}]}

CONVERSIONS :
- 1 pomme = 180g
- 1 banane = 120g
- 1 orange = 150g
- 1 œuf = 60g
- 1ml de liquide = 1g
- 1 cuillère à soupe = 15g
- 1 cuillère à café = 5g

IMPORTANT : 
- N'utilise QUE des guillemets doubles (")
- Pas d'apostrophes dans les noms d'aliments
- Retourne UNIQUEMENT le JSON, rien d'autre"""
                },
                {"role": "user", "content": f"Parse: {text}"}
            ],
            "max_tokens": 200,
            "temperature": 0.1
        }
        
        logger.debug(f"🌐 DEBUG GPT: Envoi requête à OpenAI...")
        
        response = requests.post("https://api.openai.com/v1/chat/completions", 
                               headers=headers, json=payload, timeout=15)
        
        logger.debug(f"📡 DEBUG GPT: Status code: {response.status_code}")
        
        if response.status_code == 200:
            content = response.json()['choices'][0]['message']['content'].strip()
            logger.debug(f"📝 DEBUG GPT: Réponse brute: '{content}'")
            
            # Nettoyer le contenu
            cleaned_content = clean_json_content(content)
            logger.debug(f"🧹 DEBUG GPT: Contenu nettoyé: '{cleaned_content}'")
            
            try:
                parsed_json = json.loads(cleaned_content)
                logger.debug(f"✅ DEBUG GPT: JSON parsé avec succès: {parsed_json}")
                
                # Normaliser la structure pour toujours avoir "aliments"
                if 'aliment' in parsed_json and 'aliments' not in parsed_json:
                    # Convertir l'ancien format en nouveau
                    parsed_json = {
                        'aliments': [{
                            'aliment': parsed_json['aliment'],
                            'quantite': parsed_json.get('quantite', 1),
                            'unite': parsed_json.get('unite', 'g'),
                            'poids_estime': parsed_json.get('poids_estime', 100)
                        }]
                    }
                
                return parsed_json
                
            except json.JSONDecodeError as e:
                logger.error(f"❌ DEBUG GPT: Erreur JSON: {e}")
                logger.error(f"❌ DEBUG GPT: Position erreur: {e.pos if hasattr(e, 'pos') else 'N/A'}")
                logger.error(f"❌ DEBUG GPT: Contenu problématique: {cleaned_content}")
                
                # Tentative de récupération avec regex
                return fallback_json_extraction(cleaned_content, text)
                
        else:
            error_msg = response.text[:200] if response.text else "Pas de détails"
            logger.error(f"❌ DEBUG GPT: Erreur HTTP {response.status_code}: {error_msg}")
            return None
        
    except Exception as e:
        logger.error(f"❌ DEBUG GPT: Exception: {e}")
        import traceback
        logger.error(f"❌ DEBUG GPT: Traceback: {traceback.format_exc()}")
        return None

def fallback_json_extraction(content, original_text):
    """Extraction de secours si le JSON parsing échoue"""
    import logging
    logger = logging.getLogger(__name__)
    logger.debug("🔄 Tentative d'extraction fallback...")
    
    try:
        # Chercher des patterns d'aliments avec regex
        aliments = []
        
        # Pattern pour "X g/ml de Y" ou "X Y"
        patterns = [
            r'"aliment"\s*:\s*"([^"]+)"[^}]*"quantite"\s*:\s*(\d+)[^}]*"unite"\s*:\s*"([^"]+)"[^}]*"poids_estime"\s*:\s*(\d+)',
            r'(\d+)\s*(g|ml|grammes?)\s+(?:de\s+)?([^\s,]+)',
            r'(\d+)\s+([^\s,]+)'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, content + " " + original_text, re.IGNORECASE)
            if matches:
                for match in matches:
                    if len(match) == 4:  # Pattern JSON
                        aliments.append({
                            'aliment': match[0],
                            'quantite': int(match[1]),
                            'unite': match[2],
                            'poids_estime': int(match[3])
                        })
                    elif len(match) == 3:  # Pattern texte
                        aliments.append({
                            'aliment': match[2],
                            'quantite': int(match[0]),
                            'unite': match[1],
                            'poids_estime': int(match[0])
                        })
                
                if aliments:
                    return {'aliments': aliments}
        
        # Si rien trouvé, parser le texte original basiquement
        return basic_text_parsing(original_text)
        
    except Exception as e:
        logger.error(f"❌ Fallback extraction failed: {e}")
        return None

def basic_text_parsing(text):
    """Parsing basique du texte comme dernier recours"""
    import logging
    logger = logging.getLogger(__name__)
    logger.debug("🔄 Parsing basique du texte...")
    
    # Séparer par "et", "avec", ","
    parts = re.split(r'\s+(?:et|avec|,)\s+', text.lower())
    aliments = []
    
    for part in parts:
        part = part.strip()
        if not part:
            continue
            
        # Chercher quantité et aliment
        match = re.search(r'(\d+)\s*(?:g|ml|grammes?)?\s*(?:de\s+)?(.+)', part)
        if match:
            quantite = int(match.group(1))
            aliment = match.group(2).strip()
        else:
            # Chercher "une/un/deux/trois..."
            nombre_match = re.search(r'(une?|deux|trois)\s+(.+)', part)
            if nombre_match:
                nombres = {'un': 1, 'une': 1, 'deux': 2, 'trois': 3}
                quantite = nombres.get(nombre_match.group(1), 1)
                aliment = nombre_match.group(2).strip()
                # Estimer le poids
                poids = get_default_piece_weight(aliment) * quantite
                aliments.append({
                    'aliment': aliment,
                    'quantite': quantite,
                    'unite': 'pieces',
                    'poids_estime': poids
                })
                continue
            else:
                # Juste le nom de l'aliment
                aliment = part
                quantite = 100  # Par défaut
        
        aliments.append({
            'aliment': aliment,
            'quantite': quantite,
            'unite': 'g',
            'poids_estime': quantite
        })
    
    return {'aliments': aliments} if aliments else None

def analyze_text_improved(text, debug_callback=None):
    """Analyse améliorée du texte avec GPT pour comprendre les quantités"""
    import logging
    logger = logging.getLogger(__name__)
    logger.debug(f"🔍 Analyse texte améliorée: {text}")
    
    # Essayer d'abord avec GPT
    parsed_data = parse_food_text_with_gpt(text, debug_callback)
    
    if parsed_data and 'aliments' in parsed_data:
        logger.debug(f"📊 GPT a parsé {len(parsed_data['aliments'])} aliment(s)")
        return process_multiple_foods(parsed_data['aliments'], text)
    
    # Fallback vers l'ancienne méthode
    logger.warning("⚠️ GPT parsing failed, using fallback method")
    if debug_callback:
        debug_callback("⚠️ Utilisation de la méthode fallback")
    return analyze_text_fallback(text)

def process_multiple_foods(aliments_list, original_text):
    """Traite une liste d'aliments et retourne un résumé nutritionnel"""
    ingredients = []
    total_calories = 0
    total_proteins = 0
    total_fats = 0
    total_carbs = 0
    
    for aliment_data in aliments_list:
        aliment = aliment_data.get('aliment', 'Aliment')
        poids = aliment_data.get('poids_estime', 100)
        quantite = aliment_data.get('quantite', '')
        unite = aliment_data.get('unite', '')
        
        print(f"  → {aliment}: {poids}g ({quantite} {unite})")
        
        # Obtenir les données nutritionnelles
        nutrition = get_nutrition_for_ingredient(aliment, poids)
        
        ingredients.append({
            'name': aliment,
            'grams': poids,
            'calories': nutrition['calories'],
            'proteins': nutrition['proteins'],
            'fats': nutrition['fats'],
            'carbs': nutrition['carbs']
        })
        
        total_calories += nutrition['calories']
        total_proteins += nutrition['proteins']
        total_fats += nutrition['fats']
        total_carbs += nutrition['carbs']
    
    # Créer un nom descriptif
    if len(ingredients) == 1:
        # Un seul aliment
        ing = ingredients[0]
        name = f"{aliment_data.get('quantite', '')} {aliment_data.get('unite', '')} de {ing['name']}".strip()
    else:
        # Plusieurs aliments
        ingredients_names = [ing['name'] for ing in ingredients]
        name = f"Repas ({', '.join(ingredients_names[:3])}{'...' if len(ingredients_names) > 3 else ''})"
    
    total_weight = sum(ing['grams'] for ing in ingredients)
    
    return {
        'name': name,
        'calories': total_calories,
        'proteines': total_proteins,
        'lipides': total_fats,
        'glucides': total_carbs,
        'source': 'GPT-4o-mini + Base nutritionnelle',
        'detected_by': 'GPT',
        'total_weight': total_weight,
        'ingredients': ingredients,
        'time': datetime.now().strftime('%H:%M')
    }

def analyze_text_fallback(text):
    """Méthode de fallback pour l'analyse de texte"""
    print(f"🔄 Fallback analyse texte: {text}")
    
    # Utiliser le parsing basique
    parsed = basic_text_parsing(text)
    if parsed and 'aliments' in parsed:
        return process_multiple_foods(parsed['aliments'], text)
    
    # Sinon 100g par défaut
    nutrition = get_nutrition_for_ingredient(text, 100)
    return {
        'name': f"100g de {text}",
        'calories': nutrition['calories'],
        'proteines': nutrition['proteins'],
        'lipides': nutrition['fats'],
        'glucides': nutrition['carbs'],
        'source': 'Défaut 100g',
        'time': datetime.now().strftime('%H:%M')
    }

def get_piece_weight(food_type):
    """Retourne le poids d'une pièce d'aliment"""
    weights = {
        'amande': 1,
        'amandes': 1,
        'noix': 5,
        'œuf': 60,
        'œufs': 60,
        'oeuf': 60,
        'oeufs': 60,
        'tranche': 25,  # pain
        'tranches': 25,
        'pomme': 180,
        'pommes': 180,
        'banane': 120,
        'bananes': 120,
        'orange': 150,
        'oranges': 150
    }
    return weights.get(food_type.lower(), 100)  # 100g par défaut

def get_default_piece_weight(food_name):
    """Retourne le poids par défaut pour un aliment"""
    return get_piece_weight(food_name)

def download_twilio_media(media_url, account_sid, auth_token):
    """Télécharge le média depuis Twilio"""
    try:
        response = requests.get(media_url, auth=(account_sid, auth_token), timeout=30)
        if response.status_code == 200 and len(response.content) > 1000:
            return response.content
        return None
    except Exception as e:
        print(f"❌ Erreur téléchargement: {e}")
        return None

def analyze_image_openai(image_url, account_sid, auth_token, api_key):
    """Analyse une image avec OpenAI Vision - Version améliorée"""
    try:
        # Télécharger l'image
        image_bytes = download_twilio_media(image_url, account_sid, auth_token)
        if not image_bytes:
            return None
            
        # Encoder en base64
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        
        prompt = """IMPORTANT: Tu DOIS analyser cette image et retourner EXACTEMENT dans ce format JSON:

{
  "aliments": [
    {"nom": "nom_aliment", "poids": nombre_en_grammes, "description": "courte_description"}
  ]
}

RÈGLES STRICTES:
1. Retourne UNIQUEMENT le JSON, rien d'autre
2. Estime les poids réalistes selon les portions visibles
3. Pour les aliments en pièces, calcule le poids total

PORTIONS DE RÉFÉRENCE:
- Pomme/fruit moyen: 150-200g
- Salade/légumes verts: 30-50g par poignée visible
- Tomates cerises: 15g par pièce
- Avocat entier: 150g, demi: 75g
- Viande/poisson: 100-150g par portion
- Riz/pâtes cuits: 80-120g par portion
- Pain: 25g par tranche
- Fromage: 30g par portion
- Amandes: 1g par pièce
- Noix: 5g par pièce

EXEMPLES:
- Si tu vois 3 tomates cerises → {"nom": "tomates cerises", "poids": 45, "description": "3 pièces"}
- Si tu vois une poignée de salade → {"nom": "salade verte", "poids": 40, "description": "poignée"}
- Si tu vois 10 amandes → {"nom": "amandes", "poids": 10, "description": "10 pièces"}

Analyse cette image:"""
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        payload = {
            "model": "gpt-4o",
            "messages": [
                {
                    "role": "system",
                    "content": "Tu es un nutritionniste expert qui analyse les images d'aliments avec précision."
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
                    ]
                }
            ],
            "max_tokens": 500
        }
        
        response = requests.post("https://api.openai.com/v1/chat/completions", 
                               headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            content = response.json()['choices'][0]['message']['content']
            return parse_vision_response_improved(content)
            
        return None
            
    except Exception as e:
        print(f"❌ Erreur Vision: {e}")
        return None

def parse_vision_response_improved(content):
    """Parse la réponse améliorée de Vision avec format JSON"""
    print(f"🔍 Parsing réponse Vision améliorée: {content}")
    
    try:
        # Nettoyer le contenu
        cleaned_content = clean_json_content(content)
        
        # Parser le JSON
        data = json.loads(cleaned_content)
        aliments = data.get('aliments', [])
        
        if not aliments:
            print("⚠️ Aucun aliment détecté dans le JSON")
            return None
        
        ingredients = []
        total_calories = 0
        total_proteins = 0
        total_fats = 0
        total_carbs = 0
        
        for aliment in aliments:
            nom = aliment.get('nom', 'Aliment inconnu')
            poids = aliment.get('poids', 50)
            description = aliment.get('description', '')
            
            print(f"  → {nom}: {poids}g ({description})")
            
            # Obtenir les données nutritionnelles
            nutrition = get_nutrition_for_ingredient(nom, poids)
            
            ingredients.append({
                'name': nom,
                'grams': poids,
                'description': description,
                'calories': nutrition['calories'],
                'proteins': nutrition['proteins'],
                'fats': nutrition['fats'],
                'carbs': nutrition['carbs']
            })
            
            total_calories += nutrition['calories']
            total_proteins += nutrition['proteins']
            total_fats += nutrition['fats']
            total_carbs += nutrition['carbs']
        
        # Créer un résumé global
        ingredients_names = [ing['name'] for ing in ingredients]
        total_weight = sum(ing['grams'] for ing in ingredients)
        
        return {
            'name': f"Repas ({', '.join(ingredients_names[:3])}{'...' if len(ingredients_names) > 3 else ''})",
            'calories': total_calories,
            'proteines': total_proteins,
            'lipides': total_fats,
            'glucides': total_carbs,
            'source': 'OpenAI Vision Pro',
            'detected_by': 'OpenAI',
            'total_weight': total_weight,
            'ingredients': ingredients,
            'confidence': 0.95,
            'time': datetime.now().strftime('%H:%M')
        }
        
    except json.JSONDecodeError as e:
        print(f"❌ Erreur JSON Vision: {e}")
        print(f"Contenu reçu: {content}")
        return None
    except Exception as e:
        print(f"❌ Erreur parsing Vision: {e}")
        return None

def get_nutrition_for_ingredient(ingredient, grams):
    """
    Fonction améliorée utilisant la base de données nutritionnelle étendue
    """
    # Importer la nouvelle base de données
    from nutrition_database import get_nutrition_for_ingredient as get_nutrition_enhanced
    
    # Utiliser la fonction améliorée
    return get_nutrition_enhanced(ingredient, grams)
