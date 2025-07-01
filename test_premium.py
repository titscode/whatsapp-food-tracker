#!/usr/bin/env python3
"""
Script de test pour le système premium Stripe
"""

import requests
import json
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration
BASE_URL = "http://localhost:3000"
TEST_PHONE = "whatsapp:+41791234567"  # Numéro de test

def test_webhook_whatsapp(message, phone=TEST_PHONE):
    """Teste le webhook WhatsApp avec un message"""
    url = f"{BASE_URL}/whatsapp"
    
    data = {
        'From': phone,
        'Body': message,
        'To': 'whatsapp:+14155238886'
    }
    
    try:
        response = requests.post(url, data=data)
        print(f"📱 Message envoyé: '{message}'")
        print(f"📊 Status: {response.status_code}")
        print(f"📄 Response: {response.text[:200]}...")
        print("-" * 50)
        return response
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return None

def test_premium_command():
    """Teste la commande /premium"""
    print("🧪 Test de la commande /premium")
    response = test_webhook_whatsapp("/premium")
    return response

def test_message_counting():
    """Teste le comptage des messages"""
    print("🧪 Test du comptage des messages")
    
    # Envoyer plusieurs messages pour tester le comptage
    for i in range(1, 6):
        message = f"Test message #{i} - pomme"
        print(f"\n📨 Envoi du message {i}/5")
        test_webhook_whatsapp(message)

def test_dashboard():
    """Teste le dashboard"""
    print("🧪 Test du dashboard")
    
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"📊 Dashboard Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Dashboard accessible")
        else:
            print("❌ Dashboard inaccessible")
    except Exception as e:
        print(f"❌ Erreur dashboard: {e}")

def test_payment_pages():
    """Teste les pages de paiement"""
    print("🧪 Test des pages de paiement")
    
    # Test page de succès
    try:
        response = requests.get(f"{BASE_URL}/payment-success?session_id=test&phone={TEST_PHONE}")
        print(f"✅ Page succès: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur page succès: {e}")
    
    # Test page d'annulation
    try:
        response = requests.get(f"{BASE_URL}/payment-cancel?phone={TEST_PHONE}")
        print(f"✅ Page annulation: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur page annulation: {e}")

def main():
    """Fonction principale de test"""
    print("🚀 Début des tests du système premium Léa")
    print("=" * 60)
    
    # Vérifier que le serveur est en marche
    try:
        response = requests.get(BASE_URL, timeout=5)
        print(f"✅ Serveur accessible sur {BASE_URL}")
    except Exception as e:
        print(f"❌ Serveur inaccessible: {e}")
        return
    
    print("\n" + "=" * 60)
    
    # Tests
    test_dashboard()
    print("\n" + "=" * 60)
    
    test_premium_command()
    print("\n" + "=" * 60)
    
    test_message_counting()
    print("\n" + "=" * 60)
    
    test_payment_pages()
    print("\n" + "=" * 60)
    
    print("🎉 Tests terminés !")
    print("\n💡 Pour tester Stripe en mode réel:")
    print("1. Configurez STRIPE_SECRET_KEY dans Railway")
    print("2. Envoyez '/premium' via WhatsApp")
    print("3. Testez le paiement avec une carte de test Stripe")

if __name__ == "__main__":
    main()
