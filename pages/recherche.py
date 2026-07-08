import streamlit as st
from services import rechercher_documents, emprunter_document
from utils import render_sidebar, apply_custom_css, render_stars, badge, type_badge

st.set_page_config(page_title="Recherche - BiblioTech", page_icon="material:search", layout="wide")
st.set_option('client.showSidebarNavigation', False)
apply_custom_css()
render_sidebar()

st.title("Recherche avancee")

if not st.session_state.get("utilisateur"):
    st.error("Vous devez etre connecte.")
    st.stop()

with st.container(border=True):
    st.markdown("### Filtres")
    col1, col2, col3 = st.columns(3)
    with col1:
        texte = st.text_input("Recherche textuelle (titre, tags)")
        type_doc = st.selectbox("Type de document", ["", "livre", "these", "revue", "dvd"])
    with col2:
        annee_min = st.number_input("Annee min", 0, 2100, 0)
        annee_max = st.number_input("Annee max", 0, 2100, 0)
    with col3:
        dispo_only = st.checkbox("Disponibles uniquement")
        mode_recherche = st.radio("Mode recherche", options=[
            ("regex", "Parcourt (sous-chaine)"),
            ("text", "Index texte (mot entier)"),
        ], format_func=lambda x: x[1], index=0)[0]
        chercher = st.button("Rechercher", type="primary", use_container_width=True)

if chercher:
    if annee_min > 0 and annee_max > 0 and annee_min > annee_max:
        st.error("L'annee minimale ne peut pas etre superieure a l'annee maximale.")
    else:
        annee_min_val = annee_min if annee_min > 0 else None
        annee_max_val = annee_max if annee_max > 0 else None
        resultats = rechercher_documents(
            texte=texte, type_doc=type_doc,
            annee_min=annee_min_val, annee_max=annee_max_val,
            dispo_only=dispo_only, mode_recherche=mode_recherche
        )
        st.markdown(f"### Resultats ({len(resultats)} document(s))")
        if not resultats:
            st.info("Aucun resultat trouve.")
        for doc in resultats:
            type_doc = doc.get("type", "")
            note = doc.get("note_moyenne", 0)
            nb = doc.get("nb_exemplaires", 0)
            st.markdown(f"""
            <div class="doc-card">
                {type_badge(type_doc)}
                <div class="doc-body">
                    <div class="doc-title">{doc['titre']}</div>
                    <div class="doc-meta">{doc['type'].capitalize()} · {doc.get('annee', 'N/A')} · {badge(nb)} · {render_stars(note)}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if nb > 0:
                if st.button("Reserver", key=f"res_{doc['_id']}"):
                    try:
                        emprunter_document(st.session_state["utilisateur"]["_id"], str(doc["_id"]))
                        st.success("Reservation effectuee !")
                        st.rerun()
                    except Exception as e:
                        st.error(str(e))
