"""
repair_advisor.py
-----------------
Practical repair guide for minor vehicle damage in Tunisia.
Products available locally, with prices in DT and where to buy.
"""

REPAIR_GUIDES = {

    "scratch": {
        "titre":     "Rayure légère (surface uniquement — vernis ou peinture superficielle)",
        "severite":  "LÉGÈRE",
        "auto_repair": True,
        "produits_tunisie": [
            {"nom": "Efface-rayures T-Cut",       "prix": "15–25 DT",  "ou": "Magasins auto Menzah 6, Avenue Habib Bourguiba"},
            {"nom": "Meguiar's ScratchX 2.0",      "prix": "35–50 DT",  "ou": "Car Wash centers, stations Agil/Total"},
            {"nom": "Polish + Compound 3M",        "prix": "20–40 DT",  "ou": "Quincailleries, magasins de peinture auto"},
        ],
        "etapes": [
            "🧼 Nettoyez la zone avec eau savonneuse et séchez complètement (chiffon microfibre).",
            "💡 Testez d'abord le produit sur une zone cachée (seuil de porte, bas de caisse).",
            "🧪 Appliquez une petite quantité de produit sur un chiffon microfibre propre.",
            "⭕ Frottez en mouvements circulaires avec légère pression pendant 30–60 secondes.",
            "⏱️  Laissez sécher selon les instructions du produit (5–10 min en général).",
            "✨ Polissez avec un chiffon propre sec jusqu'à disparition des résidus.",
            "🔁 Répétez 2 à 3 fois si nécessaire.",
            "☀️ Évitez le plein soleil : travaillez à l'ombre, par temps sec (20–28°C idéal).",
        ],
        "quand_voir_pro": [
            "La rayure traverse le vernis jusqu'à la peinture ou révèle le métal/plastique nu.",
            "La rayure dépasse 10 cm de longueur.",
            "Après 3 essais, la rayure reste nettement visible.",
        ],
        "cout_pro_tunisie": "150–400 DT chez un carrossier selon longueur et profondeur.",
    },

    "minor_dent": {
        "titre":     "Petit enfoncement sans peinture écaillée (débosselage)",
        "severite":  "MODÉRÉE",
        "auto_repair": True,
        "produits_tunisie": [
            {"nom": "Kit débosselage PDR (sans peinture)", "prix": "80–150 DT", "ou": "Marché Libya Tunis, souks auto spécialisés"},
            {"nom": "Ventouse débosselage",                "prix": "25–60 DT",  "ou": "Quincailleries, magasins bricolage"},
        ],
        "etapes": [
            "🔍 Vérifiez d'abord : la peinture est-elle intacte ? Si écaillée → voir professionnel directement.",
            "🧼 Nettoyez et dégraissez la zone.",
            "🔥 Chauffez doucement avec un sèche-cheveux 2–3 minutes (le plastique se ramollit légèrement).",
            "🪠 Placez la ventouse au centre exact de l'enfoncement.",
            "💪 Tirez fermement et progressivement — pas de coup sec.",
            "💧 Variante : eau bouillante sur la zone + ventouse immédiatement, puis eau froide pour fixer.",
            "🔁 Répétez si nécessaire. Résultat optimal : 80–90% de récupération sur enfoncements simples.",
        ],
        "avertissement": "Technique efficace principalement sur plastique (pare-chocs). Sur métal, résultat moins garanti.",
        "quand_voir_pro": [
            "La peinture est fissurée ou écaillée.",
            "L'enfoncement fait plus de 5 cm de diamètre.",
            "L'enfoncement est sur une arête ou un pli de carrosserie.",
        ],
        "cout_pro_tunisie": "200–600 DT selon technique (débosselage PDR moins cher que repeinture).",
        "pros_recommandes": [
            "Ateliers PDR : Avenue de la Liberté Tunis, Mégrine, Ariana.",
            "Carrossiers agréés Menzah, La Soukra : compter 2–4 jours.",
        ],
    },

    "deep_scratch": {
        "titre":     "Rayure profonde (métal ou plastique visible)",
        "severite":  "ÉLEVÉE",
        "auto_repair": False,
        "produits_tunisie": [
            {"nom": "Stylo retouche (code couleur exact)",       "prix": "30–80 DT",  "ou": "Concessionnaires agréés, garages officiels"},
            {"nom": "Kit retouche complet (apprêt + peinture + vernis)", "prix": "60–120 DT", "ou": "Magasins spécialisés peinture auto"},
        ],
        "etapes": [
            "🔍 Trouvez le code couleur exact : plaquette constructeur (châssis, montant de porte, coffre).",
            "🧼 Nettoyez et dégraissez la rayure (alcool isopropylique à 70°).",
            "🪣 Si le métal est visible : appliquez un apprêt anti-rouille, laissez sécher 24h.",
            "🖌️ Appliquez la peinture en 2–3 fines couches (30 min entre chaque).",
            "⏱️  Laissez sécher 24–48h selon la température ambiante.",
            "✨ Appliquez le vernis de protection.",
            "🔁 Après 1 semaine : polish léger pour intégrer la retouche.",
        ],
        "avertissement": "⚠️ La retouche maison sera visible de près. Pour un résultat professionnel invisible, consultez un carrossier agréé.",
        "quand_voir_pro": "TOUJOURS recommandé pour un résultat durable et invisible.",
        "cout_pro_tunisie": "300–800 DT (retouche + mélange peinture + vernissage complet).",
    },

    "parking_scratch": {
        "titre":     "Accrochage parking (dégâts + autre véhicule impliqué)",
        "severite":  "MODÉRÉE à ÉLEVÉE — procédure administrative importante",
        "auto_repair": False,
        "demarches_immediates": [
            "📸 Photographiez TOUS les dégâts (votre véhicule + l'autre) sous plusieurs angles.",
            "📸 Photographiez les plaques d'immatriculation des deux véhicules.",
            "📝 Si l'autre conducteur est présent : remplissez le constat amiable ENSEMBLE.",
            "👁️  Notez : heure exacte, lieu précis, circonstances.",
            "👥 Cherchez des témoins, notez leurs coordonnées.",
            "📞 Appelez votre assurance dans les 24h (OBLIGATOIRE en Tunisie).",
        ],
        "avec_constat": {
            "etapes": [
                "Les 2 conducteurs remplissent le constat ensemble calmement.",
                "Signez et échangez les coordonnées + numéros d'assurance.",
                "Photographiez le constat rempli avant de se séparer.",
                "Envoyez le constat à votre assureur sous 5 jours ouvrables.",
                "Attendez l'accord assureur avant réparation (sauf urgence).",
            ],
        },
        "sans_autre_conducteur": {
            "etapes": [
                "Photos des dégâts + plaque du véhicule fautif si visible.",
                "Déposez une déclaration au commissariat le plus proche.",
                "Remplissez un constat amiable unilatéral.",
                "Prévenez votre assurance immédiatement.",
            ],
            "couverture": "Pris en charge uniquement avec contrat 'Tous Risques' ou 'Dommages Collision'.",
        },
        "franchise_tn": {
            "montant_moyen": "150–300 DT selon votre contrat",
            "explication":   "Somme restant à votre charge même si l'assurance paie le reste.",
        },
        "conseil_devis": [
            "Obtenez 2–3 devis de carrossiers différents.",
            "Présentez-les à votre assureur.",
            "L'assureur peut imposer son propre réseau de garages agréés.",
        ],
    },
}


def get_repair_advice(damage_type: str) -> dict:
    """Return repair guide for a given damage type."""
    guide = REPAIR_GUIDES.get(damage_type)
    if not guide:
        return {
            "found":   False,
            "message": f"Type '{damage_type}' non reconnu. Types disponibles : "
                       + ", ".join(REPAIR_GUIDES.keys()),
        }
    return {"found": True, "damage_type": damage_type, **guide}


def format_repair_advice(data: dict) -> str:
    """Format repair guide into a clean French string for LLM injection."""
    if not data.get("found"):
        return data.get("message", "Information non disponible.")

    lines = [f"🔧 {data['titre']}", ""]

    if "produits_tunisie" in data:
        lines.append("🛒 PRODUITS DISPONIBLES EN TUNISIE :")
        for p in data["produits_tunisie"]:
            lines.append(f"  • {p['nom']} ({p['prix']})")
            lines.append(f"    Où trouver : {p['ou']}")
        lines.append("")

    if "etapes" in data:
        lines.append("📋 ÉTAPES :")
        for step in data["etapes"]:
            lines.append(f"  {step}")
        lines.append("")

    if "avertissement" in data:
        lines.append(f"⚠️  {data['avertissement']}")
        lines.append("")

    if "quand_voir_pro" in data:
        lines.append("⚠️  CONSULTEZ UN PROFESSIONNEL SI :")
        wvp = data["quand_voir_pro"]
        if isinstance(wvp, list):
            for r in wvp:
                lines.append(f"  • {r}")
        else:
            lines.append(f"  {wvp}")
        lines.append("")

    if "cout_pro_tunisie" in data:
        lines.append(f"💰 COÛT PROFESSIONNEL EN TUNISIE : {data['cout_pro_tunisie']}")

    return "\n".join(lines)