import streamlit as st
from services import (
    ajouter_document,
    recuperer_catalogue,
    recuperer_document,
    modifier_document,
    supprimer_document
)
from datetime import datetime
from utils import render_sidebar, apply_custom_css, render_stars, badge, type_badge

st.set_page_config(page_title="Catalogue - BiblioTech", page_icon="material:library_books", layout="wide")
st.set_option('client.showSidebarNavigation', False)
apply_custom_css()
render_sidebar()

if not st.session_state.get("utilisateur"):
    st.error("Vous devez etre connecte.")
    st.stop()

est_bibliothecaire = st.session_state.get("role") == "bibliothecaire"
titre_page = "Gestion du catalogue" if est_bibliothecaire else "Catalogue"
st.title(titre_page)

if est_bibliothecaire:
    with st.expander("Ajouter un document", expanded=False):
        with st.form("ajout_document"):
            col1, col2 = st.columns(2)
            with col1:
                type_document = st.selectbox("Type de document", ["livre", "these", "revue", "dvd"])
                titre = st.text_input("Titre *")
                annee = st.number_input("Annee", 1900, datetime.now().year, datetime.now().year)
            with col2:
                tags = st.text_input("Tags (separes par des virgules)")
                nb_exemplaires = st.number_input("Nombre d'exemplaires", 1, 100, 1)

            specifique = {}
            if type_document == "livre":
                c1, c2, c3 = st.columns(3)
                with c1: specifique["isbn"] = st.text_input("ISBN")
                with c2: specifique["editeur"] = st.text_input("Editeur")
                with c3: specifique["nombre_pages"] = st.number_input("Pages", 1, 5000)
            elif type_document == "these":
                c1, c2, c3, c4 = st.columns(4)
                with c1: specifique["auteur"] = st.text_input("Auteur")
                with c2: specifique["universite"] = st.text_input("Universite")
                with c3: specifique["annee_soutenance"] = st.number_input("Annee soutenance", 1900, datetime.now().year, datetime.now().year)
                with c4: specifique["directeur"] = st.text_input("Directeur")
            elif type_document == "revue":
                c1, c2, c3 = st.columns(3)
                with c1: specifique["issn"] = st.text_input("ISSN")
                with c2: specifique["volume"] = st.text_input("Volume")
                with c3: specifique["numero"] = st.text_input("Numero")
            elif type_document == "dvd":
                c1, c2 = st.columns(2)
                with c1: specifique["realisateur"] = st.text_input("Realisateur")
                with c2: specifique["duree"] = st.number_input("Duree (minutes)", 1, 500)

            if st.form_submit_button("Enregistrer", type="primary", use_container_width=True):
                erreurs = []
                if not titre.strip():
                    erreurs.append("Le titre est obligatoire.")
                if type_document == "livre":
                    isbn = specifique.get("isbn", "").replace("-", "").replace(" ", "")
                    if isbn and len(isbn) not in (10, 13):
                        erreurs.append("L'ISBN doit contenir 10 ou 13 chiffres.")
                    if not specifique.get("editeur", "").strip():
                        erreurs.append("L'editeur est obligatoire pour un livre.")
                elif type_document == "these":
                    if not specifique.get("auteur", "").strip():
                        erreurs.append("L'auteur est obligatoire pour une these.")
                    if not specifique.get("universite", "").strip():
                        erreurs.append("L'universite est obligatoire pour une these.")
                if erreurs:
                    for e in erreurs:
                        st.error(e)
                else:
                    document = {
                        "type": type_document,
                        "titre": titre,
                        "annee": annee,
                        "tags": [t.strip() for t in tags.split(",") if t.strip()],
                        "nb_exemplaires": nb_exemplaires,
                        "disponible": nb_exemplaires > 0,
                        "note_moyenne": 0,
                        "avis": [],
                        **specifique
                    }
                    ajouter_document(document)
                    st.success("Document ajoute !")
                    st.rerun()

st.divider()
col_titre, col_tri = st.columns([3, 1])
with col_titre:
    st.subheader("Tous les documents")
with col_tri:
    tri = st.selectbox("Trier par", options=[
        ("defaut", "Par defaut"),
        ("note_desc", "Note moyenne ↓"),
        ("note_asc", "Note moyenne ↑"),
        ("titre_asc", "Titre A → Z"),
        ("annee_desc", "Annee ↓"),
    ], format_func=lambda x: x[1])[0]

documents = recuperer_catalogue(trier_par=tri if tri != "defaut" else None)
if not documents:
    st.info("Aucun document dans le catalogue.")
else:
    for doc in documents:
        type_doc = doc.get("type", "")
        type_label = type_doc.capitalize()
        note = doc.get("note_moyenne", 0)
        nb = doc.get("nb_exemplaires", 0)
        tags_doc = doc.get("tags", [])
        tags_html = " ".join(f"<span class='doc-tag'>{t}</span>" for t in tags_doc)

        if est_bibliothecaire:
            col_card, col_actions = st.columns([5, 1])
        else:
            col_card = st.container()
            col_actions = None

        with col_card:
            st.markdown(f"""
            <div class="doc-card">
                {type_badge(type_doc)}
                <div class="doc-body">
                    <div class="doc-title">{doc['titre']}</div>
                    <div class="doc-meta">{type_label} · {doc.get('annee', 'N/A')} · {badge(nb)} · {render_stars(note)}</div>
                    <div class="doc-tags">{tags_html}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        if col_actions:
            with col_actions:
                if st.button("Modifier", key=f"m_{doc['_id']}", use_container_width=True):
                    st.session_state["modifier"] = str(doc["_id"])
                    st.rerun()
                with st.popover("Supprimer", use_container_width=True):
                    st.warning("Supprimer ce document definitivement ?")
                    if st.button("Oui, supprimer", key=f"confirm_s_{doc['_id']}", type="primary", use_container_width=True):
                        try:
                            supprimer_document(doc["_id"])
                            st.success("Document supprime.")
                            st.rerun()
                        except Exception as e:
                            st.error(str(e))

        if doc.get("avis"):
            with st.expander(f"Avis ({len(doc['avis'])}) - Note moyenne : {doc.get('note_moyenne', 0)}/5"):
                for avis in doc["avis"]:
                    pseudo_avis = avis.get("utilisateur_pseudo", "Inconnu")
                    st.markdown(f"""
                    <div style="background:var(--gray-100);border-radius:8px;padding:0.8rem;margin-bottom:0.5rem;">
                        <strong>{pseudo_avis}</strong> · {render_stars(avis['note'])}
                        <span style="float:right;color:var(--gray-500);font-size:0.82rem;">{avis['date'].strftime('%d/%m/%Y') if isinstance(avis['date'], datetime) else ''}</span><br>
                        <span style="color:var(--gray-600);">{avis.get('commentaire', '')}</span>
                    </div>
                    """, unsafe_allow_html=True)

if est_bibliothecaire and "modifier" in st.session_state:
    doc = recuperer_document(st.session_state["modifier"])
    if doc:
        with st.expander(f"Modification : {doc['titre']}", expanded=True):
            with st.form("modifier_form"):
                col1, col2 = st.columns(2)
                with col1:
                    nouveau_titre = st.text_input("Titre", value=doc["titre"])
                    nouvelle_annee = st.number_input("Annee", 1900, datetime.now().year, value=doc["annee"])
                with col2:
                    nouveaux_exemplaires = st.number_input("Exemplaires", value=doc["nb_exemplaires"])
                if st.form_submit_button("Enregistrer", type="primary", use_container_width=True):
                    if not nouveau_titre.strip():
                        st.error("Le titre est obligatoire.")
                    elif nouvelle_annee > datetime.now().year:
                        st.error("L'annee ne peut pas depasser l'annee courante.")
                    else:
                        modifier_document(doc["_id"], {
                            "titre": nouveau_titre,
                            "annee": nouvelle_annee,
                            "nb_exemplaires": nouveaux_exemplaires,
                            "disponible": nouveaux_exemplaires > 0
                        })
                        st.success("Document modifie.")
                        del st.session_state["modifier"]
                        st.rerun()
