"""
extractor.py
------------
Lightweight structural extraction: pulls numeric values (speed, hours,
time-of-day) and normalises LLM-produced factor lists against the known
vocabulary.  Keyword matching is kept only as a fast pre-filter before the
LLM analyser runs.
"""

import re

# ─────────────────────────────────────────────
#  VOCABULARIES  (used for normalisation only)
# ─────────────────────────────────────────────

VALID_RISK_FACTORS = {
    "fatigue", "nuit", "pluie", "vitesse", "telephone",
    "alcool", "medicaments", "trafic", "longue_distance",
}

VALID_INFRACTIONS = {
    "feu_rouge", "excès_vitesse", "stationnement_interdit",
    "ceinture", "telephone_volant", "alcool_volant",
    "defaut_assurance", "defaut_controle_technique",
    "refus_priorite", "sens_interdit", "depassement_interdit",
}

VALID_EMERGENCIES = {"accident", "blessé", "panne", "fuite", "incendie"}

# Synonyms the LLM might return → canonical form
FACTOR_SYNONYMS = {
    "somnolence": "fatigue", "endormissement": "fatigue",
    "épuisement": "fatigue", "nuit noire": "nuit",
    "météo": "pluie", "intempéries": "pluie", "verglas": "pluie",
    "excès de vitesse": "vitesse", "trop vite": "vitesse",
    "portable": "telephone", "smartphone": "telephone",
    "distraction": "telephone", "ivre": "alcool", "bu": "alcool",
    "somnifère": "medicaments", "traitement": "medicaments",
    "embouteillage": "trafic", "bouchon": "trafic",
    "long trajet": "longue_distance", "voyage": "longue_distance",
}

INFRACTION_SYNONYMS = {
    "feu rouge grillé": "feu_rouge",
    "griller feu": "feu_rouge",
    "radar": "excès_vitesse",
    "flashé": "excès_vitesse",
    "pas de ceinture": "ceinture",
    "sans assurance": "defaut_assurance",
    "visite technique": "defaut_controle_technique",
    "ligne continue": "depassement_interdit",
    "contresens": "sens_interdit",
}

# ─────────────────────────────────────────────
#  NUMERIC EXTRACTORS
# ─────────────────────────────────────────────

def extract_hours_driven(text: str) -> float | None:
    patterns = [
        r"depuis\s+(\d+(?:[.,]\d+)?)\s*h",
        r"(\d+(?:[.,]\d+)?)\s*heure[s]?\s+de conduite",
        r"condui[st]\s+depuis\s+(\d+)",
        r"roule[s]?\s+depuis\s+(\d+)",
        r"(\d+)\s*h\s+(?:de|sur)\s+la route",
    ]
    for p in patterns:
        m = re.search(p, text.lower())
        if m:
            return float(m.group(1).replace(",", "."))
    return None


def extract_time_of_day(text: str) -> int | None:
    m = re.search(r"\b(\d{1,2})\s*h(?:eure)?s?\b", text.lower())
    if m:
        h = int(m.group(1))
        if 0 <= h <= 23:
            return h
    m = re.search(r"\b(\d{1,2}):(\d{2})\b", text)
    if m:
        return int(m.group(1))
    return None


def extract_speed_value(text: str) -> int | None:
    m = re.search(r"(\d{2,3})\s*km(?:/h)?", text.lower())
    if m:
        return int(m.group(1))
    return None


# ─────────────────────────────────────────────
#  NORMALISATION
# ─────────────────────────────────────────────

def normalise_factors(raw: list) -> list:
    """Map LLM-produced factor strings → canonical vocabulary."""
    out = []
    for item in raw:
        item = item.lower().strip()
        canonical = FACTOR_SYNONYMS.get(item, item)
        if canonical in VALID_RISK_FACTORS and canonical not in out:
            out.append(canonical)
    return out


def normalise_infractions(raw: list) -> list:
    out = []
    for item in raw:
        item = item.lower().strip()
        canonical = INFRACTION_SYNONYMS.get(item, item)
        if canonical in VALID_INFRACTIONS and canonical not in out:
            out.append(canonical)
    return out


def normalise_emergencies(raw: list) -> list:
    out = []
    for item in raw:
        item = item.lower().strip()
        if item in VALID_EMERGENCIES and item not in out:
            out.append(item)
    return out


# ─────────────────────────────────────────────
#  AUTO-AUGMENT FROM NUMERIC VALUES
# ─────────────────────────────────────────────

def augment_factors(factors: list, hours: float | None, hour: int | None) -> list:
    """Infer additional factors from numeric extractions."""
    factors = list(factors)
    if hours is not None:
        if hours >= 2.0 and "fatigue" not in factors:
            factors.append("fatigue")
        if hours >= 4.0 and "longue_distance" not in factors:
            factors.append("longue_distance")
    if hour is not None and (hour >= 20 or hour <= 6):
        if "nuit" not in factors:
            factors.append("nuit")
    return factors


# ─────────────────────────────────────────────
#  FAST KEYWORD PRE-FILTER  (no LLM needed)
# ─────────────────────────────────────────────

# Maps a keyword that appears in text → factor/infraction/emergency it signals
_FAST_RISK = {
    "fatigué": "fatigue", "somnol": "fatigue", "endorm": "fatigue",
    "bâille": "fatigue", "yeux lourds": "fatigue", "sommeil": "fatigue",
    "pleut": "pluie", "pluie": "pluie", "brouillard": "pluie",
    "verglas": "pluie", "inondé": "pluie",
    "nuit": "nuit", "soir": "nuit",
    "téléphone": "telephone", "portable": "telephone", "sms": "telephone",
    "alcool": "alcool", "bu ": "alcool", "verre ": "alcool", "ivre": "alcool",
    "médicament": "medicaments", "comprimé": "medicaments",
    "bouchon": "trafic", "embouteillage": "trafic",
    "long trajet": "longue_distance", "depuis des heures": "longue_distance",
    "vite": "vitesse", "vitesse": "vitesse",
}
_FAST_INFRACTION = {
    "feu rouge": "feu_rouge", "grillé": "feu_rouge",
    "flashé": "excès_vitesse", "radar": "excès_vitesse",
    "sans ceinture": "ceinture", "ceinture": "ceinture",
    "sans assurance": "defaut_assurance", "assurance": "defaut_assurance",
    "contrôle technique": "defaut_controle_technique",
    "sens interdit": "sens_interdit",
}
_FAST_EMERGENCY = {
    "accident": "accident", "blessé": "blessé", "collision": "accident",
    "panne": "panne", "crevaison": "panne", "en feu": "incendie",
    "incendie": "incendie", "fuite": "fuite",
}


def fast_keyword_scan(text: str) -> dict:
    """
    Quick keyword scan to give the LLM a head-start and provide a
    fallback if the LLM is unavailable.
    Returns raw (non-normalised) lists.
    """
    tl = text.lower()
    factors, infractions, emergencies = [], [], []
    for kw, cat in _FAST_RISK.items():
        if kw in tl and cat not in factors:
            factors.append(cat)
    for kw, cat in _FAST_INFRACTION.items():
        if kw in tl and cat not in infractions:
            infractions.append(cat)
    for kw, cat in _FAST_EMERGENCY.items():
        if kw in tl and cat not in emergencies:
            emergencies.append(cat)

    hours = extract_hours_driven(text)
    hour  = extract_time_of_day(text)
    speed = extract_speed_value(text)

    factors = augment_factors(factors, hours, hour)

    return {
        "factors":     factors,
        "infractions": infractions,
        "emergencies": emergencies,
        "hours_driven": hours,
        "time_of_day":  hour,
        "speed_value":  speed,
    }