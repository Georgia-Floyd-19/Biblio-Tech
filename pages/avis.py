import streamlit as st
from services import emprunts_par_utilisateur, ajouter_avis, recuperer_catalogue
from utils import render_sidebar, apply_custom_css, render_stars

st.set_page_config(page_title="Avis - BiblioTech", page_icon="material:star", layout="wide")
st.set_option('client.showSidebarNavigation', False)
apply_custom_css()
render_sidebar()

st.title("Mes avis")

if not st.session_state.get("utilisateur"):
    st.error("Vous devez etre connecte.")
    st.stop()

pseudo = st.session_state["utilisateur"]["pseudo"]
utilisateur_id = st.session_state["utilisateur"]["_id"]

emprunts = emprunts_par_utilisateur(utilisateur_id)
documents_empruntes = {}
for emp in emprunts:
    did = str(emp.get("document_id", ""))
    if did and emp.get("date_retour_effective") is not None:
        documents_empruntes[did] = emp["titre_snapshot"]

tuples_docs = list(documents_empruntes.items())

if tuples_docs:
    st.subheader("Donner un avis")
    with st.form("avis_form"):
        doc_choisi = st.selectbox("Document a noter", options=tuples_docs, format_func=lambda x: x[1])
        note = st.select_slider("Note", options=[1, 2, 3, 4, 5], value=3)
        commentaire = st.text_area("Commentaire *")
        st.caption("Le commentaire est obligatoire (500 caracteres max).")
        if st.form_submit_button("Publier l'avis", type="primary", use_container_width=True):
            if not commentaire.strip():
                st.error("Le commentaire est obligatoire.")
            elif len(commentaire) > 500:
                st.error("Le commentaire ne peut pas depasser 500 caracteres.")
            else:
                try:
                    ajouter_avis(doc_choisi[0], pseudo, note, commentaire)
                    st.success("Avis publie !")
                    st.rerun()
                except Exception as e:
                    st.error(str(e))
else:
    st.info("Apres avoir emprunte et retourne un document, vous pourrez laisser un avis.")

st.divider()
st.subheader("Tous les avis")

catalogue = recuperer_catalogue()
for doc in catalogue:
    if doc.get("avis"):
        with st.expander(f"{doc['titre']} — {doc.get('note_moyenne', 0)}/5"):
            for avis in doc["avis"]:
                st.markdown(f"""
                <div style="background:var(--gray-100);border-radius:8px;padding:0.8rem;margin-bottom:0.6rem;">
                    <strong>{avis['utilisateur_pseudo']}</strong>
                    <span style="float:right;color:var(--gray-500);font-size:0.82rem;">{avis['date'].strftime('%d/%m/%Y')}</span><br>
                    {render_stars(avis['note'])}<br>
                    <span style="color:var(--gray-600);">{avis.get('commentaire', '')}</span>
                </div>
                """, unsafe_allow_html=True)
