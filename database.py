import sqlite3
from flask import g

DATABASE = 'lea_nutrition.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

def init_db():
    """Initialise la base de données"""
    conn = sqlite3.connect(DATABASE)
    
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            phone_number TEXT PRIMARY KEY,
            name TEXT,
            age INTEGER,
            sex TEXT,
            objective TEXT,
            weight REAL,
            height REAL DEFAULT 170,
            activity_level REAL,
            activity_text TEXT,
            target_calories INTEGER,
            target_proteins INTEGER,
            target_fats INTEGER,
            target_carbs INTEGER,
            onboarding_step TEXT DEFAULT 'welcome',
            message_count INTEGER DEFAULT 0,
            is_premium BOOLEAN DEFAULT 0,
            premium_expires_at TIMESTAMP,
            stripe_customer_id TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_interaction TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Supprimer l'ancienne table daily_intake si elle existe
    conn.execute('DROP TABLE IF EXISTS daily_intake')
    
    # Créer la nouvelle table avec contrainte unique
    conn.execute('''
        CREATE TABLE daily_intake (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone_number TEXT,
            date DATE,
            calories REAL DEFAULT 0,
            proteins REAL DEFAULT 0,
            fats REAL DEFAULT 0,
            carbs REAL DEFAULT 0,
            FOREIGN KEY (phone_number) REFERENCES users(phone_number),
            UNIQUE(phone_number, date)
        )
    ''')
    
    conn.execute('''
        CREATE TABLE IF NOT EXISTS meals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone_number TEXT,
            date DATE,
            time TIME,
            meal_name TEXT,
            calories REAL,
            proteins REAL,
            fats REAL,
            carbs REAL,
            FOREIGN KEY (phone_number) REFERENCES users(phone_number)
        )
    ''')
    
    conn.commit()
    conn.close()

def increment_message_count(phone_number):
    """Incrémente le compteur de messages pour un utilisateur"""
    conn = sqlite3.connect(DATABASE)
    
    conn.execute('''
        UPDATE users 
        SET message_count = message_count + 1, last_interaction = CURRENT_TIMESTAMP
        WHERE phone_number = ?
    ''', (phone_number,))
    
    # Récupérer le nouveau compteur
    result = conn.execute(
        'SELECT message_count FROM users WHERE phone_number = ?',
        (phone_number,)
    ).fetchone()
    
    conn.commit()
    conn.close()
    
    return result[0] if result else 0

def is_user_premium(phone_number):
    """Vérifie si un utilisateur est premium et si son abonnement est valide"""
    conn = sqlite3.connect(DATABASE)
    
    result = conn.execute('''
        SELECT is_premium, premium_expires_at 
        FROM users 
        WHERE phone_number = ?
    ''', (phone_number,)).fetchone()
    
    conn.close()
    
    if not result:
        return False
    
    is_premium, expires_at = result
    
    if not is_premium:
        return False
    
    if expires_at:
        from datetime import datetime
        expiry_date = datetime.fromisoformat(expires_at)
        return datetime.now() < expiry_date
    
    return True

def set_user_premium(phone_number, stripe_customer_id, expires_at):
    """Active le statut premium pour un utilisateur"""
    conn = sqlite3.connect(DATABASE)
    
    conn.execute('''
        UPDATE users 
        SET is_premium = 1, 
            premium_expires_at = ?, 
            stripe_customer_id = ?
        WHERE phone_number = ?
    ''', (expires_at, stripe_customer_id, phone_number))
    
    conn.commit()
    conn.close()

def get_user_message_count(phone_number):
    """Récupère le nombre de messages d'un utilisateur"""
    conn = sqlite3.connect(DATABASE)
    
    result = conn.execute(
        'SELECT message_count FROM users WHERE phone_number = ?',
        (phone_number,)
    ).fetchone()
    
    conn.close()
    
    return result[0] if result else 0

def set_test_message_count(phone_number, count):
    """Définit le compteur de messages pour les tests (commandes /on30 et /off30)"""
    conn = sqlite3.connect(DATABASE)
    
    # S'assurer que l'utilisateur existe
    conn.execute('''
        INSERT OR IGNORE INTO users (phone_number, onboarding_step, message_count)
        VALUES (?, 'complete', 0)
    ''', (phone_number,))
    
    # Mettre à jour le compteur
    conn.execute('''
        UPDATE users 
        SET message_count = ?, last_interaction = CURRENT_TIMESTAMP
        WHERE phone_number = ?
    ''', (count, phone_number))
    
    conn.commit()
    conn.close()
    
    return count

def delete_user_data(phone_number):
    """Supprime complètement un utilisateur de la base de données"""
    conn = sqlite3.connect(DATABASE)
    
    # Supprimer toutes les données de l'utilisateur
    conn.execute('DELETE FROM meals WHERE phone_number = ?', (phone_number,))
    conn.execute('DELETE FROM daily_intake WHERE phone_number = ?', (phone_number,))
    conn.execute('DELETE FROM users WHERE phone_number = ?', (phone_number,))
    
    conn.commit()
    conn.close()

def get_all_users():
    """Récupère tous les utilisateurs actifs"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    
    users = conn.execute(
        'SELECT * FROM users WHERE onboarding_step = "complete"'
    ).fetchall()
    
    conn.close()
    
    return [dict(user) for user in users]

def get_user_data(phone_number):
    """Récupère les données utilisateur"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    
    # Récupérer les données utilisateur
    user = conn.execute(
        'SELECT * FROM users WHERE phone_number = ?', 
        (phone_number,)
    ).fetchone()
    
    if not user:
        return None
    
    # Récupérer les données nutritionnelles du jour
    from datetime import date
    today = date.today().isoformat()
    
    daily = conn.execute(
        'SELECT * FROM daily_intake WHERE phone_number = ? AND date = ?',
        (phone_number, today)
    ).fetchone()
    
    # Récupérer les repas du jour
    meals = conn.execute(
        'SELECT * FROM meals WHERE phone_number = ? AND date = ? ORDER BY time',
        (phone_number, today)
    ).fetchall()
    
    conn.close()
    
    # Construire l'objet utilisateur avec tous les champs onboarding
    user_data = {
        'phone_number': user['phone_number'],
        'name': user['name'],
        'age': user['age'],
        'sex': user['sex'],
        'gender': user['sex'],  # Mapping pour l'onboarding
        'objective': user['objective'],
        'goal': user['objective'],  # Mapping pour l'onboarding
        'weight': user['weight'],
        'height': user['height'],
        'activity_level': user['activity_level'],
        'activity_text': user['activity_text'],
        'target_calories': user['target_calories'],
        'target_proteins': user['target_proteins'],
        'target_fats': user['target_fats'],
        'target_carbs': user['target_carbs'],
        'onboarding_step': user['onboarding_step'],
        'onboarding_complete': user['onboarding_step'] == 'complete',
        'message_count': user['message_count'] or 0,
        'is_premium': bool(user['is_premium']),
        'premium_expires_at': user['premium_expires_at'],
        'stripe_customer_id': user['stripe_customer_id'],
        'daily_calories': daily['calories'] if daily else 0,
        'daily_proteins': daily['proteins'] if daily else 0,
        'daily_fats': daily['fats'] if daily else 0,
        'daily_carbs': daily['carbs'] if daily else 0,
        'meals': [dict(meal) for meal in meals] if meals else []
    }
    
    return user_data

def update_user_data(phone_number, user_data):
    """Met à jour les données utilisateur"""
    conn = sqlite3.connect(DATABASE)
    
    # Mettre à jour les données utilisateur avec mapping des champs
    conn.execute('''
        INSERT OR REPLACE INTO users 
        (phone_number, name, age, sex, objective, weight, height, activity_level, activity_text, 
         target_calories, target_proteins, target_fats, target_carbs, onboarding_step, last_interaction)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
    ''', (
        phone_number,
        user_data.get('name'),
        user_data.get('age'),
        user_data.get('sex') or user_data.get('gender'),  # Support des deux noms
        user_data.get('objective') or user_data.get('goal'),  # Support des deux noms
        user_data.get('weight'),
        user_data.get('height', 170),  # Valeur par défaut
        user_data.get('activity_level'),
        user_data.get('activity_text'),
        user_data.get('target_calories'),
        user_data.get('target_proteins'),
        user_data.get('target_fats'),
        user_data.get('target_carbs'),
        user_data.get('onboarding_step', 'complete')
    ))
    
    # Mettre à jour les données nutritionnelles du jour
    from datetime import date
    today = date.today().isoformat()
    
    # Maintenant INSERT OR REPLACE fonctionnera grâce à la contrainte UNIQUE
    conn.execute('''
        INSERT OR REPLACE INTO daily_intake 
        (phone_number, date, calories, proteins, fats, carbs)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        phone_number,
        today,
        user_data.get('daily_calories', 0),
        user_data.get('daily_proteins', 0),
        user_data.get('daily_fats', 0),
        user_data.get('daily_carbs', 0)
    ))
    
    # Supprimer les anciens repas du jour et ajouter les nouveaux
    conn.execute('DELETE FROM meals WHERE phone_number = ? AND date = ?', (phone_number, today))
    
    for meal in user_data.get('meals', []):
        conn.execute('''
            INSERT INTO meals 
            (phone_number, date, time, meal_name, calories, proteins, fats, carbs)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            phone_number,
            today,
            meal.get('time', ''),
            meal.get('name', ''),
            meal.get('calories', 0),
            meal.get('proteines', meal.get('proteins', 0)),  # Support des deux noms
            meal.get('lipides', meal.get('fats', 0)),        # Support des deux noms
            meal.get('glucides', meal.get('carbs', 0))       # Support des deux noms
        ))
    
    conn.commit()
    conn.close()
