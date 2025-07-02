#!/usr/bin/env python3
"""
Script de déploiement Railway pour Léa Bot WhatsApp Nutrition
"""

import os
import subprocess
import sys

def check_requirements():
    """Vérifie que tous les fichiers requis sont présents"""
    required_files = [
        'app_production.py',
        'requirements.txt',
        'railway.json',
        'config.py',
        'database.py',
        'utils.py',
        'nutrition_improved.py',
        'nutrition_chat_improved.py',
        'simple_onboarding.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Fichiers manquants: {', '.join(missing_files)}")
        return False
    
    print("✅ Tous les fichiers requis sont présents")
    return True

def main():
    """Fonction principale"""
    print("🤖 Léa Bot - Prêt pour Railway")
    print("=" * 50)
    
    if check_requirements():
        print("✅ Tous les fichiers sont prêts pour le déploiement Railway")
        print("🚀 Push sur GitHub pour déploiement automatique")
    else:
        print("❌ Fichiers manquants")

if __name__ == "__main__":
    main()
