import streamlit as st
import requests
import pandas as pd

# Configuration de la page
st.set_page_config(
    page_title="ToxicGuard AI | Modération Connectée",
    page_icon="🛡️",
    layout="centered"
)

# Design CSS personnalisé (On garde le même style Premium)
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stTextArea textarea { background-color: #161b22; color: white; border: 1px solid #30363d; border-radius: 10px; }
    .toxic-card { padding: 20px; border-radius: 15px; background: linear-gradient(135deg, #1f1f1f 0%, #2d2d2d 100%); border-left: 5px solid #ff4b4b; margin-bottom: 10px; }
    .clean-card { padding: 20px; border-radius: 15px; background: linear-gradient(135deg, #1f1f1f 0%, #2d2d2d 100%); border-left: 5px solid #00c853; margin-bottom: 10px; }
    .title-text { font-family: 'Inter', sans-serif; font-weight: 800; background: -webkit-linear-gradient(#ff4b4b, #ff8a8a); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 3rem; }
    </style>
""", unsafe_allow_html=True)

# URL de votre API locale
API_URL = "http://localhost:8000/v1/moderate"

# Header
st.markdown('<p class="title-text">ToxicGuard AI</p>', unsafe_allow_html=True)
st.markdown("### Interface Client Connectée à l'API")
st.write("Cette interface envoie des requêtes HTTP à votre serveur de modération.")

# Zone d'entrée
user_input = st.text_area("Entrez le commentaire à analyser :", placeholder="Tapez quelque chose ici...", height=150)

if st.button("Analyser via l'API"):
    if user_input.strip() == "":
        st.warning("Veuillez entrer un texte.")
    else:
        try:
            with st.spinner("Appel de l'API de modération..."):
                # On appelle l'API FastAPI
                response = requests.post(API_URL, json={"text": user_input})
                
                if response.status_code == 200:
                    data = response.json()
                    decision = data["decision"]
                    score = data["toxicity_score"]
                    latency = data["latency_ms"]
                    
                    st.markdown("---")
                    
                    if decision == "BLOCK":
                        st.markdown(f'<div class="toxic-card"><h4>⚠️ Décision API : BLOCK</h4>Le contenu a été jugé trop toxique.</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="clean-card"><h4>✅ Décision API : ALLOW</h4>Le contenu est conforme.</div>', unsafe_allow_html=True)

                    # Affichage des scores
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Score de Toxicité", f"{score:.2%}")
                    col2.metric("Latence API", f"{latency} ms")
                    col3.metric("Statut Serveur", "En ligne 🟢")
                    
                    st.progress(score)
                    
                else:
                    st.error(f"Erreur API : Le serveur a répondu avec le code {response.status_code}")
                    
        except Exception as e:
            st.error(f"Impossible de contacter l'API. Vérifiez que le serveur tourne sur le port 8000. Erreur : {e}")

# Footer
st.markdown("---")
st.caption("Architecture : Client Streamlit ➡️ Serveur FastAPI ➡️ Modèle BERT")

