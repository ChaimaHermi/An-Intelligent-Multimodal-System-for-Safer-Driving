"""
retriever.py
------------
RAG module: embeds the road safety rules and retrieves the most relevant
ones using FAISS semantic search + optional category/severity filters.
"""

import json
import pickle
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer
import faiss

# ─────────────────────────────────────────────
#  PATHS  (all relative to this file — no assumptions about parent dirs)
# ─────────────────────────────────────────────

BASE_DIR       = Path(__file__).parent
DATA_PATH      = BASE_DIR / "road_safety_rules.json"
EMBED_DIR      = BASE_DIR / "embeddings"
INDEX_PATH     = EMBED_DIR / "rules.index"
META_PATH      = EMBED_DIR / "rules_meta.pkl"

MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"


# ─────────────────────────────────────────────
#  BUILD INDEX  (run once)
# ─────────────────────────────────────────────

def build_index() -> tuple:
    print("📦 Loading rules from JSON …")
    with open(DATA_PATH, encoding="utf-8") as f:
        rules = json.load(f)
    print(f"   → {len(rules)} rules loaded")

    print("🤖 Loading embedding model …")
    model = SentenceTransformer(MODEL_NAME)

    print("🔢 Computing embeddings …")
    texts      = [r["text"] for r in rules]
    embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)

    EMBED_DIR.mkdir(parents=True, exist_ok=True)
    dim   = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings.astype(np.float32))
    faiss.write_index(index, str(INDEX_PATH))

    with open(META_PATH, "wb") as f:
        pickle.dump(rules, f)

    print(f"✅ Index saved → {INDEX_PATH}")
    return index, rules, model


# ─────────────────────────────────────────────
#  RETRIEVER
# ─────────────────────────────────────────────

class RuleRetriever:
    """Semantic search over the road safety rule DB."""

    def __init__(self):
        if not INDEX_PATH.exists() or not META_PATH.exists():
            print("⚠️  Index not found — building now …")
            self.index, self.rules, self.model = build_index()
        else:
            print("📂 Loading existing FAISS index …")
            self.model = SentenceTransformer(MODEL_NAME)
            self.index = faiss.read_index(str(INDEX_PATH))
            with open(META_PATH, "rb") as f:
                self.rules = pickle.load(f)
            print(f"   → {len(self.rules)} rules in index")

    # ── public API ────────────────────────────

    def search(
        self,
        query:       str,
        top_k:       int  = 3,
        factors:     list = None,
        severity:    str  = None,   # "critical" | "high" | "medium" | "low"
        jurisdiction:str  = None,   # "TN" | "ALL"
    ) -> list:
        """
        Semantic search with optional boosting/filtering.

        - Boosts rules whose category matches a detected factor (+0.25)
        - Boosts Tunisia-specific rules (+0.15) by default
        - Filters by severity or jurisdiction if provided
        """
        qvec = self.model.encode([query], convert_to_numpy=True)
        dists, idxs = self.index.search(qvec.astype(np.float32), top_k * 3)

        seen, results = set(), []
        for dist, idx in zip(dists[0], idxs[0]):
            if idx == -1:
                continue
            rule = self.rules[idx]
            rid  = rule["id"]
            if rid in seen:
                continue
            seen.add(rid)

            # Hard filters
            if jurisdiction and rule.get("jurisdiction") not in (jurisdiction, "ALL"):
                continue
            if severity and rule.get("severity") != severity:
                continue

            # Relevance score (lower L2 = better)
            rel = 1.0 / (1.0 + float(dist))

            # Boosts
            if factors and rule.get("category") in factors:
                rel += 0.25
            if rule.get("jurisdiction") == "TN":
                rel += 0.15
            if rule.get("severity") == "critical":
                rel += 0.10

            results.append({**rule, "relevance": round(rel, 4)})

        results.sort(key=lambda x: x["relevance"], reverse=True)
        return results[:top_k]

    def search_by_category(self, categories: list, max_per: int = 2) -> list:
        """Direct category lookup — useful when semantic search is too broad."""
        results, seen = [], set()
        for rule in self.rules:
            if rule.get("category") in categories and rule["id"] not in seen:
                seen.add(rule["id"])
                results.append(rule)
            if len(results) >= max_per * len(categories):
                break
        return results

    def format_context(self, rules: list) -> str:
        """Format retrieved rules into a clean block for LLM injection."""
        lines = []
        for i, r in enumerate(rules, 1):
            src = r.get("source", "Source officielle")
            sev = r.get("severity", "")
            severity_tag = f" [{sev.upper()}]" if sev else ""
            lines.append(f"[Règle {i} — {src}{severity_tag}]")
            lines.append(r["text"])
            lines.append("")
        return "\n".join(lines)