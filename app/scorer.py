"""
scorer.py
---------
Risk scoring engine.
Risk is multiplicative + contextual, not just additive.
"""

# ─────────────────────────────────────────────
#  BASE WEIGHTS  (per factor, 1–5 scale)
# ─────────────────────────────────────────────

RISK_WEIGHTS = {
    "alcool":          5,   # zero tolerance in TN (0.3g/L)
    "fatigue":         4,
    "telephone":       4,
    "vitesse":         4,
    "nuit":            3,
    "pluie":           3,
    "medicaments":     3,
    "longue_distance": 2,
    "trafic":          1,
}

# ─────────────────────────────────────────────
#  COMBINATION MULTIPLIERS
#  (combo set) → (bonus pts, warning message)
# ─────────────────────────────────────────────

COMBO_BONUSES = [
    ({"fatigue", "nuit", "pluie"},       4, "⛔ Triple facteur critique : fatigue + nuit + pluie = risque x8"),
    ({"alcool", "vitesse"},              4, "⛔ Alcool + excès de vitesse = risque mortel immédiat"),
    ({"fatigue", "nuit"},                2, "🔴 Fatigue nocturne : vigilance maximale ou arrêt"),
    ({"alcool", "nuit"},                 2, "🔴 Alcool + conduite nocturne : stop immédiat"),
    ({"telephone", "vitesse"},           2, "🔴 Téléphone à grande vitesse : risque de collision majeur"),
    ({"medicaments", "alcool"},          3, "⛔ Médicaments + alcool : effet multiplicateur dangereux"),
    ({"fatigue", "longue_distance"},     2, "🔴 Fatigue de monotonie sur long trajet"),
    ({"pluie", "vitesse"},               2, "🔴 Pluie + vitesse : risque d'aquaplaning"),
]

# ─────────────────────────────────────────────
#  RISK LEVELS  (min_score, max_score, label, emoji, hex_color, description)
# ─────────────────────────────────────────────

RISK_LEVELS = [
    (0,  3,  "FAIBLE",   "🟢", "#22c55e",
     "Conduite globalement sûre. Restez vigilant."),
    (4,  6,  "MODÉRÉ",  "🟡", "#eab308",
     "Quelques facteurs à surveiller. Soyez prudent."),
    (7,  10, "ÉLEVÉ",   "🟠", "#f97316",
     "Risque significatif. Réduisez la vitesse, redoublez d'attention."),
    (11, 16, "CRITIQUE","🔴", "#ef4444",
     "Danger immédiat. Arrêtez-vous dès que possible en sécurité."),
    (17, 99, "EXTRÊME", "⛔", "#7f1d1d",
     "Risque extrême. Ne conduisez pas dans ces conditions."),
]

# ─────────────────────────────────────────────
#  CONTEXTUAL ADVICE  (per factor)
# ─────────────────────────────────────────────

FACTOR_ACTIONS = {
    "fatigue": [
        "Arrêtez-vous à la prochaine station ou aire de repos",
        "Faites une sieste de 15 à 20 minutes minimum",
        "Buvez un café et attendez 20 minutes avant de reprendre",
        "Si possible, changez de conducteur",
    ],
    "nuit": [
        "Réduisez votre vitesse de 20 km/h par rapport à la limite",
        "Allumez les feux de route hors agglomération si la voie est libre",
        "Augmentez votre distance de sécurité au double",
        "Restez attentif aux animaux sur les routes rurales tunisiennes",
    ],
    "pluie": [
        "Réduisez immédiatement votre vitesse de 20 km/h minimum",
        "Doublez la distance de sécurité avec le véhicule devant",
        "Allumez feux de croisement et essuie-glaces",
        "Ne traversez jamais un oued ou une route inondée",
    ],
    "vitesse": [
        "Respectez la limitation : 50 en ville, 90 sur route, 110 sur autoroute",
        "Adaptez votre vitesse aux conditions réelles (nuit, pluie, trafic)",
        "Anticipez les obstacles : regardez loin devant",
    ],
    "telephone": [
        "Posez votre téléphone hors de portée immédiate",
        "Activez le mode 'Ne pas déranger en voiture' (iOS / Android)",
        "Arrêtez-vous sur un parking pour passer vos appels",
    ],
    "alcool": [
        "Ne conduisez pas — appelez Bolt, InDriver ou un proche",
        "En Tunisie, la limite est 0.3g/L (2 verres peuvent suffire à dépasser)",
        "Attendez 1 heure par verre consommé MINIMUM avant de conduire",
        "Dormez sur place si vous avez trop bu",
    ],
    "medicaments": [
        "Lisez le pictogramme sur la boîte (orange ou rouge = dangereux)",
        "Consultez votre pharmacien ou médecin avant de conduire",
        "Évitez la conduite si vous ressentez des vertiges ou somnolence",
    ],
    "trafic": [
        "Maintenez 2 secondes de distance (règle des 2 secondes)",
        "Évitez les changements de voie brusques",
        "Surveillez les motos entre les files — pratique fréquente en Tunisie",
    ],
    "longue_distance": [
        "Planifiez une pause toutes les 2 heures",
        "Hydratez-vous régulièrement (1L pour 2h de route)",
        "En Tunisie : Tunis–Sfax = 1 pause min, Tunis–Tozeur = 3 pauses min",
    ],
}


# ─────────────────────────────────────────────
#  MAIN SCORING FUNCTION
# ─────────────────────────────────────────────

def compute_risk(factors: list, hours_driven: float | None = None) -> dict:
    """
    Compute a full risk assessment from detected factors.

    Args:
        factors:      list of risk category strings
        hours_driven: optional float (hours behind wheel)

    Returns:
        dict — score, level, color, emoji, warnings, actions
    """
    score = sum(RISK_WEIGHTS.get(f, 1) for f in factors)

    # Hours-driven bonus (contextual fatigue amplifier)
    if hours_driven is not None:
        if hours_driven >= 6:
            score += 3
        elif hours_driven >= 4:
            score += 2
        elif hours_driven >= 2:
            score += 1

    # Combination bonuses
    factors_set = set(factors)
    warnings = []
    for combo, bonus, msg in COMBO_BONUSES:
        if combo.issubset(factors_set):
            score += bonus
            warnings.append(msg)

    # Resolve level
    level_row = RISK_LEVELS[-1]
    for row in RISK_LEVELS:
        lo, hi = row[0], row[1]
        if lo <= score <= hi:
            level_row = row
            break

    _, _, level, emoji, color, description = level_row

    # Collect actions
    seen, actions = set(), []
    for f in factors:
        for a in FACTOR_ACTIONS.get(f, []):
            if a not in seen:
                seen.add(a)
                actions.append(a)

    return {
        "score":        min(score, 20),
        "level":        level,
        "emoji":        emoji,
        "color":        color,
        "description":  description,
        "factors":      factors,
        "warnings":     warnings,
        "actions":      actions[:5],
        "hours_driven": hours_driven,
    }