import streamlit as st
from services import emprunts_en_cours, emprunts_en_retard, retourner_document, tous_les_emprunts, obtenir_utilisateur_par_id
from datetime import datetime
from utils import render_sidebar, apply_custom_css, status_badge, type_badge

st.set_page_config(page_title="Gestion emprunts - BiblioTech", page_icon="material:assignment", layout="wide")
st.set_option('client.showSidebarNavigation', False)
apply_custom_css()
render_sidebar()

st.title("Gestion des emprunts")

if st.session_state.get("role") != "bibliothecaire":
    st.error("Acces reserve aux bibliothecaires.")
    st.stop()

tab1, tab2, tab3 = st.tabs(["En cours", "Retards", "Historique"])

with tab1:
    st.subheader("Emprunts en cours")
    encours = emprunts_en_cours()
    if not encours:
        st.info("Aucun emprunt en cours.")
    for emp in encours:
        util = obtenir_utilisateur_par_id(emp["utilisateur_id"])
        pseudo = util["pseudo"] if util else "Inconnu"
        est_retard = emp["date_retour_prevue"] < datetime.now()
        statut = "retard" if est_retard else "en_cours"
        st.markdown(f"""
        <div class="doc-card">
            {type_badge(emp.get("type_snapshot", ""))}
            <div class="doc-body">
                <div class="doc-title">{emp['titre_snapshot']}</div>
                <div class="doc-meta">{status_badge(statut)} · Emprunte par <strong>{pseudo}</strong> · {emp['date_emprunt'].strftime('%d/%m/%Y')} > {emp['date_retour_prevue'].strftime('%d/%m/%Y')}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Retourne", key=f"ret_{emp['_id']}", use_container_width=True):
            try:
                retourner_document(str(emp["_id"]))
                st.success("Retour enregistre !")
                st.rerun()
            except Exception as e:
                st.error(str(e))

with tab2:
    st.subheader("Emprunts en retard")
    retards = emprunts_en_retard()
    if not retards:
        st.success("Aucun emprunt en retard !")
    for emp in retards:
        util = obtenir_utilisateur_par_id(emp["utilisateur_id"])
        pseudo = util["pseudo"] if util else "Inconnu"
        jours_retard = (datetime.now() - emp["date_retour_prevue"]).days
        st.markdown(f"""
        <div class="doc-card" style="border-color:var(--danger);">
            {type_badge(emp.get("type_snapshot", ""))}
            <div class="doc-body">
                <div class="doc-title">{emp['titre_snapshot']}</div>
                <div class="doc-meta">{status_badge('retard')} · <strong>{pseudo}</strong> · Retour prevu {emp['date_retour_prevue'].strftime('%d/%m/%Y')}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.error(f"{jours_retard} jour(s) de retard")

with tab3:
    st.subheader("Historique complet")
    historique = tous_les_emprunts()
    if not historique:
        st.info("Aucun emprunt.")
    for emp in historique:
        util = obtenir_utilisateur_par_id(emp["utilisateur_id"])
        pseudo = util["pseudo"] if util else "Inconnu"
        statut = "retourne" if emp["date_retour_effective"] else "en_cours"
        retour_str = emp['date_retour_effective'].strftime('%d/%m/%Y') if emp['date_retour_effective'] else 'En cours'
        st.markdown(f"""
        <div class="doc-card">
            {type_badge(emp.get("type_snapshot", ""))}
            <div class="doc-body">
                <div class="doc-title">{emp['titre_snapshot']}</div>
                <div class="doc-meta">{status_badge(statut)} · {pseudo} · {emp['date_emprunt'].strftime('%d/%m/%Y')} > {retour_str}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
