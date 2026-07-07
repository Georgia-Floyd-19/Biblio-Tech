import streamlit as st
from services import top_5_documents_plus_empruntes, emprunts_par_type, taux_retour, top_5_utilisateurs_plus_actifs
from datetime import datetime
from utils import render_sidebar, apply_custom_css, ICONES_TYPE
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Tableau de bord - BiblioTech", page_icon="📊", layout="wide")
st.set_option('client.showSidebarNavigation', False)
apply_custom_css()
render_sidebar()

st.title("📊 Tableau de bord statistique")

if st.session_state.get("role") != "bibliothecaire":
    st.error("Accès réservé aux bibliothécaires.")
    st.stop()

st.markdown(f"<p style='color:var(--gray-600);'>Dernière mise à jour : {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>", unsafe_allow_html=True)

a_temps, en_retard = taux_retour()
total_retours = a_temps + en_retard
taux_conformite = round(a_temps / total_retours * 100, 1) if total_retours > 0 else 0

k1, k2, k3, k4 = st.columns(4)
k1.markdown(f"<div class='kpi-card'><div class='kpi-value'>{total_retours}</div><div class='kpi-label'>Emprunts total</div></div>", unsafe_allow_html=True)
k2.markdown(f"<div class='kpi-card'><div class='kpi-value' style='color:var(--success);'>{a_temps}</div><div class='kpi-label'>Retours à temps</div></div>", unsafe_allow_html=True)
k3.markdown(f"<div class='kpi-card'><div class='kpi-value' style='color:var(--danger);'>{en_retard}</div><div class='kpi-label'>Retards</div></div>", unsafe_allow_html=True)
k4.markdown(f"<div class='kpi-card'><div class='kpi-value'>{taux_conformite}%</div><div class='kpi-label'>Taux conformité</div></div>", unsafe_allow_html=True)

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("🏆 Top 5 documents")
    top_docs = top_5_documents_plus_empruntes()
    if top_docs:
        fig = px.bar(
            x=[d["titre"] for d in top_docs],
            y=[d["total"] for d in top_docs],
            labels={"x": "", "y": "Emprunts"},
            color=[d["total"] for d in top_docs],
            color_continuous_scale="blues",
            text=[d["total"] for d in top_docs]
        )
        fig.update_traces(textposition="outside")
        fig.update_layout(height=300, margin=dict(l=0, r=0, t=10, b=40), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Aucune donnée.")

with col2:
    st.subheader("👤 Top 5 utilisateurs")
    top_users = top_5_utilisateurs_plus_actifs()
    if top_users:
        fig = px.bar(
            x=[d["pseudo"] for d in top_users],
            y=[d["total"] for d in top_users],
            labels={"x": "", "y": "Emprunts"},
            color=[d["total"] for d in top_users],
            color_continuous_scale="oranges",
            text=[d["total"] for d in top_users]
        )
        fig.update_traces(textposition="outside")
        fig.update_layout(height=300, margin=dict(l=0, r=0, t=10, b=40), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Aucune donnée.")

st.divider()

col3, col4 = st.columns(2)

with col3:
    st.subheader("📊 Emprunts par type")
    data_type = emprunts_par_type()
    if data_type:
        labels = [f"{ICONES_TYPE.get(d['_id'], '📄')} {d['_id'].capitalize()}" for d in data_type]
        valeurs = [d["total"] for d in data_type]
        fig = go.Figure(data=[go.Pie(labels=labels, values=valeurs, hole=0.4,
                                      marker=dict(colors=["#1E3A5F", "#2B5A8C", "#FF6B35", "#FF8F5E"]))])
        fig.update_layout(height=320, margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Aucune donnée.")

with col4:
    st.subheader("⏱️ Taux de retour")
    if total_retours > 0:
        fig = go.Figure(data=[go.Pie(
            labels=["Dans les délais", "En retard"],
            values=[a_temps, en_retard],
            hole=0.4,
            marker=dict(colors=["#28A745", "#DC3545"])
        )])
        fig.update_layout(height=320, margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Aucun retour enregistré.")
