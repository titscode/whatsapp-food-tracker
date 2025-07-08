"""
Politique de confidentialité pour Léa Nutrition
Version complète et conforme RGPD
"""

def get_privacy_policy_html():
    """Retourne le HTML complet de la politique de confidentialité"""
    return '''
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Politique de Confidentialité - Léa Nutrition</title>
        <style>
            body { 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
                line-height: 1.7; 
                margin: 0; 
                padding: 20px; 
                background: #f8f9fa; 
                color: #333;
                font-size: 16px;
            }
            .container { 
                max-width: 900px; 
                margin: 0 auto; 
                background: white; 
                padding: 50px; 
                border-radius: 10px; 
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            }
            h1 { 
                color: #2c3e50; 
                text-align: center; 
                margin-bottom: 10px;
                font-size: 2.2em;
                font-weight: 600;
            }
            .subtitle {
                text-align: center;
                color: #4CAF50;
                font-size: 1.2em;
                margin-bottom: 40px;
                font-weight: 500;
            }
            h2 { 
                color: #2c3e50; 
                border-bottom: 3px solid #4CAF50; 
                padding-bottom: 8px;
                margin-top: 40px;
                font-size: 1.4em;
                font-weight: 600;
            }
            h3 {
                color: #34495e;
                margin-top: 25px;
                font-size: 1.1em;
                font-weight: 600;
            }
            .last-updated { 
                text-align: center; 
                color: #666; 
                font-style: italic; 
                margin-bottom: 40px;
                background: #f8f9fa;
                padding: 15px;
                border-radius: 8px;
                border-left: 4px solid #4CAF50;
            }
            .contact-info { 
                background: #f8f9fa; 
                padding: 25px; 
                border-radius: 8px; 
                margin-top: 40px;
                border-left: 4px solid #4CAF50;
            }
            .important-notice {
                background: #fff3cd;
                border: 1px solid #ffeaa7;
                border-radius: 8px;
                padding: 20px;
                margin: 25px 0;
                border-left: 4px solid #fdcb6e;
            }
            .data-table {
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
                background: white;
            }
            .data-table th, .data-table td {
                border: 1px solid #ddd;
                padding: 12px;
                text-align: left;
            }
            .data-table th {
                background: #4CAF50;
                color: white;
                font-weight: 600;
            }
            .data-table tr:nth-child(even) {
                background: #f9f9f9;
            }
            ul, ol {
                padding-left: 25px;
            }
            li {
                margin-bottom: 8px;
            }
            .legal-section {
                background: #f8f9fa;
                padding: 20px;
                border-radius: 8px;
                margin: 20px 0;
                border-left: 4px solid #6c757d;
            }
            .gdpr-rights {
                background: #e3f2fd;
                padding: 20px;
                border-radius: 8px;
                margin: 20px 0;
                border-left: 4px solid #2196F3;
            }
            strong {
                color: #2c3e50;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Politique de Confidentialité</h1>
            <div class="subtitle">Léa Nutrition - Service de Coaching Nutritionnel Intelligent</div>
            
            <div class="last-updated">
                <strong>Dernière mise à jour :</strong> 8 janvier 2025<br>
                <strong>Version :</strong> 2.1<br>
                <strong>Entrée en vigueur :</strong> 8 janvier 2025
            </div>
            
            <div class="important-notice">
                <strong>⚠️ Information importante :</strong> Cette politique de confidentialité s'applique à tous les utilisateurs du service Léa Nutrition accessible via WhatsApp Business API. En utilisant notre service, vous acceptez les termes décrits dans cette politique.
            </div>
            
            <h2>1. Responsable du Traitement des Données</h2>
            <div class="legal-section">
                <p><strong>Entité responsable :</strong> Léa Nutrition</p>
                <p><strong>Type de service :</strong> Plateforme de coaching nutritionnel automatisé</p>
                <p><strong>Moyen de contact :</strong> WhatsApp Business API</p>
                <p><strong>Hébergement :</strong> Railway (États-Unis) - Conforme GDPR</p>
                <p><strong>Contact DPO :</strong> support@lea-nutrition.ch</p>
            </div>
            
            <h2>2. Données Personnelles Collectées</h2>
            <p>Nous collectons et traitons les catégories de données personnelles suivantes, strictement nécessaires au fonctionnement du service :</p>
            
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Catégorie de Données</th>
                        <th>Détails</th>
                        <th>Base Légale</th>
                        <th>Durée de Conservation</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>Données d'identification</strong></td>
                        <td>Numéro de téléphone WhatsApp, nom d'utilisateur (optionnel)</td>
                        <td>Exécution du contrat</td>
                        <td>Durée d'utilisation du service</td>
                    </tr>
                    <tr>
                        <td><strong>Données de communication</strong></td>
                        <td>Messages WhatsApp, historique des conversations</td>
                        <td>Exécution du contrat</td>
                        <td>30 jours maximum</td>
                    </tr>
                    <tr>
                        <td><strong>Données nutritionnelles</strong></td>
                        <td>Aliments consommés, calories, macronutriments, objectifs</td>
                        <td>Exécution du contrat</td>
                        <td>Durée d'utilisation du service</td>
                    </tr>
                    <tr>
                        <td><strong>Données de santé (optionnel)</strong></td>
                        <td>Allergies, intolérances, objectifs de poids</td>
                        <td>Consentement explicite</td>
                        <td>Durée d'utilisation du service</td>
                    </tr>
                    <tr>
                        <td><strong>Données techniques</strong></td>
                        <td>Logs de connexion, métadonnées des messages</td>
                        <td>Intérêt légitime</td>
                        <td>7 jours maximum</td>
                    </tr>
                    <tr>
                        <td><strong>Données de paiement</strong></td>
                        <td>Informations de transaction (via Stripe)</td>
                        <td>Exécution du contrat</td>
                        <td>7 ans (obligations légales)</td>
                    </tr>
                </tbody>
            </table>
            
            <h3>2.1 Données Sensibles</h3>
            <p>Conformément à l'article 9 du RGPD, nous pouvons traiter certaines données de santé (allergies, intolérances alimentaires) uniquement avec votre <strong>consentement explicite</strong>. Ces données sont chiffrées et stockées séparément.</p>
            
            <h3>2.2 Données Non Collectées</h3>
            <p>Nous ne collectons <strong>jamais</strong> :</p>
            <ul>
                <li>Données de géolocalisation précise</li>
                <li>Contacts de votre répertoire téléphonique</li>
                <li>Données biométriques</li>
                <li>Informations bancaires complètes (gérées par Stripe)</li>
                <li>Données de navigation web (pas de cookies)</li>
            </ul>
            
            <h2>3. Finalités du Traitement</h2>
            <p>Vos données personnelles sont traitées exclusivement pour les finalités suivantes :</p>
            
            <h3>3.1 Finalités Principales</h3>
            <ol>
                <li><strong>Fourniture du service de coaching nutritionnel :</strong>
                    <ul>
                        <li>Analyse nutritionnelle des aliments</li>
                        <li>Calcul des apports caloriques et macronutriments</li>
                        <li>Recommandations personnalisées</li>
                        <li>Suivi des objectifs nutritionnels</li>
                    </ul>
                </li>
                <li><strong>Communication avec l'utilisateur :</strong>
                    <ul>
                        <li>Réponses aux questions nutritionnelles</li>
                        <li>Envoi de conseils personnalisés</li>
                        <li>Support technique</li>
                    </ul>
                </li>
                <li><strong>Gestion du compte utilisateur :</strong>
                    <ul>
                        <li>Authentification et identification</li>
                        <li>Sauvegarde des préférences</li>
                        <li>Historique nutritionnel</li>
                    </ul>
                </li>
            </ol>
            
            <h3>3.2 Finalités Secondaires</h3>
            <ol>
                <li><strong>Amélioration du service :</strong> Analyse anonymisée des interactions pour optimiser les réponses</li>
                <li><strong>Sécurité :</strong> Détection de fraudes et protection contre les abus</li>
                <li><strong>Conformité légale :</strong> Respect des obligations légales et réglementaires</li>
            </ol>
            
            <h2>4. Base Légale du Traitement</h2>
            <div class="legal-section">
                <p>Conformément à l'article 6 du RGPD, nos traitements reposent sur les bases légales suivantes :</p>
                <ul>
                    <li><strong>Exécution d'un contrat (art. 6.1.b) :</strong> Fourniture du service de coaching nutritionnel</li>
                    <li><strong>Consentement (art. 6.1.a) :</strong> Traitement des données de santé sensibles</li>
                    <li><strong>Intérêt légitime (art. 6.1.f) :</strong> Amélioration du service, sécurité, prévention des fraudes</li>
                    <li><strong>Obligation légale (art. 6.1.c) :</strong> Conservation des données de facturation</li>
                </ul>
            </div>
            
            <h2>5. Partage et Transfert des Données</h2>
            
            <h3>5.1 Principe de Non-Partage</h3>
            <p>Vos données personnelles ne sont <strong>jamais vendues, louées ou partagées</strong> à des fins commerciales avec des tiers.</p>
            
            <h3>5.2 Sous-Traitants Autorisés</h3>
            <p>Nous faisons appel aux sous-traitants suivants, tous soumis à des accords de confidentialité stricts :</p>
            
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Sous-traitant</th>
                        <th>Service</th>
                        <th>Localisation</th>
                        <th>Garanties RGPD</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Meta (WhatsApp Business API)</td>
                        <td>Messagerie instantanée</td>
                        <td>UE/États-Unis</td>
                        <td>Clauses contractuelles types</td>
                    </tr>
                    <tr>
                        <td>Railway</td>
                        <td>Hébergement cloud</td>
                        <td>États-Unis</td>
                        <td>Certification SOC 2, clauses contractuelles types</td>
                    </tr>
                    <tr>
                        <td>Stripe</td>
                        <td>Traitement des paiements</td>
                        <td>UE/États-Unis</td>
                        <td>Certification PCI DSS, clauses contractuelles types</td>
                    </tr>
                </tbody>
            </table>
            
            <h3>5.3 Transferts Internationaux</h3>
            <p>Certaines données peuvent être transférées vers des pays tiers (États-Unis) dans le cadre de l'utilisation de services cloud. Ces transferts sont encadrés par :</p>
            <ul>
                <li>Clauses contractuelles types approuvées par la Commission européenne</li>
                <li>Certifications de sécurité (SOC 2, ISO 27001)</li>
                <li>Mesures de sécurité supplémentaires (chiffrement end-to-end)</li>
            </ul>
            
            <h2>6. Sécurité et Protection des Données</h2>
            
            <h3>6.1 Mesures Techniques</h3>
            <ul>
                <li><strong>Chiffrement :</strong> Toutes les communications sont chiffrées en transit (TLS 1.3) et au repos (AES-256)</li>
                <li><strong>Authentification :</strong> Accès sécurisé par numéro de téléphone vérifié</li>
                <li><strong>Isolation :</strong> Données utilisateur isolées dans des environnements séparés</li>
                <li><strong>Sauvegarde :</strong> Sauvegardes chiffrées quotidiennes avec rétention limitée</li>
                <li><strong>Monitoring :</strong> Surveillance 24/7 des accès et détection d'anomalies</li>
            </ul>
            
            <h3>6.2 Mesures Organisationnelles</h3>
            <ul>
                <li><strong>Accès restreint :</strong> Principe du moindre privilège, accès sur base du besoin de savoir</li>
                <li><strong>Formation :</strong> Sensibilisation régulière du personnel à la protection des données</li>
                <li><strong>Audit :</strong> Audits de sécurité réguliers et tests de pénétration</li>
                <li><strong>Incident response :</strong> Procédures de réponse aux incidents de sécurité</li>
            </ul>
            
            <h3>6.3 Notification de Violation</h3>
            <p>En cas de violation de données personnelles susceptible d'engendrer un risque élevé pour vos droits et libertés, nous vous en informerons dans les <strong>72 heures</strong> suivant la découverte de l'incident.</p>
            
            <h2>7. Conservation des Données</h2>
            
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Type de Données</th>
                        <th>Durée de Conservation</th>
                        <th>Justification</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Données nutritionnelles actives</td>
                        <td>Durée d'utilisation du service</td>
                        <td>Nécessaire au fonctionnement du service</td>
                    </tr>
                    <tr>
                        <td>Historique des messages</td>
                        <td>30 jours maximum</td>
                        <td>Support technique et amélioration du service</td>
                    </tr>
                    <tr>
                        <td>Logs techniques</td>
                        <td>7 jours maximum</td>
                        <td>Sécurité et débogage</td>
                    </tr>
                    <tr>
                        <td>Données de facturation</td>
                        <td>7 ans</td>
                        <td>Obligations légales comptables</td>
                    </tr>
                    <tr>
                        <td>Données après suppression du compte</td>
                        <td>30 jours maximum</td>
                        <td>Sauvegardes de sécurité</td>
                    </tr>
                </tbody>
            </table>
            
            <h3>7.1 Suppression Automatique</h3>
            <p>Un système automatisé supprime les données expirées selon les durées définies ci-dessus. Les données supprimées sont irrécupérables.</p>
            
            <h2>8. Vos Droits (RGPD)</h2>
            
            <div class="gdpr-rights">
                <p>Conformément au Règlement Général sur la Protection des Données (RGPD), vous disposez des droits suivants :</p>
                
                <h3>8.1 Droit d'Accès (Art. 15 RGPD)</h3>
                <p><strong>Comment l'exercer :</strong> Tapez <code>/export</code> dans votre conversation avec Léa</p>
                <p><strong>Délai de réponse :</strong> 1 mois maximum</p>
                <p><strong>Contenu :</strong> Copie de toutes vos données personnelles et informations sur leur traitement</p>
                
                <h3>8.2 Droit de Rectification (Art. 16 RGPD)</h3>
                <p><strong>Comment l'exercer :</strong> Tapez <code>/profil</code> pour modifier vos informations</p>
                <p><strong>Délai de réponse :</strong> Immédiat pour les données de profil, 1 mois pour les autres</p>
                
                <h3>8.3 Droit à l'Effacement (Art. 17 RGPD)</h3>
                <p><strong>Comment l'exercer :</strong> Tapez <code>/delete</code> pour supprimer définitivement votre compte</p>
                <p><strong>Délai de réponse :</strong> Immédiat, suppression complète sous 30 jours</p>
                <p><strong>Exceptions :</strong> Données de facturation conservées 7 ans (obligation légale)</p>
                
                <h3>8.4 Droit à la Portabilité (Art. 20 RGPD)</h3>
                <p><strong>Comment l'exercer :</strong> Tapez <code>/export-json</code> pour recevoir vos données au format JSON</p>
                <p><strong>Contenu :</strong> Données nutritionnelles, préférences, historique dans un format structuré</p>
                
                <h3>8.5 Droit d'Opposition (Art. 21 RGPD)</h3>
                <p><strong>Comment l'exercer :</strong> Contactez-nous via <code>/aide</code></p>
                <p><strong>Motifs :</strong> Situation particulière, prospection commerciale</p>
                
                <h3>8.6 Droit à la Limitation (Art. 18 RGPD)</h3>
                <p><strong>Comment l'exercer :</strong> Contactez-nous via <code>/aide</code></p>
                <p><strong>Effet :</strong> Gel temporaire du traitement de vos données</p>
                
                <h3>8.7 Droit de Retrait du Consentement</h3>
                <p><strong>Comment l'exercer :</strong> Tapez <code>/retrait-consentement</code></p>
                <p><strong>Effet :</strong> Arrêt du traitement des données de santé sensibles</p>
            </div>
            
            <h2>9. Cookies et Technologies de Suivi</h2>
            <div class="important-notice">
                <p><strong>Léa Nutrition n'utilise AUCUN cookie, pixel de suivi, ou technologie de tracking.</strong></p>
                <p>Notre service fonctionne exclusivement via WhatsApp Business API sans interface web nécessitant des cookies.</p>
            </div>
            
            <h2>10. Mineurs et Protection de l'Enfance</h2>
            <p>Notre service n'est pas destiné aux mineurs de moins de 16 ans. Si nous découvrons qu'un mineur a fourni des données personnelles, nous les supprimerons immédiatement.</p>
            <p>Pour les mineurs de 16-18 ans, le consentement parental est requis pour le traitement des données de santé.</p>
            
            <h2>11. Modifications de la Politique</h2>
            <p>Cette politique peut être modifiée pour refléter :</p>
            <ul>
                <li>Évolutions réglementaires</li>
                <li>Nouvelles fonctionnalités du service</li>
                <li>Amélioration de la protection des données</li>
            </ul>
            
            <p><strong>Notification des modifications :</strong></p>
            <ul>
                <li>Modifications mineures : Notification via WhatsApp</li>
                <li>Modifications substantielles : Notification 30 jours à l'avance avec demande de nouveau consentement si nécessaire</li>
            </ul>
            
            <h2>12. Autorité de Contrôle et Recours</h2>
            <div class="legal-section">
                <p>Si vous estimez que vos droits ne sont pas respectés, vous pouvez :</p>
                <ul>
                    <li><strong>Nous contacter directement :</strong> support@lea-nutrition.ch</li>
                    <li><strong>Saisir l'autorité de contrôle compétente :</strong>
                        <ul>
                            <li>France : CNIL (Commission Nationale de l'Informatique et des Libertés)</li>
                            <li>Suisse : PFPDT (Préposé fédéral à la protection des données et à la transparence)</li>
                            <li>UE : Autorité de protection des données de votre pays de résidence</li>
                        </ul>
                    </li>
                    <li><strong>Exercer un recours judiciaire</strong> devant les tribunaux compétents</li>
                </ul>
            </div>
            
            <h2>13. Dispositions Finales</h2>
            
            <h3>13.1 Droit Applicable</h3>
            <p>Cette politique de confidentialité est régie par :</p>
            <ul>
                <li>Le Règlement Général sur la Protection des Données (RGPD) - UE 2016/679</li>
                <li>La Loi fédérale sur la protection des données (LPD) - Suisse</li>
                <li>Les lois nationales applicables selon votre lieu de résidence</li>
            </ul>
            
            <h3>13.2 Langue</h3>
            <p>Cette politique est rédigée en français. En cas de traduction, la version française fait foi.</p>
            
            <h3>13.3 Validité</h3>
            <p>Si une disposition de cette politique est déclarée invalide, les autres dispositions restent en vigueur.</p>
            
            <h2>14. Contact et Support</h2>
            <div class="contact-info">
                <p><strong>Pour toute question concernant cette politique de confidentialité :</strong></p>
                
                <h3>📱 Support via WhatsApp</h3>
                <ul>
                    <li>Tapez <code>/aide</code> dans votre conversation avec Léa</li>
                    <li>Tapez <code>/privacy</code> pour des questions spécifiques sur vos données</li>
                    <li>Tapez <code>/contact</code> pour parler à un humain</li>
                </ul>
                
                <h3>📧 Contact Email</h3>
                <ul>
                    <li><strong>Support général :</strong> support@lea-nutrition.ch</li>
                    <li><strong>Protection des données :</strong> dpo@lea-nutrition.ch</li>
                    <li><strong>Urgences sécurité :</strong> security@lea-nutrition.ch</li>
                </ul>
                
                <h3>🌐 Ressources en Ligne</h3>
                <ul>
                    <li><strong>Site web :</strong> https://web-production-eed0c.up.railway.app</li>
                    <li><strong>Documentation :</strong> https://web-production-eed0c.up.railway.app/privacy-policy</li>
                    <li><strong>Statut du service :</strong> https://web-production-eed0c.up.railway.app</li>
                </ul>
                
                <p><strong>⏱️ Délais de réponse :</strong></p>
                <ul>
                    <li>Questions générales : 48h maximum</li>
                    <li>Demandes RGPD : 1 mois maximum</li>
                    <li>Incidents de sécurité : 24h maximum</li>
                </ul>
            </div>
            
            <div style="text-align: center; margin-top: 50px; padding: 30px; background: #f8f9fa; border-radius: 10px;">
                <h3 style="color: #4CAF50; margin-bottom: 20px;">🥗 Léa Nutrition</h3>
                <p style="font-size: 1.1em; margin-bottom: 15px;"><strong>Votre Coach Nutrition Intelligent et Respectueux de votre Vie Privée</strong></p>
                <p style="color: #666; margin-bottom: 10px;">Développé avec ❤️ pour votre bien-être et votre sécurité</p>
                <p style="color: #666; font-size: 0.9em;">© 2025 Léa Nutrition - Tous droits réservés</p>
                <p style="color: #666; font-size: 0.8em; margin-top: 20px;">
                    Cette politique de confidentialité a été rédigée avec soin pour garantir la transparence<br>
                    et le respect de vos droits fondamentaux à la protection des données personnelles.
                </p>
            </div>
        </div>
    </body>
    </html>
    '''
