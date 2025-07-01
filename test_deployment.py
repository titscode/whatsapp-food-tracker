#!/usr/bin/env python3
"""
Script pour tester si le déploiement premium est actif en production
"""

import requests
import time

BASE_URL = "https://web-production-eed0c.up.railway.app"
TEST_PHONE = "whatsapp:+41791234567"

def test_premium_commands():
    """Teste si les nouvelles commandes premium sont déployées"""
    print("🧪 Test du déploiement premium en production")
    print("=" * 50)
    
    commands_to_test = [
        ("/on30", "Commande test activation"),
        ("/off30", "Commande test désactivation"), 
        ("/premium", "Commande premium"),
        ("pomme", "Message normal")
    ]
    
    for command, description in commands_to_test:
        print(f"\n📨 Test: {description} - '{command}'")
        
        try:
            response = requests.post(f"{BASE_URL}/whatsapp", data={
                'From': TEST_PHONE,
                'Body': command,
                'To': 'whatsapp:+14155238886'
            }, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ Réponse OK (200)")
                if response.text:
                    print(f"📄 Contenu: {response.text[:100]}...")
            else:
                print(f"❌ Erreur: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Erreur réseau: {e}")
        
        time.sleep(1)  # Pause entre les tests
    
    print("\n" + "=" * 50)
    print("🎯 Si toutes les commandes retournent 200, le déploiement est OK")
    print("💡 Testez maintenant via WhatsApp avec votre vrai numéro !")

def test_dashboard():
    """Teste le dashboard"""
    print("\n🖥️ Test du dashboard")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=10)
        if response.status_code == 200:
            print("✅ Dashboard accessible")
            if "v3.0" in response.text:
                print("✅ Version v3.0 détectée")
            else:
                print("⚠️ Version non détectée dans le HTML")
        else:
            print(f"❌ Dashboard erreur: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur dashboard: {e}")

if __name__ == "__main__":
    test_dashboard()
    test_premium_commands()
    
    print(f"\n🔗 URLs de test:")
    print(f"Dashboard: {BASE_URL}/")
    print(f"Webhook: {BASE_URL}/whatsapp")
    print(f"SMS Inbox: {BASE_URL}/sms-inbox")
