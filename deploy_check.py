#!/usr/bin/env python3
"""
🚀 Script de Vérification Pré-Déploiement - Léa Bot WhatsApp
Vérifie que tous les composants sont prêts pour le déploiement Railway
"""

import os
import sys
import json
import sqlite3
from pathlib import Path
from dotenv import load_dotenv

# Couleurs pour l'affichage
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_status(message, status="info"):
    """Affiche un message avec couleur selon le statut"""
    if status == "success":
        print(f"{Colors.GREEN}✅ {message}{Colors.END}")
    elif status == "error":
        print(f"{Colors.RED}❌ {message}{Colors.END}")
    elif status == "warning":
        print(f"{Colors.YELLOW}⚠️  {message}{Colors.END}")
    else:
        print(f"{Colors.BLUE}ℹ️  {message}{Colors.END}")

def check_file_exists(filepath, description):
    """Vérifie qu'un fichier existe"""
    if Path(filepath).exists():
        print_status(f"{description}: {filepath}", "success")
        return True
    else:
        print_status(f"{description} MANQUANT: {filepath}", "error")
        return False

def check_env_variables():
    """Vérifie les variables d'environnement"""
    print(f"\n{Colors.BOLD}🔑 VÉRIFICATION VARIABLES D'ENVIRONNEMENT{Colors.END}")
    
    load_dotenv()
    
    required_vars = [
        ("OPENAI_API_KEY", "Clé API OpenAI"),
        ("TWILIO_ACCOUNT_SID", "SID Compte Twilio"),
        ("TWILIO_AUTH_TOKEN", "Token Auth Twilio"),
        ("TWILIO_PHONE_NUMBER", "Numéro WhatsApp Twilio")
    ]
    
    all_good = True
    for var_name, description in required_vars:
        value = os.getenv(var_name)
        if value and value != f"your-{var_name.lower().replace('_', '-')}-here":
            print_status(f"{description}: Configuré", "success")
        else:
            print_status(f"{description}: NON CONFIGURÉ", "error")
            all_good = False
    
    return all_good

def check_dependencies():
    """Vérifie les dépendances Python"""
    print(f"\n{Colors.BOLD}📦 VÉRIFICATION DÉPENDANCES{Colors.END}")
    
    try:
        import flask
        print_status(f"Flask: {flask.__version__}", "success")
    except ImportError:
        print_status("Flask: NON INSTALLÉ", "error")
        return False
    
    try:
        import twilio
        print_status(f"Twilio: {twilio.__version__}", "success")
    except ImportError:
        print_status("Twilio: NON INSTALLÉ", "error")
        return False
    
    try:
        import openai
        print_status(f"OpenAI: {openai.__version__}", "success")
    except ImportError:
        print_status("OpenAI: NON INSTALLÉ", "error")
        return False
    
    return True

def check_database():
    """Vérifie la base de données"""
    print(f"\n{Colors.BOLD}💾 VÉRIFICATION BASE DE DONNÉES{Colors.END}")
    
    try:
        from database import init_db
        init_db()
        
        # Vérifier les tables
        conn = sqlite3.connect('lea_nutrition.db')
        cursor = conn.cursor()
        
        tables = ['users', 'daily_intake', 'meals']
        for table in tables:
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
            if cursor.fetchone():
                print_status(f"Table {table}: OK", "success")
            else:
                print_status(f"Table {table}: MANQUANTE", "error")
                return False
        
        conn.close()
        return True
        
    except Exception as e:
        print_status(f"Erreur base de données: {e}", "error")
        return False

def check_api_connections():
    """Teste les connexions API (optionnel)"""
    print(f"\n{Colors.BOLD}🌐 TEST CONNEXIONS API{Colors.END}")
    
    load_dotenv()
    
    # Test OpenAI (optionnel car coûteux)
    openai_key = os.getenv('OPENAI_API_KEY')
    if openai_key and openai_key.startswith('sk-'):
        print_status("Clé OpenAI: Format valide", "success")
    else:
        print_status("Clé OpenAI: Format invalide", "warning")
    
    # Test Twilio (optionnel)
    twilio_sid = os.getenv('TWILIO_ACCOUNT_SID')
    if twilio_sid and twilio_sid.startswith('AC'):
        print_status("SID Twilio: Format valide", "success")
    else:
        print_status("SID Twilio: Format invalide", "warning")
    
    return True

def check_railway_config():
    """Vérifie la configuration Railway"""
    print(f"\n{Colors.BOLD}🚂 VÉRIFICATION CONFIGURATION RAILWAY{Colors.END}")
    
    files_ok = True
    
    # Vérifier Procfile
    if check_file_exists("Procfile", "Procfile"):
        with open("Procfile", "r") as f:
            content = f.read().strip()
            if "python app_production.py" in content:
                print_status("Procfile: Commande correcte", "success")
            else:
                print_status("Procfile: Commande incorrecte", "error")
                files_ok = False
    else:
        files_ok = False
    
    # Vérifier railway.json
    if check_file_exists("railway.json", "Configuration Railway"):
        try:
            with open("railway.json", "r") as f:
                config = json.load(f)
                if config.get("deploy", {}).get("startCommand") == "python app_production.py":
                    print_status("railway.json: Configuration correcte", "success")
                else:
                    print_status("railway.json: Configuration incorrecte", "warning")
        except json.JSONDecodeError:
            print_status("railway.json: Format JSON invalide", "error")
            files_ok = False
    else:
        files_ok = False
    
    # Vérifier requirements.txt
    if check_file_exists("requirements.txt", "Dépendances Python"):
        with open("requirements.txt", "r") as f:
            deps = f.read()
            required_deps = ["flask", "twilio", "openai", "python-dotenv"]
            for dep in required_deps:
                if dep in deps.lower():
                    print_status(f"Dépendance {dep}: OK", "success")
                else:
                    print_status(f"Dépendance {dep}: MANQUANTE", "error")
                    files_ok = False
    else:
        files_ok = False
    
    return files_ok

def main():
    """Fonction principale de vérification"""
    print(f"{Colors.BOLD}🚀 VÉRIFICATION PRÉ-DÉPLOIEMENT - LÉA BOT WHATSAPP{Colors.END}")
    print("=" * 60)
    
    checks = [
        ("Fichiers de configuration", check_railway_config),
        ("Variables d'environnement", check_env_variables),
        ("Dépendances Python", check_dependencies),
        ("Base de données", check_database),
        ("Connexions API", check_api_connections)
    ]
    
    results = []
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print_status(f"Erreur lors de {check_name}: {e}", "error")
            results.append((check_name, False))
    
    # Résumé final
    print(f"\n{Colors.BOLD}📊 RÉSUMÉ FINAL{Colors.END}")
    print("=" * 60)
    
    all_passed = True
    for check_name, passed in results:
        if passed:
            print_status(f"{check_name}: VALIDÉ", "success")
        else:
            print_status(f"{check_name}: ÉCHEC", "error")
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print_status("🎉 TOUS LES TESTS PASSÉS - PRÊT POUR DÉPLOIEMENT!", "success")
        print(f"{Colors.BLUE}Prochaines étapes:{Colors.END}")
        print("1. Pusher le code sur GitHub")
        print("2. Connecter le repo à Railway")
        print("3. Configurer les variables d'environnement sur Railway")
        print("4. Déployer et tester")
        return 0
    else:
        print_status("❌ CERTAINS TESTS ONT ÉCHOUÉ - CORRIGER AVANT DÉPLOIEMENT", "error")
        return 1

if __name__ == "__main__":
    sys.exit(main())
