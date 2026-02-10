"""
main.py
-------
Connects all modules into a single pipeline.
Run as: python main.py
Or serve as API: uvicorn app.main:app --reload
"""

from extractor import extract_risk_factors
from scorer    import compute_risk
from retriever import RuleRetriever
from generator import generate_advice


# ─────────────────────────────────────────────
#  INITIALIZE (load once at startup)
# ─────────────────────────────────────────────

retriever = RuleRetriever()


# ─────────────────────────────────────────────
#  FULL PIPELINE FUNCTION
# ─────────────────────────────────────────────

def analyze_situation(user_input: str, backend: str = None) -> dict:
    """
    Full pipeline: text in → structured safety advice out.

    Args:
        user_input: raw French text from the user
        backend:    LLM backend ('openai', 'mistral', 'ollama')

    Returns:
        Complete analysis dict
    """

    # ── Step 1: NLP Extraction ────────────────
    extraction = extract_risk_factors(user_input)
    factors      = extraction["factors"]
    hours_driven = extraction["hours_driven"]

    # ── Step 2: Risk Scoring ──────────────────
    risk = compute_risk(factors, hours_driven)

    # ── Step 3: RAG Retrieval ─────────────────
    retrieved_rules = retriever.search(
        query   = user_input,
        top_k   = 3,
        factors = factors
    )
    context = retriever.format_context(retrieved_rules)

    # ── Step 4: LLM Generation ────────────────
    advice = generate_advice(
        situation     = user_input,
        risk          = risk,
        context_rules = context,
        backend       = backend
    )

    # ── Step 5: Assemble final response ───────
    return {
        # Risk summary
        "risk_level":   risk["level"],
        "risk_emoji":   risk["emoji"],
        "risk_score":   risk["score"],
        "risk_color":   risk["color"],

        # Detected factors
        "factors":      factors,
        "warnings":     risk["warnings"],
        "hours_driven": hours_driven,

        # LLM advice
        "explication":  advice["explication"],
        "conseils":     advice["conseils"],
        "message":      advice["message"],

        # Sources used
        "sources": [r.get("source", "Officielle") for r in retrieved_rules],
    }


# ─────────────────────────────────────────────
#  FASTAPI APP  (optional, for web/mobile UI)
# ─────────────────────────────────────────────

try:
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from pydantic import BaseModel

    app = FastAPI(
        title="🚗 Road Safety AI",
        description="Module 2 — Conseils de sécurité routière basés sur la situation",
        version="1.0.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    class SituationRequest(BaseModel):
        text: str
        backend: str = "ollama"

    @app.post("/analyze")
    async def analyze_endpoint(request: SituationRequest):
        """Main endpoint: analyze a driving situation."""
        result = analyze_situation(request.text, backend=request.backend)
        return result

    @app.get("/health")
    async def health():
        return {"status": "ok", "rules_loaded": len(retriever.rules)}

except ImportError:
    pass   # FastAPI not installed, CLI mode only


# ─────────────────────────────────────────────
#  CLI TEST  (run: python main.py)
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("🚗 ROAD SAFETY AI — FULL PIPELINE TEST")
    print("=" * 60)

    test_cases = [
        "Je conduis depuis 5 heures, il est 23h et il pleut fort.",
        "Je suis sur l'autoroute, beaucoup de trafic, j'ai mal dormi.",
        "J'ai bu 2 verres de vin et je dois rentrer chez moi.",
        "Un peu fatigué mais ça va, je roule depuis 2h.",
    ]

    for situation in test_cases:
        print(f"\n{'─'*60}")
        print(f"📝 SITUATION: {situation}")

        result = analyze_situation(situation)

        print(f"\n{result['risk_emoji']} NIVEAU: {result['risk_level']} (score={result['risk_score']}/12)")
        print(f"⚠️  FACTEURS: {result['factors']}")
        if result['warnings']:
            print(f"🚨 ALERTES: {result['warnings']}")

        print(f"\n💬 EXPLICATION:")
        print(f"   {result['explication']}")

        print(f"\n✅ CONSEILS:")
        for i, conseil in enumerate(result['conseils'], 1):
            print(f"   {i}. {conseil}")

        print(f"\n📣 MESSAGE: {result['message']}")
        print(f"📚 SOURCES: {result['sources']}")