"""
retriever.py
------------
RAG module: embeds the road safety rules database and retrieves
the most relevant rules for a given situation using semantic search.
"""

import os
import json
import pickle
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer
import faiss


# ─────────────────────────────────────────────
#  PATHS
# ─────────────────────────────────────────────

BASE_DIR      = Path(__file__).parent.parent
DATA_PATH     = BASE_DIR / "data" / "road_safety_rules.json"
INDEX_PATH    = BASE_DIR / "embeddings" / "rules.index"
META_PATH     = BASE_DIR / "embeddings" / "rules_meta.pkl"
EMBEDDINGS_DIR = BASE_DIR / "embeddings"


# ─────────────────────────────────────────────
#  MODEL
#  paraphrase-multilingual-MiniLM-L12-v2 works
#  well for French without needing a French-only model
# ─────────────────────────────────────────────

MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"


# ─────────────────────────────────────────────
#  BUILD INDEX  (run once to create the vector DB)
# ─────────────────────────────────────────────

def build_index():
    """
    Load rules from JSON, embed them, and save a FAISS index.
    Run this once before using retrieve_rules().
    """
    print("📦 Loading rules from JSON...")
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        rules = json.load(f)

    print(f"   → {len(rules)} rules loaded")

    print("🤖 Loading embedding model...")
    model = SentenceTransformer(MODEL_NAME)

    print("🔢 Computing embeddings...")
    texts = [rule["text"] for rule in rules]
    embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)

    print("💾 Saving FAISS index...")
    EMBEDDINGS_DIR.mkdir(parents=True, exist_ok=True)

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings.astype(np.float32))

    faiss.write_index(index, str(INDEX_PATH))

    with open(META_PATH, "wb") as f:
        pickle.dump(rules, f)

    print(f"✅ Index saved: {INDEX_PATH}")
    print(f"✅ Metadata saved: {META_PATH}")
    return index, rules, model


# ─────────────────────────────────────────────
#  RETRIEVER CLASS
# ─────────────────────────────────────────────

class RuleRetriever:
    """
    Loads the FAISS index and provides semantic search over road safety rules.
    Usage:
        retriever = RuleRetriever()
        rules = retriever.search("je suis fatigué et il pleut", top_k=3)
    """

    def __init__(self):
        # Auto-build index if it doesn't exist yet
        if not INDEX_PATH.exists() or not META_PATH.exists():
            print("⚠️  Index not found. Building it now...")
            self.index, self.rules, self.model = build_index()
        else:
            print("📂 Loading existing index...")
            self.model = SentenceTransformer(MODEL_NAME)
            self.index = faiss.read_index(str(INDEX_PATH))
            with open(META_PATH, "rb") as f:
                self.rules = pickle.load(f)
            print(f"   → {len(self.rules)} rules in index")

    def search(self, query: str, top_k: int = 3, factors: list = None) -> list:
        """
        Find the most relevant rules for a given situation.

        Args:
            query:   user's situation text
            top_k:   number of rules to return
            factors: detected risk factors (used to boost category matching)

        Returns:
            list of rule dicts, sorted by relevance
        """
        # Embed the query
        query_embedding = self.model.encode([query], convert_to_numpy=True)

        # Search in FAISS
        distances, indices = self.index.search(
            query_embedding.astype(np.float32), top_k * 2  # fetch more, then filter
        )

        retrieved = []
        seen_ids = set()

        for dist, idx in zip(distances[0], indices[0]):
            if idx == -1:
                continue
            rule = self.rules[idx]
            if rule["id"] in seen_ids:
                continue
            seen_ids.add(rule["id"])

            # Compute a relevance score (lower L2 distance = more relevant)
            relevance = float(1 / (1 + dist))

            # Boost score if rule category matches a detected factor
            category_boost = 0
            if factors and rule.get("category") in factors:
                category_boost = 0.3

            retrieved.append({
                **rule,
                "relevance": round(relevance + category_boost, 4)
            })

        # Sort by relevance (highest first) and return top_k
        retrieved.sort(key=lambda x: x["relevance"], reverse=True)
        return retrieved[:top_k]

    def search_by_category(self, categories: list, max_per_category: int = 2) -> list:
        """
        Fallback: directly fetch rules by category when semantic search
        is not specific enough.
        """
        results = []
        for rule in self.rules:
            if rule.get("category") in categories:
                results.append(rule)
            if len(results) >= max_per_category * len(categories):
                break
        return results

    def format_context(self, rules: list) -> str:
        """
        Format retrieved rules into a clean string for LLM injection.
        """
        lines = []
        for i, rule in enumerate(rules, 1):
            lines.append(f"[Règle {i} — {rule.get('source', 'Source officielle')}]")
            lines.append(rule["text"])
            lines.append("")
        return "\n".join(lines)


# ─────────────────────────────────────────────
#  QUICK TEST  (run: python retriever.py)
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("RETRIEVER TEST")
    print("=" * 60)

    retriever = RuleRetriever()

    queries = [
        ("Je conduis depuis 5h et je me sens somnolent", ["fatigue"]),
        ("Il pleut beaucoup et il fait nuit noire",       ["pluie", "nuit"]),
        ("J'ai bu 2 verres de vin ce soir",               ["alcool"]),
    ]

    for query, factors in queries:
        print(f"\n📝 Query  : {query}")
        print(f"⚠️  Factors: {factors}")
        results = retriever.search(query, top_k=2, factors=factors)
        for r in results:
            print(f"   [{r['category']}] (relevance={r['relevance']}) {r['text'][:80]}...")