import streamlit as st
import requests
import time

st.set_page_config(page_title="SocialGuard", page_icon="🛡️", layout="centered")

API_URL = "http://127.0.0.1:8000/v1/moderate"

# Initialisation des variables d'état (Likes, Commentaires, Authentification)
if "likes" not in st.session_state:
    st.session_state.likes = 124
if "is_liked" not in st.session_state:
    st.session_state.is_liked = False

if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

if "comments" not in st.session_state:
    st.session_state.comments = [
        {"user": "Alice", "avatar": "👩", "text": "This is amazing! Great work on the AI integration. 👏", "status": "ALLOW", "categories": {}},
        {"user": "Bob", "avatar": "👨", "text": "Can't wait to see the final defense tomorrow!", "status": "ALLOW", "categories": {}}
    ]

# Navigation latérale (Sidebar)
st.sidebar.markdown("""
    <div style="text-align: center; margin-bottom: 20px;">
        <span style="font-size: 50px;">🛡️</span>
        <h2 style="margin-top: 10px; font-weight: 800; color: #1a1a1a;">ToxicGuard</h2>
        <p style="color: #65676B; font-size: 13px;">AI Control Panel v1.0</p>
    </div>
""", unsafe_allow_html=True)

page = st.sidebar.radio("Navigation", ["📱 Instagram Feed", "🔑 Admin Dashboard"])

# CSS Avancé
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stApp {
        background-color: #f0f2f5;
        font-family: 'Inter', sans-serif;
    }
    
    [data-testid="block-container"] {
        background-color: white;
        border-radius: 12px;
        padding: 0px 0px 20px 0px !important;
        max-width: 650px;
        margin-top: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border: 1px solid #e4e6eb;
        overflow: hidden;
    }

    .custom-navbar {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        background-color: white;
        height: 60px;
        display: flex;
        align-items: center;
        padding: 0 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04);
        z-index: 1000;
        justify-content: space-between;
    }
    .brand {
        font-size: 20px;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #FF3366, #FF9933);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .post-header { display: flex; align-items: center; padding: 20px; }
    .avatar { width: 44px; height: 44px; border-radius: 50%; background-color: #f0f2f5; display: flex; align-items: center; justify-content: center; font-size: 22px; margin-right: 12px; border: 1px solid #e0e0e0; }
    .user-name { font-weight: 600; color: #050505; font-size: 15px; }
    .post-time { color: #65676B; font-size: 13px; }
    .post-text { padding: 0 20px 15px 20px; color: #050505; font-size: 15px; line-height: 1.5; }
    
    div[data-testid="column"] button {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        color: #65676B !important;
        font-weight: 600 !important;
        font-size: 15px !important;
        padding: 10px 0 !important;
        transition: 0.2s;
    }
    div[data-testid="column"] button:hover {
        color: #050505 !important;
        background-color: #f2f2f2 !important;
        border-radius: 8px;
    }
    
    .comments-section { padding: 0 20px; }
    .comment-row { display: flex; margin-bottom: 15px; align-items: center; }
    .comment-avatar { width: 32px; height: 32px; border-radius: 50%; background-color: #e0e0e0; display: flex; align-items: center; justify-content: center; font-size: 16px; margin-right: 10px; flex-shrink: 0; }
    .clean-comment { background-color: #f0f2f5; padding: 10px 14px; border-radius: 18px; color: #050505; font-size: 14px; max-width: 85%; }
    .comment-author { font-weight: 600; margin-right: 5px; color: #050505; }
    .blocked-comment { background-color: #fff0f0; color: #d32f2f; padding: 10px 14px; border-radius: 18px; font-size: 14px; font-style: italic; border: 1px solid #ffcdd2; display: flex; align-items: center; max-width: 85%; }
    .shield-icon { margin-right: 8px; font-size: 16px; }
    
    .spacer { margin-top: 40px; }
    </style>
""", unsafe_allow_html=True)

if page == "📱 Instagram Feed":
    st.markdown("""
        <!-- Navbar HTML -->
        <div class="custom-navbar">
            <div class="brand">🛡️ ToxicGuard AI</div>
            <div style="color: #050505; font-weight: 600; font-size: 15px;">Feed</div>
        </div>
        <div class="spacer"></div>
    """, unsafe_allow_html=True)

    # -- INTERACTION CHAT (Invisible) --
    if new_comment := st.chat_input("Write a comment..."):
        with st.spinner("Protecting community..."):
            try:
                response = requests.post(API_URL, json={"text": new_comment})
                if response.status_code == 200:
                    data = response.json()
                    decision = data["decision"]
                    categories = data.get("categories", {})
                    st.session_state.comments.append({
                        "user": "Douaa",
                        "avatar": "👩🏽",
                        "text": new_comment,
                        "status": decision,
                        "categories": categories
                    })
                    if decision == "BLOCK":
                        st.toast("⚠️ Comment removed by AI to protect users.", icon="🛡️")
                else:
                    st.toast("API Error", icon="❌")
            except Exception as e:
                st.toast("ToxicGuard API is offline.", icon="🔌")

    # -- HAUT DU POST --
    st.markdown("""
        <div class="post-header">
            <div class="avatar">👩‍💻</div>
            <div style="display: flex; flex-direction: column;">
                <span class="user-name">Manal</span>
                <span class="post-time">2 hours ago • 🌍 Public</span>
            </div>
        </div>
        <div class="post-text">
            Just finished my final year project on AI Moderation! So excited to share this with you all. It filters toxicity in real-time to create safer communities. 🚀🛡️ #AI #MachineLearning #PFA
        </div>
        <img src="https://images.unsplash.com/photo-1555949963-aa79dcee981c?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80" width="100%" style="border-top: 1px solid #e4e6eb; border-bottom: 1px solid #e4e6eb;">
    """, unsafe_allow_html=True)

    # -- BARRE D'ACTIONS INTERACTIVE (Boutons Streamlit) --
    st.write("") 
    col1, col2, col3 = st.columns(3)

    with col1:
        like_text = f"❤️ Liked ({st.session_state.likes})" if st.session_state.is_liked else f"🤍 Like ({st.session_state.likes})"
        if st.button(like_text, use_container_width=True):
            st.session_state.is_liked = not st.session_state.is_liked
            st.session_state.likes += 1 if st.session_state.is_liked else -1
            st.rerun()

    with col2:
        st.button("💬 Comment", use_container_width=True)

    with col3:
        st.button("↗️ Share", use_container_width=True)

    # -- SECTION COMMENTAIRES --
    st.write("---") 

    comments_html = '<div class="comments-section">'
    for c in st.session_state.comments:
        comments_html += f'<div class="comment-row"><div class="comment-avatar">{c["avatar"]}</div>'
        if c["status"] == "ALLOW":
            comments_html += f'<div class="clean-comment"><span class="comment-author">{c["user"]}</span> {c["text"]}</div>'
        else:
            comments_html += f'<div class="blocked-comment"><span class="shield-icon">🛡️</span> This comment was automatically removed to protect the community.</div>'
        comments_html += "</div>"
    comments_html += '</div>'

    st.markdown(comments_html, unsafe_allow_html=True)

elif page == "🔑 Admin Dashboard":
    st.markdown("""
        <div class="custom-navbar">
            <div class="brand">🛡️ ToxicGuard Admin</div>
            <div style="color: #d32f2f; font-weight: 600; font-size: 15px;">Secure Panel</div>
        </div>
        <div class="spacer"></div>
    """, unsafe_allow_html=True)

    if not st.session_state.admin_logged_in:
        # Formulaire de Connexion
        st.subheader("🔑 Authentication Required")
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter username (admin)...")
            password = st.text_input("Password", type="password", placeholder="Enter password (admin)...")
            submitted = st.form_submit_button("Sign In")
            
            if submitted:
                if username == "admin" and password == "admin":
                    st.session_state.admin_logged_in = True
                    st.success("Successfully logged in!")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error("Invalid Username or Password.")
    else:
        # Interface Admin Connectée
        st.subheader("🛡️ Moderation Intelligence Dashboard")
        
        # Deconnexion
        if st.sidebar.button("Logout"):
            st.session_state.admin_logged_in = False
            st.rerun()
            
        # Calculer les métriques
        total_comments = len(st.session_state.comments)
        blocked_comments = [c for c in st.session_state.comments if c["status"] == "BLOCK"]
        num_blocked = len(blocked_comments)
        num_allowed = total_comments - num_blocked
        block_rate = (num_blocked / total_comments) * 100 if total_comments > 0 else 0.0

        # Affichage des KPI Cards
        k1, k2, k3 = st.columns(3)
        k1.metric("Analyzed", total_comments)
        k2.metric("Blocked", num_blocked)
        k3.metric("Block Rate", f"{block_rate:.1f}%")

        st.write("---")
        
        if num_blocked == 0:
            st.info("No comments have been blocked yet. Go to the Feed page and test some toxic comments!")
        else:
            st.write("### 🗂️ Audit Log: Blocked Comments")
            
            # Selectbox pour choisir le commentaire bloqué à inspecter
            blocked_options = [f"#{i+1} : \"{c['text'][:30]}...\"" for i, c in enumerate(blocked_comments)]
            selected_idx = st.selectbox("Select a blocked comment to analyze in-depth:", range(len(blocked_options)), format_func=lambda x: blocked_options[x])
            
            selected_comment = blocked_comments[selected_idx]
            
            # Section d'analyse approfondie
            st.markdown(f"""
                <div style="background-color: #fff0f0; border-left: 5px solid #d32f2f; padding: 15px; border-radius: 4px; margin-bottom: 20px;">
                    <h5 style="color: #d32f2f; margin: 0 0 10px 0;">🚫 Moderated Content</h5>
                    <p style="font-size: 16px; font-weight: 500; font-style: italic; color: #333; margin: 0;">"{selected_comment['text']}"</p>
                    <small style="color: #666; margin-top: 5px; display: block;">Posted by: <b>{selected_comment['user']}</b></small>
                </div>
            """, unsafe_allow_html=True)
            
            st.write("### 📊 AI Classification breakdown (Explainable AI)")
            categories = selected_comment.get("categories", {})
            
            if not categories:
                st.warning("No detailed classification data available for this placeholder comment.")
            else:
                # Affichage des scores avec des barres de progression de couleur
                col_left, col_right = st.columns(2)
                
                cat_keys = list(categories.keys())
                for index, cat in enumerate(cat_keys):
                    score = categories[cat]
                    target_col = col_left if index % 2 == 0 else col_right
                    
                    with target_col:
                        # Rendre le nom plus lisible
                        label = cat.replace("_", " ").title()
                        st.write(f"**{label}** : `{score:.2%}`")
                        st.progress(score)
            
            st.write("---")
            st.write("### 💡 AI Interpretation")
            # Trouver la catégorie dominante
            if categories:
                max_cat = max(categories, key=categories.get)
                max_score = categories[max_cat]
                if max_score > 0.50:
                    st.error(f"🚨 **Critical Alert:** This comment was blocked primarily due to **{max_cat.replace('_', ' ').upper()}** detection with a confidence score of **{max_score:.1%}**.")
                else:
                    st.warning(f"⚠️ **Caution:** The comment shows border-line toxic behavior across several categories.")
