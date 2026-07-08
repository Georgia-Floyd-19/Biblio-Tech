import re
import streamlit as st
from services import creer_utilisateur, authentifier_utilisateur
from utils import render_sidebar, apply_custom_css

st.set_page_config(page_title="Connexion - BiblioTech", page_icon="material:login", layout="wide")
st.set_option('client.showSidebarNavigation', False)
apply_custom_css()
render_sidebar()

if st.session_state.get("utilisateur"):
    st.markdown(f"""
    <div class="auth-card">
        <div class="auth-title">Bienvenue, {st.session_state['utilisateur']['pseudo']} !</div>
        <p style="text-align:center;color:var(--gray-500);">Vous etes connecte.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Se deconnecter", use_container_width=True):
        st.session_state["utilisateur"] = None
        st.session_state["role"] = None
        st.rerun()
    st.stop()

st.markdown('<div class="auth-card">', unsafe_allow_html=True)
st.markdown('<div class="auth-title">BiblioTech</div>', unsafe_allow_html=True)

tab_connexion, tab_inscription = st.tabs(["Se connecter", "Creer un compte"])

with tab_connexion:
    with st.form("login_form"):
        pseudo = st.text_input("Pseudo", key="login_pseudo")
        mot_de_passe = st.text_input("Mot de passe", type="password", key="login_mdp")
        if st.form_submit_button("Se connecter", type="primary", use_container_width=True):
            if not pseudo or not mot_de_passe:
                st.error("Veuillez remplir tous les champs.")
            else:
                utilisateur = authentifier_utilisateur(pseudo, mot_de_passe)
                if utilisateur:
                    st.session_state["utilisateur"] = utilisateur
                    st.session_state["role"] = utilisateur.get("role", "etudiant")
                    st.rerun()
                else:
                    st.error("Pseudo ou mot de passe incorrect.")

with tab_inscription:
    with st.form("register_form"):
        nouveau_pseudo = st.text_input("Pseudo")
        nouveau_email = st.text_input("Email")
        nouveau_mdp = st.text_input("Mot de passe", type="password")
        nouveau_mdp_confirm = st.text_input("Confirmer le mot de passe", type="password")
        if st.form_submit_button("Creer un compte", type="primary", use_container_width=True):
            if not nouveau_pseudo or not nouveau_email or not nouveau_mdp:
                st.error("Tous les champs sont obligatoires.")
            elif len(nouveau_pseudo) < 3:
                st.error("Le pseudo doit contenir au moins 3 caracteres.")
            elif not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", nouveau_email):
                st.error("Format d'email invalide.")
            elif nouveau_mdp != nouveau_mdp_confirm:
                st.error("Les mots de passe ne correspondent pas.")
            elif len(nouveau_mdp) < 4:
                st.error("Le mot de passe doit contenir au moins 4 caracteres.")
            else:
                try:
                    creer_utilisateur(nouveau_pseudo, nouveau_email, nouveau_mdp)
                    st.success("Compte cree ! Connectez-vous.")
                except Exception as e:
                    st.error(str(e))

st.markdown('</div>', unsafe_allow_html=True)
