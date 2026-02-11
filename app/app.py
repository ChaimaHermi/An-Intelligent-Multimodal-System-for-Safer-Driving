"""
app.py
------
Road Safety AI — Tunisia
Streamlit interface with text + voice input and TTS output.

Run:
  streamlit run app.py

Install:
  pip install streamlit streamlit-mic-recorder openai-whisper gTTS
"""

import streamlit as st
import sys
import os
import base64

# ── Make sure project modules are on the path ──────────────
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main         import analyze_situation
from audio_utils  import transcribe_audio, text_to_speech, build_tts_text

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="Road Safety AI — Tunisie",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  CSS — Dark automotive dashboard
# ─────────────────────────────────────────────

st.markdown("""
<style>
/* ── Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=Space+Mono:wght@400;700&display=swap');

/* ── Root theme ── */
:root {
    --bg-deep:    #07080d;
    --bg-panel:   #0e1018;
    --bg-card:    #141720;
    --bg-input:   #1a1f2e;
    --border:     #252b3b;
    --amber:      #f59e0b;
    --amber-dim:  #92610a;
    --red:        #ef4444;
    --orange:     #f97316;
    --green:      #22c55e;
    --blue:       #3b82f6;
    --text-primary:   #e8eaf0;
    --text-secondary: #8891a8;
    --text-muted:     #4a5168;
}

/* ── Global ── */
html, body, .stApp {
    background-color: var(--bg-deep) !important;
    font-family: 'DM Sans', sans-serif;
    color: var(--text-primary);
}

/* ── Hide default Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 2rem 2rem 2rem !important; max-width: 100% !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--bg-deep); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--bg-panel) !important;
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] .block-container { padding: 1.5rem 1rem !important; }

/* ── Sidebar labels ── */
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stRadio label {
    color: var(--text-secondary) !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

/* ── Select boxes ── */
[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    background: var(--bg-input) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
}

/* ── Toggle / radio ── */
.stRadio > div { gap: 0.5rem; }
.stRadio [data-testid="stMarkdownContainer"] p {
    font-size: 0.85rem;
    color: var(--text-secondary);
}

/* ── Text area & inputs ── */
textarea, .stTextArea textarea {
    background: var(--bg-input) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    color: var(--text-primary) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    resize: none !important;
    transition: border-color 0.2s;
}
textarea:focus { border-color: var(--amber) !important; outline: none !important; }

/* ── Buttons ── */
.stButton > button {
    background: var(--bg-input) !important;
    border: 1px solid var(--border) !important;
    color: var(--text-primary) !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    border-color: var(--amber) !important;
    color: var(--amber) !important;
}

/* ── Spinner ── */
.stSpinner > div { border-top-color: var(--amber) !important; }

/* ── Audio component ── */
[data-testid="stAudio"] audio {
    width: 100%;
    border-radius: 8px;
}

/* ── Dividers ── */
hr { border-color: var(--border) !important; margin: 1rem 0 !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  SESSION STATE INIT
# ─────────────────────────────────────────────

def init_state():
    defaults = {
        "messages":         [],      # list of {role, content, result}
        "input_mode":       "text",  # "text" | "audio"
        "pending_text":     "",      # text waiting to be sent
        "last_audio_key":   None,    # track audio recorder state
        "processing":       False,
        "tts_autoplay":     False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()


# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────

with st.sidebar:
    # Logo / brand
    st.markdown("""
    <div style="text-align:center; padding: 0.5rem 0 1.5rem;">
        <div style="font-family:'Space Mono',monospace; font-size:1.6rem; color:#f59e0b; letter-spacing:0.04em;">
            🚗 ROAD<br><span style="color:#e8eaf0;">SAFETY</span>
        </div>
        <div style="font-size:0.7rem; color:#4a5168; letter-spacing:0.15em; text-transform:uppercase; margin-top:4px;">
            Tunisie · AI Assistant
        </div>
    </div>
    <hr>
    """, unsafe_allow_html=True)

    st.markdown('<p style="color:#8891a8;font-size:0.7rem;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:0.5rem;">Modèle LLM</p>', unsafe_allow_html=True)
    backend = st.selectbox(
        label="LLM Backend",
        options=["ollama", "openai", "mistral"],
        index=0,
        label_visibility="collapsed",
    )

    st.markdown('<hr>', unsafe_allow_html=True)

    st.markdown('<p style="color:#8891a8;font-size:0.7rem;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:0.5rem;">Langue de reconnaissance vocale</p>', unsafe_allow_html=True)
    stt_lang = st.selectbox(
        label="Langue STT",
        options=[("Français", "fr"), ("Arabe (Tunisien)", "ar"), ("Anglais", "en")],
        format_func=lambda x: x[0],
        index=0,
        label_visibility="collapsed",
    )

    st.markdown('<hr>', unsafe_allow_html=True)

    st.markdown('<p style="color:#8891a8;font-size:0.7rem;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:0.5rem;">Taille modèle Whisper</p>', unsafe_allow_html=True)
    whisper_size = st.selectbox(
        label="Whisper size",
        options=[("Tiny — rapide", "tiny"), ("Base — équilibré ✓", "base"), ("Small — précis", "small")],
        format_func=lambda x: x[0],
        index=1,
        label_visibility="collapsed",
    )

    st.markdown('<hr>', unsafe_allow_html=True)

    tts_enabled  = st.toggle("🔊 Réponse vocale activée", value=True)
    tts_autoplay = st.toggle("▶️  Lecture auto", value=False)
    st.session_state.tts_autoplay = tts_autoplay

    st.markdown('<hr>', unsafe_allow_html=True)

    # Emergency numbers quick ref
    st.markdown("""
    <div style="background:#0e1018; border:1px solid #252b3b; border-radius:10px; padding:1rem;">
        <p style="color:#f59e0b; font-size:0.7rem; letter-spacing:0.1em; text-transform:uppercase; margin:0 0 0.75rem;">Urgences Tunisie</p>
        <div style="font-size:0.8rem; color:#8891a8; line-height:2;">
            📞 <b style="color:#e8eaf0;">197</b> Police<br>
            📞 <b style="color:#e8eaf0;">190</b> SAMU<br>
            📞 <b style="color:#e8eaf0;">198</b> Protection Civile<br>
            📞 <b style="color:#e8eaf0;">193</b> Garde Nationale<br>
            📞 <b style="color:#e8eaf0;">1021</b> Urgence universelle
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<hr>', unsafe_allow_html=True)

    if st.button("🗑️  Effacer la conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# ─────────────────────────────────────────────
#  HEADER
# ─────────────────────────────────────────────

st.markdown("""
<div style="
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.5rem 0 1rem;
    border-bottom: 1px solid #252b3b;
    margin-bottom: 1.5rem;
">
    <div>
        <h1 style="
            font-family: 'Space Mono', monospace;
            font-size: 1.3rem;
            color: #e8eaf0;
            margin: 0;
            letter-spacing: 0.04em;
        ">Assistant Sécurité Routière</h1>
        <p style="color:#4a5168; font-size:0.8rem; margin: 4px 0 0; letter-spacing:0.05em;">
            Conseils · Infractions · Urgences · Réparations · Tunisie
        </p>
    </div>
    <div style="
        background: #0e1018;
        border: 1px solid #252b3b;
        border-radius: 20px;
        padding: 0.4rem 1rem;
        font-size: 0.75rem;
        color: #22c55e;
        letter-spacing: 0.05em;
    ">● EN LIGNE</div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  RISK LEVEL → STYLE MAPPING
# ─────────────────────────────────────────────

LEVEL_STYLES = {
    "FAIBLE":   {"bg": "#052010", "border": "#22c55e", "color": "#22c55e"},
    "MODÉRÉ":  {"bg": "#1a1400", "border": "#eab308", "color": "#eab308"},
    "ÉLEVÉ":   {"bg": "#1a0e00", "border": "#f97316", "color": "#f97316"},
    "CRITIQUE": {"bg": "#1a0505", "border": "#ef4444", "color": "#ef4444"},
    "EXTRÊME":  {"bg": "#0f0005", "border": "#7f1d1d", "color": "#ff4466"},
}

TYPE_ICONS = {
    "dangerous_situation": "⚠️",
    "infraction_question":  "ℹ️",
    "infraction_committed": "🚨",
    "emergency":            "🆘",
    "minor_damage":         "🔧",
    "prevention":           "🛡️",
    "unknown":              "💬",
}

TYPE_LABELS = {
    "dangerous_situation": "Situation dangereuse",
    "infraction_question":  "Question infraction",
    "infraction_committed": "Infraction commise",
    "emergency":            "Urgence",
    "minor_damage":         "Dégât mineur",
    "prevention":           "Conseil préventif",
}


# ─────────────────────────────────────────────
#  RENDER A RESULT CARD
# ─────────────────────────────────────────────

def render_result(result: dict):
    rtype     = result.get("type", "unknown")
    icon      = TYPE_ICONS.get(rtype, "💬")
    label     = TYPE_LABELS.get(rtype, rtype)
    level     = result.get("risk_level", "MODÉRÉ")
    style     = LEVEL_STYLES.get(level, LEVEL_STYLES["MODÉRÉ"])

    # ── Card wrapper ──
    st.markdown(f"""
    <div style="
        background: {style['bg']};
        border: 1px solid {style['border']}40;
        border-left: 3px solid {style['border']};
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        margin: 0.25rem 0 0.75rem;
    ">
    """, unsafe_allow_html=True)

    # Type badge
    col_badge, col_score = st.columns([3, 1])
    with col_badge:
        st.markdown(f"""
        <span style="
            background: {style['border']}22;
            color: {style['color']};
            font-size: 0.7rem;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            padding: 0.2rem 0.7rem;
            border-radius: 20px;
            border: 1px solid {style['border']}40;
            font-family: 'Space Mono', monospace;
        ">{icon} {label}</span>
        """, unsafe_allow_html=True)

    with col_score:
        if result.get("risk_score") is not None:
            emoji = result.get("risk_emoji", "")
            score = result.get("risk_score", 0)
            st.markdown(f"""
            <div style="text-align:right; font-family:'Space Mono',monospace;
                        color:{style['color']}; font-size:0.85rem;">
                {emoji} {score}/20
            </div>
            """, unsafe_allow_html=True)

    # Emergency number — prominent
    if rtype == "emergency" and result.get("primary_number"):
        st.markdown(f"""
        <div style="
            background: #1a0505;
            border: 1px solid #ef4444;
            border-radius: 10px;
            padding: 0.75rem 1.25rem;
            margin: 0.75rem 0;
            font-family: 'Space Mono', monospace;
            font-size: 1.1rem;
            color: #ef4444;
            text-align: center;
        ">🆘 APPELEZ LE {result['primary_number']} MAINTENANT</div>
        """, unsafe_allow_html=True)

    # Infraction fines
    if rtype in ("infraction_question", "infraction_committed"):
        a_min = result.get("amende_min", 0)
        a_max = result.get("amende_max", 0)
        if a_min or a_max:
            cols = st.columns(3)
            with cols[0]:
                st.markdown(f"""
                <div style="background:#1a1400; border:1px solid #eab30840;
                    border-radius:8px; padding:0.6rem 1rem; text-align:center;">
                    <div style="font-size:0.65rem; color:#8891a8; letter-spacing:0.1em;
                                text-transform:uppercase;">Amende</div>
                    <div style="font-size:1.1rem; color:#eab308; font-family:'Space Mono',monospace;">
                        {a_min}–{a_max} DT</div>
                </div>
                """, unsafe_allow_html=True)
            with cols[1]:
                if result.get("permis_risque"):
                    st.markdown("""
                    <div style="background:#1a0e00; border:1px solid #f9731640;
                        border-radius:8px; padding:0.6rem 1rem; text-align:center;">
                        <div style="font-size:0.65rem; color:#8891a8; letter-spacing:0.1em;
                                    text-transform:uppercase;">Permis</div>
                        <div style="font-size:0.9rem; color:#f97316;">⚠️ Retrait possible</div>
                    </div>
                    """, unsafe_allow_html=True)
            with cols[2]:
                if result.get("prison_risque"):
                    st.markdown("""
                    <div style="background:#1a0505; border:1px solid #ef444440;
                        border-radius:8px; padding:0.6rem 1rem; text-align:center;">
                        <div style="font-size:0.65rem; color:#8891a8; letter-spacing:0.1em;
                                    text-transform:uppercase;">Pénal</div>
                        <div style="font-size:0.9rem; color:#ef4444;">⛔ Prison possible</div>
                    </div>
                    """, unsafe_allow_html=True)
            st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)

    # Warnings
    for w in result.get("warnings", []):
        st.markdown(f"""
        <div style="font-size:0.8rem; color:#f97316; margin: 0.25rem 0;
                    padding-left: 0.5rem; border-left: 2px solid #f97316;">
            {w}
        </div>
        """, unsafe_allow_html=True)

    # Explication
    explication = result.get("explication", "")
    if explication:
        st.markdown(f"""
        <p style="color:#c8cad6; font-size:0.9rem; line-height:1.7;
                  margin: 0.75rem 0 0.5rem;">{explication}</p>
        """, unsafe_allow_html=True)

    # Conseils
    conseils = result.get("conseils", [])
    if conseils:
        st.markdown("""
        <p style="color:#8891a8; font-size:0.7rem; letter-spacing:0.1em;
                  text-transform:uppercase; margin: 0.75rem 0 0.4rem;">Conseils</p>
        """, unsafe_allow_html=True)
        for c in conseils[:5]:
            st.markdown(f"""
            <div style="display:flex; gap:0.6rem; align-items:flex-start;
                        margin-bottom:0.4rem;">
                <div style="color:{style['color']}; flex-shrink:0; margin-top:2px;">→</div>
                <div style="color:#c8cad6; font-size:0.88rem; line-height:1.6;">{c}</div>
            </div>
            """, unsafe_allow_html=True)

    # Message
    message = result.get("message", "")
    if message:
        st.markdown(f"""
        <div style="
            margin-top: 0.75rem;
            padding: 0.6rem 1rem;
            background: {style['border']}15;
            border-radius: 8px;
            font-size: 0.88rem;
            color: {style['color']};
            font-style: italic;
        ">{message}</div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  RENDER CHAT HISTORY
# ─────────────────────────────────────────────

def render_chat():
    if not st.session_state.messages:
        # Welcome screen
        st.markdown("""
        <div style="
            text-align: center;
            padding: 4rem 2rem;
            color: #4a5168;
        ">
            <div style="font-size:3rem; margin-bottom:1rem;">🚗</div>
            <h2 style="color:#8891a8; font-size:1.1rem; font-weight:400; margin-bottom:0.75rem;">
                Comment puis-je vous aider aujourd'hui ?
            </h2>
            <p style="font-size:0.85rem; max-width:500px; margin:0 auto; line-height:1.8; color:#3a4158;">
                Décrivez votre situation en texte ou utilisez votre microphone.<br>
                Je comprends les situations de danger, les infractions, les urgences et les petits dégâts.
            </p>
            <div style="
                display:flex; flex-wrap:wrap; gap:0.5rem;
                justify-content:center; margin-top:2rem;
            ">
                <span style="background:#141720; border:1px solid #252b3b; border-radius:20px;
                             padding:0.4rem 1rem; font-size:0.78rem; color:#8891a8;">
                    ⚠️ Je me sens fatigué...
                </span>
                <span style="background:#141720; border:1px solid #252b3b; border-radius:20px;
                             padding:0.4rem 1rem; font-size:0.78rem; color:#8891a8;">
                    🚨 J'ai grillé un feu rouge
                </span>
                <span style="background:#141720; border:1px solid #252b3b; border-radius:20px;
                             padding:0.4rem 1rem; font-size:0.78rem; color:#8891a8;">
                    🆘 Accident sur la route
                </span>
                <span style="background:#141720; border:1px solid #252b3b; border-radius:20px;
                             padding:0.4rem 1rem; font-size:0.78rem; color:#8891a8;">
                    💰 Amende vitesse Tunisie ?
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    for msg in st.session_state.messages:
        role = msg["role"]

        if role == "user":
            mode_icon = "🎙️" if msg.get("audio_input") else "💬"
            st.markdown(f"""
            <div style="
                display:flex; justify-content:flex-end; margin-bottom:1rem;
            ">
                <div style="
                    background:#1a1f2e;
                    border:1px solid #252b3b;
                    border-radius:14px 14px 2px 14px;
                    padding:0.75rem 1.1rem;
                    max-width:75%;
                    font-size:0.9rem;
                    color:#c8cad6;
                    line-height:1.6;
                ">
                    <span style="font-size:0.7rem; color:#4a5168; margin-right:0.4rem;">{mode_icon}</span>
                    {msg['content']}
                </div>
            </div>
            """, unsafe_allow_html=True)

        else:  # assistant
            result = msg.get("result", {})
            if result:
                render_result(result)
            else:
                st.markdown(f"""
                <div style="
                    background:#141720; border:1px solid #252b3b;
                    border-radius:14px 14px 14px 2px;
                    padding:0.75rem 1.1rem; max-width:75%;
                    font-size:0.9rem; color:#c8cad6;
                    margin-bottom:1rem;
                ">{msg['content']}</div>
                """, unsafe_allow_html=True)

            # TTS audio player if available
            if msg.get("audio_bytes"):
                with st.expander("🔊 Écouter la réponse", expanded=st.session_state.tts_autoplay):
                    st.audio(msg["audio_bytes"], format="audio/mp3", autoplay=st.session_state.tts_autoplay)


# ─────────────────────────────────────────────
#  PROCESS A SUBMITTED PROMPT
# ─────────────────────────────────────────────

def process_prompt(text: str, audio_input: bool = False):
    if not text.strip():
        return

    # Add user message
    st.session_state.messages.append({
        "role":        "user",
        "content":     text.strip(),
        "audio_input": audio_input,
    })

    # Run pipeline
    with st.spinner("Analyse en cours …"):
        try:
            result = analyze_situation(text.strip(), backend=backend)
        except Exception as e:
            result = {
                "type":        "unknown",
                "explication": f"Erreur : {str(e)}",
                "conseils":    ["Vérifiez que le backend LLM est bien démarré (ollama serve)."],
                "message":     "Service temporairement indisponible.",
            }

    # Build TTS if enabled
    audio_bytes = None
    if tts_enabled:
        spoken = build_tts_text(result)
        audio_bytes = text_to_speech(spoken, lang=stt_lang[1])

    # Build text summary for history record
    summary = result.get("explication") or result.get("message", "Réponse reçue.")

    st.session_state.messages.append({
        "role":        "assistant",
        "content":     summary,
        "result":      result,
        "audio_bytes": audio_bytes,
    })


# ─────────────────────────────────────────────
#  MAIN LAYOUT
# ─────────────────────────────────────────────

# Chat area
chat_container = st.container()
with chat_container:
    render_chat()

st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# ── Input mode toggle ──────────────────────────────────────

col_toggle_l, col_toggle_r = st.columns([1, 3])

with col_toggle_l:
    input_mode = st.radio(
        label="Mode de saisie",
        options=["✏️  Texte", "🎙️  Microphone"],
        index=0 if st.session_state.input_mode == "text" else 1,
        horizontal=True,
        label_visibility="collapsed",
    )
    st.session_state.input_mode = "text" if "Texte" in input_mode else "audio"

# ── TEXT MODE ─────────────────────────────────────────────

if st.session_state.input_mode == "text":
    col_input, col_send = st.columns([6, 1])

    with col_input:
        user_text = st.text_area(
            label="Prompt",
            placeholder="Décrivez votre situation… ex: Je me sens fatigué sur l'autoroute et il commence à pleuvoir.",
            height=80,
            key="text_input",
            label_visibility="collapsed",
        )

    with col_send:
        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
        send_clicked = st.button("Envoyer →", use_container_width=True)

    if send_clicked and user_text.strip():
        process_prompt(user_text, audio_input=False)
        st.rerun()

    # Also allow Enter key via form trick
    with st.form(key="enter_form", clear_on_submit=True):
        quick = st.text_input(
            label="Appuyez sur Entrée pour envoyer",
            placeholder="Ou tapez ici et appuyez Entrée …",
            key="quick_input",
            label_visibility="visible",
        )
        submitted = st.form_submit_button("↵", use_container_width=False)
        if submitted and quick.strip():
            process_prompt(quick, audio_input=False)
            st.rerun()

# ── AUDIO MODE ────────────────────────────────────────────

else:
    try:
        from streamlit_mic_recorder import mic_recorder

        st.markdown("""
        <div style="
            background:#0e1018; border:1px solid #252b3b;
            border-radius:12px; padding:1.25rem 1.5rem;
            margin-bottom:0.75rem;
        ">
            <p style="color:#8891a8; font-size:0.8rem; margin:0 0 0.5rem;
                      letter-spacing:0.05em;">
                🎙️  Appuyez sur le bouton pour parler. L'envoi est automatique à la fin.
            </p>
        """, unsafe_allow_html=True)

        audio = mic_recorder(
            start_prompt="⏺  Démarrer l'enregistrement",
            stop_prompt="⏹  Arrêter et envoyer",
            just_once=True,
            use_container_width=True,
            key="mic_recorder",
        )

        st.markdown("</div>", unsafe_allow_html=True)

        # Process audio if new recording received
        if audio and audio.get("bytes"):
            # Detect if it's a new recording (key changes)
            rec_id = audio.get("id", None)
            if rec_id != st.session_state.last_audio_key:
                st.session_state.last_audio_key = rec_id

                with st.spinner("🎙️  Transcription en cours …"):
                    # Inject whisper size from sidebar setting
                    import audio_utils as au
                    au._whisper_model = None   # reset to reload with new size if changed
                    import whisper
                    au._whisper_model = whisper.load_model(whisper_size[1])

                    transcribed = transcribe_audio(audio["bytes"], language=stt_lang[1])

                if transcribed:
                    st.markdown(f"""
                    <div style="
                        background:#141720; border:1px solid #22c55e40;
                        border-radius:10px; padding:0.6rem 1rem;
                        font-size:0.9rem; color:#c8cad6; margin:0.5rem 0;
                    ">
                        <span style="color:#22c55e; font-size:0.7rem;">TRANSCRIPTION ✓</span><br>
                        {transcribed}
                    </div>
                    """, unsafe_allow_html=True)

                    process_prompt(transcribed, audio_input=True)
                    st.rerun()
                else:
                    st.warning("Transcription vide. Parlez plus fort ou réessayez.")

    except ImportError:
        st.markdown("""
        <div style="
            background:#1a0e00; border:1px solid #f97316;
            border-radius:10px; padding:1rem 1.25rem;
        ">
            <p style="color:#f97316; font-size:0.85rem; margin:0;">
                ⚠️  Module microphone non installé.<br>
                <code style="background:#141720; padding:2px 6px; border-radius:4px;">
                pip install streamlit-mic-recorder
                </code>
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Fallback: text area in audio mode
        fallback_text = st.text_area(
            label="Saisie texte (fallback)",
            placeholder="Module microphone non disponible — tapez votre message ici.",
            height=80,
            label_visibility="collapsed",
        )
        if st.button("Envoyer", use_container_width=True):
            if fallback_text.strip():
                process_prompt(fallback_text, audio_input=False)
                st.rerun()

# ─────────────────────────────────────────────
#  EXAMPLE PROMPTS  (quick-click chips)
# ─────────────────────────────────────────────

st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
st.markdown('<p style="color:#3a4158; font-size:0.72rem; letter-spacing:0.08em; text-transform:uppercase;">Exemples</p>', unsafe_allow_html=True)

examples = [
    "Je me sens fatigué et il pleut sur la route Tunis–Sfax",
    "J'ai bu deux verres, j'ai un long trajet ce matin",
    "J'ai grillé un feu rouge, quelle est l'amende ?",
    "Accident sur la route, l'autre conducteur est blessé",
    "J'ai une rayure sur la portière",
    "Conseils conduite de nuit en Tunisie",
]

cols = st.columns(len(examples))
for col, ex in zip(cols, examples):
    with col:
        if st.button(ex[:28] + "…" if len(ex) > 28 else ex, use_container_width=True, key=f"ex_{ex[:15]}"):
            process_prompt(ex, audio_input=False)
            st.rerun()