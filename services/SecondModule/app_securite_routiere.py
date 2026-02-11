# -*- coding: utf-8 -*-
"""
Application Streamlit - Chatbot de Sécurité Routière
Interface moderne pour l'analyse de risque routier avec IA
"""

import streamlit as st
import json
import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env file
load_dotenv()

# ============================
# Configuration de la Page
# ============================
st.set_page_config(
    page_title="🚗 Sécurité Routière - Assistant IA",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================
# Styles CSS Personnalisés
# ============================
st.markdown("""
<style>
    .main-header {
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .main-header p {
        margin-top: 0.5rem;
        font-size: 1.1rem;
        opacity: 0.95;
    }
    
    .risk-card {
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        border-left: 6px solid;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .risk-low {
        background: linear-gradient(135deg, #28a74522 0%, #28a74544 100%);
        border-color: #28a745;
    }
    
    .risk-medium {
        background: linear-gradient(135deg, #ffc10722 0%, #ffc10744 100%);
        border-color: #ffc107;
    }
    
    .risk-high {
        background: linear-gradient(135deg, #fd7e1422 0%, #fd7e1444 100%);
        border-color: #fd7e14;
    }
    
    .risk-critical {
        background: linear-gradient(135deg, #dc354522 0%, #dc354544 100%);
        border-color: #dc3545;
    }
    
    .risk-badge {
        display: inline-block;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        color: white;
        font-weight: 600;
        text-transform: uppercase;
        font-size: 0.9rem;
    }
    
    .badge-low { background: #28a745; }
    .badge-medium { background: #ffc107; color: #000; }
    .badge-high { background: #fd7e14; }
    .badge-critical { background: #dc3545; }
    
    .advice-box {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        border: 1px solid #dee2e6;
    }
    
    .footer {
        margin-top: 3rem;
        padding: 1.5rem;
        background: #f8f9fa;
        border-radius: 10px;
        text-align: center;
        border-top: 3px solid #667eea;
    }
    
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        padding: 0.75rem 2rem;
        border-radius: 10px;
        border: none;
        font-size: 1.1rem;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    .factor-chip {
        display: inline-block;
        background: #667eea;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        margin: 0.2rem;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================
# Configuration API Groq
# ============================
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    st.error("❌ API_KEY not found. Please check your .env file.")
    st.stop()

# Initialiser client Groq
@st.cache_resource
def get_groq_client():
    return Groq(api_key=API_KEY)

client = get_groq_client()

# ============================
# Base de Connaissances Statique
# ============================
SAFETY_RULES_DATABASE = {
    "fatigue": {
        "none": {
            "risk_level": "low",
            "official_rule": "Article 45 Code de la Route: Maintenir vigilance constante",
            "description": "État normal, aucun signe de fatigue détecté"
        },
        "light": {
            "risk_level": "low-medium",
            "official_rule": "Article 45: La fatigue compromet la sécurité",
            "description": "Premiers signes de fatigue, vigilance recommandée",
            "statistics": "Réflexes diminués de 20%"
        },
        "moderate": {
            "risk_level": "medium-high",
            "official_rule": "Article 45: Interdiction de conduire en état de fatigue significative",
            "description": "Fatigue modérée avec bâillements et clignements fréquents",
            "statistics": "Réflexes diminués de 50%, risque accident x3"
        },
        "severe": {
            "risk_level": "critical",
            "official_rule": "Article 45: Interdiction formelle de conduire en état de somnolence",
            "description": "Fatigue sévère, yeux qui se ferment, danger imminent",
            "statistics": "Temps de réaction doublé, risque accident x6-8",
            "penalties": "Amende 150-500 DT, Retrait 3 points permis"
        }
    },

    "weather": {
        "clear": {
            "visibility": "excellente",
            "adherence": "normale",
            "speed_adjustment": 0
        },
        "rain": {
            "official_rule": "Article 78: Adapter vitesse aux conditions météo",
            "visibility": "réduite",
            "adherence": "diminuée 30-50%",
            "speed_adjustment": -20,
            "risks": "Aquaplaning >80 km/h, distance freinage doublée"
        },
        "fog": {
            "official_rule": "Article 82: Feux brouillard obligatoires si visibilité <50m, vitesse max 50 km/h",
            "visibility": "très_réduite",
            "adherence": "normale",
            "speed_adjustment": -50,
            "risks": "Collision frontale, carambolage",
            "penalties": "Amende si feux non allumés"
        },
        "snow": {
            "official_rule": "Article 78: Équipements hiver obligatoires",
            "visibility": "réduite",
            "adherence": "très_diminuée 70%",
            "speed_adjustment": -40,
            "risks": "Perte contrôle, sortie route"
        },
        "wind": {
            "official_rule": "Article 78: Vigilance renforcée",
            "risks": "Déport latéral véhicules légers",
            "speed_adjustment": -15
        }
    },

    "situation": {
        "day_driving": {
            "visibility": "bonne",
            "fatigue_multiplier": 1.0
        },
        "night_driving": {
            "official_rule": "Article 95: Feux de route obligatoires hors agglomération",
            "visibility": "réduite 90%",
            "fatigue_multiplier": 1.5,
            "risks": "Piétons/animaux invisibles, fatigue accrue",
            "recommendation": "Pauses plus fréquentes (1h30 vs 2h)"
        },
        "rain": {
            "see": "weather.rain"
        },
        "fog": {
            "see": "weather.fog"
        },
        "traffic_dense": {
            "official_rule": "Article 25: Maintenir distance sécurité",
            "stress_factor": "high",
            "risks": "Collision arrière (70% accidents ville)",
            "recommendation": "Distance 3-4m minimum, patience"
        }
    },

    "traffic": {
        "fluide": {
            "stress": "low",
            "attention_required": "normal"
        },
        "modéré": {
            "stress": "medium",
            "attention_required": "elevated"
        },
        "dense": {
            "stress": "high",
            "attention_required": "maximum",
            "official_rule": "Article 25: Distance sécurité obligatoire",
            "recommendation": "Concentration maximale, éviter distractions"
        },
        "embouteillage": {
            "stress": "very_high",
            "fatigue_multiplier": 1.3,
            "official_rule": "Article 25: Maintenir distance même à l'arrêt",
            "recommendation": "Rester calme, accepter lenteur, musique apaisante"
        }
    },

    "duration": {
        "<1h": {
            "fatigue_risk": "low",
            "break_needed": False
        },
        "1-2h": {
            "fatigue_risk": "medium",
            "break_needed": False,
            "official_rule": "Recommandation: Pause après 2h",
            "recommendation": "Pause recommandée dans 30-60 min"
        },
        "2-4h": {
            "fatigue_risk": "high",
            "break_needed": True,
            "official_rule": "Pause OBLIGATOIRE toutes les 2h",
            "recommendation": "PAUSE IMMÉDIATE de 20-30 min requise",
            "penalties": "Risque accident x2 après 2h continues"
        },
        ">4h": {
            "fatigue_risk": "critical",
            "break_needed": True,
            "official_rule": "Pause OBLIGATOIRE toutes les 2h maximum",
            "recommendation": "ARRÊT IMMÉDIAT - Fatigue extrême",
            "penalties": "Risque accident x4, capacités très diminuées"
        }
    }
}

# ============================
# Fonction de Calcul de Risque
# ============================
def calculate_risk_score(fatigue, situation, traffic, weather, duration):
    """Calcule score de risque 0-100 basé sur tous les facteurs"""
    
    score = 0
    factors = []
    
    # Fatigue (poids 40%)
    fatigue_scores = {"none": 0, "light": 25, "moderate": 60, "severe": 90}
    score += fatigue_scores[fatigue] * 0.4
    if fatigue in ["moderate", "severe"]:
        factors.append(f"fatigue_{fatigue}")
    
    # Météo (poids 25%)
    weather_scores = {"clear": 0, "rain": 30, "fog": 60, "snow": 70, "wind": 20}
    score += weather_scores[weather] * 0.25
    if weather != "clear":
        factors.append(f"météo_{weather}")
    
    # Situation (poids 15%)
    situation_scores = {
        "day_driving": 0,
        "night_driving": 30,
        "rain": 30,
        "fog": 60,
        "traffic_dense": 40
    }
    score += situation_scores[situation] * 0.15
    if situation == "night_driving":
        factors.append("conduite_nocturne")
    
    # Trafic (poids 10%)
    traffic_scores = {"fluide": 0, "modéré": 20, "dense": 50, "embouteillage": 70}
    score += traffic_scores[traffic] * 0.10
    if traffic in ["dense", "embouteillage"]:
        factors.append(f"trafic_{traffic}")
    
    # Durée (poids 10%)
    duration_scores = {"<1h": 0, "1-2h": 20, "2-4h": 50, ">4h": 80}
    score += duration_scores[duration] * 0.10
    if duration in ["2-4h", ">4h"]:
        factors.append(f"conduite_prolongée_{duration}")
    
    # Combinaisons dangereuses (bonus risque)
    if fatigue in ["moderate", "severe"] and situation == "night_driving":
        score += 15
        factors.append("COMBO_DANGEREUX: fatigue+nuit")
    
    if fatigue in ["moderate", "severe"] and weather in ["rain", "fog"]:
        score += 10
        factors.append("COMBO_DANGEREUX: fatigue+météo")
    
    if weather == "fog" and situation == "night_driving":
        score += 10
        factors.append("COMBO_DANGEREUX: brouillard+nuit")
    
    # Déterminer niveau
    if score < 25:
        level = "low"
    elif score < 50:
        level = "medium"
    elif score < 75:
        level = "high"
    else:
        level = "critical"
    
    return {
        "score": round(score, 1),
        "level": level,
        "factors": factors
    }

# ============================
# Construction du Prompt
# ============================
def build_safety_prompt(fatigue, situation, traffic, weather, duration, risk_assessment):
    """Construit prompt contextualisé selon niveau de risque"""
    
    fatigue_rules = SAFETY_RULES_DATABASE["fatigue"][fatigue]
    weather_rules = SAFETY_RULES_DATABASE["weather"][weather]
    situation_rules = SAFETY_RULES_DATABASE["situation"][situation]
    traffic_rules = SAFETY_RULES_DATABASE["traffic"][traffic]
    duration_rules = SAFETY_RULES_DATABASE["duration"][duration]
    
    # Template selon niveau de risque
    if risk_assessment["level"] == "low":
        prompt_template = """
📊 SCORE DE RISQUE: {score}/100 (Faible)

🚗 SITUATION ACTUELLE:
- Fatigue: {fatigue}
- Situation: {situation}
- Trafic: {traffic}
- Météo: {weather}
- Durée prévue: {duration}

📜 RÈGLES APPLICABLES:
{official_rules}

⚠️ FACTEURS IDENTIFIÉS:
{risk_factors}

🎯 INSTRUCTIONS:
Tu es un conseiller en sécurité routière bienveillant. La situation est FAVORABLE.

Rédige un conseil court (200 mots max) qui:
1. Félicite brièvement les bonnes conditions
2. Rappelle 2-3 réflexes de base (distance, ceinture, limitations)
3. Termine sur une note positive et encourageante

Ton: CORDIAL, CONFIANT, BREF
Format: Paragraphes courts, maximum 3 émojis légers, style conversationnel
"""
    
    elif risk_assessment["level"] == "medium":
        prompt_template = """
📊 SCORE DE RISQUE: {score}/100 (Modéré)

🚗 SITUATION ACTUELLE:
- Fatigue: {fatigue}
- Situation: {situation}
- Trafic: {traffic}
- Météo: {weather}
- Durée prévue: {duration}

📜 RÈGLES APPLICABLES:
{official_rules}

⚠️ FACTEURS AGGRAVANTS:
{risk_factors}

🎯 INSTRUCTIONS:
Tu es un conseiller expérimenté. La situation nécessite VIGILANCE ACCRUE.

Rédige un conseil structuré (300 mots) qui:
1. Résume objectivement la situation (30 mots)
2. Identifie les 2-3 risques principaux avec statistiques
3. Donne 4-5 actions concrètes et applicables immédiatement
4. Rappelle les articles du code de la route pertinents
5. Recommande une pause si durée >1h30

Ton: PROFESSIONNEL, PRÉCIS, PÉDAGOGIQUE
Format: Utilise des sections claires, émojis modérés (⚠️🚦), maximum 350 mots
Structure recommandée:
⚠️ Situation
📊 Risques
✅ Actions recommandées
📜 Cadre légal
"""
    
    elif risk_assessment["level"] == "high":
        prompt_template = """
📊 SCORE DE RISQUE: {score}/100 (ÉLEVÉ) ⚠️

🚗 SITUATION ACTUELLE:
- Fatigue: {fatigue}
- Situation: {situation}
- Trafic: {traffic}
- Météo: {weather}
- Durée prévue: {duration}

📜 RÈGLES APPLICABLES:
{official_rules}

🚨 FACTEURS AGGRAVANTS MULTIPLES:
{risk_factors}

🎯 INSTRUCTIONS:
Tu es un expert en prévention. La situation est DANGEREUSE.

Rédige un avertissement ferme (400 mots) qui:
1. OUVRE avec "🚨 ATTENTION: Situation à risque élevé" (ligne dédiée)
2. Expose clairement pourquoi c'est dangereux (statistiques d'accidents)
3. Liste 5-7 mesures OBLIGATOIRES à prendre AVANT de partir
4. Insiste sur les conséquences (amendes, accidents, blessures)
5. Propose des alternatives concrètes (reporter trajet, co-voiturage, pause longue)
6. TERMINE par "Ne prenez pas ce risque à la légère"

Ton: FERME, DIRECT, SANS COMPLAISANCE (mais respectueux)
Format: Sections visuelles, émojis d'alerte (🚨⚠️🛑), maximum 450 mots
IMPORTANT: Faire comprendre la gravité sans infantiliser
"""
    
    else:  # critical
        prompt_template = """
📊 SCORE DE RISQUE: {score}/100 (🔴 CRITIQUE - DANGER IMMÉDIAT)

🚗 SITUATION ACTUELLE:
- Fatigue: {fatigue}
- Situation: {situation}
- Trafic: {traffic}
- Météo: {weather}
- Durée prévue: {duration}

📜 RÈGLES APPLICABLES:
{official_rules}

🔴 FACTEURS DE DANGER EXTRÊME:
{risk_factors}

🎯 INSTRUCTIONS:
Tu es un expert mandaté pour prévenir un accident mortel. Cette situation est POTENTIELLEMENT FATALE.

Rédige un ORDRE D'ARRÊT IMMÉDIAT (500 mots max) qui:

1. PREMIÈRE LIGNE: "🔴 STOP - NE CONDUISEZ PAS DANS CET ÉTAT"
2. Explique factuellement pourquoi la mort ou blessure grave est PROBABLE (stats chiffrées)
3. Liste les capacités compromises (réflexes, jugement, temps de réaction)
4. Donne des ALTERNATIVES IMMÉDIATES:
   - Appeler quelqu'un pour venir chercher
   - Taxi/VTC/Transport en commun
   - Dormir sur place (2-3h minimum)
   - Reporter le déplacement
5. Cite les sanctions légales + responsabilité pénale en cas d'accident
6. TERMINE par: "Votre vie et celles des autres valent plus que votre rendez-vous"

Exemples de formulations interdites (trop douces):
   ❌ "Il serait préférable de..."
   ❌ "Nous vous recommandons de considérer..."
   ❌ "Peut-être devriez-vous..."

Formulations OBLIGATOIRES (directives):
   ✅ "Vous DEVEZ vous arrêter immédiatement"
   ✅ "NE conduisez PAS dans cet état"
   ✅ "Il est INTERDIT de..."
   ✅ "Dans ton état, tu es un danger mortel sur la route"

Ton: IMPÉRATIF, ALARMANT (justifié), SANS CONCESSION
Format: Très visuel, émojis danger maximum, maximum 500 mots
CRUCIAL: Faire réaliser au conducteur qu'il risque SA VIE et celle des autres
"""
    
    # Construire contexte règles
    official_rules = []
    
    if "official_rule" in fatigue_rules:
        official_rules.append(f"• FATIGUE: {fatigue_rules['official_rule']}")
    if "official_rule" in weather_rules:
        official_rules.append(f"• MÉTÉO: {weather_rules['official_rule']}")
    if "official_rule" in traffic_rules:
        official_rules.append(f"• TRAFIC: {traffic_rules['official_rule']}")
    if "official_rule" in duration_rules:
        official_rules.append(f"• DURÉE: {duration_rules['official_rule']}")
    
    official_rules_text = "\n".join(official_rules) if official_rules else "Règles générales de prudence"
    
    # Facteurs de risque
    risk_factors_text = "\n".join([f"• {factor}" for factor in risk_assessment["factors"]]) if risk_assessment["factors"] else "Aucun facteur aggravant majeur"
    
    # Formater prompt
    prompt = prompt_template.format(
        score=risk_assessment["score"],
        fatigue=fatigue,
        situation=situation,
        traffic=traffic,
        weather=weather,
        duration=duration,
        official_rules=official_rules_text,
        risk_factors=risk_factors_text
    )
    
    return prompt

# ============================
# Appel API Groq
# ============================
def get_safety_advice(fatigue, situation, traffic, weather, duration):
    """Génère conseil via Groq LLM"""
    
    # Calculer risque
    risk_assessment = calculate_risk_score(fatigue, situation, traffic, weather, duration)
    
    # Construire prompt
    prompt = build_safety_prompt(fatigue, situation, traffic, weather, duration, risk_assessment)
    
    try:
        # Appel Groq API
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "Tu es un expert en sécurité routière. Tu bases tes conseils UNIQUEMENT sur le code de la route officiel et les statistiques d'accidents. Tu es précis, factuel, et adaptes ton ton à la gravité de la situation."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            max_tokens=1500
        )
        
        advice = chat_completion.choices[0].message.content
        
        return {
            "risk_assessment": risk_assessment,
            "advice": advice,
            "prompt_used": prompt
        }
    
    except Exception as e:
        return {
            "error": str(e),
            "risk_assessment": risk_assessment
        }

# ============================
# INTERFACE UTILISATEUR STREAMLIT
# ============================

# En-tête principal
st.markdown("""
<div class="main-header">
    <h1>🚗 Assistant Sécurité Routière IA</h1>
    <p>⚠️ Analyse intelligente basée sur le Code de la Route officiel</p>
</div>
""", unsafe_allow_html=True)

# Introduction
st.markdown("""
### 📋 Comment ça marche ?

Sélectionnez vos conditions de conduite actuelles ci-dessous. Notre système analysera votre situation 
en se basant sur le Code de la Route tunisien et des statistiques d'accidents réels pour vous fournir 
des conseils personnalisés adaptés au niveau de risque détecté.
""")

st.markdown("---")

# ============================
# Formulaire de saisie
# ============================
st.markdown("### 📊 Paramètres de conduite")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🚦 Conditions de circulation")
    
    fatigue = st.selectbox(
        "😴 Niveau de fatigue",
        options=["none", "light", "moderate", "severe"],
        format_func=lambda x: {
            "none": "Aucune fatigue",
            "light": "Fatigue légère",
            "moderate": "Fatigue modérée",
            "severe": "Fatigue sévère"
        }[x],
        help="Évaluez honnêtement votre niveau de fatigue actuel"
    )
    
    situation = st.selectbox(
        "🚗 Type de conduite",
        options=["day_driving", "night_driving", "rain", "fog", "traffic_dense"],
        format_func=lambda x: {
            "day_driving": "Conduite de jour",
            "night_driving": "Conduite de nuit",
            "rain": "Conduite sous la pluie",
            "fog": "Conduite dans le brouillard",
            "traffic_dense": "Trafic dense"
        }[x],
        help="Situation principale de conduite"
    )
    
    traffic = st.selectbox(
        "🚦 État du trafic",
        options=["fluide", "modéré", "dense", "embouteillage"],
        format_func=lambda x: {
            "fluide": "Fluide",
            "modéré": "Modéré",
            "dense": "Dense",
            "embouteillage": "Embouteillage"
        }[x],
        help="Densité du trafic sur votre itinéraire"
    )

with col2:
    st.markdown("#### 🌤️ Conditions météorologiques")
    
    weather = st.selectbox(
        "🌤️ Météo actuelle",
        options=["clear", "rain", "fog", "snow", "wind"],
        format_func=lambda x: {
            "clear": "☀️ Temps clair",
            "rain": "🌧️ Pluie",
            "fog": "🌫️ Brouillard",
            "snow": "❄️ Neige",
            "wind": "💨 Vent fort"
        }[x],
        help="Conditions météorologiques actuelles"
    )
    
    duration = st.selectbox(
        "⏱️ Durée de conduite prévue",
        options=["<1h", "1-2h", "2-4h", ">4h"],
        format_func=lambda x: {
            "<1h": "Moins d'1 heure",
            "1-2h": "1 à 2 heures",
            "2-4h": "2 à 4 heures",
            ">4h": "Plus de 4 heures"
        }[x],
        help="Durée estimée de votre trajet"
    )

st.markdown("---")

# ============================
# Bouton d'analyse
# ============================
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    analyze_button = st.button("🔍 Analyser la Situation", use_container_width=True)

# ============================
# Affichage des résultats
# ============================
if analyze_button:
    with st.spinner("⏳ Analyse en cours..."):
        # Appeler la fonction
        result = get_safety_advice(fatigue, situation, traffic, weather, duration)
    
    if "error" in result:
        st.error(f"❌ Erreur lors de l'analyse: {result['error']}")
        st.info(f"Score de risque calculé: {result['risk_assessment']['score']}/100")
    else:
        risk = result['risk_assessment']
        
        # Mapping des couleurs et icônes
        risk_config = {
            "low": {
                "color": "#28a745",
                "icon": "✅",
                "label": "FAIBLE",
                "class": "risk-low",
                "badge": "badge-low"
            },
            "medium": {
                "color": "#ffc107",
                "icon": "⚠️",
                "label": "MODÉRÉ",
                "class": "risk-medium",
                "badge": "badge-medium"
            },
            "high": {
                "color": "#fd7e14",
                "icon": "🚨",
                "label": "ÉLEVÉ",
                "class": "risk-high",
                "badge": "badge-high"
            },
            "critical": {
                "color": "#dc3545",
                "icon": "🔴",
                "label": "CRITIQUE",
                "class": "risk-critical",
                "badge": "badge-critical"
            }
        }
        
        config = risk_config[risk['level']]
        
        # Carte de risque
        st.markdown(f"""
        <div class="risk-card {config['class']}">
            <h2 style="margin: 0; color: {config['color']};">
                {config['icon']} ÉVALUATION DU RISQUE
            </h2>
            <div style="margin-top: 1rem; font-size: 1.2rem;">
                <strong>Score de risque:</strong> {risk['score']}/100
                <span class="risk-badge {config['badge']}" style="margin-left: 1rem;">
                    {config['label']}
                </span>
            </div>
        """, unsafe_allow_html=True)
        
        # Facteurs de risque
        if risk['factors']:
            st.markdown("<div style='margin-top: 1rem;'><strong>⚠️ Facteurs aggravants identifiés:</strong></div>", unsafe_allow_html=True)
            factors_html = "".join([f"<span class='factor-chip'>{factor}</span>" for factor in risk['factors']])
            st.markdown(f"<div style='margin-top: 0.5rem;'>{factors_html}</div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Conseil personnalisé
        st.markdown("### 💬 Conseil de Sécurité Personnalisé")
        
        st.markdown(f"""
        <div class="advice-box">
            {result['advice'].replace('\n', '<br>')}
        </div>
        """, unsafe_allow_html=True)
        
        # Expander pour voir le prompt (optionnel, pour debug)
        with st.expander("🔍 Voir les détails techniques (développeurs)"):
            st.markdown("**Prompt utilisé:**")
            st.code(result['prompt_used'], language="text")

# ============================
# Footer
# ============================
st.markdown("""
<div class="footer">
    <p style="margin: 0; font-size: 0.9rem; color: #6c757d;">
        📚 <strong>Sources:</strong> Code de la Route Tunisien + Base de Connaissances Sécurité Routière
    </p>
    <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; color: #6c757d;">
        🤖 <strong>Technologie:</strong> Groq LLM (llama-3.3-70b-versatile) + Streamlit
    </p>
    <p style="margin: 0.5rem 0 0 0; font-size: 0.8rem; color: #adb5bd;">
        ⚠️ Cet outil est fourni à titre indicatif. En cas de doute, consultez un professionnel ou abstenez-vous de conduire.
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar (optionnel) avec informations supplémentaires
with st.sidebar:
    st.markdown("### ℹ️ À propos")
    st.markdown("""
    Cet assistant analyse votre situation de conduite en temps réel et vous fournit 
    des conseils basés sur :
    
    - 📜 Le Code de la Route officiel
    - 📊 Les statistiques d'accidents
    - 🧠 L'intelligence artificielle
    
    #### 🎯 Niveaux de risque
    
    - ✅ **Faible** : Conditions favorables
    - ⚠️ **Modéré** : Vigilance accrue requise
    - 🚨 **Élevé** : Situation dangereuse
    - 🔴 **Critique** : Danger immédiat
    
    #### 💡 Conseils d'utilisation
    
    1. Soyez honnête dans votre évaluation
    2. Suivez les recommandations données
    3. En cas de doute, ne prenez pas de risque
    4. Votre sécurité prime toujours
    """)
    
    st.markdown("---")
    st.markdown("**Version:** 1.0")
    st.markdown("**Dernière mise à jour:** Février 2025")
