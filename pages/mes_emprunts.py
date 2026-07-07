import streamlit as st
from services import emprunts_par_utilisateur
from datetime import datetime
from utils import render_sidebar, apply_custom_css, status_badge, ICONES_TYPE

st.set_page_config(page_title="Mes emprunts - BiblioTech", page_icon="📖", layout="wide")
st.set_option('client.showSidebarNavigation', False)
apply_custom_css()
render_sidebar()

st.title("📖 Mes emprunts")

if not st.session_state.get("utilisateur"):
    st.error("Vous devez être connecté.")
    st.stop()

utilisateur_id = st.session_state["utilisateur"]["_id"]
emprunts = emprunts_par_utilisateur(utilisateur_id)

if not emprunts:
    st.info("Vous n'avez aucun emprunt.")
    st.stop()

en_cours = [e for e in emprunts if e["date_retour_effective"] is None]
termines = [e for e in emprunts if e["date_retour_effective"] is not None]

c1, c2 = st.columns(2)
c1.metric("📌 En cours", len(en_cours))
c2.metric("✅ Terminés", len(termines))

if en_cours:
    st.subheader("📌 Emprunts en cours")
    for emp in en_cours:
        est_en_retard = emp["date_retour_prevue"] < datetime.now()
        statut = "retard" if est_en_retard else "en_cours"
        icone = ICONES_TYPE.get(emp.get("type_snapshot", ""), "📄")
        jours_restants = (emp["date_retour_prevue"] - datetime.now()).days if not est_en_retard else 0
        st.markdown(f"""
        <div class="doc-card">
            <div class="doc-icon">{icone}</div>
            <div class="doc-body">
                <div class="doc-title">{emp['titre_snapshot']}</div>
                <div class="doc-meta">{status_badge(statut)} · Emprunté le {emp['date_emprunt'].strftime('%d/%m/%Y')} · Retour prévu {emp['date_retour_prevue'].strftime('%d/%m/%Y')}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if not est_en_retard and jours_restants > 0:
            st.progress(min(1.0, jours_restants / 21), text=f"{jours_restants} jour(s) restant(s)")
        elif est_en_retard:
            jours_retard = (datetime.now() - emp["date_retour_prevue"]).days
            st.error(f"⚠️ {jours_retard} jour(s) de retard")

if termines:
    st.subheader("✅ Emprunts terminés")
    for emp in termines:
        icone = ICONES_TYPE.get(emp.get("type_snapshot", ""), "📄")
        st.markdown(f"""
        <div class="doc-card">
            <div class="doc-icon">{icone}</div>
            <div class="doc-body">
                <div class="doc-title">{emp['titre_snapshot']}</div>
                <div class="doc-meta">{status_badge('retourne')} · Emprunté {emp['date_emprunt'].strftime('%d/%m/%Y')} → Retourné {emp['date_retour_effective'].strftime('%d/%m/%Y')}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
