"""
tunisia_handler.py
------------------
All Tunisia-specific data:
  - Traffic penalties (Code de la Route Tunisien, updated 2024)
  - Emergency procedures and contacts
  - Infraction info lookup
"""


# ─────────────────────────────────────────────
#  EMERGENCY CONTACTS  (official Tunisian numbers)
# ─────────────────────────────────────────────

EMERGENCY_CONTACTS = {
    "police":       {"name": "Police Nationale",              "number": "197"},
    "ambulance":    {"name": "SAMU — Urgences médicales",     "number": "190"},
    "pompiers":     {"name": "Protection Civile",             "number": "198"},
    "gendarmerie":  {"name": "Garde Nationale (routes nat.)", "number": "193"},
    "autoroute":    {"name": "STAP — Urgences autoroute",     "number": "71 861 000"},
    "universal":    {"name": "Numéro d'urgence universel",    "number": "1021"},
    "onas":         {"name": "ONAS — Inondations",            "number": "1818"},
    "remorquage":   {"name": "Assistance routière (variable)","number": "Voir carte verte"},
}


# ─────────────────────────────────────────────
#  TRAFFIC PENALTIES
#  Source: Code de la Route Tunisien (Loi 99-71 + amendements 2019/2024)
#  All amounts in TND (Tunisian Dinar)
# ─────────────────────────────────────────────

TUNISIA_PENALTIES = {

    "feu_rouge": {
        "infraction":    "Franchissement d'un feu rouge ou non-respect d'un signal Stop",
        "amende_min":    40,
        "amende_max":    120,
        "points":        3,
        "retrait_permis": False,
        "prison":        False,
        "notes": (
            "Amende 40–120 DT + retrait 3 points. En cas de récidive ou accident causé : "
            "majoration + suspension du permis possible. Constaté par agent ou caméra."
        ),
        "que_faire": [
            "Restez calme et coopérez avec l'agent.",
            "Acceptez le PV et payez dans les 30 jours (tarif réduit possible).",
            "Au-delà de 30 jours : majoration de 50%.",
            "En cas de contestation : tribunal de première instance du ressort.",
        ],
    },

    "excès_vitesse": {
        "infraction":    "Excès de vitesse",
        "paliers": [
            {"de": 1,  "a": 20,  "amende": 40,  "prison": False, "retrait": False,
             "label": "1–20 km/h au-dessus → 40 DT"},
            {"de": 21, "a": 40,  "amende": 80,  "prison": False, "retrait": True,
             "label": "21–40 km/h au-dessus → 80 DT + retrait temporaire possible"},
            {"de": 41, "a": 60,  "amende": 120, "prison": False, "retrait": True,
             "label": "41–60 km/h au-dessus → 120 DT + suspension 15–90 jours"},
            {"de": 61, "a": 999, "amende": 200, "prison": True,  "retrait": True,
             "label": "60+ km/h au-dessus → 200 DT min + suspension immédiate + prison possible"},
        ],
        "amende_min":    40,
        "amende_max":    500,
        "retrait_permis": True,
        "prison":        True,
        "notes": (
            "Radars fixes sur A1 (Bou Argoub km 62, Enfida km 120), A3 (Medjez el Bab), "
            "A4 (Borj Cedria). Radars mobiles réguliers sur GP1, GP7, GP11. "
            "Dépasser de 40+ km/h : suspension immédiate sur place."
        ),
        "que_faire": [
            "Acceptez le PV de l'agent ou attendez le courrier si flashé par radar.",
            "Payez dans les 30 jours pour éviter la majoration.",
            "Si permis retiré : ne conduisez pas jusqu'à restitution officielle.",
            "Récidive dans les 12 mois : sanctions doublées.",
        ],
    },

    "stationnement_interdit": {
        "infraction":    "Stationnement irrégulier ou gênant",
        "amende_min":    20,
        "amende_max":    80,
        "points":        0,
        "retrait_permis": False,
        "prison":        False,
        "fourriere":     True,
        "notes": (
            "Mise en fourrière possible. Frais : 30–80 DT + 10 DT/jour supplémentaire. "
            "Vous devez régler amende + frais de fourrière pour récupérer le véhicule. "
            "Zones interdites : double file, sur trottoir, face sortie de garage, "
            "sur passage piéton, zone rouge."
        ),
        "que_faire": [
            "Si sabot (roue bloquée) : payez au bureau de police du secteur.",
            "Si fourrière : appelez le commissariat local pour connaître l'adresse.",
            "Présentez permis + carte grise + reçu de paiement pour récupérer le véhicule.",
            "Agissez vite — les frais augmentent chaque jour.",
        ],
    },

    "ceinture": {
        "infraction":    "Non-port de la ceinture de sécurité",
        "amende_min":    20,
        "amende_max":    40,
        "points":        0,
        "retrait_permis": False,
        "prison":        False,
        "notes": (
            "Obligatoire pour conducteur ET tous les passagers (y compris sièges arrière). "
            "Amende par personne non attachée dans le véhicule. "
            "Un passager arrière non ceinturé projeté en avant peut tuer le conducteur."
        ),
        "que_faire": [
            "Acceptez le PV et payez l'amende.",
            "Attachez immédiatement votre ceinture et celle de vos passagers.",
            "En Tunisie, les contrôles ceinture sont fréquents aux checkpoints.",
        ],
    },

    "telephone_volant": {
        "infraction":    "Usage du téléphone portable en conduisant",
        "amende_min":    40,
        "amende_max":    100,
        "points":        2,
        "retrait_permis": False,
        "prison":        False,
        "notes": (
            "Interdit même à l'arrêt au feu rouge ou dans un embouteillage. "
            "Seul le kit mains-libres intégré au tableau de bord est toléré. "
            "Tenir le téléphone à la main suffit à constituer l'infraction."
        ),
        "que_faire": [
            "Acceptez le PV.",
            "Activez le mode mains-libres ou rangez le téléphone avant de rouler.",
            "En cas de contestation : tribunal du ressort (preuve vidéo souvent utilisée).",
        ],
    },

    "alcool_volant": {
        "infraction":    "Conduite en état d'ivresse (taux > 0.3 g/L en Tunisie)",
        "amende_min":    300,
        "amende_max":    1000,
        "points":        None,
        "retrait_permis": True,
        "prison":        True,
        "notes": (
            "⚠️ ATTENTION : Le taux légal en Tunisie est 0.3 g/L (plus strict que la France). "
            "Suspension immédiate du permis 1 à 6 mois. Emprisonnement 15 jours à 1 an "
            "(Code Pénal Tunisien Art. 284). Si accident causé sous alcool : prison jusqu'à 5 ans. "
            "Refus d'éthylomètre = infraction supplémentaire."
        ),
        "que_faire": [
            "Coopérez avec les forces de l'ordre — le refus aggrave la situation.",
            "Ne refusez pas l'éthylomètre : c'est une infraction supplémentaire.",
            "Contactez immédiatement un avocat si vous êtes arrêté.",
            "Ne conduisez plus jusqu'à restitution officielle du permis.",
        ],
    },

    "defaut_assurance": {
        "infraction":    "Conduite sans assurance responsabilité civile (RC)",
        "amende_min":    100,
        "amende_max":    500,
        "points":        None,
        "retrait_permis": True,
        "prison":        True,
        "fourriere":     True,
        "notes": (
            "L'assurance RC est obligatoire pour tout véhicule en circulation en Tunisie. "
            "Le véhicule peut être immobilisé sur place. En cas d'accident sans assurance : "
            "responsabilité personnelle TOTALE pour tous les dommages corporels et matériels, "
            "sans plafond légal — potentiellement des millions de dinars."
        ),
        "que_faire": [
            "Contactez votre assureur immédiatement pour régulariser.",
            "Présentez une attestation valide à l'agent pour levée de saisie.",
            "Sans assurance valide : NE REPRENEZ PAS LA ROUTE.",
            "L'assurance RC de base coûte 150–400 DT/an selon le véhicule.",
        ],
    },

    "defaut_controle_technique": {
        "infraction":    "Défaut de contrôle technique (visite technique)",
        "amende_min":    30,
        "amende_max":    80,
        "points":        0,
        "retrait_permis": False,
        "prison":        False,
        "notes": (
            "Visite technique annuelle obligatoire pour tout véhicule de plus de 3 ans. "
            "Centres agréés : SOTAC, CTAC, COTUSAL dans tous les gouvernorats. "
            "Coût : 30–60 DT. Vignette technique visible sur le pare-brise."
        ),
        "que_faire": [
            "Acceptez le PV.",
            "Prenez rendez-vous au centre de contrôle technique dès que possible.",
            "Évitez de circuler si l'agent impose l'immobilisation.",
            "En cas de vignette périmée depuis moins de 3 mois : régularisation sans suite possible.",
        ],
    },

    "refus_priorite": {
        "infraction":    "Refus de priorité / non-respect d'un Stop",
        "amende_min":    40,
        "amende_max":    100,
        "points":        2,
        "retrait_permis": False,
        "prison":        False,
        "notes": (
            "Cause fréquente d'accidents graves en Tunisie. En cas d'accident : "
            "responsabilité entière engagée. Aux ronds-points : priorité aux véhicules "
            "déjà engagés dans le giratoire (priorité à gauche)."
        ),
        "que_faire": [
            "Acceptez le PV.",
            "Si accident : établissez le constat amiable immédiatement.",
            "Prévenez votre assurance dans les 24 heures.",
        ],
    },

    "sens_interdit": {
        "infraction":    "Circulation en sens interdit / contresens",
        "amende_min":    40,
        "amende_max":    120,
        "points":        3,
        "retrait_permis": False,
        "prison":        False,
        "notes": (
            "Très dangereux et lourdement sanctionné. En cas d'accident en contresens : "
            "responsabilité totale du conducteur en infraction. Sur autoroute en contresens : "
            "amende maximale + poursuite pénale."
        ),
        "que_faire": [
            "Rebroussez chemin immédiatement et prudemment.",
            "Allumez les feux de détresse pendant la manœuvre.",
            "Acceptez le PV.",
            "Si accident : appelez le 197 (police) et le 190 (SAMU si blessés).",
        ],
    },

    "depassement_interdit": {
        "infraction":    "Dépassement dangereux ou sur ligne continue",
        "amende_min":    40,
        "amende_max":    120,
        "points":        3,
        "retrait_permis": False,
        "prison":        False,
        "notes": (
            "Principale cause d'accidents frontaux mortels sur les routes tunisiennes (GP1, GP7). "
            "Ne dépassez que si vous voyez clairement sur 400+ mètres et si la voie est libre. "
            "Dépassement en zone de virages ou en sommet de côte = infraction grave."
        ),
        "que_faire": [
            "Acceptez le PV.",
            "Sur route à double sens : ne doublez jamais sur ligne continue ou en virage.",
        ],
    },
}


# ─────────────────────────────────────────────
#  EMERGENCY PROCEDURES
# ─────────────────────────────────────────────

EMERGENCY_PROCEDURES = {

    "accident": {
        "titre":   "Accident de la route",
        "urgence": True,
        "etapes": [
            "🚨 Allumez immédiatement les feux de détresse.",
            "🦺 Enfilez votre gilet fluorescent AVANT de sortir du véhicule.",
            "⛔ Placez le triangle de sécurité à 150 m en amont.",
            "📞 Appelez le 190 (SAMU) si des blessés sont présents.",
            "📞 Appelez le 197 (Police) ou 193 (Garde Nationale) pour le constat officiel.",
            "🚫 Ne déplacez pas les blessés sauf danger immédiat (incendie, noyade).",
            "📸 Photographiez les positions des véhicules AVANT de les déplacer.",
            "📋 Remplissez le constat amiable avec l'autre conducteur.",
            "📞 Prévenez votre assurance dans les 24 heures (obligatoire légalement).",
        ],
        "contacts": ["ambulance", "police", "gendarmerie"],
        "warning":  "Ne reconnaissez JAMAIS votre responsabilité verbalement. Attendez l'évaluation officielle.",
    },

    "blessé": {
        "titre":   "Blessé grave sur la route",
        "urgence": True,
        "etapes": [
            "📞 Appelez le 190 (SAMU) EN PREMIER.",
            "🔴 Signalez précisément : localisation GPS ou nom de la route + km, nombre de blessés, état de conscience.",
            "🚫 Ne déplacez pas un blessé sauf danger immédiat (feu, risque de noyade).",
            "🩸 En cas de saignement abondant : compression directe sur la plaie avec un tissu propre.",
            "🫁 Si la personne ne respire pas et que vous êtes formé : massage cardiaque (30 compressions / 2 insufflations).",
            "🏥 Le SAMU (190) vous guidera par téléphone jusqu'à l'arrivée des secours.",
        ],
        "contacts": ["ambulance", "pompiers"],
        "warning":  "Ne donnez jamais à boire à un blessé inconscient. Gardez-le immobile.",
    },

    "panne": {
        "titre":   "Panne ou immobilisation sur route",
        "urgence": False,
        "etapes": [
            "💡 Allumez immédiatement les feux de détresse.",
            "🚗 Garez-vous sur le bas-côté droit ou la bande d'arrêt d'urgence (autoroute).",
            "🦺 Enfilez le gilet fluorescent AVANT de sortir.",
            "⛔ Placez le triangle à 150 m derrière (200 m sur autoroute).",
            "🛣️ Sur autoroute : éloignez-vous de la voie, restez derrière la glissière de sécurité.",
            "📞 Sur autoroute : appelez le 71 861 000 (STAP) ou utilisez les bornes SOS oranges (tous les 2 km).",
            "📞 En dehors de l'autoroute : appelez le 197 ou votre assistance dépannage.",
        ],
        "contacts": ["police", "autoroute", "remorquage"],
        "warning":  "Ne restez JAMAIS dans votre véhicule immobilisé sur l'autoroute — sortez et éloignez-vous.",
    },

    "fuite": {
        "titre":   "Délit de fuite après accident",
        "urgence": False,
        "etapes": [
            "📞 Appelez le 197 (Police) ou 193 (Garde Nationale) immédiatement.",
            "📝 Notez tout ce dont vous vous souvenez : couleur, marque, immatriculation (même partielle).",
            "📸 Photographiez vos dégâts et la scène de l'accident.",
            "👥 Cherchez des témoins et demandez leurs coordonnées.",
            "📹 Signalez la présence éventuelle de caméras de surveillance.",
            "📋 Déposez une plainte au commissariat dans les 24 heures.",
            "📞 Prévenez votre assurance (délit de fuite couvert si contrat tous risques).",
        ],
        "contacts": ["police", "gendarmerie"],
        "warning":  "Ne poursuivez JAMAIS un conducteur en fuite — c'est dangereux et illégal.",
    },

    "incendie": {
        "titre":   "Incendie du véhicule",
        "urgence": True,
        "etapes": [
            "🚗 Arrêtez le véhicule IMMÉDIATEMENT et coupez le contact.",
            "🚪 Sortez du véhicule en urgence avec TOUS les passagers.",
            "🏃 Éloignez-vous d'au moins 50 mètres — un réservoir peut exploser.",
            "📞 Appelez le 198 (Protection Civile) immédiatement.",
            "🚫 N'essayez PAS d'éteindre un incendie important seul.",
            "⚠️  Prévenez les autres usagers du danger (signes, triangle).",
        ],
        "contacts": ["pompiers", "police"],
        "warning":  "Un réservoir d'essence peut exploser. NE RESTEZ JAMAIS près d'un véhicule en feu.",
    },
}


# ─────────────────────────────────────────────
#  HANDLER FUNCTIONS
# ─────────────────────────────────────────────

def get_infraction_info(infractions: list, speed_value: int = None) -> dict:
    """Return full penalty information for a list of infractions."""
    results = []

    for key in infractions:
        info = TUNISIA_PENALTIES.get(key)
        if not info:
            continue
        entry = {"key": key, **info}

        # Speed fine: calculate based on detected speed vs assumed limit
        if key == "excès_vitesse" and speed_value:
            limit = 90   # default assumed limit (GP road)
            # Try to pick a better limit based on speed context
            if speed_value <= 80:
                limit = 50
            elif speed_value <= 100:
                limit = 90
            else:
                limit = 110  # could be autoroute

            excess = max(0, speed_value - limit)
            if excess > 0:
                for palier in info["paliers"]:
                    if palier["de"] <= excess < palier["a"]:
                        entry["amende_calculee"] = palier["amende"]
                        entry["palier_actif"]    = palier["label"]
                        entry["excès_km"]        = excess
                        entry["limite_assumee"]  = limit
                        break

        results.append(entry)

    return {
        "infractions_count": len(results),
        "details":           results,
        "total_amende_min":  sum(r.get("amende_min", 0) for r in results),
        "total_amende_max":  sum(r.get("amende_max", 0) for r in results),
        "permis_risque":     any(r.get("retrait_permis") for r in results),
        "prison_risque":     any(r.get("prison") for r in results),
        "fourriere_risque":  any(r.get("fourriere") for r in results),
    }


def get_emergency_procedure(emergencies: list) -> dict:
    """Return step-by-step procedures + contacts for detected emergencies."""
    procedures, contacts = [], set()

    for key in emergencies:
        proc = EMERGENCY_PROCEDURES.get(key)
        if proc:
            procedures.append({"key": key, **proc})
            contacts.update(proc.get("contacts", []))

    procedures.sort(key=lambda x: x.get("urgence", False), reverse=True)

    contacts_detail = {
        k: EMERGENCY_CONTACTS[k]
        for k in contacts if k in EMERGENCY_CONTACTS
    }

    is_urgent      = any(p.get("urgence") for p in procedures)
    primary_number = "190" if is_urgent else "197"

    return {
        "procedures":      procedures,
        "contacts":        contacts_detail,
        "is_urgent":       is_urgent,
        "primary_number":  primary_number,
    }


def format_infraction_response(data: dict) -> str:
    """Format infraction info into a clean French string for LLM context."""
    lines = ["📋 INFRACTIONS ET SANCTIONS — CODE DE LA ROUTE TUNISIEN :\n"]

    for d in data["details"]:
        lines.append(f"🚨 {d['infraction']}")
        if "amende_calculee" in d:
            lines.append(
                f"   💰 Amende estimée : {d['amende_calculee']} DT "
                f"({d['palier_actif']}, limite assumée {d.get('limite_assumee', 90)} km/h)"
            )
        elif "amende_min" in d:
            lines.append(f"   💰 Amende : {d['amende_min']} à {d['amende_max']} DT")
        if d.get("retrait_permis"):
            lines.append("   ⚠️  Retrait / suspension de permis possible")
        if d.get("prison"):
            lines.append("   ⛔ Emprisonnement possible")
        if d.get("fourriere"):
            lines.append("   🚗 Mise en fourrière possible")
        lines.append(f"   📌 {d['notes']}")
        lines.append("")

    lines.append(f"💸 Amende totale estimée : {data['total_amende_min']}–{data['total_amende_max']} DT")
    if data["permis_risque"]:
        lines.append("⚠️  RISQUE : Retrait ou suspension du permis de conduire")
    if data["prison_risque"]:
        lines.append("⛔ RISQUE : Poursuites pénales / emprisonnement possible")

    return "\n".join(lines)


def format_emergency_response(data: dict) -> str:
    """Format emergency procedures into a readable French string."""
    lines = []
    if data["is_urgent"]:
        lines.append(f"🆘 URGENCE — Appelez le {data['primary_number']} MAINTENANT\n")

    for proc in data["procedures"]:
        lines.append(f"📍 {proc['titre']}\n")
        for step in proc["etapes"]:
            lines.append(f"  {step}")
        if proc.get("warning"):
            lines.append(f"\n  ⚠️  IMPORTANT : {proc['warning']}")
        lines.append("")

    if data["contacts"]:
        lines.append("📞 NUMÉROS UTILES EN TUNISIE :")
        for _, contact in data["contacts"].items():
            lines.append(f"  • {contact['name']} : {contact['number']}")

    return "\n".join(lines)