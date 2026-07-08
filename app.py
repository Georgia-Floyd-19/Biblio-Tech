import streamlit as st
from database import test_connection
from utils import render_sidebar, apply_custom_css, feature_icon

st.set_page_config(
    page_title="BiblioTech",
    page_icon="material:menu_book",
    layout="wide"
)
st.set_option('client.showSidebarNavigation', False)

if "utilisateur" not in st.session_state:
    st.session_state["utilisateur"] = None
if "role" not in st.session_state:
    st.session_state["role"] = None

if not test_connection():
    st.error("Impossible de se connecter a MongoDB")
    st.stop()

apply_custom_css()
render_sidebar()

st.markdown("""
<div class="hero">
    <h1>BiblioTech</h1>
    <p>Plateforme collaborative de gestion de bibliotheque universitaire.<br>
    Recherchez, empruntez, notez — tout en un clic.</p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
features = [
    ("catalogue", "Catalogue heterogene", "Livres, theses, revues, DVD aux attributs varies"),
    ("recherche", "Recherche avancee", "Filtres combines par texte, type, annee, disponibilite"),
    ("emprunts", "Emprunts et retours", "Suivi en temps reel avec alertes de retard"),
    ("avis", "Avis et notation", "Notez les documents et consultez les avis"),
]
for col, (icon_name, title, desc) in zip([col1, col2, col3, col4], features):
    with col:
        st.markdown(f"""
        <div class="feature-card">
            {feature_icon(icon_name)}
            <h3>{title}</h3>
            <p>{desc}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<h2 style='text-align:center;margin:2rem 0 1rem;color:var(--primary);'>Comment ca marche ?</h2>", unsafe_allow_html=True)
col_a, col_b, col_c = st.columns(3)
steps = [
    ("1", "Creez votre compte", "Inscrivez-vous en quelques secondes et connectez-vous."),
    ("2", "Parcourez le catalogue", "Explorez les documents, filtrez par criteres."),
    ("3", "Empruntez et notez", "Reservez un document, donnez votre avis apres lecture."),
]
for col, (num, title, desc) in zip([col_a, col_b, col_c], steps):
    with col:
        st.markdown(f"""
        <div class="step">
            <div class="step-num">{num}</div>
            <strong>{title}</strong><br>
            <span style="color:var(--gray-500);font-size:0.85rem;">{desc}</span>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<hr><p style='text-align:center;color:var(--gray-500);font-size:0.8rem;'>BiblioTech - Projet NoSQL Session 4</p>", unsafe_allow_html=True)
