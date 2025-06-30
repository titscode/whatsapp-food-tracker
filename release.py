#!/usr/bin/env python3
"""
Script de release automatique pour Léa Chatbot Nutrition
Usage: python release.py 0.91
"""

import sys
import subprocess
import os
from datetime import datetime

def run_command(cmd):
    """Exécute une commande et retourne le résultat"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Erreur: {result.stderr}")
            return False
        print(f"✅ {cmd}")
        return True
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def update_version_file(version):
    """Met à jour le fichier VERSION"""
    with open('VERSION', 'w') as f:
        f.write(f"{version}\n")
    print(f"✅ VERSION mise à jour: {version}")

def update_changelog(version):
    """Ajoute une nouvelle entrée dans le CHANGELOG"""
    date = datetime.now().strftime("%d/%m/%Y")
    
    # Lire le changelog existant
    with open('CHANGELOG.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Nouvelle entrée
    new_entry = f"""## 🚀 v{version} - Nouvelle Version ({date})

### ✨ **Nouvelles Fonctionnalités**
- À compléter...

### 🔧 **Améliorations**
- À compléter...

### 🐛 **Corrections**
- À compléter...

---

"""
    
    # Insérer après le titre
    lines = content.split('\n')
    insert_index = 2  # Après le titre et la ligne vide
    lines.insert(insert_index, new_entry)
    
    # Réécrire le fichier
    with open('CHANGELOG.md', 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f"✅ CHANGELOG mis à jour pour v{version}")

def create_release(version):
    """Crée une nouvelle release"""
    print(f"🚀 Création de la release v{version}")
    
    # 1. Mettre à jour les fichiers
    update_version_file(version)
    update_changelog(version)
    
    # 2. Git add
    if not run_command("git add ."):
        return False
    
    # 3. Git commit
    commit_msg = f"Release: Léa v{version} - Nouvelle version"
    if not run_command(f'git commit -m "{commit_msg}"'):
        return False
    
    # 4. Créer le tag
    tag_msg = f"Léa v{version} - Release automatique"
    if not run_command(f'git tag -a v{version} -m "{tag_msg}"'):
        return False
    
    # 5. Push tout
    if not run_command("git push"):
        return False
    
    if not run_command(f"git push origin v{version}"):
        return False
    
    print(f"🎉 Release v{version} créée avec succès !")
    print(f"📱 Test: https://web-production-eed0c.up.railway.app/whatsapp")
    return True

def main():
    if len(sys.argv) != 2:
        print("Usage: python release.py <version>")
        print("Exemple: python release.py 0.91")
        sys.exit(1)
    
    version = sys.argv[1]
    
    # Validation du format de version
    if not version.replace('.', '').isdigit():
        print("❌ Format de version invalide. Utilisez X.XX (ex: 0.91)")
        sys.exit(1)
    
    print(f"🔄 Préparation de la release v{version}...")
    
    # Vérifier qu'on est sur main
    result = subprocess.run("git branch --show-current", shell=True, capture_output=True, text=True)
    if result.stdout.strip() != "main":
        print("❌ Vous devez être sur la branche main")
        sys.exit(1)
    
    # Vérifier qu'il n'y a pas de changements non commitées
    result = subprocess.run("git status --porcelain", shell=True, capture_output=True, text=True)
    if result.stdout.strip():
        print("❌ Il y a des changements non commitées. Commitez d'abord.")
        sys.exit(1)
    
    # Créer la release
    if create_release(version):
        print(f"✅ Release v{version} terminée !")
    else:
        print(f"❌ Échec de la release v{version}")
        sys.exit(1)

if __name__ == "__main__":
    main()
