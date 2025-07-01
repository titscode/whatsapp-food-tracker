#!/usr/bin/env python3
"""
Test de la limite de 30 messages et du système premium
"""

import requests
import time

BASE_URL = "http://localhost:3000"
TEST_PHONE = "whatsapp:+41791234567"

def send_message(message):
    """Envoie un message via le webhook"""
    data = {
        'From': TEST_PHONE,
        'Body': message,
        'To': 'whatsapp:+14155238886'
    }
    
    try:
        response = requests.post(f"{BASE_URL}/whatsapp", data=data)
        return response.status_code == 200
    except:
        return False

def test_message_limit():
    """Teste la limite de 30 messages"""
    print("🧪 Test de la limite de 30 messages")
    print("=" * 50)
    
    # Envoyer 32 messages pour dépasser la limite
    for i in range(1, 33):
        message = f"Test message #{i} - banane"
        success = send_message(message)
        
        if success:
            print(f"✅ Message {i}/32 envoyé")
        else:
            print(f"❌ Message {i}/32 échoué")
        
        # Petite pause pour éviter le rate limiting
        time.sleep(0.5)
        
        # Messages spéciaux à certains moments
        if i == 30:
            print("\n🔔 Message 30 - Limite atteinte normalement")
        elif i == 31:
            print("\n🚫 Message 31 - Devrait être bloqué")
        elif i == 32:
            print("\n🚫 Message 32 - Devrait être bloqué")
    
    print("\n" + "=" * 50)
    print("🧪 Test de la commande /premium après limite")
    
    # Tester la commande premium
    success = send_message("/premium")
    if success:
        print("✅ Commande /premium envoyée")
    else:
        print("❌ Commande /premium échouée")

if __name__ == "__main__":
    print("🚀 Test du système de limitation premium")
    print("📱 Numéro de test:", TEST_PHONE)
    print("🎯 Objectif: Tester la limite de 30 messages")
    print()
    
    test_message_limit()
    
    print("\n🎉 Test terminé !")
    print("\n💡 Vérifiez les logs du serveur pour voir:")
    print("- Le comptage des messages")
    print("- Le blocage après 30 messages")
    print("- La génération du lien Stripe")
