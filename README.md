# 🚗 Assistant Sécurité Routière Tunisienne

Un système RAG (Retrieval Augmented Generation) interactif pour répondre aux questions sur le code de la route tunisien, les amendes, les sanctions et la sécurité routière.

## 🎯 Fonctionnalités

- **💬 Interface de chat interactive** avec Streamlit
- **🔍 Recherche hybride** (sémantique + mots-clés) dans la base de connaissances
- **🤖 Génération de réponses** contextualisées avec GPT-4o via LitAI
- **⚠️ Détection des situations d'urgence** avec protocoles spécifiques
- **📜 Références légales** au code de la route tunisien
- **📊 Statistiques** de sécurité routière (ONSR 2023-2024)
- **📞 Contacts d'urgence** tunisiens (Police 197, SAMU 190, etc.)
- **🎨 Interface bilingue** (Français/Arabe) avec émojis pour les niveaux de risque

## 🛠️ Technologies Utilisées

- **Streamlit** - Interface utilisateur web interactive
- **LitAI** - Intégration LLM (GPT-4o)
- **NumPy** - Calculs vectoriels et embeddings
- **Custom Embedding Model** - TF-IDF pondéré pour la recherche sémantique
- **Python 3.8+** - Langage de base

## 📋 Prérequis

- Python 3.8 ou supérieur
- Clé API OpenAI (pour LitAI)

## 🚀 Installation

1. **Cloner le projet:**
   ```bash
   cd week2
   ```

2. **Installer les dépendances:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurer la clé API:**
   
   Définir la variable d'environnement pour OpenAI:
   ```bash
   # Windows PowerShell
   $env:OPENAI_API_KEY="votre-cle-api"
   
   # Windows CMD
   set OPENAI_API_KEY=votre-cle-api
   
   # Linux/Mac
   export OPENAI_API_KEY=votre-cle-api
   ```

## 📦 Structure du Projet

```
week2/
├── main.py              # Application Streamlit principale
├── knowledge_base.py    # Base de connaissances (code routier tunisien)
├── requirements.txt     # Dépendances Python
└── README.md           # Documentation
```

## ▶️ Utilisation

1. **Lancer l'application:**
   ```bash
   streamlit run main.py
   ```

2. **Accéder à l'interface:**
   - L'application s'ouvrira automatiquement dans votre navigateur
   - URL par défaut: `http://localhost:8501`

3. **Poser des questions:**
   - Utiliser les questions suggérées
   - Ou taper votre propre question dans la zone de chat

## 💡 Exemples de Questions

- "Quelle est l'amende pour excès de vitesse ?"
- "Règles de la ceinture de sécurité ?"
- "Que faire en cas d'accident ?"
- "Téléphone au volant : sanctions ?"
- "Limites de vitesse sur autoroute ?"
- "Taux d'alcool autorisé en Tunisie ?"

## 🗂️ Base de Connaissances

Le fichier `knowledge_base.py` contient:

- **Infractions et sanctions** (excès de vitesse, téléphone, alcool, etc.)
- **Règles de sécurité** (ceinture, casque, éclairage, etc.)
- **Protocoles d'urgence** (accidents, pannes, premiers secours)
- **Statistiques ONSR** (2023-2024)
- **Références légales** (articles du code de la route)
- **Contacts d'urgence** tunisiens

### Structure des documents:

```python
{
    "title": "Titre du document",
    "risk_level": "CRITICAL|HIGH|MEDIUM|LOW|INFO",
    "content": "Contenu détaillé...",
    "category": "Catégorie",
    "keywords": ["mot1", "mot2"],
    "legal_references": ["Article X"],
    "statistics": {...},
    "metadata": {...}
}
```

## 🔧 Architecture Technique

### 1. **EmbeddingModel**
- Calcul TF-IDF pondéré pour chaque document
- Dimension: 300
- Tokenisation avec support des accents français

### 2. **VectorStore**
- Stockage des embeddings de documents
- Recherche par similarité cosinus
- Recherche hybride (sémantique + mots-clés)

### 3. **ResponseGenerator**
- Templates spécialisés par type de question (legal, statistical, emergency, general)
- Intégration LitAI avec GPT-4o
- Détection automatique du type de question
- Génération de réponses contextualisées

### 4. **KnowledgeBaseLoader**
- Chargement dynamique de `knowledge_base.py`
- Validation et conversion en objets `Document`
- Fallback vers documents par défaut

## 📞 Contacts d'Urgence (Tunisie)

| Service | Numéro |
|---------|--------|
| 🚔 Police | **197** |
| 🚑 SAMU | **190** |
| 🧯 Protection Civile | **198** |
| 🛡️ Garde Nationale | **193** |
| ℹ️ Info Routes | **1717** |

## ⚠️ Niveaux de Risque

- 🔴 **CRITIQUE** - Danger immédiat, action urgente requise
- 🟠 **ÉLEVÉ** - Risque important, vigilance accrue
- 🟡 **MOYEN** - Risque modéré, attention nécessaire
- 🟢 **FAIBLE** - Risque limité, information préventive
- 🔵 **INFORMATION** - Contenu éducatif ou statistique

## 🔄 Personnalisation

Pour ajouter du contenu à la base de connaissances:

1. Éditer `knowledge_base.py`
2. Ajouter un nouveau dictionnaire dans `KNOWLEDGE_BASE`
3. Respecter la structure requise (voir ci-dessus)
4. Relancer l'application

## 📝 Notes Importantes

- Le système répond **uniquement** basé sur la base de connaissances
- Les statistiques sont basées sur l'ONSR (Observatoire National de Sécurité Routière) 2023-2024
- Les références légales sont extraites du code de la route tunisien
- En cas de situation d'urgence réelle, **toujours appeler les secours** (197/190)

## 🤝 Contribution

Pour contribuer au projet:
1. Vérifier la précision des informations légales
2. Ajouter de nouvelles catégories dans `knowledge_base.py`
3. Améliorer les templates de réponse
4. Signaler les bugs ou inexactitudes

## 📄 Licence

Ce projet est destiné à des fins éducatives et informatives. Les informations fournies ne remplacent pas les conseils juridiques professionnels.

## 🙏 Remerciements

- **ONSR Tunisie** - Statistiques de sécurité routière
- **Code de la Route Tunisien** - Références légales
- **Streamlit** - Framework d'interface
- **LitAI** - Intégration LLM
