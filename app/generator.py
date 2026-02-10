"""
generator.py
------------
LLM module: takes the analyzed situation + risk score + retrieved rules
and generates a clear, personalized safety advice in French.

Supports: OpenAI API, Mistral API, or local Ollama (free)
"""

import os
import json
from typing import Literal


# ─────────────────────────────────────────────
#  BACKEND SELECTION
#  Set LLM_BACKEND in your environment:
#    export LLM_BACKEND=openai    (needs API key)
#    export LLM_BACKEND=mistral   (needs API key)
#    export LLM_BACKEND=ollama    (free, local)
# ─────────────────────────────────────────────

LLM_BACKEND = os.getenv("LLM_BACKEND", "ollama")   # default = free local


# ─────────────────────────────────────────────
#  SYSTEM PROMPT
# ─────────────────────────────────────────────

SYSTEM_PROMPT = """Tu es un assistant expert en sécurité routière, bienveillant mais direct.
Ton rôle est d'aider les conducteurs à comprendre les risques et à prendre les bonnes décisions.

Règles de réponse:
- Toujours répondre en français
- Être direct et concret, jamais vague
- Utiliser des faits chiffrés quand disponibles
- Éviter le jargon technique
- Ton ton est celui d'un ami expert, pas d'un robot
- Ne jamais minimiser un risque réel"""


# ─────────────────────────────────────────────
#  PROMPT BUILDER
# ─────────────────────────────────────────────

def build_prompt(situation: str, risk: dict, context_rules: str) -> str:
    """Build the full prompt to send to the LLM."""

    factors_str = ", ".join(risk["factors"]) if risk["factors"] else "aucun facteur majeur"
    actions_hint = "\n".join([f"- {a}" for a in risk["actions"][:3]])
    warnings_str = " | ".join(risk["warnings"]) if risk["warnings"] else ""

    prompt = f"""SITUATION DU CONDUCTEUR:
"{situation}"

ANALYSE DE RISQUE:
- Facteurs détectés: {factors_str}
- Niveau de danger: {risk['emoji']} {risk['level']} (score: {risk['score']}/12)
- Avertissements spéciaux: {warnings_str if warnings_str else "aucun"}

RÈGLES DE SÉCURITÉ PERTINENTES:
{context_rules}

ACTIONS SUGGÉRÉES (à reformuler naturellement):
{actions_hint}

---
Génère une réponse structurée avec EXACTEMENT ce format JSON:

{{
  "explication": "1-2 phrases expliquant POURQUOI cette situation est dangereuse. Cite un chiffre si possible.",
  "conseils": [
    "Conseil 1 concret et actionnable",
    "Conseil 2 concret et actionnable",
    "Conseil 3 concret et actionnable"
  ],
  "message": "Une phrase courte d'encouragement ou d'avertissement fort selon le niveau de risque.",
  "urgence": "{risk['level']}"
}}

Réponds UNIQUEMENT avec le JSON, sans texte avant ou après."""

    return prompt


# ─────────────────────────────────────────────
#  LLM BACKENDS
# ─────────────────────────────────────────────

def _call_openai(prompt: str) -> str:
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o-mini",     # cheap and fast
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": prompt}
        ],
        temperature=0.4,
        max_tokens=500,
    )
    return response.choices[0].message.content


def _call_mistral(prompt: str) -> str:
    from mistralai.client import MistralClient
    from mistralai.models.chat_completion import ChatMessage
    client = MistralClient(api_key=os.getenv("MISTRAL_API_KEY"))
    response = client.chat(
        model="mistral-small-latest",
        messages=[
            ChatMessage(role="system", content=SYSTEM_PROMPT),
            ChatMessage(role="user",   content=prompt),
        ],
        temperature=0.4,
        max_tokens=500,
    )
    return response.choices[0].message.content


def _call_ollama(prompt: str, model: str = "mistral") -> str:
    """
    Use local Ollama (free, no API key needed).
    Install: https://ollama.ai
    Run:     ollama pull mistral
    """
    import requests
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model,
            "prompt": f"{SYSTEM_PROMPT}\n\n{prompt}",
            "stream": False,
            "options": {"temperature": 0.4}
        },
        timeout=60,
    )
    return response.json()["response"]


def _parse_llm_response(raw: str) -> dict:
    """Parse the JSON response from the LLM, with fallback."""
    raw = raw.strip()

    # Remove markdown code blocks if present
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # Fallback: return structured error response
        return {
            "explication": "Situation à risque détectée. Veuillez être prudent.",
            "conseils": [
                "Réduisez votre vitesse",
                "Augmentez la distance de sécurité",
                "Arrêtez-vous si vous vous sentez en danger",
            ],
            "message": "Votre sécurité est la priorité.",
            "urgence": "MODÉRÉ",
        }


# ─────────────────────────────────────────────
#  MAIN GENERATOR FUNCTION
# ─────────────────────────────────────────────

def generate_advice(
    situation: str,
    risk: dict,
    context_rules: str,
    backend: str = None
) -> dict:
    """
    Generate personalized safety advice using an LLM.

    Args:
        situation:     original user input
        risk:          result from scorer.compute_risk()
        context_rules: formatted string from retriever.format_context()
        backend:       'openai', 'mistral', or 'ollama' (overrides env var)

    Returns:
        dict with keys: explication, conseils (list), message, urgence
    """
    backend = backend or LLM_BACKEND
    prompt  = build_prompt(situation, risk, context_rules)

    print(f"🤖 Calling LLM backend: {backend}")

    if backend == "openai":
        raw = _call_openai(prompt)
    elif backend == "mistral":
        raw = _call_mistral(prompt)
    elif backend == "ollama":
        raw = _call_ollama(prompt)
    else:
        raise ValueError(f"Unknown backend: {backend}. Use 'openai', 'mistral', or 'ollama'.")

    return _parse_llm_response(raw)


# ─────────────────────────────────────────────
#  QUICK TEST  (run: python generator.py)
# ─────────────────────────────────────────────

if __name__ == "__main__":
    # Simulate a full pipeline result
    mock_risk = {
        "score":    8,
        "level":    "CRITIQUE",
        "emoji":    "🔴",
        "factors":  ["fatigue", "nuit", "pluie"],
        "warnings": ["Fatigue + nuit = combo très dangereux", "Triple risque critique"],
        "actions":  [
            "Arrêtez-vous à la prochaine aire de repos",
            "Faites une sieste de 20 minutes",
            "Réduisez votre vitesse de 20 km/h",
        ],
    }

    mock_context = """[Règle 1 — Sécurité Routière]
La somnolence au volant est responsable de 1 accident mortel sur 3 sur autoroute.

[Règle 2 — Code de la Route]
Par temps de pluie, la distance de freinage est multipliée par 2.

[Règle 3 — Études scientifiques]
La combinaison fatigue + nuit + pluie multiplie le risque d'accident par 8."""

    situation = "Je conduis depuis 5 heures, il est 23h et il pleut fort."

    print("=" * 60)
    print("GENERATOR TEST")
    print("=" * 60)
    print(f"Situation: {situation}")
    print(f"Backend: {LLM_BACKEND}")
    print()

    result = generate_advice(situation, mock_risk, mock_context)

    print("📋 RESULT:")
    print(f"⚠️  Explication: {result['explication']}")
    print(f"✅ Conseils:")
    for i, c in enumerate(result['conseils'], 1):
        print(f"   {i}. {c}")
    print(f"💬 Message: {result['message']}")