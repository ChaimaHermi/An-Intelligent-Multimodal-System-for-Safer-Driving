import re
import json
import numpy as np
from typing import List, Tuple, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum
import hashlib
from datetime import datetime
import os
import sys
import importlib.util
import streamlit as st
from litai import LLM

# ============================================================================
# RAG SYSTEM FOR TUNISIAN ROAD SAFETY - STREAMLIT VERSION
# ============================================================================

class RiskLevel(Enum):
    CRITICAL = "🔴 CRITIQUE"
    HIGH = "🟠 ÉLEVÉ"
    MEDIUM = "🟡 MOYEN"
    LOW = "🟢 FAIBLE"
    INFO = "🔵 INFORMATION"

@dataclass
class Document:
    id: str
    title: str
    content: str
    risk_level: RiskLevel
    category: str
    keywords: List[str]
    legal_references: List[str]
    statistics: Dict[str, Any]
    metadata: Dict[str, Any]
    embedding: Optional[np.ndarray] = None

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "risk_level": self.risk_level.value,
            "category": self.category,
            "keywords": self.keywords,
            "legal_references": self.legal_references,
            "statistics": self.statistics,
            "metadata": self.metadata
        }


class EmbeddingModel:
    def __init__(self):
        self.word_vectors = {}
        self.dimension = 300

    def fit(self, documents: List[Document]):
        from collections import defaultdict

        word_doc_count = defaultdict(int)

        for doc in documents:
            words = set(self._tokenize(doc.content + " " + " ".join(doc.keywords)))
            for word in words:
                word_doc_count[word] += 1

        for doc in documents:
            words = self._tokenize(doc.content + " " + " ".join(doc.keywords))
            word_freq = defaultdict(int)

            for word in words:
                word_freq[word] += 1

            embedding = np.zeros(self.dimension)

            for word, freq in word_freq.items():
                if word in self.word_vectors:
                    word_vec = self.word_vectors[word]
                else:
                    np.random.seed(hash(word) % 2**32)
                    word_vec = np.random.randn(self.dimension)
                    word_vec = word_vec / np.linalg.norm(word_vec)
                    self.word_vectors[word] = word_vec

                tf = freq / len(words) if len(words) > 0 else 0
                idf = np.log(len(documents) / (word_doc_count[word] + 1))
                embedding += word_vec * tf * idf

            norm = np.linalg.norm(embedding)
            if norm > 0:
                embedding = embedding / norm

            doc.embedding = embedding

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b[a-zà-ÿ]+\b', text)
        return tokens

    def embed_query(self, query: str) -> np.ndarray:
        words = self._tokenize(query)
        embedding = np.zeros(self.dimension)
        for word in words:
            if word in self.word_vectors:
                embedding += self.word_vectors[word]
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = embedding / norm
        return embedding


class VectorStore:
    def __init__(self):
        self.documents: List[Document] = []
        self.embeddings: Optional[np.ndarray] = None
        self.index = {}

    def add_documents(self, documents: List[Document], embedding_model: EmbeddingModel):
        self.documents.extend(documents)
        embedding_model.fit(self.documents)
        embeddings = []
        for doc in self.documents:
            if doc.embedding is not None:
                embeddings.append(doc.embedding)
        if embeddings:
            self.embeddings = np.vstack(embeddings)
            self.index = {doc.id: idx for idx, doc in enumerate(self.documents)}

    def similarity_search(self, query_embedding: np.ndarray, k: int = 5) -> List[Tuple[Document, float]]:
        if self.embeddings is None or len(self.documents) == 0:
            return []
        similarities = np.dot(self.embeddings, query_embedding)
        positive_indices = np.where(similarities > 0)[0]
        if len(positive_indices) == 0:
            return []
        filtered_sims = similarities[positive_indices]
        top_indices = np.argsort(filtered_sims)[-k:][::-1]
        results = []
        for idx in top_indices:
            orig_idx = positive_indices[idx]
            results.append((self.documents[orig_idx], float(similarities[orig_idx])))
        return results

    def hybrid_search(self, query: str, query_embedding: np.ndarray,
                     keyword_weight: float = 0.3, semantic_weight: float = 0.7,
                     k: int = 5) -> List[Tuple[Document, float]]:
        query_words = set(re.findall(r'\w+', query.lower()))

        keyword_results = []
        for doc in self.documents:
            score = 0
            keywords_in_doc = set(kw.lower() for kw in doc.keywords)
            score += len(query_words & keywords_in_doc) * 10
            if any(word in doc.title.lower() for word in query_words):
                score += 5
            if score > 0:
                keyword_results.append((doc, score))

        if keyword_results:
            max_score = max(s for _, s in keyword_results)
            if max_score > 0:
                keyword_results = [(d, s / max_score) for d, s in keyword_results]
            else:
                keyword_results = []

        semantic_results = self.similarity_search(query_embedding, k=len(self.documents))

        combined = {}
        for doc, score in semantic_results:
            combined[doc.id] = combined.get(doc.id, 0.0) + score * semantic_weight
        for doc, score in keyword_results:
            combined[doc.id] = combined.get(doc.id, 0.0) + score * keyword_weight

        sorted_docs = sorted(combined.items(), key=lambda x: x[1], reverse=True)
        doc_map = {doc.id: doc for doc in self.documents}
        return [(doc_map[did], score) for did, score in sorted_docs[:k] if did in doc_map]


class ResponseGenerator:
    def __init__(self):
        self.llm = LLM(model="openai/gpt-4o")
        self.templates = {
            "legal": """En tant que policier tunisien ou professeur de conduite, répondez directement et brièvement à la question en vous basant sur le contexte suivant. Concentrez-vous UNIQUEMENT sur les pénalités, amendes et sanctions légales.

Question: {query}
Contexte: {context}

Fournissez une réponse brève et directe en français (2-3 phrases maximum) en vous concentrant sur les chiffres du contexte.""",

            "statistical": """Répondez directement et brièvement à la question en vous basant sur les données statistiques suivantes.

Question: {query}
Contexte: {context}

Fournissez une réponse brève et directe en français (2-3 phrases maximum).""",

            "emergency": """C'est une situation d'URGENCE. Fournissez les actions immédiates et critiques basées sur le contexte.

Question: {query}
Contexte: {context}

Fournissez des instructions d'urgence claires en français (4-5 phrases maximum).""",

            "general": """Répondez directement et brièvement à la question en vous basant UNIQUEMENT sur le contexte suivant. Soyez bref et précis.

Question: {query}
Contexte: {context}

Fournissez une réponse brève et directe en français (2-3 phrases maximum)."""
        }

    def generate_response(self, query: str, relevant_docs: List[Tuple[Document, float]]) -> Dict[str, Any]:
        if not relevant_docs:
            return {
                "status": "no_results",
                "answer": "Je n'ai pas trouvé d'informations pertinentes. Veuillez reformuler votre question.",
                "sources": [],
                "is_emergency": False,
                "suggested_actions": [],
                "legal_references": [],
                "emergency_contacts": {},
                "top_document": None
            }

        top_doc, top_score = relevant_docs[0]
        all_docs = [doc for doc, _ in relevant_docs]
        response_type = self._determine_response_type(query, all_docs)
        llm_answer = self._construct_answer(query, all_docs, response_type)

        return {
            "status": "success",
            "query": query,
            "answer": llm_answer,
            "response_type": response_type,
            "top_document": {
                "title": top_doc.title,
                "risk_level": top_doc.risk_level.value,
                "confidence_score": round(top_score, 3),
                "category": top_doc.category
            },
            "sources": [{"title": d.title, "category": d.category} for d in all_docs[:3]],
            "is_emergency": response_type == "emergency",
            "suggested_actions": self._get_suggested_actions(top_doc) if response_type == "emergency" else [],
            "legal_references": list(set(ref for d in all_docs[:2] for ref in d.legal_references))[:3],
            "emergency_contacts": {"Police": "197", "SAMU": "190", "Protection Civile": "198"} if response_type == "emergency" else {}
        }

    def _determine_response_type(self, query: str, docs: List[Document]) -> str:
        q = query.lower()
        if any(kw in q for kw in ["accident", "urgent", "blessé", "sang", "incendie", "secours", "urgence", "collision", "mort"]):
            return "emergency"
        elif any(kw in q for kw in ["amende", "sanction", "pénalité", "penalité", "infraction", "points", "dt", "retrait", "suspension"]):
            return "legal"
        elif any(kw in q for kw in ["statistique", "pourcentage", "%", "chiffres", "combien"]):
            return "statistical"
        return "general"

    def _construct_answer(self, query: str, docs: List[Document], response_type: str) -> str:
        context = "\n\n".join([f"Document: {d.title}\n{d.content[:800]}" for d in docs[:2]])
        template = self.templates.get(response_type, self.templates["general"])
        prompt = template.format(query=query, context=context)
        try:
            return self.llm.chat(prompt).strip()
        except Exception as e:
            return f"Erreur lors de la génération de la réponse: {e}"

    def _get_suggested_actions(self, doc: Document) -> List[str]:
        if doc.risk_level == RiskLevel.CRITICAL:
            return [
                "🔺 Sécuriser la zone avec triangle de présignalisation",
                "📞 Appeler immédiatement les secours (197 ou 190)",
                "🚫 Ne pas déplacer les blessés graves",
                "🤝 Porter assistance dans la limite de vos capacités"
            ]
        return []


class KnowledgeBaseLoader:
    @staticmethod
    def load_knowledge_base(kb_path: str = "knowledge_base.py") -> List[Document]:
        if not os.path.exists(kb_path):
            return []
        try:
            spec = importlib.util.spec_from_file_location("knowledge_base", kb_path)
            if spec is None or spec.loader is None:
                return []
            kb_module = importlib.util.module_from_spec(spec)
            sys.modules["knowledge_base"] = kb_module
            spec.loader.exec_module(kb_module)

            if not hasattr(kb_module, 'KNOWLEDGE_BASE'):
                return []

            documents = []
            risk_map = {
                "CRITICAL": RiskLevel.CRITICAL, "HIGH": RiskLevel.HIGH,
                "MEDIUM": RiskLevel.MEDIUM, "LOW": RiskLevel.LOW, "INFO": RiskLevel.INFO
            }
            for item in kb_module.KNOWLEDGE_BASE:
                doc_id = item.get("id", f"kb_{hashlib.md5(item['title'].encode()).hexdigest()[:8]}")
                risk_level = risk_map.get(item.get("risk_level", "MEDIUM").upper(), RiskLevel.MEDIUM)
                documents.append(Document(
                    id=doc_id, title=item["title"], content=item["content"],
                    risk_level=risk_level, category=item.get("category", "Général"),
                    keywords=item.get("keywords", []),
                    legal_references=item.get("legal_references", []),
                    statistics=item.get("statistics", {}),
                    metadata=item.get("metadata", {})
                ))
            return documents
        except Exception:
            return []


class TunisianRoadSafetyRAG:
    def __init__(self, kb_path: str = "knowledge_base.py"):
        self.embedding_model = EmbeddingModel()
        self.vector_store = VectorStore()
        self.response_generator = ResponseGenerator()

        self.documents = KnowledgeBaseLoader.load_knowledge_base(kb_path)
        if not self.documents:
            self.documents = self._get_default_documents()

        if self.documents:
            self.vector_store.add_documents(self.documents, self.embedding_model)

    def _get_default_documents(self) -> List[Document]:
        return [
            Document(
                id="fatigue_001", title="Fatigue au volant sur autoroute",
                content="La fatigue est responsable de 20% des accidents mortels sur autoroute. Faire une pause toutes les 2 heures. Amende: 300 DT.",
                risk_level=RiskLevel.HIGH, category="Comportement",
                keywords=["fatigue", "sommeil", "autoroute", "pause"],
                legal_references=["Article 85-86"], statistics={}, metadata={}
            ),
        ]

    def query(self, question: str) -> Dict[str, Any]:
        query_embedding = self.embedding_model.embed_query(question)
        relevant_docs = self.vector_store.hybrid_search(question, query_embedding)
        return self.response_generator.generate_response(question, relevant_docs)


# ============================================================================
# STREAMLIT INTERFACE
# ============================================================================

def init_rag_system():
    """Initialize the RAG system once and cache it in session state."""
    if "rag_system" not in st.session_state:
        with st.spinner("🚀 Chargement du système RAG..."):
            # Try multiple possible knowledge base paths
            kb_paths = ["knowledge_base.py", "road_safety_tunisia.py", "safety_docs_2024.py"]
            rag = None
            for path in kb_paths:
                if os.path.exists(path):
                    rag = TunisianRoadSafetyRAG(kb_path=path)
                    break
            if rag is None:
                rag = TunisianRoadSafetyRAG(kb_path="knowledge_base.py")
            st.session_state.rag_system = rag
            st.session_state.doc_count = len(rag.documents)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []


def render_sidebar():
    """Render the sidebar with info and theme browser."""
    with st.sidebar:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/ce/Flag_of_Tunisia.svg/200px-Flag_of_Tunisia.svg.png", width=80)
        st.title("🇹🇳 Code Routier TN")

        st.markdown("---")
        st.metric("📚 Documents indexés", st.session_state.doc_count)

        st.markdown("---")
        st.subheader("📂 Thèmes disponibles")

        # Group documents by category
        categories = {}
        for doc in st.session_state.rag_system.documents:
            cat = doc.category
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(doc)

        for cat, docs in sorted(categories.items()):
            with st.expander(f"📁 {cat} ({len(docs)})"):
                for doc in docs:
                    st.markdown(f"• {doc.risk_level.value} **{doc.title}**")

        st.markdown("---")
        st.subheader("📞 Urgences")
        st.markdown("""
        | Service | Numéro |
        |---------|--------|
        | 🚔 Police | **197** |
        | 🚑 SAMU | **190** |
        | 🧯 Protection Civile | **198** |
        | 🛡️ Garde Nationale | **193** |
        | ℹ️ Info Routes | **1717** |
        """)

        st.markdown("---")
        if st.button("🗑️ Effacer l'historique", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()


def render_welcome():
    """Render welcome message if no chat history."""
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1>🚗 Assistant Sécurité Routière Tunisienne</h1>
        <p style="font-size: 1.2rem; color: #666;">
            Posez vos questions sur le code de la route tunisien, les amendes,
            les règles de conduite et la sécurité routière.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Quick-access buttons
    st.markdown("### 💡 Questions fréquentes")
    cols = st.columns(2)
    sample_questions = [
        "Quelle est l'amende pour excès de vitesse ?",
        "Règles de la ceinture de sécurité ?",
        "Que faire en cas d'accident ?",
        "Téléphone au volant : sanctions ?",
        "Limites de vitesse sur autoroute ?",
        "Taux d'alcool autorisé en Tunisie ?",
    ]
    for i, question in enumerate(sample_questions):
        col = cols[i % 2]
        if col.button(question, key=f"sample_{i}", use_container_width=True):
            st.session_state.chat_history.append({"role": "user", "content": question})
            with st.spinner("🔍 Recherche en cours..."):
                response = st.session_state.rag_system.query(question)
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            st.rerun()


def render_response(response: Dict[str, Any]):
    """Render a formatted response in the chat."""
    if response["status"] == "no_results":
        st.warning(response["answer"])
        return

    # Main answer
    st.markdown(response["answer"])

    # Metadata in columns
    if response.get("top_document"):
        col1, col2, col3 = st.columns(3)
        col1.markdown(f"**Risque:** {response['top_document']['risk_level']}")
        col2.markdown(f"**Confiance:** {response['top_document']['confidence_score']}")
        col3.markdown(f"**Catégorie:** {response['top_document']['category']}")

    # Sources
    if response.get("sources"):
        with st.expander("📚 Sources consultées"):
            for src in response["sources"]:
                st.markdown(f"• **{src['title']}** ({src['category']})")

    # Legal references
    if response.get("legal_references"):
        with st.expander("📜 Références légales"):
            for ref in response["legal_references"]:
                st.markdown(f"• {ref}")

    # Emergency section
    if response.get("is_emergency"):
        st.error("🚨 **SITUATION D'URGENCE**")
        if response.get("suggested_actions"):
            for action in response["suggested_actions"]:
                st.markdown(f"  {action}")
        if response.get("emergency_contacts"):
            st.markdown("**📞 Contacts d'urgence:**")
            for service, number in response["emergency_contacts"].items():
                st.markdown(f"  • **{service}:** {number}")


def render_chat():
    """Render the chat history."""
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"], avatar="🧑" if message["role"] == "user" else "🤖"):
            if message["role"] == "assistant" and isinstance(message["content"], dict):
                render_response(message["content"])
            else:
                st.markdown(message["content"])


def main():
    st.set_page_config(
        page_title="🚗 Sécurité Routière Tunisienne",
        page_icon="🇹🇳",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Custom CSS
    st.markdown("""
    <style>
        .stChatMessage { padding: 1rem; }
        .stExpander { border: 1px solid #ddd; border-radius: 8px; }
        section[data-testid="stSidebar"] { background-color: #f8f9fa; }
        .stMetric { background-color: #f0f2f6; padding: 1rem; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

    # Initialize
    init_rag_system()
    render_sidebar()

    # Welcome or chat
    if not st.session_state.chat_history:
        render_welcome()
    else:
        render_chat()

    # Chat input
    if user_input := st.chat_input("Posez votre question sur le code de la route tunisien..."):
        # Add user message
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        # Display user message immediately
        with st.chat_message("user", avatar="🧑"):
            st.markdown(user_input)

        # Generate response
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("🔍 Recherche et analyse en cours..."):
                response = st.session_state.rag_system.query(user_input)
            render_response(response)

        # Save to history
        st.session_state.chat_history.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    main()