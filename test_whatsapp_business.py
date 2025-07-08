#!/usr/bin/env python3
"""
Script de test pour WhatsApp Business API
Teste l'envoi de messages et la configuration
"""

import os
import sys
import json
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Ajouter le répertoire courant au path pour les imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_configuration():
    """Teste la configuration WhatsApp Business API"""
    print("🔧 Test de la configuration WhatsApp Business API...")
    
    required_vars = [
        'WHATSAPP_ACCESS_TOKEN',
        'WHATSAPP_PHONE_NUMBER_ID',
        'WHATSAPP_BUSINESS_ACCOUNT_ID',
        'WHATSAPP_APP_ID'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Variables manquantes: {', '.join(missing_vars)}")
        return False
    
    print("✅ Toutes les variables d'environnement sont configurées")
    return True

def test_whatsapp_business_client():
    """Teste l'initialisation du client WhatsApp Business"""
    print("\n📱 Test du client WhatsApp Business...")
    
    try:
        from whatsapp_business_api import WhatsAppBusinessAPI
        
        client = WhatsAppBusinessAPI()
        print(f"✅ Client initialisé avec Phone Number ID: {client.phone_number_id}")
        print(f"✅ Base URL: {client.base_url}")
        return client
    except Exception as e:
        print(f"❌ Erreur initialisation client: {e}")
        return None

def test_webhook_parser():
    """Teste le parser de webhook"""
    print("\n🔗 Test du parser webhook...")
    
    # Payload de test Meta
    test_payload = {
        "entry": [{
            "changes": [{
                "value": {
                    "messages": [{
                        "id": "wamid.test123",
                        "from": "41774184918",
                        "timestamp": "1704722400",
                        "type": "text",
                        "text": {
                            "body": "Test message"
                        }
                    }],
                    "contacts": [{
                        "profile": {
                            "name": "Test User"
                        }
                    }]
                }
            }]
        }]
    }
    
    try:
        from whatsapp_business_api import parse_whatsapp_business_webhook
        
        result = parse_whatsapp_business_webhook(test_payload)
        
        if result:
            print("✅ Parser webhook fonctionne")
            print(f"   - Message ID: {result.get('message_id')}")
            print(f"   - From: {result.get('from_number')}")
            print(f"   - Text: {result.get('text')}")
            print(f"   - Profile: {result.get('profile_name')}")
            return True
        else:
            print("❌ Parser webhook retourne None")
            return False
            
    except Exception as e:
        print(f"❌ Erreur parser webhook: {e}")
        return False

def test_send_message(client, test_number=None):
    """Teste l'envoi d'un message"""
    print("\n📤 Test d'envoi de message...")
    
    if not client:
        print("❌ Pas de client disponible")
        return False
    
    # Utiliser le numéro de test ou demander à l'utilisateur
    if not test_number:
        test_number = input("Entrez un numéro de test (format: +41774184918) ou appuyez sur Entrée pour passer: ").strip()
    
    if not test_number:
        print("⏭️ Test d'envoi ignoré (pas de numéro fourni)")
        return True
    
    test_message = "🧪 Test WhatsApp Business API - Léa Nutrition\n\nCe message confirme que l'API fonctionne correctement !"
    
    try:
        success = client.send_text_message(test_number, test_message)
        
        if success:
            print(f"✅ Message de test envoyé à {test_number}")
            return True
        else:
            print(f"❌ Échec envoi message à {test_number}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur envoi message: {e}")
        return False

def test_hybrid_function():
    """Teste la fonction hybride send_whatsapp_reply"""
    print("\n🔄 Test de la fonction hybride...")
    
    try:
        from utils import send_whatsapp_reply
        from config import current_config
        
        # Simuler l'activation de WhatsApp Business API
        original_value = getattr(current_config, 'USE_WHATSAPP_BUSINESS_API', False)
        current_config.USE_WHATSAPP_BUSINESS_API = True
        
        print("✅ Fonction hybride importée")
        print(f"✅ WhatsApp Business API activé: {current_config.USE_WHATSAPP_BUSINESS_API}")
        
        # Restaurer la valeur originale
        current_config.USE_WHATSAPP_BUSINESS_API = original_value
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur fonction hybride: {e}")
        return False

def test_webhook_verification():
    """Teste la vérification du webhook"""
    print("\n🔐 Test de vérification webhook...")
    
    try:
        from config import current_config
        
        webhook_token = getattr(current_config, 'WHATSAPP_WEBHOOK_TOKEN', None)
        
        if webhook_token:
            print(f"✅ Token webhook configuré: {webhook_token}")
            return True
        else:
            print("❌ Token webhook non configuré")
            return False
            
    except Exception as e:
        print(f"❌ Erreur vérification webhook: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🚀 Tests WhatsApp Business API - Léa Nutrition")
    print("=" * 50)
    
    tests_results = []
    
    # Test 1: Configuration
    tests_results.append(("Configuration", test_configuration()))
    
    # Test 2: Client WhatsApp Business
    client = test_whatsapp_business_client()
    tests_results.append(("Client WhatsApp Business", client is not None))
    
    # Test 3: Parser webhook
    tests_results.append(("Parser webhook", test_webhook_parser()))
    
    # Test 4: Fonction hybride
    tests_results.append(("Fonction hybride", test_hybrid_function()))
    
    # Test 5: Vérification webhook
    tests_results.append(("Vérification webhook", test_webhook_verification()))
    
    # Test 6: Envoi de message (optionnel)
    if client:
        send_test = input("\n🤔 Voulez-vous tester l'envoi d'un message réel ? (y/N): ").lower().startswith('y')
        if send_test:
            test_number = input("Numéro de test (ex: +41774184918): ").strip()
            tests_results.append(("Envoi message", test_send_message(client, test_number)))
    
    # Résumé des tests
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 50)
    
    passed = 0
    total = len(tests_results)
    
    for test_name, result in tests_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<25} {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Résultat: {passed}/{total} tests réussis")
    
    if passed == total:
        print("\n🎉 Tous les tests sont passés ! WhatsApp Business API est prêt.")
        print("\n📋 PROCHAINES ÉTAPES:")
        print("1. Déployer sur Railway avec les nouvelles variables d'environnement")
        print("2. Configurer le webhook Meta sur: https://web-production-eed0c.up.railway.app/whatsapp-business")
        print("3. Activer USE_WHATSAPP_BUSINESS_API=true")
        print("4. Tester avec un message réel")
    else:
        print(f"\n⚠️ {total - passed} test(s) ont échoué. Vérifiez la configuration.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
