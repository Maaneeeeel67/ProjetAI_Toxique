@"
# 🛡️ ToxicGuard AI : Détection et Modération de Commentaires Toxiques

> Une solution complète d'IA pour modérer les réseaux sociaux en temps réel, avec API REST, intégration Instagram (Webhook) et tableau de bord interactif.

## 🎯 Objectif
Ce projet propose un système de modération automatique de commentaires toxiques. Il combine un modèle NLP avancé (**Toxic-BERT**) avec une architecture micro-services pour bloquer les contenus haineux instantanément.

## ⚙️ Architecture du Projet
Le projet est divisé en plusieurs modules :
- **`src/interface.py`** : Cœur de l'IA. Utilise le modèle `unitary/toxic-bert` (HuggingFace) pour classifier le texte en 6 catégories (toxic, severe_toxic, obscene, threat, insult, identity_hate).
- **`src/api.py`** : Serveur **FastAPI** exposant une route `/v1/moderate` et un **Webhook pour Instagram/Meta**. Il supprime automatiquement les commentaires toxiques sur Instagram si le score dépasse 50%.
- **`src/app_streamlit.py`** : Interface client Streamlit connectée à l'API pour tester la modération en temps réel.
- **`src/social_sim.py`** : Simulation d'un fil d'actualité type Instagram avec un tableau de bord Admin sécurisé (login) pour voir les logs de modération (Explainable AI).
- **`src/train_baseline.py`** : Entraînement d'un modèle baseline (TF-IDF + Logistic Regression).
- **`src/train_transformer.py`** : Script de fine-tuning de `xlm-roberta-base` sur un dataset de toxicité.
- **`src/eda.py`** : Analyse exploratoire des données.

## 🚀 Installation & Lancement

**1. Cloner le repo et installer les dépendances :**
``````bash
git clone https://github.com/Maaneeeeel67/ProjetAI_Toxique.git
cd ProjetAI_Toxique
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
