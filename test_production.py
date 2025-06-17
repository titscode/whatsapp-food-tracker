#!/usr/bin/env python3
"""
🧪 Tests Post-Déploiement - Léa Bot WhatsApp
Script automatisé pour tester le bot en production
"""

import requests
import json
import time
import sys
from urllib.parse import urljoin

# Couleurs pour l'affichage
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_test(test_name, status="info", details=""):
    """Affiche le résultat d'un test"""
    if status == "pass":
        print(f"{Colors.GREEN}✅ {test_name}{Colors.END}")
    elif status == "fail":
        print(f"{Colors.RED}❌ {test_name}{Colors.END}")
    elif status == "warning":
        print(f"{Colors.YELLOW}⚠️  {test_name}{Colors.END}")
    else:
        print(f"{Colors.BLUE}🧪 {test_name}{Colors.END}")
    
    if details:
        print(f"   {details}")

def test_dashboard_accessible(base_url):
    """Test 1: Dashboard accessible"""
    try:
        response = requests.get(base_url, timeout=10)
        if response.status_code == 200 and "Léa - Dashboard" in response.text:
            print_test("Dashboard accessible", "pass", f"Status: {response.status_code}")
            return True
        else:
            print_test("Dashboard accessible", "fail", f"Status: {response.status_code}")
            return False
    except Exception as e:
        print_test("Dashboard accessible", "fail", f"Erreur: {e}")
        return False

def test_api_stats(base_url):
    """Test 2: API Stats fonctionne"""
    try:
        url = urljoin(base_url, "/api/stats")
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if 'dau' in data and 'wau' in data:
                print_test("API Stats", "pass", f"DAU: {data.get('dau', 0)}, WAU: {data.get('wau', 0)}")
                return True
            else:
                print_test("API Stats", "fail", "Format JSON invalide")
                return False
        else:
            print_test("API Stats", "fail", f"Status: {response.status_code}")
            return False
    except Exception as e:
        print_test("API Stats", "fail", f"Erreur: {e}")
        return False

def test_api_dau_history(base_url):
    """Test 3: API DAU History fonctionne"""
    try:
        url = urljoin(base_url, "/api/dau-history")
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                print_test("API DAU History", "pass", f"{len(data)} jours d'historique")
                return True
            else:
                print_test("API DAU History", "fail", "Données vides ou format invalide")
                return False
        else:
            print_test("API DAU History", "fail", f"Status: {response.status_code}")
            return False
    except Exception as e:
        print_test("API DAU History", "fail", f"Erreur: {e}")
        return False

def test_webhook_active(base_url):
    """Test 4: Webhook WhatsApp actif"""
    try:
        url = urljoin(base_url, "/whatsapp")
        response = requests.get(url, timeout=10)
        if response.status_code == 200 and "Webhook WhatsApp actif" in response.text:
            print_test("Webhook WhatsApp", "pass", "Endpoint répond correctement")
            return True
        else:
            print_test("Webhook WhatsApp", "fail", f"Status: {response.status_code}")
            return False
    except Exception as e:
        print_test("Webhook WhatsApp", "fail", f"Erreur: {e}")
        return False

def test_response_time(base_url):
    """Test 5: Temps de réponse acceptable"""
    try:
        start_time = time.time()
        response = requests.get(base_url, timeout=10)
        response_time = time.time() - start_time
        
        if response.status_code == 200:
            if response_time < 2.0:
                print_test("Temps de réponse", "pass", f"{response_time:.2f}s (< 2s)")
                return True
            elif response_time < 5.0:
                print_test("Temps de réponse", "warning", f"{response_time:.2f}s (acceptable)")
                return True
            else:
                print_test("Temps de réponse", "fail", f"{response_time:.2f}s (trop lent)")
                return False
        else:
            print_test("Temps de réponse", "fail", f"Status: {response.status_code}")
            return False
    except Exception as e:
        print_test("Temps de réponse", "fail", f"Erreur: {e}")
        return False

def test_ssl_certificate(base_url):
    """Test 6: Certificat SSL valide"""
    try:
        if base_url.startswith('https://'):
            response = requests.get(base_url, timeout=10, verify=True)
            if response.status_code == 200:
                print_test("Certificat SSL", "pass", "HTTPS fonctionnel")
                return True
            else:
                print_test("Certificat SSL", "fail", f"Status: {response.status_code}")
                return False
        else:
            print_test("Certificat SSL", "warning", "URL non HTTPS")
            return True
    except requests.exceptions.SSLError:
        print_test("Certificat SSL", "fail", "Certificat SSL invalide")
        return False
    except Exception as e:
        print_test("Certificat SSL", "fail", f"Erreur: {e}")
        return False

def test_error_handling(base_url):
    """Test 7: Gestion d'erreurs"""
    try:
        # Test endpoint inexistant
        url = urljoin(base_url, "/endpoint-inexistant")
        response = requests.get(url, timeout=10)
        if response.status_code == 404:
            print_test("Gestion d'erreurs 404", "pass", "Erreur 404 correctement gérée")
            return True
        else:
            print_test("Gestion d'erreurs 404", "warning", f"Status: {response.status_code}")
            return True
    except Exception as e:
        print_test("Gestion d'erreurs", "fail", f"Erreur: {e}")
        return False

def test_webhook_post_method(base_url):
    """Test 8: Webhook accepte POST"""
    try:
        url = urljoin(base_url, "/whatsapp")
        # Simuler un POST vide (sans données Twilio)
        response = requests.post(url, data={}, timeout=10)
        # Le webhook devrait répondre même avec des données vides
        if response.status_code in [200, 400]:  # 200 ou 400 acceptable
            print_test("Webhook POST", "pass", f"Accepte méthode POST (Status: {response.status_code})")
            return True
        else:
            print_test("Webhook POST", "fail", f"Status: {response.status_code}")
            return False
    except Exception as e:
        print_test("Webhook POST", "fail", f"Erreur: {e}")
        return False

def run_production_tests(base_url):
    """Lance tous les tests de production"""
    print(f"{Colors.BOLD}🧪 TESTS POST-DÉPLOIEMENT - LÉA BOT WHATSAPP{Colors.END}")
    print(f"URL testée: {base_url}")
    print("=" * 60)
    
    tests = [
        ("Dashboard accessible", test_dashboard_accessible),
        ("API Stats", test_api_stats),
        ("API DAU History", test_api_dau_history),
        ("Webhook WhatsApp", test_webhook_active),
        ("Temps de réponse", test_response_time),
        ("Certificat SSL", test_ssl_certificate),
        ("Gestion d'erreurs", test_error_handling),
        ("Webhook POST", test_webhook_post_method)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func(base_url)
            results.append((test_name, result))
        except Exception as e:
            print_test(f"{test_name}", "fail", f"Exception: {e}")
            results.append((test_name, False))
        
        time.sleep(0.5)  # Pause entre tests
    
    # Résumé
    print(f"\n{Colors.BOLD}📊 RÉSUMÉ DES TESTS{Colors.END}")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        if result:
            print_test(f"{test_name}", "pass")
            passed += 1
        else:
            print_test(f"{test_name}", "fail")
    
    print(f"\n{Colors.BOLD}Résultat: {passed}/{total} tests réussis{Colors.END}")
    
    if passed == total:
        print_test("🎉 TOUS LES TESTS PASSÉS - PRODUCTION OPÉRATIONNELLE!", "pass")
        print(f"\n{Colors.BLUE}Tests manuels WhatsApp recommandés:{Colors.END}")
        print("1. Envoyer 'join live-cold' au +1 415 523 8886")
        print("2. Tester '50g de poulet'")
        print("3. Tester 'Salut Léa !'")
        print("4. Envoyer une photo de repas")
        print("5. Tester '/aide'")
        return 0
    elif passed >= total * 0.8:  # 80% de réussite
        print_test("⚠️  TESTS MAJORITAIREMENT RÉUSSIS - VÉRIFIER ÉCHECS", "warning")
        return 1
    else:
        print_test("❌ PLUSIEURS TESTS ÉCHOUÉS - CORRIGER AVANT UTILISATION", "fail")
        return 2

def main():
    """Fonction principale"""
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <URL_PRODUCTION>")
        print(f"Exemple: {sys.argv[0]} https://your-app-name.railway.app")
        sys.exit(1)
    
    base_url = sys.argv[1].rstrip('/')
    
    if not base_url.startswith(('http://', 'https://')):
        print("❌ URL doit commencer par http:// ou https://")
        sys.exit(1)
    
    return run_production_tests(base_url)

if __name__ == "__main__":
    sys.exit(main())
