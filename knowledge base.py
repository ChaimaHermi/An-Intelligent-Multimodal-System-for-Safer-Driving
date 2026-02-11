# ============================================================================
# BASE DE CONNAISSANCES COMPLÈTE - CODE ROUTIER TUNISIEN 2024
# ============================================================================

SAFETY_DOCS = {
    "fatigue": {
        "title": "FATIGUE ET SOMMEIL AU VOLANT",
        "risk": "🔴 CRITIQUE",
        "content": """
STATISTIQUES TUNISIENNES :
• 28% des accidents mortels liés à la fatigue (ONSR Tunisie 2023)
• 72% des conducteurs tunisiens déclarent conduire fatigués (Enquête ANSV 2023)
• Risque x6 entre 2h et 5h du matin

LOI TUNISIENNE (Article 85 du Code de la Route) :
• Temps de conduite continu maximal : 4h30
• Pause obligatoire : 45 minutes minimum après 4h30
• Durée quotidienne max : 9h de conduite (Article 86)

SIGNES D'ALERTE CRITIQUES :
• Bâillements répétés (plus de 3 en 5 minutes)
• Difficulté à maintenir la vitesse constante
• Erreurs de trajectoire fréquentes
• Perception réduite des panneaux
• Oubli des derniers kilomètres parcourus

PROTOCOLE OBLIGATOIRE :
1. ARRÊT IMMÉDIAT dans aire aménagée (interdit sur bande d'arrêt d'urgence)
2. Sieste de 15-25 minutes
3. Étirements et marche de 5 minutes
4. Hydratation (eau, pas de café seul)
5. Attendre 10 minutes après réveil avant reprise

SANCTIONS (Article 144) :
• Conduite en état de fatigue manifeste : 100 DT + 4 points
• Si accident causé : 200-500 DT + 6 points + suspension permis

RECOMMANDATIONS ONSR :
• Dormir 7-8h minimum avant long trajet
• Éviter conduite entre 13h-15h et 2h-5h
• Pauses préventives toutes les 2h
• Voyager accompagné si possible
""",
        "keywords": ["fatigué", "fatigue", "sommeil", "dormir", "somnolence", "bâillement", 
                     "yeux lourds", "sieste", "repos", "pause obligatoire", "micro-sommeil",
                     "épuisement", "sommeil au volant"],
        "reference": "Code de la Route Tunisien - Articles 85-86, ONSR 2023"
    },
    
    "vitesse": {
        "title": "LIMITATIONS DE VITESSE EN TUNISIE",
        "risk": "🟠 ÉLEVÉ",
        "content": """
LIMITES LÉGALES 2024 (Article 45) :

ZONES URBANISÉES (agglomération) :
• Rue à sens unique : 50 km/h
• Rue résidentielle : 30 km/h
• Aux abords écoles : 30 km/h signalé
• Zones piétonnes : 20 km/h

HORS AGGLOMÉRATION :
• Routes nationales : 90 km/h
• Routes secondaires : 70 km/h
• Chemins agricoles : 50 km/h

AUTOROUTES (Articles 46-47) :
• Voies principales : 110 km/h maximum
• Voies d'accès : 70 km/h
• Bande d'arrêt urgence : 0 km/h (arrêt interdit)
• Période d'essai nouveau conducteur (2 ans) : 90 km/h max

CONDITIONS PARTICULIÈRES :
• Pluie/Brouillard : -20 km/h sur toutes limites
• Visibilité < 50m : maximum 50 km/h
• Chaussée verglacée : maximum 30 km/h
• Travaux : limitation signalée (généralement 50 km/h)

DISTANCES OFFICIELLES (ONSR) :
• Distance perception-réaction : 1 seconde
• Distance freinage à 50 km/h : 14 mètres (sec) / 28 mètres (mouillé)
• Distance freinage à 90 km/h : 45 mètres (sec) / 90 mètres (mouillé)
• Distance freinage à 110 km/h : 67 mètres (sec) / 134 mètres (mouillé)

SANCTIONS (Article 144) :
• Excès ≤ 20 km/h : 30 DT + 1 point
• Excès 21-40 km/h : 100 DT + 3 points
• Excès 41-60 km/h : 200 DT + 4 points + stage obligatoire
• Excès > 60 km/h : 500 DT + 6 points + suspension 3 mois
• Récidive dans l'année : suspension 6 mois minimum

RADARS AUTOMATIQUES (Article 145 bis) :
• Tolérance technique : 5 km/h jusqu'à 100 km/h, 5% au-delà
• Délai paiement amende : 30 jours
• Majoration après délai : +50%
""",
        "keywords": ["vitesse", "limite", "km/h", "radar", "excès", "ralentir", 
                     "freinage", "distance sécurité", "110", "90", "50", "autoroute",
                     "amende", "points"],
        "reference": "Code de la Route Tunisien - Articles 45-47, 144-145"
    },
    
    "conditions": {
        "title": "CONDUITE PAR CONDITIONS DIFFICILES",
        "risk": "🟠 ÉLEVÉ",
        "content": """
PLUIE (Article 48) :
• Allumage feux obligatoire dès pluie
• Réduction vitesse minimum 20 km/h
• Distance sécurité doublée
• Aquaplaning dès 4mm d'eau à 80 km/h

PROTOCOLE AQUAPLANING :
1. NE JAMAIS freiner brusquement
2. Décélérer progressivement
3. Maintenir trajectoire sans mouvement brusque
4. Attendre reprise adhérence
5. Redémarrer doucement

BROUILLARD (Article 49) :
• Feux antibrouillard avant autorisés si visibilité < 100m
• Feux antibrouillard arrière obligatoires si visibilité < 50m
• Vitesse max = visibilité en mètres (ex: 50m → 50 km/h)
• Distance sécurité = temps 4 secondes minimum

VENT VIOLENT/SIROCO :
• Tenir fermement volant à 2 mains
• Réduire vitesse significativement
• Distance latérale augmentée avec poids lourds
• Attention aux objets projetés

NUIT (Article 50) :
• Allumage feux : 30 min après coucher jusqu'à 30 min avant lever
• Feux de route interdits en ville et face à véhicules
• Éblouissement : regarder bord droit chaussée
• Vitesse adaptée à portée feux

LUMINOSITÉ RÉDUITE :
• Crépuscule : allumer feux
• Tunnels > 100m : feux obligatoires
• Aires non éclairées : feux même à l'arrêt
""",
        "keywords": ["pluie", "brouillard", "nuit", "vent", "sirocco", "aquaplaning",
                     "visibilité", "feux", "éblouissement", "météo", "intempéries"],
        "reference": "Code de la Route Tunisien - Articles 48-50"
    },
    
    "ceinture": {
        "title": "CEINTURE DE SÉCURITÉ ET ÉQUIPEMENTS",
        "risk": "🔴 CRITIQUE",
        "content": """
OBLIGATIONS LÉGALES (Article 54) :
• Conducteur : CEINTURE OBLIGATOIRE
• Passagers avant : CEINTURE OBLIGATOIRE
• Passagers arrière : CEINTURE OBLIGATOIRE si équipés
• Enfants < 10 ans : SIÈGE AUTO HOMOLOGUÉ

STATISTIQUES TUNISIENNES (ONSR 2023) :
• Taux port ceinture conducteur : 62% seulement
• Taux port ceinture passager avant : 35%
• Ceinture réduit risque mort de 45% à l'avant, 25% à l'arrière

SIÈGES ENFANTS (Article 55) :
• Groupe 0 (0-10kg) : siège dos à la route
• Groupe 1 (9-18kg) : siège harnais ou bouclier
• Groupe 2/3 (15-36kg) : rehausseur avec dossier
• Interdiction place avant avec airbag actif (sauf désactivation)

UTILISATION CORRECTE :
• Sangle diagonale sur épaule/clavicule
• Sangle ventrale sur bassin (pas abdomen)
• Tension correcte (maximum 5cm de jeu)
• Pas de vrillage des sangles

SANCTIONS (Article 144) :
• Conducteur non ceinturé : 30 DT + 1 point
• Passager non ceinturé : 20 DT par personne
• Enfant non attaché : 50 DT + 2 points
• Récidive : double amende

AIRBAGS :
• Complément à la ceinture, pas substitut
• Distance minimum 25cm entre poitrine et volant
• Jamais d'enfant dos à l'avant avec airbag
""",
        "keywords": ["ceinture", "attacher", "sangle", "siège enfant", "bébé", 
                     "rehausseur", "airbag", "sécurité passive", "harnais"],
        "reference": "Code de la Route Tunisien - Articles 54-55"
    },
    
    "telephone": {
        "title": "UTILISATION DU TÉLÉPHONE AU VOLANT",
        "risk": "🔴 CRITIQUE",
        "content": """
INTERDICTIONS ABSOLUES (Article 51) :
• Téléphone tenu en main pendant conduite
• Composition ou consultation messages
• Navigation manuelle sur écran
• Même à l'arrêt (feux, embouteillages)

AUTORISATIONS STRICTEMENT LIMITÉES :
• Kit mains-libres intégré au véhicule
• Système Bluetooth intégré
• Commandes vocales sans manipulation
• GPS fixé programmé avant démarrage

STATISTIQUES ALARMANTES :
• Téléphone main : risque accident x4
• SMS/WhatsApp : risque x23 (étude ONSR)
• 40% des jeunes conducteurs utilisent téléphone en conduisant
• 2 secondes d'inattention = 55m parcourus à 100 km/h

DÉTECTION ET SANCTIONS (Article 144) :
• Téléphone main en conduisant : 50 DT + 3 points
• Même infraction avec passager < 15 ans : 100 DT + 4 points
• En cas d'accident : responsabilité aggravée + suspension permis
• Récidive < 1 an : suspension 1 à 3 mois

PROTOCOLE D'URGENCE :
1. Trouver place de stationnement autorisée
2. Immobiliser complètement véhicule
3. Couper contact
4. Répondre à l'appel

RECOMMANDATIONS ONSR :
• Mode conduite sur smartphone
• Répondeur automatique avec message "En conduite"
• Passager désigné pour communications
• Arrêts programmés pour appels importants
""",
        "keywords": ["téléphone", "portable", "sms", "whatsapp", "message", "appel",
                     "kit mains-libres", "bluetooth", "déconcentration", "inattention"],
        "reference": "Code de la Route Tunisien - Article 51"
    },
    
    "alcool": {
        "title": "ALCOOL, DROGUES ET MÉDICAMENTS",
        "risk": "🔴 CRITIQUE",
        "content": """
TAUX LÉGAUX MAXIMAUX (Article 52) :
• Conducteurs : 0.2 gramme par litre de sang
• Conducteurs permis probatoire (<2 ans) : 0.0 g/L
• Professionnels (transport, bus, taxi) : 0.0 g/L
• Drogues illicites : tolérance ZÉRO

ÉQUIVALENCES ALCOOL :
• 1 verre bière (25cl) = 0.15 g/L
• 1 verre vin (10cl) = 0.10 g/L
• 1 verre spiritueux (3cl) = 0.10 g/L
• Délai élimination : 0.15 g/L par heure

EFFETS SUR LA CONDUITE (ONSR) :
• 0.2 g/L : réflexes diminués de 15%
• 0.5 g/L : champ visuel réduit de 25%
• 0.8 g/L : temps réaction +50%
• 1.0 g/L : risque accident x15

CONTRÔLES ET SANCTIONS (Article 144) :
• Refus dépistage : 200 DT + 6 points + suspension 6 mois
• 0.2-0.4 g/L : 100 DT + 4 points + suspension 1 mois
• 0.4-0.8 g/L : 200 DT + 6 points + suspension 3 mois
• > 0.8 g/L : 500 DT + retrait permis + tribunal
• Drogues positives : 1000 DT + retrait + tribunal

MÉDICAMENTS DANGEREUX :
• Pictogramme jaune : vigilance
• Pictogramme orange : consultation médecin
• Pictogramme rouge : conduite interdite
• Listes disponibles pharmacies

PROTOCOLE "ZÉRO RISQUE" :
• Capitaine de soirée désigné
• Transport alternatif organisé à l'avance
• Test d'auto-évaluation interdit comme preuve
• Dormir sur place si doute
""",
        "keywords": ["alcool", "éthylotest", "ivresse", "drogue", "cannabis", 
                     "médicament", "taux", "dépistage", "sobriété", "permis probatoire"],
        "reference": "Code de la Route Tunisien - Article 52"
    },
    
    "priorite": {
        "title": "RÈGLES DE PRIORITÉ ET CÉDÉS",
        "risk": "🟡 MOYEN",
        "content": """
HIÉRARCHIE DES RÈGLES (Article 32) :
1. Agents de circulation
2. Feux tricolores
3. Signaux routiers
4. Règles générales

PRIORITÉ À DROITE (Article 33) :
• Application en l'absence signalisation
• Abrogée par panneau "Cédez le passage" ou "Stop"
• Exception : véhicules sur voie prioritaire

CARREFOURS À SENS GIRATOIRE (Article 34) :
• Priorité aux véhicules déjà engagés
• Signalisation par panneaux spécifiques
• Clignotant droit pour sortir
• Respect marquage au sol

PASSAGE PIÉTONS (Article 35) :
• Priorité ABSOLUE aux piétons engagés
• Arrêt OBLIGATOIRE si piéton attend
• Sanction : 30 DT + 1 point
• Zone 30 : priorité systématique piétons

VÉHICULES D'URGENCE (Article 36) :
• Avertisseurs sonores ET lumineux actifs
• Obligation dégager voie immédiatement
• En cas d'impossibilité : serrer à droite
• Interdiction suivre à moins de 50m

SANCTIONS INFRACTIONS :
• Non-respect stop : 50 DT + 3 points
• Non-respect passage piéton : 30 DT + 1 point
• Refus priorité véhicule prioritaire : 100 DT + 4 points
• Circulation sens interdit : 30 DT + 1 point

CAS PARTICULIERS TUNISIENS :
• Ronds-points : attention aux variations locales
• Routes secondaires : priorité souvent mal signalée
• Agglomérations : vigilance enfants et animaux
""",
        "keywords": ["priorité", "cédez", "stop", "passage piéton", "rond-point",
                     "sens giratoire", "véhicule prioritaire", "feux", "agent"],
        "reference": "Code de la Route Tunisien - Articles 32-36"
    },
    
    "stationnement": {
        "title": "STATIONNEMENT ET ARRÊT",
        "risk": "🟡 MOYEN",
        "content": """
DÉFINITIONS (Article 39) :
• Arrêt : immobilisation < 5 minutes, conducteur présent
• Stationnement : immobilisation > 5 minutes ou conducteur absent

INTERDICTIONS ABSOLUES (Article 40) :
• Sur passage piéton et 5m avant
• Sur voies cyclables
• Devoir bouches incendie
• En double file
• En courbe ou sommet de côte
• Tunnel, pont, passage souterrain
• Bande d'arrêt urgence autoroute

STATIONNEMENT DANGEREUX (Article 41) :
• Visibilité réduite < 50m
• Voie étroite < 3m restants
• Pente > 5% sans cales
• Proximité écoles/hôpitaux (<30m)

ZONES RÉGLEMENTÉES (Article 42) :
• Zone bleue : disque ou paiement
• Zone jaune : livraison seulement
• Zone rouge : interdiction totale
• Handicapés : places réservées uniquement

SANCTIONS (Article 144) :
• Stationnement gênant : 20 DT
• Stationnement dangereux : 30 DT + 1 point
• Double file : 50 DT + 2 points
• Place handicapé : 100 DT + 3 points
• Fourrière possible après mise en demeure

RÈGLES SPÉCIFIQUES AUTOROUTE :
• Arrêt interdit sur bande d'arrêt urgence
• Aires de repos aménagées obligatoires
• Borne SOS tous les 2 km
• Signalisation triangle + gilet obligatoire

RECOMMANDATIONS :
• Toujours vérifier panneaux complémentaires
• Respecter durée maximale indiquée
• Caler roues en pente
• Ne jamais laisser enfants/animaux seuls
""",
        "keywords": ["stationnement", "arrêt", "parking", "double file", "zone bleue",
                     "gênant", "dangereux", "fourrière", "disque", "place handicapé"],
        "reference": "Code de la Route Tunisien - Articles 39-42"
    },
    
    "equipement": {
        "title": "ÉQUIPEMENTS OBLIGATOIRES VÉHICULE",
        "risk": "🟡 MOYEN",
        "content": """
ÉQUIPEMENTS OBLIGATOIRES (Article 58) :
1. Triangle de présignalisation homologué (1)
2. Gilet haute visibilité homologué (1 par occupant)
3. Roue de secours ou kit réparation
4. Éthylotest électronique homologué (depuis 2022)
5. Éclairage complet fonctionnel
6. Dispositif rétroréfléchissant arrière

CONTROLE TECHNIQUE (Article 60) :
• Véhicule < 4 ans : pas de contrôle
• 4-8 ans : contrôle tous les 2 ans
• > 8 ans : contrôle annuel
• Contre-visite sous 2 mois maximum
• Amende absence contrôle : 50 DT

PNEUS (Règlement technique) :
• Profondeur sculpture minimum : 1.6mm
• Même type sur même essieu
• Pression vérifiée à froid
• Date fabrication < 10 ans
• Pneus hiver autorisés novembre-mars

ÉCLAIRAGE (Article 59) :
• Feux de croisement fonctionnels
• Feux stop, position, recul
• Clignotants avant/arrière/latéraux
• Rétroviseurs intérieur et extérieur
• Essuie-glaces avant/arrière (si équipé)

SANCTIONS DÉFAUT ÉQUIPEMENT :
• Absence triangle/gilet : 30 DT
• Éthylotest non conforme : 20 DT
• Pneus lisses : 50 DT + 2 points
• Éclairage défectueux : 30 DT + 1 point
• Contrôle technique absent : 50 DT

DOCUMENTS OBLIGATOIRES :
• Permis de conduire valide
• Carte grise originale
• Assurance valide (vignette)
• Carte de contrôle technique (si exigible)
""",
        "keywords": ["équipement", "triangle", "gilet", "éthylotest", "pneus",
                     "contrôle technique", "éclairage", "freins", "document", "assurance"],
        "reference": "Code de la Route Tunisien - Articles 58-60"
    },
    
    "jeune": {
        "title": "PERMIS PROBATOIRE ET JEUNES CONDUCTEURS",
        "risk": "🟠 ÉLEVÉ",
        "content": """
DURÉE PROBATOIRE (Article 25) :
• Permis B : 2 ans probatoire
• 6 points seulement première année
• +2 points chaque année sans infraction
• Attente 12 points après 3 ans sans faute

RESTRICTIONS PENDANT PROBATOIRE :
• Vitesse maximale réduite :
  - Agglomération : 50 km/h (inchangé)
  - Route nationale : 80 km/h (-10)
  - Autoroute : 90 km/h (-20)
• Taux alcool : ZÉRO tolérance (0.0 g/L)
• Pas de remorque > 750kg

FORMATION POST-PERMIS :
• Stage obligatoire après infraction grave
• Récupération points possible après stage
• Évaluation conduite après suspension

STATISTIQUES JEUNES (ONSR 2023) :
• 18-24 ans : 24% des accidents mortels
• 1ère cause : vitesse inadaptée (38%)
• 2ème cause : alcool/drogues (22%)
• 3ème cause : téléphone (18%)

ACCOMPAGNEMENT RECOMMANDÉ :
• Conduite accompagnée possible dès 17 ans
• 3000 km minimum avec accompagnateur
• 2 ans d'expérience minimum accompagnateur
• Pas d'infraction grave accompagnateur

SANCTIONS SPÉCIFIQUES :
• Excès vitesse pendant probatoire : double déduction points
• Alcool > 0.0 g/L : retrait immédiat permis
• Récidive infraction grave : annulation permis

CONSEILS ONSR :
• Éviter conduite nuit première année
• Limiter passagers jeunes
• Pas de musique forte
• Pauses fréquentes
• Véhicule adapté (petit, maniable)
""",
        "keywords": ["jeune conducteur", "permis probatoire", "accompagné", "points",
                     "vitesse limitée", "alcool zéro", "stage", "récupération points",
                     "18-24 ans", "novice"],
        "reference": "Code de la Route Tunisien - Article 25, Arrêté 2022"
    },
    
    "urgence": {
        "title": "PROTOCOLE D'URGENCE ET SECOURS",
        "risk": "🔴 CRITIQUE",
        "content": """
NUMÉROS D'URGENCE TUNISIE :

🚨 SERVICES DE SECOURS :
• 197 - Police Nationale (urgence routière)
• 190 - SAMU (Secours Médicaux Urgents)
• 198 - Protection Civile (incendies, accidents)
• 193 - Garde Nationale (routière/autoroute)
• 1717 - Info routes et circulation

PROTOCOLE ACCIDENT (Article 64) :
1. SÉCURISATION IMMÉDIATE :
   - Feux de détresse allumés
   - Triangle à 30m minimum (100m autoroute)
   - Gilet haute visibilité PORTÉ

2. PROTECTION VICTIMES :
   - Ne JAMAIS déplacer blessé grave
   - Couvrir avec couverture de survie
   - Ne rien donner à boire/manger
   - Parler, rassurer, surveiller

3. ALERTE PRÉCISE :
   - Lieu exact (route, km, direction)
   - Nombre et type véhicules
   - Nombre victimes apparent
   - Nature blessures visibles
   - Votre nom et téléphone

4. PREMIERS SECOURS :
   - PLS si inconscient respiration normale
   - Compression hémorragie abondante
   - Bouche-à-bouche/CPR si absence respiration

OBLIGATIONS LÉGALES :
• S'arrêter et porter assistance : OBLIGATOIRE
• Déclaration accident sous 24h (Police)
• Échange constat amiable si dommages légers
• Témoignage obligatoire si requis

AUTOROUTE SPÉCIFIQUE :
• Bornes SOS tous 2 km
• Postes d'appel d'urgence
• Véhicule d'intervention spécialisé
• Bande arrêt urgence strictement réservée

SANCTIONS DÉFAUT ASSISTANCE (Article 145) :
• Défaut assistance personne en danger : 200-500 DT
• Défaut déclaration accident : 100 DT
• Fausse déclaration : 200 DT + tribunal
""",
        "keywords": ["urgence", "accident", "secours", "197", "190", "198", "193",
                     "protocole", "triangle", "gilet", "SAMU", "police", "blessé",
                     "constat", "assistance", "témoignage"],
        "reference": "Code de la Route Tunisien - Articles 64-65, 145"
    },

    # ====================================================================
    # NEW ENTRIES BELOW
    # ====================================================================

    "depassement": {
        "title": "RÈGLES DE DÉPASSEMENT",
        "risk": "🟠 ÉLEVÉ",
        "content": """
PRINCIPES GÉNÉRAUX (Article 37) :
• Le dépassement s'effectue par la GAUCHE uniquement
• Vérifier rétroviseur + angle mort AVANT tout dépassement
• Signaler avec clignotant gauche AVANT de dévier
• Revenir à droite sans gêner le véhicule dépassé

INTERDICTIONS DE DÉPASSER (Article 38) :
• Ligne continue (blanche ou jaune)
• Sommet de côte sans visibilité suffisante
• Virage sans visibilité
• Passage à niveau et 50m avant
• Intersection sans signalisation favorable
• Passage piétons occupé
• Quand un véhicule devant signale un dépassement
• Quand un véhicule derrière a commencé à dépasser

DISTANCES MINIMALES DE DÉPASSEMENT :
• Véhicule léger : 1 mètre latéral en agglomération
• Véhicule léger : 1.5 mètre hors agglomération
• Poids lourds / bus : 1.5 mètre minimum partout
• Cyclistes / piétons : 1.5 mètre minimum

DÉPASSEMENT PAR LA DROITE AUTORISÉ (Article 37 bis) :
• Véhicule signalant un tournant à gauche
• Tramway circulant au milieu de la chaussée
• Voies d'accélération / décélération autoroute
• Files parallèles en agglomération (vitesse réduite)

SANCTIONS (Article 144) :
• Dépassement dangereux : 100 DT + 4 points
• Dépassement par la droite interdit : 50 DT + 3 points
• Dépassement ligne continue : 100 DT + 4 points + suspension possible
• Si accident causé : 200-500 DT + 6 points + suspension 3-6 mois
• Récidive : double sanctions

STATISTIQUES ONSR :
• 18% des accidents mortels hors agglomération liés au dépassement
• Cause principale : mauvaise évaluation distance/vitesse véhicule en face
""",
        "keywords": ["dépassement", "dépasser", "doubler", "ligne continue", "interdit",
                     "angle mort", "rétroviseur", "clignotant", "collision frontale",
                     "vis-à-vis", "voie opposée"],
        "reference": "Code de la Route Tunisien - Articles 37-38, 144"
    },

    "permis": {
        "title": "CATÉGORIES DE PERMIS DE CONDUIRE TUNISIEN",
        "risk": "🔵 INFORMATION",
        "content": """
CATÉGORIES DE PERMIS (Décret n°2000-142, modifié 2022) :

CATÉGORIE A :
• A1 : Motocyclettes ≤ 125 cm³ et ≤ 11 kW — âge minimum 16 ans
• A : Motocyclettes > 125 cm³ — âge minimum 18 ans

CATÉGORIE B :
• Véhicules légers ≤ 3.5 tonnes, ≤ 9 places
• Âge minimum : 18 ans
• Remorque ≤ 750 kg sans permis supplémentaire
• Remorque > 750 kg : permis B+E requis

CATÉGORIE C :
• Véhicules > 3.5 tonnes (poids lourds)
• Âge minimum : 21 ans
• Visite médicale obligatoire tous les 5 ans
• C1 : 3.5 à 7.5 tonnes — C : > 7.5 tonnes

CATÉGORIE D :
• Transport de personnes > 9 places
• Âge minimum : 24 ans
• Visite médicale tous les 3 ans
• D1 : ≤ 16 places — D : > 16 places

CATÉGORIE E :
• Extension remorque > 750 kg
• B+E, C+E, D+E selon véhicule tracteur

OBTENTION DU PERMIS :
• Inscription auto-école agréée obligatoire
• Examen théorique (code) : 40 questions, minimum 35 correctes
• Examen pratique : parcours + manœuvres + circulation
• Visite médicale préalable obligatoire
• Délai entre deux tentatives : 15 jours minimum

VALIDITÉ ET RENOUVELLEMENT :
• Permis B : validité 10 ans (renouvellement administratif)
• Permis C/D : renouvellement tous les 5 ans avec visite médicale
• Permis international : validité 3 ans, délivré par bureau régional
• Échange permis étranger : conditions bilatérales

SYSTÈME DE POINTS (Article 144 bis) :
• Capital initial : 12 points (6 en probatoire)
• Récupération automatique : 4 points après 3 ans sans infraction
• Stage volontaire : récupération 4 points (1 stage par an maximum)
• Solde 0 : annulation permis, nouvel examen après 6 mois

SANCTIONS CONDUITE SANS PERMIS (Article 143) :
• Sans permis valide : 200 DT + immobilisation véhicule
• Permis non correspondant : 100 DT + 4 points
• Permis étranger non échangé > 1 an : 100 DT
• Récidive conduite sans permis : 500 DT + tribunal
""",
        "keywords": ["permis", "catégorie", "A", "B", "C", "D", "examen", "code",
                     "auto-école", "renouvellement", "points", "annulation", "échange",
                     "international", "visite médicale", "conduire sans permis"],
        "reference": "Code de la Route Tunisien - Décret n°2000-142, Articles 143-144 bis"
    },

    "autoroute": {
        "title": "RÈGLES SPÉCIFIQUES AUTOROUTES TUNISIENNES",
        "risk": "🟠 ÉLEVÉ",
        "content": """
RÉSEAU AUTOROUTIER TUNISIEN (Tunisie Autoroutes) :
• A1 : Tunis – Sfax (286 km)
• A3 : Tunis – Oued Zarga / Bousalem (102 km)
• A4 : Tunis – Bizerte (60 km)
• M'saken – Kairouan (en cours d'extension)

ACCÈS AUTOROUTE (Article 70) :
• Véhicules autorisés : vitesse min 60 km/h
• INTERDITS : piétons, cyclistes, cyclomoteurs < 50 cm³, tracteurs agricoles,
  véhicules à traction animale, engins de chantier non autorisés
• Accès uniquement par voies d'insertion désignées

RÈGLES DE CIRCULATION (Articles 71-75) :
• Circulation à droite obligatoire sauf dépassement
• Voie gauche : dépassement uniquement, pas de roulage continu
• Bande d'arrêt d'urgence : STRICTEMENT réservée aux pannes/urgences
• Marche arrière et demi-tour : INTERDITS en toutes circonstances
• Distance sécurité : minimum 2 secondes (4 sec par mauvais temps)

PÉAGES :
• Paiement aux gares de péage (espèces, carte prépayée)
• Système télépéage (badge) disponible
• Tarifs selon catégorie véhicule et distance
• Franchise aux véhicules d'urgence

PANNES ET INCIDENTS :
• Garer véhicule sur bande d'arrêt d'urgence au maximum à droite
• Allumer feux de détresse immédiatement
• Placer triangle à 100 mètres en amont
• Revêtir gilet haute visibilité AVANT de sortir
• Appeler le 193 (Garde Nationale) ou bornes SOS
• Passagers doivent sortir et se placer derrière glissière de sécurité

SANCTIONS SPÉCIFIQUES AUTOROUTE :
• Circulation bande d'arrêt urgence : 100 DT + 4 points
• Marche arrière / demi-tour : 200 DT + 6 points + suspension
• Non-paiement péage : 50 DT + poursuites
• Arrêt non justifié : 50 DT + 2 points
• Excès vitesse > 130 km/h : 500 DT + 6 points + suspension 3 mois

STATISTIQUES AUTOROUTE (ONSR 2023) :
• 12% des accidents mortels surviennent sur autoroute
• Cause n°1 : excès de vitesse (42%)
• Cause n°2 : fatigue/somnolence (28%)
• Cause n°3 : distance sécurité insuffisante (15%)
""",
        "keywords": ["autoroute", "A1", "A3", "A4", "péage", "voie d'insertion",
                     "bande d'arrêt d'urgence", "distance sécurité", "panne",
                     "demi-tour", "marche arrière", "Tunis", "Sfax", "Bizerte"],
        "reference": "Code de la Route Tunisien - Articles 70-75, Tunisie Autoroutes"
    },

    "moto": {
        "title": "MOTOCYCLETTES ET DEUX-ROUES",
        "risk": "🟠 ÉLEVÉ",
        "content": """
CASQUE OBLIGATOIRE (Article 56) :
• Conducteur ET passager : casque homologué OBLIGATOIRE
• Casque attaché correctement (jugulaire fermée)
• Casque intégral ou jet avec visière recommandé
• Interdiction casque non homologué (vélo, chantier)

ÉQUIPEMENTS OBLIGATOIRES MOTO :
• Casque homologué (norme ECE 22.05 ou équivalent)
• Gants homologués recommandés
• Rétroviseurs gauche et droit fonctionnels
• Éclairage : feux de croisement allumés en permanence (jour et nuit)
• Plaque d'immatriculation lisible et éclairée

CIRCULATION DEUX-ROUES (Article 57) :
• Interfile : INTERDIT en Tunisie (circulation entre files de véhicules)
• Maximum 2 motos de front sur même voie
• Passager autorisé uniquement si selle et repose-pieds prévus
• Enfant < 5 ans : INTERDIT comme passager moto
• Transport objets encombrants : INTERDIT

PERMIS SPÉCIFIQUES :
• Cyclomoteur ≤ 50 cm³ : pas de permis si > 16 ans (carte cyclomoteur)
• 50-125 cm³ : permis A1 (dès 16 ans)
• > 125 cm³ : permis A (dès 18 ans)
• Formation pratique spécifique obligatoire

SANCTIONS (Article 144) :
• Absence casque conducteur : 30 DT + 2 points
• Absence casque passager : 30 DT + 1 point
• Circulation interfile : 50 DT + 3 points
• Passager enfant < 5 ans : 50 DT + 2 points
• Défaut éclairage moto : 30 DT + 1 point

STATISTIQUES ONSR 2023 :
• Deux-roues : 32% des tués sur la route en Tunisie
• 65% des victimes ne portaient pas de casque
• 18-30 ans : tranche d'âge la plus touchée (48%)
• Agglomération : 70% des accidents moto
""",
        "keywords": ["moto", "motocyclette", "deux-roues", "casque", "scooter",
                     "cyclomoteur", "permis A", "interfile", "passager moto",
                     "équipement moto", "gants"],
        "reference": "Code de la Route Tunisien - Articles 56-57, 144"
    },

    "pietons": {
        "title": "DROITS ET OBLIGATIONS DES PIÉTONS",
        "risk": "🟡 MOYEN",
        "content": """
DROITS DES PIÉTONS (Article 90) :
• Priorité ABSOLUE sur les passages piétons marqués
• Priorité dans les zones 30 et zones de rencontre
• Priorité lorsqu'ils sont engagés sur la chaussée (même hors passage)
• Droit de traverser aux intersections même sans passage marqué

OBLIGATIONS DES PIÉTONS (Article 91) :
• Utiliser les trottoirs lorsqu'ils existent
• Traverser aux passages piétons s'il en existe à moins de 50 mètres
• Respecter les feux piétons (rouge/vert)
• Hors agglomération : marcher à GAUCHE face aux véhicules
• De nuit : porter vêtement réfléchissant recommandé

OBLIGATIONS DES CONDUCTEURS ENVERS LES PIÉTONS (Article 35) :
• S'arrêter si piéton engagé ou attendant sur passage
• Vitesse réduite aux abords des écoles, hôpitaux, marchés
• Interdiction de stationner sur passage piétons et 5m avant
• Zones 30 : vigilance permanente

PIÉTONS VULNÉRABLES :
• Enfants : attention redoublée près des écoles (30 km/h)
• Personnes âgées : temps de traversée plus long
• Personnes à mobilité réduite : accessibilité trottoirs
• Non-voyants : canne blanche = priorité absolue

SANCTIONS CONDUCTEURS (Article 144) :
• Non-respect passage piéton occupé : 30 DT + 1 point
• Refus priorité piéton en zone 30 : 50 DT + 2 points
• Stationnement sur passage piéton : 30 DT + 1 point
• Accident avec piéton : responsabilité présumée du conducteur

SANCTIONS PIÉTONS :
• Traversée hors passage (si passage < 50m) : 5 DT
• Non-respect feu piéton : 5 DT
• Marche sur chaussée avec trottoir disponible : 5 DT
• Jeux dangereux sur chaussée : 10 DT

STATISTIQUES ONSR 2023 :
• Piétons : 22% des tués sur la route en Tunisie
• 60% des accidents piétons surviennent hors passage
• Enfants < 14 ans : 18% des piétons victimes
• Heures de pointe : 7h-9h et 16h-19h les plus dangereuses
""",
        "keywords": ["piéton", "piétons", "traverser", "passage piéton", "trottoir",
                     "zone 30", "école", "enfant", "personne âgée", "non-voyant",
                     "feu piéton", "traversée"],
        "reference": "Code de la Route Tunisien - Articles 35, 90-91, 144"
    },

    "signalisation": {
        "title": "SIGNALISATION ROUTIÈRE EN TUNISIE",
        "risk": "🔵 INFORMATION",
        "content": """
TYPES DE PANNEAUX (Arrêté du Ministre du Transport 2004) :

PANNEAUX DE DANGER (triangulaires, bordure rouge) :
• Virage dangereux (gauche/droite)
• Succession de virages
• Chaussée rétrécie
• Passage à niveau avec/sans barrière
• Intersection avec priorité à droite
• Travaux en cours
• Animaux sur la route (fréquent zones rurales)
• Chaussée glissante

PANNEAUX D'INTERDICTION (circulaires, bordure rouge) :
• Sens interdit
• Interdiction de dépasser
• Limitation de vitesse
• Interdiction de stationner / d'arrêter
• Interdiction piétons / cyclistes
• Poids/hauteur/largeur limités

PANNEAUX D'OBLIGATION (circulaires, fond bleu) :
• Direction obligatoire
• Contournement obligatoire
• Piste cyclable obligatoire
• Chaînes à neige obligatoires
• Vitesse minimale

PANNEAUX D'INDICATION (carrés/rectangulaires, fond bleu) :
• Parking
• Hôpital
• Poste de police
• Station-service
• Aire de repos autoroute
• Borne SOS

PANNEAUX DE DIRECTION :
• Fond vert : autoroute
• Fond bleu : route nationale
• Fond blanc : direction locale
• Fond jaune : direction temporaire (déviation)

MARQUAGE AU SOL :
• Ligne continue blanche : interdiction de franchir
• Ligne discontinue : dépassement autorisé
• Ligne mixte : selon côté
• Bande jaune en bordure : stationnement interdit
• Zébra : zone neutralisée (interdit de rouler dessus)

FEUX TRICOLORES :
• Vert : passage autorisé
• Orange : arrêt si possible (passage si trop près)
• Rouge : arrêt OBLIGATOIRE (y compris pour tourner)
• Flèche verte : direction autorisée uniquement
• Clignotant orange : prudence, priorité à droite

SANCTIONS NON-RESPECT SIGNALISATION (Article 144) :
• Feu rouge grillé : 50 DT + 4 points
• Stop non respecté : 50 DT + 3 points
• Sens interdit : 30 DT + 3 points
• Ligne continue franchie : 100 DT + 4 points
• Panneau limitation ignoré : selon excès de vitesse
""",
        "keywords": ["panneau", "signalisation", "feu rouge", "stop", "sens interdit",
                     "ligne continue", "marquage", "obligation", "interdiction", "danger",
                     "direction", "indication", "triangle", "circulaire"],
        "reference": "Code de la Route Tunisien - Arrêté signalisation 2004, Article 144"
    },

    "assurance": {
        "title": "ASSURANCE AUTOMOBILE EN TUNISIE",
        "risk": "🟡 MOYEN",
        "content": """
ASSURANCE OBLIGATOIRE (Loi n°2005-86) :
• Responsabilité civile (RC) : OBLIGATOIRE pour tout véhicule motorisé
• Couvre les dommages causés aux tiers (corporels et matériels)
• Vignette d'assurance visible sur pare-brise obligatoire
• Validité : 1 an renouvelable

TYPES DE COUVERTURE :
• RC seule (tiers) : couverture minimale légale
• RC + vol + incendie : protection intermédiaire
• Tous risques : couverture complète (y compris dommages propres)
• Bris de glace : option séparée
• Assistance routière : option recommandée

CONSTAT AMIABLE (Article 65) :
• Formulaire standardisé disponible auprès assureurs
• À remplir sur les lieux de l'accident
• Signé par les deux parties
• Envoyer à l'assureur dans 5 jours ouvrables
• Si désaccord : ne pas signer, appeler police

DÉCLARATION DE SINISTRE :
• Délai maximum : 5 jours ouvrables après accident
• Documents requis : constat, permis, carte grise, photos
• Si blessés : procès-verbal police obligatoire
• Expertise véhicule : organisée par l'assureur

FONDS DE GARANTIE AUTOMOBILE (FGA) :
• Indemnise les victimes d'accidents avec véhicule non assuré
• Indemnise si conducteur en fuite non identifié
• Recours contre le responsable non assuré

SANCTIONS DÉFAUT D'ASSURANCE (Article 143) :
• Conduite sans assurance valide : 200 DT + immobilisation véhicule
• Vignette non apposée : 20 DT
• Fausse attestation assurance : 500 DT + tribunal
• Récidive : 500 DT + confiscation véhicule possible

BONUS-MALUS :
• Bonus : réduction prime si aucun sinistre (jusqu'à -50%)
• Malus : majoration si sinistre responsable (jusqu'à +200%)
• Coefficient recalculé chaque année
• Historique transférable entre assureurs

CONSEILS PRATIQUES :
• Comparer les offres de plusieurs assureurs
• Vérifier les exclusions de garantie
• Garder copie du constat dans le véhicule
• Photographier les dommages immédiatement
• Ne jamais admettre la responsabilité sur les lieux
""",
        "keywords": ["assurance", "RC", "responsabilité civile", "constat", "sinistre",
                     "vignette", "tous risques", "tiers", "bonus", "malus", "prime",
                     "FGA", "indemnisation", "expertise"],
        "reference": "Loi n°2005-86, Code de la Route Tunisien - Articles 65, 143"
    },

    "transport_marchandises": {
        "title": "TRANSPORT DE MARCHANDISES ET POIDS LOURDS",
        "risk": "🟠 ÉLEVÉ",
        "content": """
POIDS ET DIMENSIONS (Arrêté du Ministre du Transport) :
• Poids total autorisé en charge (PTAC) max : 40 tonnes (ensemble articulé)
• Largeur maximale : 2.55 mètres (2.60 m frigorifique)
• Hauteur maximale : 4 mètres
• Longueur max camion seul : 12 mètres
• Longueur max ensemble articulé : 16.50 mètres

PERMIS REQUIS :
• 3.5 - 7.5 tonnes : permis C1
• > 7.5 tonnes : permis C
• Avec remorque > 750 kg : permis C+E
• Matières dangereuses : autorisation spéciale ADR

TEMPS DE CONDUITE PROFESSIONNELS (Article 86) :
• Conduite continue max : 4h30
• Pause obligatoire : 45 minutes minimum
• Durée quotidienne max : 9h (10h deux fois par semaine)
• Repos journalier : 11h consécutives minimum
• Repos hebdomadaire : 45h consécutives minimum
• Carnet de bord / chronotachygraphe obligatoire

CHARGEMENT (Article 76) :
• Ne doit pas dépasser les dimensions autorisées
• Arrimage solide obligatoire (sangles, chaînes)
• Bâche si risque de chute de matériaux
• Signalisation dépassement arrière (panneau réfléchissant)
• Répartition équilibrée de la charge

RESTRICTIONS DE CIRCULATION :
• Centre-ville : restriction horaire poids lourds (6h-9h, 16h-19h)
• Autoroute : voie de droite obligatoire sauf dépassement
• Interdiction circulation dimanche et jours fériés (certains axes)
• Itinéraires obligatoires pour matières dangereuses

SANCTIONS (Article 144) :
• Surcharge ≤ 5% : 50 DT
• Surcharge 5-20% : 100 DT + immobilisation
• Surcharge > 20% : 200 DT + immobilisation + déchargement
• Dépassement temps conduite : 100 DT + 4 points
• Absence chronotachygraphe : 100 DT + 4 points
• Chargement non arrimé : 50 DT + 2 points + immobilisation possible

STATISTIQUES ONSR 2023 :
• Poids lourds impliqués dans 15% des accidents mortels
• 40% des accidents PL liés à la fatigue
• Surcharge détectée dans 25% des contrôles
""",
        "keywords": ["poids lourd", "camion", "marchandises", "transport", "PTAC",
                     "surcharge", "chronotachygraphe", "chargement", "arrimage",
                     "matières dangereuses", "permis C", "remorque", "semi-remorque"],
        "reference": "Code de la Route Tunisien - Articles 76, 86, 144"
    },

    "transport_personnes": {
        "title": "TRANSPORT EN COMMUN ET TAXI",
        "risk": "🟡 MOYEN",
        "content": """
TRANSPORT EN COMMUN (Loi n°2004-33) :

BUS ET AUTOCARS :
• Permis D obligatoire (D1 pour ≤ 16 places)
• Visite médicale tous les 3 ans
• Contrôle technique semestriel
• Extincteur et trousse de secours obligatoires
• Ceintures obligatoires si équipées
• Nombre places debout limité et affiché

TAXIS :
• Licence taxi délivrée par le Gouvernorat
• Permis B + 3 ans d'expérience minimum
• Casier judiciaire vierge exigé
• Compteur horokilométrique homologué et visible
• Tarifs officiels affichés dans le véhicule
• Plaque taxi et lumineux sur le toit obligatoires

TARIFS TAXI 2024 :
• Prise en charge : 0.450 DT
• Tarif jour (6h-21h) : 0.550 DT/km
• Tarif nuit (21h-6h) : 0.700 DT/km
• Attente : 7.200 DT/heure
• Bagages volumineux : supplément forfaitaire

TRANSPORT SCOLAIRE :
• Véhicule agréé et contrôlé spécifiquement
• Accompagnateur adulte obligatoire
• Signalisation "Transport Scolaire" visible
• Vitesse limitée à 60 km/h hors agglomération
• Places assises uniquement (pas de places debout)
• Ceintures obligatoires

OBLIGATIONS DU CONDUCTEUR PROFESSIONNEL :
• Taux alcool : 0.0 g/L (tolérance zéro)
• Téléphone : interdit même kit mains-libres en service
• Formation continue obligatoire tous les 5 ans
• Carte professionnelle visible

LOUAGE (transport interurbain tunisien) :
• Véhicule 5 ou 8 places agréé
• Itinéraire fixe station à station
• Départ quand véhicule complet
• Tarif réglementé par trajet
• Conducteur : permis B + licence professionnelle

SANCTIONS :
• Taxi sans licence : 200 DT + immobilisation
• Compteur non fonctionnel : 100 DT + suspension licence
• Surcharge passagers : 50 DT par passager excédentaire + 2 points
• Transport scolaire non conforme : 200 DT + immobilisation
""",
        "keywords": ["taxi", "bus", "autocar", "transport en commun", "louage",
                     "transport scolaire", "licence", "compteur", "tarif", "permis D",
                     "passagers", "places"],
        "reference": "Loi n°2004-33, Code de la Route Tunisien - Articles 86, 144"
    },

    "environnement": {
        "title": "POLLUTION ET CONTRÔLE TECHNIQUE ENVIRONNEMENTAL",
        "risk": "🟢 FAIBLE",
        "content": """
NORMES D'ÉMISSIONS (Arrêté 2018) :
• Véhicules essence : CO max 3.5% au ralenti
• Véhicules diesel : opacité max 2.5 m⁻¹
• Contrôle antipollution intégré au contrôle technique
• Véhicules > 8 ans : contrôle annuel incluant émissions

CONTRÔLE TECHNIQUE ENVIRONNEMENTAL :
• Mesure des gaz d'échappement
• Niveau sonore (silencieux fonctionnel)
• Absence de fuites d'huile / carburant
• État du pot catalytique (si équipé)

VÉHICULES GPL (Gaz de Pétrole Liquéfié) :
• Installation par garage agréé uniquement
• Contrôle spécifique réservoir GPL
• Certificat de conformité obligatoire
• Stationnement souterrain : interdit

NUISANCES SONORES (Article 53) :
• Klaxon : utilisation en ville limitée aux cas de danger
• Silencieux obligatoire et fonctionnel
• Modifications échappement interdites (augmentation volume)
• Musique forte audible extérieur : interdite

SANCTIONS :
• Véhicule polluant (contrôle échoué) : 30 DT + contre-visite
• Absence silencieux / échappement modifié : 30 DT
• Klaxon abusif en agglomération : 10 DT
• Fuite de carburant / huile : 30 DT + immobilisation
• Jet de déchets sur la route : 20 DT

ENCOURAGEMENTS :
• Exonération partielle taxe pour véhicules hybrides/électriques
• Bonus écologique à l'achat (véhicules peu polluants)
• Réseau de bornes de recharge en développement (Tunis, Sousse, Sfax)
""",
        "keywords": ["pollution", "émissions", "gaz", "échappement", "contrôle technique",
                     "environnement", "bruit", "klaxon", "GPL", "électrique", "hybride",
                     "catalytique", "silencieux"],
        "reference": "Code de la Route Tunisien - Article 53, Arrêté 2018"
    },
    "infractions_graves": {
        "title": "INFRACTIONS GRAVES ET DÉLITS ROUTIERS",
        "risk": "🔴 CRITIQUE",
        "content": """
CLASSIFICATION DES INFRACTIONS (Code de la Route Tunisien) :

CONTRAVENTIONS DE 1ÈRE CLASSE (5-20 DT) :
• Piéton traversant hors passage
• Non-port vêtement réfléchissant (piéton nuit)
• Klaxon abusif

CONTRAVENTIONS DE 2ÈME CLASSE (20-50 DT) :
• Stationnement gênant ou interdit
• Absence éthylotest / triangle
• Défaut clignotant
• Vignette assurance non visible

CONTRAVENTIONS DE 3ÈME CLASSE (50-100 DT) :
• Excès vitesse modéré (≤ 20 km/h)
• Non-respect stop
• Téléphone au volant
• Dépassement dangereux

CONTRAVENTIONS DE 4ÈME CLASSE (100-500 DT) :
• Excès vitesse grave (> 40 km/h)
• Alcool au volant
• Feu rouge grillé en zone à risque
• Ligne continue + dépassement

DÉLITS ROUTIERS (Code Pénal - tribunal) :
• Conduite sous influence drogues : 1000-5000 DT + prison possible
• Délit de fuite après accident corporel : 2000-5000 DT + 6 mois-2 ans prison
• Homicide involontaire par accident : 1-5 ans prison
• Blessures graves par accident : 6 mois-3 ans prison
• Récidive délit routier : peines doublées

SUSPENSION ET RETRAIT DE PERMIS :
• Suspension administrative : 1-6 mois (décision préfectorale)
• Suspension judiciaire : 6 mois-5 ans (tribunal)
• Annulation permis : nouvel examen après 6 mois minimum
• Interdiction de conduire : prononcée par tribunal

IMMOBILISATION ET MISE EN FOURRIÈRE :
• Immobilisation immédiate : alcool, sans permis, sans assurance
• Mise en fourrière : stationnement dangereux, épave
• Frais de fourrière : à la charge du propriétaire
• Délai de récupération : 30 jours avant vente aux enchères

CASIER ROUTIER :
• Enregistrement de toutes les infractions
• Accessible par les forces de l'ordre
• Impact sur assurance (bonus-malus)
• Consultable par le conducteur

CIRCONSTANCES AGGRAVANTES :
• Alcool + vitesse : cumul sanctions
• Permis probatoire : sanctions doublées
• Avec passagers mineurs : sanctions alourdies
• Zone scolaire : sanctions alourdies
• Récidive < 1 an : sanctions doublées
""",
        "keywords": ["infraction", "délit", "amende", "prison", "tribunal",
                     "suspension", "retrait permis", "annulation", "fourrière",
                     "délit de fuite", "homicide", "récidive", "casier routier",
                     "contravention"],
        "reference": "Code de la Route Tunisien - Articles 143-145, Code Pénal Tunisien"
    },

    "zones_dangereuses": {
        "title": "ZONES ET AXES DANGEREUX EN TUNISIE",
        "risk": "🟠 ÉLEVÉ",
        "content": """
POINTS NOIRS IDENTIFIÉS (ONSR 2023) :

GRANDS AXES ROUTIERS :
• GP1 (Tunis-Sfax par la côte) : 45 points noirs identifiés
• GP3 (Tunis-Le Kef) : virages dangereux zone montagneuse
• GP7 (Tunis-Bizerte ancienne route) : carrefours non sécurisés
• GP8 (Sousse-Kairouan) : traversées de villages
• Route Tunis-Zaghouan : virages et pentes

ZONES URBAINES À RISQUE :
• Grand Tunis : Ariana, Manouba, Ben Arous (trafic dense)
• Sousse centre-ville : mélange piétons/véhicules
• Sfax médina : rues étroites, stationnement anarchique
• Nabeul-Hammamet : zone touristique, conduite erratique
• Kairouan : carrefours mal signalisés

PÉRIODES À HAUT RISQUE :
• Ramadan : heures iftar (accidents +35%)
• Été (juillet-août) : trafic touristique +40%
• Fêtes nationales : grands départs
• Week-ends prolongés : autoroutes saturées
• Retour vacances : fatigue + précipitation

FACTEURS LOCAUX :
• Routes nationales traversant les souks hebdomadaires
• Animaux sur les routes rurales (moutons, dromadaires)
• Engins agricoles lents sans signalisation
• Chaussée dégradée (nids-de-poule) zones rurales
• Éclairage public déficient hors agglomération

RECOMMANDATIONS PAR ZONE :
• Autoroutes : respecter distance, pauses régulières
• Routes nationales : anticiper véhicules lents, pas de dépassement risqué
• Zones urbaines : vitesse réduite, attention piétons
• Routes rurales : vigilance animaux, chaussée dégradée
• Zones touristiques : attention piétons, loueurs de voitures inexpérimentés

STATISTIQUES RÉGIONALES (ONSR 2023) :
• Grand Tunis : 28% des accidents nationaux
• Sousse : 12% des accidents
• Sfax : 10% des accidents
• Nabeul : 8% des accidents
• Reste du pays : 42%
""",
        "keywords": ["zone dangereuse", "point noir", "GP1", "GP3", "Tunis", "Sfax",
                     "Sousse", "Nabeul", "Kairouan", "Bizerte", "ramadan", "été",
                     "route nationale", "accident fréquent", "virage"],
        "reference": "ONSR Tunisie - Rapport annuel 2023, Carte des points noirs"
    },

    "rond_point": {
        "title": "CIRCULATION EN ROND-POINT ET GIRATOIRE",
        "risk": "🟡 MOYEN",
        "content": """
RÈGLES DE CIRCULATION (Article 34) :

ENTRÉE DANS LE ROND-POINT :
• Ralentir à l'approche
• Céder le passage aux véhicules DÉJÀ engagés dans le giratoire
• Signaler avec clignotant gauche si entrée par la gauche
• Vérifier l'absence de piétons sur le passage avant l'entrée
• Ne JAMAIS s'arrêter dans le giratoire sauf danger immédiat

CIRCULATION DANS LE ROND-POINT :
• Sens unique : sens inverse des aiguilles d'une montre (droite)
• Rester dans sa voie (intérieure si l'on continue, extérieure si sortie proche)
• Vitesse modérée (généralement 30-40 km/h)
• Pas de dépassement dans le giratoire
• Pas de marche arrière

SORTIE DU ROND-POINT :
• Signaler avec clignotant DROIT avant la sortie souhaitée
• Se placer sur la voie extérieure avant de sortir
• Vérifier l'angle mort (motos, vélos)
• Céder le passage aux piétons sur le passage de la sortie

CAS PARTICULIERS TUNISIENS :
• Grands ronds-points (Place Barcelone, Place Pasteur Tunis) : 2-3 voies
• Mini giratoires en zone résidentielle : même règles
• Giratoires avec feux tricolores : respecter les feux en priorité
• Rond-point non signalé : priorité à droite par défaut

ERREURS FRÉQUENTES :
• Entrer sans céder le passage
• Ne pas signaler la sortie
• Rester sur voie intérieure et couper pour sortir
• S'arrêter dans le giratoire pour laisser entrer

SANCTIONS :
• Non-respect priorité dans giratoire : 50 DT + 2 points
• Absence de clignotant : 20 DT + 1 point
• Marche arrière dans giratoire : 100 DT + 4 points
""",
        "keywords": ["rond-point", "giratoire", "sens giratoire", "cédez le passage",
                     "clignotant", "voie intérieure", "voie extérieure", "carrefour",
                     "place", "circulation giratoire"],
        "reference": "Code de la Route Tunisien - Article 34"
    },

    "accident_procedure": {
        "title": "PROCÉDURE COMPLÈTE APRÈS UN ACCIDENT",
        "risk": "🔴 CRITIQUE",
        "content": """
ÉTAPE 1 - SÉCURISER LA ZONE :
• Allumer les feux de détresse immédiatement
• Porter le gilet haute visibilité AVANT de sortir
• Placer le triangle à 30m (100m sur autoroute) en amont
• Si véhicule peut bouger et accident matériel : dégager la chaussée
• Si blessés : NE PAS déplacer les véhicules

ÉTAPE 2 - ÉVALUER LA SITUATION :
• Vérifier s'il y a des blessés
• Compter le nombre de véhicules impliqués
• Évaluer les risques supplémentaires (fuite carburant, incendie)

ÉTAPE 3 - ALERTER LES SECOURS (si nécessaire) :
• 197 - Police (accident urbain)
• 193 - Garde Nationale (accident route/autoroute)
• 190 - SAMU (si blessés)
• 198 - Protection Civile (si incendie/désincarcération)
• Donner : lieu exact, nombre de véhicules, nombre de blessés, votre nom

ÉTAPE 4 - PORTER SECOURS :
• Ne pas déplacer un blessé (sauf danger vital immédiat : feu, noyade)
• Position latérale de sécurité si inconscient mais respire
• Compression directe sur plaie qui saigne abondamment
• Couvrir les blessés (couverture de survie)
• Rassurer et parler aux victimes

ÉTAPE 5 - CONSTAT AMIABLE (si accident matériel) :
• Remplir le formulaire recto-verso
• Recto : ensemble, NE PAS modifier après signature
• Verso : individuellement, observations personnelles
• Dessiner le croquis précisément (rues, sens, position véhicules)
• Noter les coordonnées des témoins

ÉTAPE 6 - DOCUMENTATION :
• Photographier les dégâts (tous les véhicules, tous les angles)
• Photographier la scène (position véhicules, traces, panneaux)
• Noter les plaques d'immatriculation
• Relever les noms et coordonnées des parties

ÉTAPE 7 - DÉCLARATIONS :
• Déclaration police/gendarmerie : sous 24h si blessés
• Déclaration assureur : sous 5 jours ouvrables
• Garder tous les originaux de documents

DROITS DU CONDUCTEUR :
• Droit de ne pas admettre sa responsabilité
• Droit de contester le constat sous 10 jours
• Droit à un avocat si poursuites judiciaires
• Droit à une contre-expertise du véhicule

SANCTIONS POUR NON-RESPECT :
• Défaut d'assistance : 200-500 DT + tribunal
• Délit de fuite : 2000-5000 DT + 6 mois-2 ans prison
• Non-déclaration accident : 100 DT
• Fausse déclaration : 200 DT + tribunal
""",
        "keywords": ["accident", "constat", "procédure", "blessé", "secours",
                     "déclaration", "assurance", "police", "gendarmerie", "dégâts",
                     "responsabilité", "délit de fuite", "témoins", "croquis"],
        "reference": "Code de la Route Tunisien - Articles 64-65, 145, Code Pénal"
    },

    "conduite_defensive": {
        "title": "TECHNIQUES DE CONDUITE DÉFENSIVE",
        "risk": "🟢 FAIBLE",
        "content": """
PRINCIPES DE BASE :
• Anticiper les actions des autres usagers
• Maintenir une distance de sécurité suffisante
• Adapter sa vitesse aux conditions réelles
• Toujours avoir un plan d'échappement
• Ne jamais présumer que l'autre respectera les règles

RÈGLE DES 2 SECONDES :
• Repérer un point fixe quand le véhicule devant le passe
• Compter "un-mille-un, un-mille-deux"
• Si vous passez le point avant la fin : vous êtes TROP PRÈS
• Par pluie : 4 secondes / Par nuit : 4 secondes / Brouillard : 6 secondes

BALAYAGE VISUEL :
• Regarder loin devant (12-15 secondes d'avance)
• Vérifier rétroviseurs toutes les 5-8 secondes
• Scanner les côtés aux intersections
• Attention aux angles morts (motos, piétons, vélos)

ANTICIPATION DES DANGERS :
• Ballon sur la route = enfant qui peut suivre
• Véhicule garé avec roues tournées = risque de sortir
• Feux stop véhicule devant = freiner préventivement
• Piéton au bord de la route = risque de traversée
• Bus à l'arrêt = piétons qui traversent devant/derrière

GESTION DES SITUATIONS CRITIQUES :
• Éclatement pneu : maintenir volant, ne PAS freiner, décélérer
• Freins défaillants : rétrograder, frein à main progressif
• Éblouissement : regarder bord droit, ralentir, NE PAS fixer
• Aquaplaning : lâcher accélérateur, maintenir volant droit
• Animal sur la route : klaxon, freiner si possible, NE PAS braquer

CONDUITE ÉCONOMIQUE ET SÛRE :
• Accélérations douces
• Anticipation des freinages
• Vitesse stabilisée sur autoroute
• Régulateur de vitesse si disponible
• Entretien régulier du véhicule

RECOMMANDATIONS ONSR :
• Formation conduite défensive recommandée
• Stages disponibles dans les auto-écoles agréées
• Réduction possible de prime d'assurance après stage
""",
        "keywords": ["conduite défensive", "anticipation", "distance sécurité",
                     "balayage visuel", "danger", "situation critique", "éclatement",
                     "aquaplaning", "freinage", "technique conduite", "prudence"],
        "reference": "ONSR Tunisie - Guide de conduite défensive 2023"
    },

    "immatriculation": {
        "title": "IMMATRICULATION ET DOCUMENTS VÉHICULE",
        "risk": "🔵 INFORMATION",
        "content": """
SYSTÈME D'IMMATRICULATION TUNISIEN :
• Format actuel : XXX TU YYYY (série + gouvernorat + numéro)
• Plaque avant et arrière obligatoires
• Plaques homologuées et fixées solidement
• Lisibilité obligatoire (propres, non masquées)

CODES GOUVERNORATS :
• TU : Tunis (01-02)
• AR : Ariana (03)
• BA : Ben Arous (04)
• MN : Manouba (05)
• NB : Nabeul (06)
• BZ : Bizerte (07)
• BJ : Béja (08)
• JN : Jendouba (09)
• KF : Le Kef (10)
• SL : Siliana (11)
• KR : Kairouan (12)
• KS : Kasserine (13)
• SS : Sidi Bouzid (14)
• SO : Sousse (15)
• MO : Monastir (16)
• MH : Mahdia (17)
• SF : Sfax (18)
• GF : Gafsa (19)
• TZ : Tozeur (20)
• KB : Kébili (21)
• GB : Gabès (22)
• MD : Médenine (23)
• TT : Tataouine (24)
• RS : Corps diplomatique
• IT : Importation temporaire

CARTE GRISE (Certificat d'immatriculation) :
• Délivrée par la recette des finances
• Obligatoire pour circuler (original dans le véhicule)
• Changement propriétaire : mutation sous 30 jours
• Changement adresse : mise à jour sous 30 jours
• Perte : déclaration police + demande duplicata

VIGNETTE (Taxe de circulation) :
• Payable annuellement (recette des finances ou en ligne)
• Montant selon puissance fiscale du véhicule
• Délai : avant le 31 mars de chaque année
• Pénalité retard : 0.5% par mois de retard

DOCUMENTS À BORD OBLIGATOIRES :
• Permis de conduire valide
• Carte grise originale
• Attestation d'assurance valide
• Certificat de contrôle technique (si > 4 ans)
• Vignette fiscale de l'année en cours

SANCTIONS :
• Conduite sans carte grise : 50 DT + immobilisation
• Plaques non conformes : 30 DT
• Plaques masquées intentionnellement : 200 DT + tribunal
• Vignette non payée : 20 DT + majoration
• Défaut mutation propriété : 50 DT
""",
        "keywords": ["immatriculation", "plaque", "carte grise", "vignette", "taxe",
                     "mutation", "gouvernorat", "certificat", "documents", "propriétaire",
                     "recette des finances", "puissance fiscale"],
        "reference": "Code de la Route Tunisien, Décret immatriculation 2014"
    }
}


# ============================================================================
# CONVERSION TO KNOWLEDGE_BASE FORMAT FOR RAG SYSTEM
# ============================================================================

KNOWLEDGE_BASE = []

for doc_id, doc_data in SAFETY_DOCS.items():
    # Map risk emoji to risk level enum
    risk_mapping = {
        "🔴 CRITIQUE": "CRITICAL",
        "🟠 ÉLEVÉ": "HIGH",
        "🟡 MOYEN": "MEDIUM",
        "🟢 FAIBLE": "LOW",
        "🔵 INFORMATION": "INFO"
    }
    
    risk_level = risk_mapping.get(doc_data.get("risk", "🟡 MOYEN"), "MEDIUM")
    
    # Extract category from content keywords
    category_mapping = {
        "fatigue": "Comportement",
        "vitesse": "Vitesse",
        "conditions": "Météo",
        "ceinture": "Équipement Sécurité",
        "telephone": "Comportement",
        "alcool": "Substances",
        "priorite": "Règles de Circulation",
        "stationnement": "Stationnement",
        "equipement": "Équipement Véhicule",
        "jeune": "Permis & Formation",
        "urgence": "Urgence",
        "depassement": "Règles de Circulation",
        "permis": "Permis & Formation",
        "autoroute": "Autoroute",
        "moto": "Deux-Roues",
        "pietons": "Piétons",
        "signalisation": "Signalisation",
        "assurance": "Assurance & Documents",
        "transport_marchandises": "Transport Professionnel",
        "transport_personnes": "Transport Professionnel",
        "environnement": "Environnement",
        "infractions_graves": "Infractions & Sanctions",
        "zones_dangereuses": "Zones à Risque",
        "rond_point": "Règles de Circulation",
        "accident_procedure": "Urgence & Procédures",
        "conduite_defensive": "Conseils Conduite",
        "immatriculation": "Assurance & Documents"
    }
    
    document = {
        "id": doc_id,
        "title": doc_data.get("title", ""),
        "content": doc_data.get("content", ""),
        "risk_level": risk_level,
        "category": category_mapping.get(doc_id, "Sécurité Routière"),
        "keywords": doc_data.get("keywords", []),
        "legal_references": [doc_data.get("reference", "")] if doc_data.get("reference") else [],
        "statistics": {},
        "metadata": {
            "source": doc_data.get("reference", "Code de la Route Tunisien"),
            "last_update": "2024"
        }
    }
    
    KNOWLEDGE_BASE.append(document)

print(f"📚 Knowledge base loaded: {len(KNOWLEDGE_BASE)} documents")