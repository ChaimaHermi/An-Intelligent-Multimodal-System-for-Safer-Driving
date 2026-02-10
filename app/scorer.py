"""
scorer.py
---------
Takes the list of detected risk factors and computes a danger score.
Returns a structured risk assessment with level, score, and color.
"""


# ─────────────────────────────────────────────
#  RISK WEIGHTS
#  Higher = more dangerous
# ─────────────────────────────────────────────

RISK_WEIGHTS = {
    "fatigue":        3,
    "nuit":           2,
    "pluie":          2,
    "vitesse":        3,
    "telephone":      3,
    "alcool":         4,   # highest: zero tolerance
    "medicaments":    2,
    "trafic":         1,
    "longue_distance": 2,
}

# Bonus: combinations that are especially dangerous together
COMBINATION_BONUSES = [
    ({"fatigue", "nuit"},           2, "Fatigue + nuit = combo très dangereux"),
    ({"fatigue", "nuit", "pluie"},  2, "Triple risque critique"),
    ({"alcool", "vitesse"},         3, "Alcool + excès de vitesse = risque mortel"),
    ({"telephone", "vitesse"},      2, "Téléphone + vitesse = très dangereux"),
    ({"alcool", "nuit"},            2, "Alcool + conduite nocturne"),
    ({"fatigue", "longue_distance"},1, "Longue distance + fatigue"),
]


# ─────────────────────────────────────────────
#  RISK LEVELS
# ─────────────────────────────────────────────

RISK_LEVELS = [
    (0,  2,  "FAIBLE",    "🟢", "#22c55e", "Conduite globalement sûre. Restez vigilant."),
    (3,  4,  "MODÉRÉ",   "🟡", "#eab308", "Quelques facteurs à surveiller. Soyez prudent."),
    (5,  7,  "ÉLEVÉ",    "🟠", "#f97316", "Risque significatif. Réduisez la vitesse et redoublez d'attention."),
    (8,  11, "CRITIQUE", "🔴", "#ef4444", "Danger immédiat. Arrêtez-vous dès que possible."),
    (12, 99, "EXTRÊME",  "⛔", "#7f1d1d", "Risque extrême. Ne conduisez pas dans ces conditions."),
]


# ─────────────────────────────────────────────
#  ADVICE ACTIONS (per factor)
#  These feed into the LLM as structured hints
# ─────────────────────────────────────────────

FACTOR_ACTIONS = {
    "fatigue": [
        "Arrêtez-vous à la prochaine aire de repos",
        "Faites une sieste de 20 minutes",
        "Changez de conducteur si possible",
        "Ne repartez que lorsque vous vous sentez alerte",
    ],
    "nuit": [
        "Réduisez votre vitesse de 20 km/h",
        "Augmentez la distance de sécurité",
        "Allumez vos feux de route si la route est déserte",
        "Faites des pauses plus fréquentes la nuit",
    ],
    "pluie": [
        "Réduisez votre vitesse immédiatement",
        "Doublez la distance de sécurité avec le véhicule devant",
        "Allumez vos feux de croisement",
        "Évitez les freinages brusques",
    ],
    "vitesse": [
        "Respectez les limitations de vitesse",
        "Adaptez votre vitesse à la visibilité",
        "Anticipez les obstacles plus tôt",
    ],
    "telephone": [
        "Posez votre téléphone hors de portée",
        "Activez le mode 'Ne pas déranger'",
        "Arrêtez-vous pour passer vos appels",
    ],
    "alcool": [
        "Ne conduisez pas — appelez un taxi ou un proche",
        "Attendez minimum 2h par verre consommé",
        "Dormez avant de reprendre la route",
    ],
    "medicaments": [
        "Vérifiez le pictogramme sur la boîte (catégorie 2 ou 3 = dangereux)",
        "Consultez un médecin avant de conduire sous traitement",
        "Évitez de conduire si vous ressentez des effets",
    ],
    "trafic": [
        "Maintenez 2 secondes de distance avec le véhicule devant",
        "Évitez les changements de file brusques",
        "Restez patient et anticipez les freinages",
    ],
    "longue_distance": [
        "Planifiez une pause toutes les 2 heures",
        "Hydratez-vous régulièrement",
        "Préférez repartir après une nuit de repos",
    ],
}


# ─────────────────────────────────────────────
#  MAIN SCORING FUNCTION
# ─────────────────────────────────────────────

def compute_risk(factors: list, hours_driven: float = None) -> dict:
    """
    Compute a full risk assessment from detected factors.

    Args:
        factors: list of risk category strings (from extractor.py)
        hours_driven: optional float, number of hours driven

    Returns:
        dict with score, level, color, emoji, warnings, and actions
    """

    # ── Base score from weights ───────────────
    score = sum(RISK_WEIGHTS.get(f, 1) for f in factors)

    # ── Add hours-driven bonus ────────────────
    if hours_driven is not None:
        if hours_driven >= 5:
            score += 2
        elif hours_driven >= 3:
            score += 1

    # ── Combination bonuses ───────────────────
    factors_set = set(factors)
    active_warnings = []
    for combo, bonus, warning in COMBINATION_BONUSES:
        if combo.issubset(factors_set):
            score += bonus
            active_warnings.append(warning)

    # ── Get risk level ────────────────────────
    level_info = RISK_LEVELS[-1]   # default = highest
    for low, high, label, emoji, color, description in RISK_LEVELS:
        if low <= score <= high:
            level_info = (low, high, label, emoji, color, description)
            break

    _, _, level, emoji, color, description = level_info

    # ── Collect relevant actions ──────────────
    all_actions = []
    for factor in factors:
        actions = FACTOR_ACTIONS.get(factor, [])
        all_actions.extend(actions)

    # Remove duplicates while preserving order
    seen = set()
    unique_actions = []
    for action in all_actions:
        if action not in seen:
            seen.add(action)
            unique_actions.append(action)

    # Keep top 4 actions max
    top_actions = unique_actions[:4]

    return {
        "score":        min(score, 12),    # cap at 12
        "level":        level,
        "emoji":        emoji,
        "color":        color,
        "description":  description,
        "factors":      factors,
        "warnings":     active_warnings,
        "actions":      top_actions,
        "hours_driven": hours_driven,
    }


# ─────────────────────────────────────────────
#  QUICK TEST  (run: python scorer.py)
# ─────────────────────────────────────────────

if __name__ == "__main__":
    test_cases = [
        (["trafic"],                                   None),
        (["pluie", "nuit"],                            None),
        (["fatigue", "nuit", "pluie"],                 5.0),
        (["alcool", "vitesse", "nuit"],                None),
        (["fatigue", "telephone", "longue_distance"],  6.0),
    ]

    print("=" * 60)
    print("SCORER TEST")
    print("=" * 60)

    for factors, hours in test_cases:
        result = compute_risk(factors, hours)
        print(f"\n⚠️  Factors  : {factors}")
        print(f"🕐 Hours     : {hours}h")
        print(f"{result['emoji']} Level    : {result['level']}  (score={result['score']})")
        print(f"💬 Desc      : {result['description']}")
        if result['warnings']:
            print(f"🚨 Warnings  : {result['warnings']}")
        print(f"✅ Actions   : {result['actions'][:2]}")  # show first 2