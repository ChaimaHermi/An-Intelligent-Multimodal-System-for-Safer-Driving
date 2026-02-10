import re
import spacy
import subprocess
import sys

# Try to load model, if not found, download it
def load_spacy_model():
    try:
        # First try medium model
        return spacy.load("fr_core_news_md")
    except OSError:
        try:
            # Try small model
            return spacy.load("fr_core_news_sm")
        except OSError:
            print("Downloading spaCy French model...")
            # Download the small model
            subprocess.check_call([sys.executable, "-m", "spacy", "download", "fr_core_news_sm"])
            return spacy.load("fr_core_news_sm")

# Load the model
nlp = load_spacy_model()

# ─────────────────────────────────────────────
#  KEYWORD DICTIONARY  (French)
#  Each category has: main keywords + synonyms + number patterns
# ─────────────────────────────────────────────

RISK_KEYWORDS = {

    "fatigue": [
        "fatigué", "fatigue", "épuisé", "épuisement",
        "somnolence", "somnolent", "endormi", "sommeil",
        "bâillement", "bâille", "yeux lourds", "j'ai sommeil",
        "pas dormi", "mal dormi", "nuit blanche",
        "conduis depuis", "roule depuis",
        r"\d+\s*h(eures)?",          # matches "5h", "5 heures"
        r"\d+\s*heure(s)?",
    ],

    "nuit": [
        "nuit", "nocturne", "soir", "minuit",
        "23h", "22h", "21h", "00h", "01h", "02h", "03h", "04h",
        "obscurité", "noir", "pas de lumière",
        "après minuit", "très tard",
        r"2[0-3]h", r"0[0-6]h",      # regex for night hours 20h-06h
    ],

    "pluie": [
        "pluie", "pleut", "pluvieux", "mouillé",
        "brouillard", "brume", "verglas",
        "neige", "grêle", "tempête",
        "chaussée glissante", "route mouillée",
        "mauvais temps", "visibilité réduite",
    ],

    "vitesse": [
        "vite", "trop vite", "vitesse",
        "dépasse", "dépassement", "accélère",
        r"1[3-9]\d\s*km",            # 130-199 km/h
        r"2\d{2}\s*km",              # 200+ km/h
        "fonce", "rapide", "à fond",
    ],

    "telephone": [
        "téléphone", "portable", "smartphone",
        "texto", "sms", "message", "appel",
        "whatsapp", "instagram", "réseaux",
        "navigation", "gps", "maps",
        "regarde mon téléphone", "écran",
    ],

    "alcool": [
        "alcool", "bu", "bière", "vin", "whisky",
        "verre", "soirée", "fête", "bar",
        "alcoolisé", "ivre", "soul",
        "apéro", "alcoolémie",
    ],

    "medicaments": [
        "médicament", "comprimé", "pilule",
        "somnifère", "anxiolytique", "antihistaminique",
        "doliprane", "lexomil", "xanax",
        "ordonnance", "traitement", "antidépresseur",
    ],

    "trafic": [
        "embouteillage", "bouchon", "trafic",
        "dense", "ralenti", "arrêté",
        "autoroute", "beaucoup de voitures",
        "heure de pointe", "rush",
    ],

    "longue_distance": [
        "long trajet", "longue route", "longue distance",
        "voyage", "des heures", "toute la journée",
        r"\d+\s*km",                 # any km mention
        "aller-retour", "traverser",
    ],
}


# ─────────────────────────────────────────────
#  NUMBER EXTRACTOR (for hours driven)
# ─────────────────────────────────────────────

def extract_hours_driven(text: str) -> float | None:
    """Extract how many hours the person has been driving."""
    patterns = [
        r"depuis\s+(\d+(?:\.\d+)?)\s*h",          # depuis 5h
        r"(\d+(?:\.\d+)?)\s*heure[s]?\s+de conduite",
        r"condui[st]\s+depuis\s+(\d+)",
        r"roule[s]?\s+depuis\s+(\d+)",
        r"(\d+)h\s+(?:de|sur)\s+la route",
    ]
    for pattern in patterns:
        match = re.search(pattern, text.lower())
        if match:
            return float(match.group(1))
    return None


# ─────────────────────────────────────────────
#  HOUR EXTRACTOR (for time of day)
# ─────────────────────────────────────────────

def extract_time_of_day(text: str) -> int | None:
    """Extract current hour from text (returns 0-23)."""
    patterns = [
        r"(\d{1,2})\s*h(?:eure)?s?",     # 23h, 23 heures
        r"il est\s+(\d{1,2})",
        r"(\d{1,2}):(\d{2})",             # 23:00
    ]
    for pattern in patterns:
        match = re.search(pattern, text.lower())
        if match:
            hour = int(match.group(1))
            if 0 <= hour <= 23:
                return hour
    return None


# ─────────────────────────────────────────────
#  MAIN EXTRACTOR FUNCTION
# ─────────────────────────────────────────────

def extract_risk_factors(text: str) -> dict:
    """
    Main function: analyze a French text and return all detected risk factors.

    Args:
        text: Raw user input in French

    Returns:
        dict with:
          - 'factors': list of detected risk category names
          - 'hours_driven': float or None
          - 'time_of_day': int (hour 0-23) or None
          - 'entities': spaCy named entities found
          - 'raw_text': original input
    """
    text_lower = text.lower()
    detected_factors = []

    # ── 1. Keyword matching ──────────────────
    for category, keywords in RISK_KEYWORDS.items():
        for kw in keywords:
            # Check if keyword is a regex pattern
            if kw.startswith(r"\d") or kw.startswith(r"[") or kw.startswith(r"2") and "\\" in kw:
                if re.search(kw, text_lower):
                    if category not in detected_factors:
                        detected_factors.append(category)
                    break
            else:
                if kw in text_lower:
                    if category not in detected_factors:
                        detected_factors.append(category)
                    break

    # ── 2. Special rule: hours driven ────────
    hours = extract_hours_driven(text)
    if hours is not None and hours >= 2.0:
        if "fatigue" not in detected_factors:
            detected_factors.append("fatigue")
        if hours >= 4.0 and "longue_distance" not in detected_factors:
            detected_factors.append("longue_distance")

    # ── 3. Special rule: night hours ─────────
    hour = extract_time_of_day(text)
    if hour is not None and (hour >= 20 or hour <= 6):
        if "nuit" not in detected_factors:
            detected_factors.append("nuit")

    # ── 4. spaCy NER (bonus entities) ────────
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]

    return {
        "factors": detected_factors,
        "hours_driven": hours,
        "time_of_day": hour,
        "entities": entities,
        "raw_text": text,
    }
# ─────────────────────────────────────────────
#  QUICK TEST  (run: python extractor.py)
# ─────────────────────────────────────────────

if __name__ == "__main__":
    test_inputs = [
        "Je conduis depuis 5 heures, il est 23h et il pleut fort.",
        "J'ai bu 2 verres de vin et je dois rentrer.",
        "Je suis sur mon téléphone depuis tout à l'heure, je roule vite.",
        "Je me sens très fatigué, j'ai pas dormi la nuit dernière.",
        "Trafic dense sur l'autoroute, je roule depuis 6h.",
    ]

    print("=" * 60)
    print("EXTRACTOR TEST")
    print("=" * 60)

    for text in test_inputs:
        result = extract_risk_factors(text)
        print(f"\n📝 Input : {text}")
        print(f"⚠️  Factors: {result['factors']}")
        if result['hours_driven']:
            print(f"🕐 Hours driven: {result['hours_driven']}h")
        if result['time_of_day'] is not None:
            print(f"🌙 Time of day: {result['time_of_day']}h")