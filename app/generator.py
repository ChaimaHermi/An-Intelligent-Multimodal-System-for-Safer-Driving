"""
generator.py
------------
Single LLM call that does BOTH intent classification AND advice generation.
Eliminates the previous double-call latency (~50% faster).

Supported backends: openai | mistral | ollama (default, free local)

Setup Ollama:
  brew install ollama          (macOS) / or https://ollama.ai
  ollama pull mistral
  ollama serve
"""

import os
import json

LLM_BACKEND = os.getenv("LLM_BACKEND", "ollama")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral")

# ─────────────────────────────────────────────
#  SYSTEM PROMPT
# ─────────────────────────────────────────────

SYSTEM_PROMPT = """Tu es un assistant expert en sécurité routière tunisienne.
Tu connais parfaitement le Code de la Route Tunisien, les sanctions légales, les routes spécifiques à la Tunisie et les numéros d'urgence tunisiens.

RÈGLES ABSOLUES :
- Réponds TOUJOURS en français
- Sois direct, concret, jamais vague
- Utilise des chiffres réels (amendes en DT, vitesses en km/h, numéros d'urgence tunisiens)
- Ton ton : ami expert bienveillant mais ferme face au danger
- Ne minimise JAMAIS un risque réel
- Ne confonds JAMAIS les lois françaises et tunisiennes (ex: taux alcool TN = 0.3g/L, pas 0.5g/L)
- Réponds UNIQUEMENT avec du JSON valide, sans texte avant ou après"""


# ─────────────────────────────────────────────
#  UNIFIED PROMPT (intent + advice in one shot)
# ─────────────────────────────────────────────

def build_unified_prompt(user_input: str, fast_scan: dict, context_rules: str) -> str:
    """
    Build a single prompt that asks the LLM to:
    1. Classify the intent
    2. Generate the appropriate advice
    All in one JSON response.
    """
    factors_hint    = ", ".join(fast_scan.get("factors", [])) or "aucun détecté"
    infractions_hint= ", ".join(fast_scan.get("infractions", [])) or "aucune détectée"
    emergencies_hint= ", ".join(fast_scan.get("emergencies", [])) or "aucune"
    speed_hint      = fast_scan.get("speed_value")
    hours_hint      = fast_scan.get("hours_driven")

    return f"""ENTRÉE CONDUCTEUR :
"{user_input}"

PRÉ-ANALYSE (aide-toi en mais reste libre de corriger) :
- Facteurs de risque détectés : {factors_hint}
- Infractions détectées : {infractions_hint}
- Urgences détectées : {emergencies_hint}
- Vitesse détectée : {speed_hint or "non détectée"} km/h
- Heures de conduite détectées : {hours_hint or "non détectées"}

RÈGLES PERTINENTES (utilise-les pour fonder tes conseils) :
{context_rules if context_rules else "Aucune règle récupérée — utilise tes connaissances."}

────────────────────────────────────────────────
Ta tâche : analyse la situation ET génère la réponse appropriée.

ÉTAPE 1 — CLASSIFICATION DE L'INTENTION :
Choisis l'une des intentions suivantes (une seule) :
  • "dangerous_situation" → situation dangereuse en cours ou passée (fatigue, pluie, vitesse…)
  • "infraction_question" → demande d'info sur une infraction hypothétique ("c'est quoi l'amende si…")
  • "infraction_committed" → infraction VRAIMENT commise ("j'ai grillé", "j'ai été flashé")
  • "emergency"           → accident réel, blessé, panne grave, incendie
  • "minor_damage"        → dégât matériel mineur (rayure, accroc, bosse)
  • "prevention"          → demande de conseil préventif ("comment éviter…", "conseils pour…")

ÉTAPE 2 — RÉPONSE ADAPTÉE :
Selon l'intention, génère une réponse JSON avec EXACTEMENT cette structure :

{{
  "intent": "...",
  "is_real_event": true/false,
  "risk_factors": ["liste des facteurs réels identifiés"],
  "infractions": ["liste des infractions identifiées"],
  "urgency_level": 0,
  "explication": "1-2 phrases expliquant le POURQUOI du danger ou de la situation. Cite un chiffre tunisien si possible.",
  "conseils": [
    "Conseil 1 — concret et actionnable, adapté à la Tunisie",
    "Conseil 2 — concret et actionnable",
    "Conseil 3 — concret et actionnable"
  ],
  "message": "Une phrase courte, percutante — avertissement ou encouragement selon la gravité.",
  "urgence_label": "FAIBLE|MODÉRÉ|ÉLEVÉ|CRITIQUE|EXTRÊME"
}}

Pour "urgency_level" : 0=info, 1=prévention, 2=vigilance, 3=action sous 24h, 4=action rapide, 5=urgence immédiate
RÉPONDS UNIQUEMENT AVEC LE JSON — aucun texte avant ou après."""


# ─────────────────────────────────────────────
#  BACKEND CALLERS
# ─────────────────────────────────────────────

def _call_ollama(prompt: str) -> str:
    import requests
    resp = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model":  OLLAMA_MODEL,
            "prompt": f"{SYSTEM_PROMPT}\n\n{prompt}",
            "stream": False,
            "options": {"temperature": 0.3},
        },
        timeout=90,
    )
    resp.raise_for_status()
    return resp.json()["response"]


def _call_openai(prompt: str) -> str:
    from openai import OpenAI
    client   = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": prompt},
        ],
        temperature=0.3,
        max_tokens=700,
    )
    return response.choices[0].message.content


def _call_mistral(prompt: str) -> str:
    from mistralai.client import MistralClient
    from mistralai.models.chat_completion import ChatMessage
    client   = MistralClient(api_key=os.getenv("MISTRAL_API_KEY"))
    response = client.chat(
        model="mistral-small-latest",
        messages=[
            ChatMessage(role="system", content=SYSTEM_PROMPT),
            ChatMessage(role="user",   content=prompt),
        ],
        temperature=0.3,
        max_tokens=700,
    )
    return response.choices[0].message.content


# ─────────────────────────────────────────────
#  JSON PARSER WITH FALLBACK
# ─────────────────────────────────────────────

def _parse(raw: str, user_input: str) -> dict:
    raw = raw.strip()
    # Strip markdown fences
    if "```json" in raw:
        raw = raw.split("```json")[1].split("```")[0]
    elif raw.startswith("```"):
        raw = raw.split("```")[1].split("```")[0]

    # First attempt: direct parse
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass

    # Second attempt: find first {...} block
    import re
    m = re.search(r"\{.*\}", raw, re.DOTALL)
    if m:
        try:
            return json.loads(m.group())
        except json.JSONDecodeError:
            pass

    # Hard fallback
    print(f"⚠️  JSON parse failed. Raw:\n{raw[:300]}")
    return {
        "intent":        "dangerous_situation",
        "is_real_event": True,
        "risk_factors":  [],
        "infractions":   [],
        "urgency_level": 2,
        "explication":   "Situation à risque détectée. Soyez prudent.",
        "conseils": [
            "Réduisez votre vitesse",
            "Augmentez la distance de sécurité",
            "Arrêtez-vous si vous ne vous sentez pas en sécurité",
        ],
        "message":       "Votre sécurité est la priorité absolue.",
        "urgence_label": "MODÉRÉ",
    }


# ─────────────────────────────────────────────
#  ADVICE GENERATION FOR PENALTY CONTEXT
#  (used when infraction handler needs LLM to format a legal response)
# ─────────────────────────────────────────────

def generate_penalty_advice(
    user_input:    str,
    context_rules: str,
    backend:       str = None,
) -> dict:
    """
    Lightweight LLM call specifically for infraction/penalty responses.
    Returns dict with explication, conseils, message.
    """
    backend = backend or LLM_BACKEND
    prompt  = f"""L'utilisateur a une question ou une situation liée à une infraction routière en Tunisie.

ENTRÉE : "{user_input}"

CONTEXTE LÉGAL TUNISIEN :
{context_rules}

Réponds en JSON avec exactement ces 3 clés :
{{
  "explication": "Explication claire et factuelle de la situation légale en Tunisie",
  "conseils": ["Conseil 1", "Conseil 2", "Conseil 3"],
  "message": "Message final court et percutant"
}}

RAPPELS : Montants en DT, taux alcool tunisien = 0.3g/L, permis retrait = droit tunisien.
RÉPONDS UNIQUEMENT AVEC LE JSON."""

    if backend == "openai":
        raw = _call_openai(prompt)
    elif backend == "mistral":
        raw = _call_mistral(prompt)
    else:
        raw = _call_ollama(prompt)

    return _parse(raw, user_input)


# ─────────────────────────────────────────────
#  MAIN ENTRY POINT
# ─────────────────────────────────────────────

def generate_unified(
    user_input:    str,
    fast_scan:     dict,
    context_rules: str,
    backend:       str = None,
) -> dict:
    """
    Single LLM call: classify intent + generate advice.

    Args:
        user_input:    raw user text
        fast_scan:     result from extractor.fast_keyword_scan()
        context_rules: formatted rules from retriever.format_context()
        backend:       'openai' | 'mistral' | 'ollama'

    Returns:
        Full analysis dict including intent, risk_factors, conseils, etc.
    """
    backend = backend or LLM_BACKEND
    prompt  = build_unified_prompt(user_input, fast_scan, context_rules)

    print(f"🤖 LLM call [{backend}] …")

    if backend == "openai":
        raw = _call_openai(prompt)
    elif backend == "mistral":
        raw = _call_mistral(prompt)
    elif backend == "ollama":
        raw = _call_ollama(prompt)
    else:
        raise ValueError(f"Unknown backend: {backend}")

    result = _parse(raw, user_input)
    result["raw_input"] = user_input
    return result