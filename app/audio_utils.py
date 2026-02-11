"""
audio_utils.py
--------------
Speech-to-Text  : OpenAI Whisper (local, free, excellent French support)
Text-to-Speech  : gTTS (Google TTS, free, supports French + Tunisian context)

Install:
  pip install openai-whisper gTTS soundfile numpy
  
IMPORTANT - FFmpeg requirement:
  Windows: Download from https://ffmpeg.org/download.html
           Add to PATH or place ffmpeg.exe in script directory
  macOS:   brew install ffmpeg
  Linux:   sudo apt install ffmpeg
"""

import io
import os
import tempfile
import numpy as np
from pathlib import Path


# ─────────────────────────────────────────────
#  FFMPEG CHECK
# ─────────────────────────────────────────────

def check_ffmpeg():
    """Check if ffmpeg is available."""
    import shutil
    ffmpeg_path = shutil.which("ffmpeg")
    if not ffmpeg_path:
        print("⚠️  WARNING: ffmpeg not found in PATH")
        print("   Download from: https://ffmpeg.org/download.html")
        print("   Or install: pip install ffmpeg-python")
        return False
    print(f"✅ ffmpeg found: {ffmpeg_path}")
    return True


# ─────────────────────────────────────────────
#  SPEECH-TO-TEXT  (Whisper local)
# ─────────────────────────────────────────────

_whisper_model = None   # lazy-loaded once
_whisper_model_size = None  # track which size is loaded

def load_whisper_model(size: str = "base", force_reload: bool = False):
    """
    Load Whisper model with proper error handling.
    
    Args:
        size: Model size (tiny/base/small/medium/large)
        force_reload: Force reload even if already cached
    """
    global _whisper_model, _whisper_model_size
    
    # Return cached model if available and same size
    if not force_reload and _whisper_model is not None and _whisper_model_size == size:
        print(f"✅ Using cached Whisper model '{size}'")
        return _whisper_model
    
    try:
        import whisper
    except ImportError:
        raise ImportError(
            "❌ Whisper not installed.\n"
            "   Install with: pip install openai-whisper\n"
            "   Also needs ffmpeg - see file header for instructions"
        )
    
    print(f"🎙️  Loading Whisper model '{size}' ...")
    
    # Check ffmpeg
    check_ffmpeg()
    
    # Setup cache directory
    cache_dir = os.path.join(os.path.expanduser("~"), ".cache", "whisper")
    os.makedirs(cache_dir, exist_ok=True)
    
    # Try to load model
    max_retries = 2
    for attempt in range(max_retries):
        try:
            _whisper_model = whisper.load_model(size, download_root=cache_dir)
            _whisper_model_size = size
            print(f"✅ Whisper model '{size}' loaded successfully!")
            return _whisper_model
            
        except RuntimeError as e:
            if "SHA256 checksum" in str(e):
                print(f"⚠️  Corrupted model detected (attempt {attempt+1}/{max_retries})")
                
                # Remove corrupted file
                model_files = {
                    "tiny": "tiny.pt",
                    "base": "base.pt", 
                    "small": "small.pt",
                    "medium": "medium.pt",
                    "large": "large.pt"
                }
                
                if size in model_files:
                    corrupt_file = os.path.join(cache_dir, model_files[size])
                    if os.path.exists(corrupt_file):
                        try:
                            os.remove(corrupt_file)
                            print(f"🗑️  Removed corrupted file: {corrupt_file}")
                        except Exception as rm_err:
                            print(f"❌ Could not remove corrupted file: {rm_err}")
                
                if attempt < max_retries - 1:
                    print("🔄 Retrying download...")
                else:
                    raise RuntimeError(
                        f"Failed to download Whisper model after {max_retries} attempts.\n"
                        f"Try manually deleting cache: {cache_dir}\n"
                        f"Original error: {e}"
                    )
            else:
                raise


def transcribe_audio(audio_bytes: bytes, language: str = "fr", model_size: str = "base") -> str:
    """
    Transcribe audio bytes (WAV / WebM / MP3 / etc.) to text using Whisper.

    Args:
        audio_bytes: raw audio bytes from mic recorder
        language:    hint to Whisper ('fr' for French, 'ar' for Arabic)
        model_size:  Whisper model size to use

    Returns:
        Transcribed text string (empty string on failure)
    """
    if not audio_bytes:
        print("⚠️  No audio bytes provided")
        return ""

    try:
        # Load model (uses cache if available)
        model = load_whisper_model(model_size)

        # Write to temp file (Whisper needs a file path)
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp.write(audio_bytes)
            tmp_path = tmp.name

        print(f"🎙️  Transcribing audio ({len(audio_bytes)} bytes) ...")
        
        # Transcribe
        result = model.transcribe(
            tmp_path,
            language=language,
            task="transcribe",
            fp16=False,           # safer for CPU
        )

        # Clean up temp file
        try:
            os.unlink(tmp_path)
        except:
            pass  # Don't fail if cleanup fails

        text = result.get("text", "").strip()
        
        if text:
            print(f"✅ Transcription: {text[:100]}...")
        else:
            print("⚠️  Empty transcription result")
            
        return text

    except Exception as e:
        print(f"❌ Transcription error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return ""


# ─────────────────────────────────────────────
#  TEXT-TO-SPEECH  (gTTS)
# ─────────────────────────────────────────────

def text_to_speech(text: str, lang: str = "fr", slow: bool = False) -> bytes | None:
    """
    Convert text to MP3 audio bytes using Google TTS.

    Args:
        text: text to speak (max ~5000 chars recommended)
        lang: language code ('fr' for French)
        slow: speak slower (useful for complex instructions)

    Returns:
        MP3 audio bytes, or None on failure
    """
    if not text or not text.strip():
        return None

    try:
        from gtts import gTTS
    except ImportError:
        print("❌ gTTS not installed. Run: pip install gTTS")
        return None

    try:
        # Clean up text for TTS (remove emojis and special chars that gTTS chokes on)
        import re
        clean = re.sub(r"[^\w\s.,!?;:''()\-àâäéèêëîïôùûüçæœ]", " ", text, flags=re.UNICODE)
        clean = re.sub(r"\s+", " ", clean).strip()

        if not clean:
            return None

        tts = gTTS(text=clean, lang=lang, slow=slow)
        buf = io.BytesIO()
        tts.write_to_fp(buf)
        buf.seek(0)
        return buf.read()

    except Exception as e:
        print(f"❌ TTS error: {e}")
        return None


def build_tts_text(result: dict) -> str:
    """
    Build a clean spoken summary from a pipeline result dict.
    Strips technical fields and keeps only what matters for TTS.
    """
    parts = []

    explication = result.get("explication", "")
    if explication:
        parts.append(explication)

    conseils = result.get("conseils", [])
    if conseils:
        parts.append("Voici mes conseils.")
        for i, c in enumerate(conseils[:3], 1):
            # Strip emojis/symbols from start of conseil
            import re
            c_clean = re.sub(r"^[\U0001F000-\U0001FFFF\u2600-\u26FF\u2700-\u27BF]+\s*", "", c)
            parts.append(f"{i}. {c_clean}")

    message = result.get("message", "")
    if message:
        import re
        msg_clean = re.sub(r"^[\U0001F000-\U0001FFFF\u2600-\u26FF\u2700-\u27BF]+\s*", "", message)
        parts.append(msg_clean)

    # Emergency: add the number explicitly
    if result.get("type") == "emergency":
        num = result.get("primary_number")
        if num:
            parts.insert(0, f"Urgence ! Appelez le {num} immédiatement.")

    return " ".join(parts)