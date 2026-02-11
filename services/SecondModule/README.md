# 🚗 Assistant Sécurité Routière IA

Application Streamlit interactive pour l'analyse de risque routier basée sur l'intelligence artificielle et le Code de la Route tunisien.

## 📋 Description

Cette application analyse votre situation de conduite en temps réel et génère des conseils personnalisés adaptés au niveau de risque détecté. Elle utilise :

- **Groq LLM** (llama-3.3-70b-versatile) pour générer des conseils contextualisés
- **Code de la Route tunisien** comme base de connaissances
- **Statistiques d'accidents réels** pour évaluer les risques
- **Streamlit** pour une interface utilisateur moderne et intuitive

## ✨ Fonctionnalités

- ✅ Analyse multi-facteurs (fatigue, météo, trafic, durée)
- ✅ Score de risque calculé (0-100)
- ✅ 4 niveaux de risque : Faible, Modéré, Élevé, Critique
- ✅ Conseils personnalisés générés par IA
- ✅ Références au Code de la Route
- ✅ Interface moderne avec codes couleur
- ✅ Détection des combinaisons dangereuses
- ✅ Recommandations d'actions concrètes

## 🚀 Installation

### 1. Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### 2. Installation des dépendances

```bash
pip install -r requirements.txt
```

Ou manuellement :

```bash
pip install streamlit groq
```

## 🎯 Utilisation

### Lancer l'application

```bash
streamlit run app_securite_routiere.py
```

L'application s'ouvrira automatiquement dans votre navigateur par défaut à l'adresse : `http://localhost:8501`

### Utilisation de l'interface

1. **Sélectionnez vos paramètres de conduite** :
   - Niveau de fatigue (aucune, légère, modérée, sévère)
   - Type de conduite (jour, nuit, pluie, brouillard, trafic dense)
   - État du trafic (fluide, modéré, dense, embouteillage)
   - Conditions météo (clair, pluie, brouillard, neige, vent)
   - Durée prévue (<1h, 1-2h, 2-4h, >4h)

2. **Cliquez sur "Analyser la Situation"**

3. **Consultez les résultats** :
   - Score de risque avec code couleur
   - Facteurs aggravants identifiés
   - Conseil personnalisé généré par IA
   - Références au Code de la Route

## 📊 Niveaux de Risque

| Niveau | Score | Couleur | Description |
|--------|-------|---------|-------------|
| ✅ **Faible** | 0-24 | Vert | Conditions favorables, conseils de base |
| ⚠️ **Modéré** | 25-49 | Jaune | Vigilance accrue requise |
| 🚨 **Élevé** | 50-74 | Orange | Situation dangereuse, mesures obligatoires |
| 🔴 **Critique** | 75-100 | Rouge | Danger immédiat, arrêt recommandé |

## 🔧 Configuration

### Clé API Groq

L'application utilise une clé API Groq pour générer les conseils. La clé est actuellement codée en dur dans le fichier pour faciliter les tests.

**Pour une utilisation en production**, il est recommandé de :

1. Créer un fichier `.env` :
```
GROQ_API_KEY=votre_cle_api_ici
```

2. Modifier le code pour charger la clé depuis les variables d'environnement :
```python
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")
```

3. Installer python-dotenv :
```bash
pip install python-dotenv
```

## 📁 Structure du Projet

```
.
├── app_securite_routiere.py    # Application principale Streamlit
├── requirements.txt             # Dépendances Python
└── README.md                    # Documentation
```

## 🛡️ Sécurité et Confidentialité

- ⚠️ **Important** : Cette application est fournie à titre indicatif uniquement
- Les conseils générés ne remplacent pas le jugement personnel du conducteur
- En cas de doute sérieux sur votre capacité à conduire, abstenez-vous
- Les données saisies ne sont pas stockées ni transmises à des tiers

## 🧠 Algorithme de Calcul du Risque

Le score de risque est calculé selon la formule :

```
Score = (Fatigue × 40%) + (Météo × 25%) + (Situation × 15%) + (Trafic × 10%) + (Durée × 10%)
```

Des **bonus de risque** sont appliqués pour les combinaisons dangereuses :
- Fatigue + Nuit : +15 points
- Fatigue + Mauvaise météo : +10 points
- Brouillard + Nuit : +10 points

## 📚 Base de Connaissances

L'application s'appuie sur :

- **Code de la Route Tunisien** (Articles 25, 45, 78, 82, 95)
- Statistiques de sécurité routière
- Recommandations officielles de prévention

## 🎨 Personnalisation

L'interface peut être personnalisée en modifiant :

- Les styles CSS dans la section `st.markdown(""" <style> ... </style> """)`
- Les couleurs des niveaux de risque
- Les prompts pour l'IA
- Les poids de calcul du score

## 🐛 Dépannage

### L'application ne démarre pas
```bash
# Vérifier la version de Python
python --version  # Doit être >= 3.8

# Réinstaller les dépendances
pip install --upgrade -r requirements.txt
```

### Erreur API Groq
- Vérifier que la clé API est valide
- Vérifier la connexion internet
- Consulter les logs dans le terminal

### Interface blanche ou erreur d'affichage
```bash
# Vider le cache de Streamlit
streamlit cache clear
```

## 📝 Licence

Ce projet est fourni à des fins éducatives et de démonstration.

## 👥 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer des améliorations
- Ajouter de nouvelles fonctionnalités

## 📞 Support

Pour toute question ou problème, consultez la documentation de :
- [Streamlit](https://docs.streamlit.io/)
- [Groq API](https://console.groq.com/docs)

---

**⚠️ Disclaimer** : Cet outil est conçu pour sensibiliser à la sécurité routière. Il ne remplace en aucun cas le bon jugement du conducteur ni les obligations légales du Code de la Route. Conduisez toujours de manière responsable.
