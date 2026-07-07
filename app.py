import streamlit as st
from database import test_connection
from utils import render_sidebar, apply_custom_css

st.set_page_config(
    page_title="BiblioTech",
    page_icon="📚",
    layout="wide"
)
st.set_option('client.showSidebarNavigation', False)

if "utilisateur" not in st.session_state:
    st.session_state["utilisateur"] = None
if "role" not in st.session_state:
    st.session_state["role"] = None

if not test_connection():
    st.error("Impossible de se connecter à MongoDB ❌")
    st.stop()

apply_custom_css()
render_sidebar()

st.markdown("""
<div class="hero">
    <h1>📚 BiblioTech</h1>
    <p>Plateforme collaborative de gestion de bibliothèque universitaire.<br>
    Recherchez, empruntez, notez — tout en un clic.</p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
features = [
    ("📘", "Catalogue hétérogène", "Livres, thèses, revues, DVD aux attributs variés"),
    ("🔍", "Recherche avancée", "Filtres combinés par texte, type, année, disponibilité"),
    ("📖", "Emprunts & retours", "Suivi en temps réel avec alertes de retard"),
    ("⭐", "Avis & notation", "Notez les documents et consultez les avis"),
]
for col, (icon, title, desc) in zip([col1, col2, col3, col4], features):
    with col:
        st.markdown(f"""
        <div class="feature-card">
            <div class="feature-icon">{icon}</div>
            <h3>{title}</h3>
            <p>{desc}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<h2 style='text-align:center;margin:2rem 0 1rem;color:var(--primary);'>Comment ça marche ?</h2>", unsafe_allow_html=True)
col_a, col_b, col_c = st.columns(3)
steps = [
    ("1", "Créez votre compte", "Inscrivez-vous en quelques secondes et connectez-vous."),
    ("2", "Parcourez le catalogue", "Explorez les documents, filtrez par critères."),
    ("3", "Empruntez & notez", "Réservez un document, donnez votre avis après lecture."),
]
for col, (num, title, desc) in zip([col_a, col_b, col_c], steps):
    with col:
        st.markdown(f"""
        <div class="step">
            <div class="step-num">{num}</div>
            <strong>{title}</strong><br>
            <span style="color:var(--gray-600);font-size:0.9rem;">{desc}</span>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<hr><p style='text-align:center;color:var(--gray-600);font-size:0.85rem;'>BiblioTech — Projet NoSQL Session 4</p>", unsafe_allow_html=True)
