"""
main.py
-------
Road Safety AI — Tunisia
Unified pipeline (replaces main.py + main_v2.py + intent_analyzer.py)

Flow:
  user_input
    → fast_keyword_scan()        (instant, no LLM)
    → RuleRetriever.search()     (semantic RAG)
    → generate_unified()         (1 LLM call: intent + advice)
    → intent router              (enriches with Tunisia-specific data)
    → structured response

Intents:
  dangerous_situation  → risk scoring + RAG + LLM advice
  infraction_question  → Tunisia penalty FAQ
  infraction_committed → Tunisia penalty + LLM legal explanation
  emergency            → step-by-step procedures + contacts
  minor_damage         → repair guide + products
  prevention           → proactive safety tips
"""

from extractor      import fast_keyword_scan, normalise_factors, normalise_infractions, normalise_emergencies, augment_factors
from scorer         import compute_risk
from retriever      import RuleRetriever
from generator      import generate_unified, generate_penalty_advice
from repair_advisor import get_repair_advice, format_repair_advice
from tunisia_handler import (
    get_infraction_info,
    get_emergency_procedure,
    format_infraction_response,
    format_emergency_response,
    EMERGENCY_CONTACTS,
)

# ── Initialise once at startup ────────────────
retriever = RuleRetriever()


# ─────────────────────────────────────────────
#  INTENT HANDLERS
# ─────────────────────────────────────────────

def _handle_dangerous_situation(llm_result: dict, fast_scan: dict) -> dict:
    """Risk scoring + RAG-backed safety advice."""
    factors      = normalise_factors(llm_result.get("risk_factors", []) or fast_scan["factors"])
    factors      = augment_factors(factors, fast_scan.get("hours_driven"), fast_scan.get("time_of_day"))
    hours_driven = fast_scan.get("hours_driven")
    risk         = compute_risk(factors, hours_driven)

    return {
        "type":        "dangerous_situation",
        "risk_level":  risk["level"],
        "risk_emoji":  risk["emoji"],
        "risk_score":  risk["score"],
        "risk_color":  risk["color"],
        "factors":     factors,
        "warnings":    risk["warnings"],
        "explication": llm_result.get("explication"),
        "conseils":    llm_result.get("conseils", risk["actions"][:3]),
        "message":     llm_result.get("message", risk["description"]),
        "urgency":     llm_result.get("urgency_level", 2),
    }


def _handle_infraction_question(llm_result: dict, fast_scan: dict, backend: str) -> dict:
    """User asks a hypothetical infraction question → provide factual Tunisia law info."""
    infractions = normalise_infractions(llm_result.get("infractions", []) or fast_scan["infractions"])
    speed       = fast_scan.get("speed_value")

    penalty_data = get_infraction_info(infractions, speed)
    context      = format_infraction_response(penalty_data)

    advice = generate_penalty_advice(
        user_input=llm_result.get("raw_input", ""),
        context_rules=context,
        backend=backend,
    )

    return {
        "type":              "infraction_question",
        "infractions_asked": infractions,
        "amende_min":        penalty_data["total_amende_min"],
        "amende_max":        penalty_data["total_amende_max"],
        "permis_risque":     penalty_data["permis_risque"],
        "prison_risque":     penalty_data["prison_risque"],
        "explication":       advice.get("explication", context),
        "conseils":          advice.get("conseils", []),
        "message":           "💡 Mieux vaut prévenir que payer une amende — ou pire.",
        "raw_penalties":     context,
        "urgency":           1,
    }


def _handle_infraction_committed(llm_result: dict, fast_scan: dict, backend: str) -> dict:
    """User actually committed a violation → explain consequences and next steps."""
    infractions = normalise_infractions(llm_result.get("infractions", []) or fast_scan["infractions"])
    speed       = fast_scan.get("speed_value")

    penalty_data = get_infraction_info(infractions, speed)
    context      = format_infraction_response(penalty_data)

    custom_prompt = (
        f"L'utilisateur a RÉELLEMENT commis une ou plusieurs infractions.\n"
        f"Situation : \"{llm_result.get('raw_input', '')}\"\n\n"
        f"{context}\n\n"
        f"Réponds avec empathie mais fermeté. Explique les VRAIES conséquences légales "
        f"en Tunisie et ce qu'il doit faire MAINTENANT."
    )

    advice = generate_penalty_advice(
        user_input=custom_prompt,
        context_rules=context,
        backend=backend,
    )

    return {
        "type":           "infraction_committed",
        "infractions":    infractions,
        "amende_min":     penalty_data["total_amende_min"],
        "amende_max":     penalty_data["total_amende_max"],
        "permis_risque":  penalty_data["permis_risque"],
        "prison_risque":  penalty_data["prison_risque"],
        "fourriere_risque": penalty_data["fourriere_risque"],
        "explication":    advice.get("explication", context),
        "conseils":       advice.get("conseils", []),
        "message":        advice.get("message", "Régularisez votre situation rapidement."),
        "raw_penalties":  context,
        "urgency":        llm_result.get("urgency_level", 3),
    }


def _handle_emergency(llm_result: dict, fast_scan: dict) -> dict:
    """Real emergency — procedures + contacts. No LLM generation needed (speed priority)."""
    # Use LLM-detected emergencies, fall back to keyword scan
    emergencies = normalise_emergencies(
        llm_result.get("risk_factors", []) + (fast_scan.get("emergencies") or [])
    )
    # Also detect from raw keywords in input
    raw = llm_result.get("raw_input", "").lower()
    for kw, key in [
        ("accident", "accident"), ("blessé", "blessé"), ("collision", "accident"),
        ("panne", "panne"), ("crevaison", "panne"), ("batterie", "panne"),
        ("feu", "incendie"), ("incendie", "incendie"), ("fuite", "fuite"),
    ]:
        if kw in raw and key not in emergencies:
            emergencies.append(key)

    if not emergencies:
        emergencies = ["accident"]  # safest default

    em_data  = get_emergency_procedure(emergencies)
    formatted = format_emergency_response(em_data)

    all_steps = [
        step
        for proc in em_data["procedures"]
        for step in proc["etapes"]
    ]

    return {
        "type":           "emergency",
        "emergencies":    emergencies,
        "is_urgent":      em_data["is_urgent"],
        "primary_number": em_data["primary_number"],
        "procedures":     em_data["procedures"],
        "contacts":       em_data["contacts"],
        "formatted":      formatted,
        "explication":    "🆘 Situation d'urgence détectée. Suivez les étapes ci-dessous immédiatement.",
        "conseils":       all_steps[:6],
        "message": (
            f"🆘 Appelez le {em_data['primary_number']} MAINTENANT."
            if em_data["is_urgent"] else
            "Restez calme et suivez les étapes."
        ),
        "urgency": 5 if em_data["is_urgent"] else 4,
    }


def _handle_minor_damage(llm_result: dict, fast_scan: dict) -> dict:
    """Repair advice for minor vehicle damage."""
    raw     = llm_result.get("raw_input", "").lower()
    damage  = llm_result.get("damage_type") or "scratch"

    # Refine damage type from input
    if any(w in raw for w in ["parking", "accrochage", "stationné", "garé"]):
        damage = "parking_scratch"
    elif any(w in raw for w in ["bosse", "enfoncement", "accroc", "accrochage"]):
        damage = "minor_dent"
    elif any(w in raw for w in ["profond", "métal", "fond", "rouille"]):
        damage = "deep_scratch"
    else:
        damage = "scratch"

    repair_data = get_repair_advice(damage)
    formatted   = format_repair_advice(repair_data)

    # Build response without extra LLM call for minor damage
    steps = repair_data.get("etapes", [])[:4] if repair_data.get("found") else []

    return {
        "type":           "minor_damage",
        "damage_type":    damage,
        "repair_guide":   repair_data,
        "explication":    f"Voici comment réparer un {repair_data.get('titre', 'dégât mineur')} en Tunisie.",
        "conseils":       steps,
        "message":        "🔧 La plupart des petites réparations sont faisables soi-même si la peinture est intacte.",
        "formatted_guide":formatted,
        "urgency":        1,
    }


def _handle_prevention(llm_result: dict, fast_scan: dict, backend: str) -> dict:
    """Proactive safety advice — no immediate risk, just advice."""
    factors  = normalise_factors(llm_result.get("risk_factors", []) or fast_scan["factors"])
    retrieved = retriever.search(
        llm_result.get("raw_input", ""),
        top_k=3,
        factors=factors,
    )
    context  = retriever.format_context(retrieved)

    return {
        "type":        "prevention",
        "risk_factors":factors,
        "explication": llm_result.get("explication"),
        "conseils":    llm_result.get("conseils", []),
        "message":     llm_result.get("message", "🛡️ La meilleure protection est l'anticipation."),
        "sources":     [r.get("source") for r in retrieved],
        "urgency":     0,
    }


# ─────────────────────────────────────────────
#  MAIN PIPELINE
# ─────────────────────────────────────────────

def analyze_situation(user_input: str, backend: str = None) -> dict:
    """
    Full pipeline: French text in → structured response out.

    Args:
        user_input: raw French text from the driver
        backend:    'openai' | 'mistral' | 'ollama' (default: env LLM_BACKEND or 'ollama')

    Returns:
        Dict with type, explication, conseils, message + type-specific fields.
    """
    print(f"\n{'='*60}")
    print(f"📝 INPUT: {user_input}")
    print(f"{'='*60}")

    # ── Step 1: Fast keyword pre-scan (zero latency) ──────────
    fast_scan = fast_keyword_scan(user_input)
    print(f"⚡ Fast scan → factors={fast_scan['factors']}, "
          f"infractions={fast_scan['infractions']}, "
          f"emergencies={fast_scan['emergencies']}")

    # ── Step 2: Semantic RAG retrieval ────────────────────────
    all_factors = fast_scan["factors"] + fast_scan["infractions"]
    retrieved   = retriever.search(user_input, top_k=3, factors=all_factors)
    context     = retriever.format_context(retrieved)

    # ── Step 3: Single LLM call (intent + advice) ─────────────
    llm_result = generate_unified(user_input, fast_scan, context, backend=backend)
    intent     = llm_result.get("intent", "dangerous_situation")
    print(f"🎯 Intent: {intent} | Urgency: {llm_result.get('urgency_level', '?')}/5")

    # ── Step 4: Route to enricher ─────────────────────────────
    if intent == "emergency":
        result = _handle_emergency(llm_result, fast_scan)

    elif intent == "infraction_question":
        result = _handle_infraction_question(llm_result, fast_scan, backend)

    elif intent == "infraction_committed":
        result = _handle_infraction_committed(llm_result, fast_scan, backend)

    elif intent == "minor_damage":
        result = _handle_minor_damage(llm_result, fast_scan)

    elif intent == "prevention":
        result = _handle_prevention(llm_result, fast_scan, backend)

    else:
        # Default: dangerous_situation
        result = _handle_dangerous_situation(llm_result, fast_scan)

    # ── Step 5: Attach universal metadata ────────────────────
    result["raw_input"]     = user_input
    result["intent"]        = intent
    result["hours_driven"]  = fast_scan.get("hours_driven")
    result["speed_detected"]= fast_scan.get("speed_value")

    return result


# ─────────────────────────────────────────────
#  FASTAPI  (optional — pip install fastapi uvicorn)
# ─────────────────────────────────────────────

try:
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from pydantic import BaseModel

    app = FastAPI(
        title="🚗 Road Safety AI — Tunisia",
        description="Safety advice · Legal penalties · Emergency help · Repair guidance",
        version="3.0.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    class AnalysisRequest(BaseModel):
        text:    str
        backend: str = "ollama"

    @app.post("/analyze")
    async def analyze_endpoint(req: AnalysisRequest):
        return analyze_situation(req.text, backend=req.backend)

    @app.get("/health")
    async def health():
        return {"status": "ok", "rules_loaded": len(retriever.rules)}

    @app.get("/contacts")
    async def emergency_contacts():
        return EMERGENCY_CONTACTS

    @app.get("/penalties")
    async def list_penalties():
        from tunisia_handler import TUNISIA_PENALTIES
        return {
            k: {"infraction": v["infraction"], "amende": f"{v.get('amende_min',0)}–{v.get('amende_max',0)} DT"}
            for k, v in TUNISIA_PENALTIES.items()
        }

except ImportError:
    pass   # FastAPI not installed — CLI-only mode


# ─────────────────────────────────────────────
#  CLI TEST
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("🚗 ROAD SAFETY AI v3 — TUNISIA")
    print("=" * 60)

    test_cases = [
        # Dangerous situations
        "Je me sens un peu étourdi et il fait nuit sur la route Tunis–Sfax.",
        "J'ai bu deux verres de vin hier soir et j'ai un long trajet ce matin.",
        "Je conduis depuis 5 heures sur l'autoroute, il pleut fort et il est 23h.",

        # Infraction questions
        "C'est quoi l'amende si je grille un feu rouge en Tunisie ?",
        "Que se passe-t-il si je roule sans assurance ?",

        # Real infractions
        "J'ai été flashé à 140 km/h sur l'A1, que faire maintenant ?",
        "J'ai grillé un feu rouge hier à Tunis.",

        # Emergencies
        "J'ai eu un accident sur la route, l'autre conducteur est blessé, qui appeler ?",
        "Ma voiture est en panne sur l'autoroute de nuit.",

        # Minor damage
        "J'ai une rayure sur la portière, quel produit utiliser en Tunisie ?",

        # Prevention
        "Quels conseils pour conduire de nuit sur les routes rurales tunisiennes ?",
    ]

    for text in test_cases:
        print(f"\n{'─'*60}")
        result = analyze_situation(text)

        t = result["type"]
        print(f"\n📊 TYPE: {t.upper()}")

        if t == "emergency":
            print(f"📞 APPELER : {result['primary_number']}")
            for s in result["conseils"][:4]:
                print(f"  {s}")

        elif t in ("infraction_question", "infraction_committed"):
            print(f"💰 AMENDE : {result['amende_min']}–{result['amende_max']} DT")
            if result.get("permis_risque"):
                print("⚠️  PERMIS : Retrait possible")
            if result.get("prison_risque"):
                print("⛔ PRISON : Risque pénal")
            print(f"💬 {result.get('explication', '')[:120]}")

        elif t == "dangerous_situation":
            print(f"{result['risk_emoji']} RISQUE : {result['risk_level']} ({result['risk_score']}/20)")
            print(f"💬 {result.get('explication', '')[:120]}")
            for c in result.get("conseils", [])[:3]:
                print(f"  → {c}")

        elif t == "minor_damage":
            print(f"🔧 DÉGÂT : {result['damage_type']}")
            for c in result.get("conseils", [])[:3]:
                print(f"  {c}")

        else:
            print(f"💬 {result.get('explication', '')[:120]}")
            for c in result.get("conseils", [])[:3]:
                print(f"  → {c}")

        print(f"📣 {result.get('message', '')}")