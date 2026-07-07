import bcrypt
import streamlit as st


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())


def apply_custom_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        * { font-family: 'Inter', sans-serif; }

        /* ── Palette ── */
        :root {
            --primary: #1E3A5F;
            --primary-light: #2B5A8C;
            --accent: #FF6B35;
            --accent-light: #FF8F5E;
            --success: #28A745;
            --danger: #DC3545;
            --warning: #FFC107;
            --gray-100: #F8F9FA;
            --gray-200: #E9ECEF;
            --gray-600: #6C757D;
            --gray-800: #343A40;
            --radius: 12px;
            --shadow: 0 2px 12px rgba(0,0,0,0.08);
            --shadow-hover: 0 6px 24px rgba(0,0,0,0.12);
        }

        /* ── Sidebar ── */
        .css-1d391kg, .stSidebar { background: var(--primary) !important; }
        .stSidebar .stTitle, .stSidebar .stMarkdown { color: white !important; }
        .stSidebar .sidebar-section { color: rgba(255,255,255,0.5); font-size: 0.7rem; text-transform: uppercase; letter-spacing: 1px; padding: 1rem 1rem 0.3rem 1rem; }
        .stSidebar .stButton button {
            background: rgba(255,255,255,0.1); color: white; border: 1px solid rgba(255,255,255,0.2);
            border-radius: 8px; padding: 0.4rem 1rem; font-size: 0.85rem; width: 100%;
            transition: all 0.2s;
        }
        .stSidebar .stButton button:hover { background: rgba(255,255,255,0.2); border-color: rgba(255,255,255,0.4); }

        /* ── Cards ── */
        .doc-card {
            background: white; border: 1px solid var(--gray-200); border-radius: var(--radius);
            padding: 1.2rem; box-shadow: var(--shadow); transition: all 0.25s;
            display: flex; align-items: flex-start; gap: 1rem; margin-bottom: 0.8rem;
        }
        .doc-card:hover { box-shadow: var(--shadow-hover); transform: translateY(-2px); }
        .doc-icon { font-size: 2.2rem; min-width: 48px; text-align: center; }
        .doc-body { flex: 1; }
        .doc-title { font-size: 1.05rem; font-weight: 600; color: var(--primary); margin: 0; }
        .doc-meta { font-size: 0.85rem; color: var(--gray-600); margin: 0.25rem 0; }
        .doc-tags { display: flex; flex-wrap: wrap; gap: 0.3rem; margin-top: 0.4rem; }
        .doc-tag {
            background: var(--gray-100); border: 1px solid var(--gray-200); border-radius: 20px;
            padding: 0.1rem 0.6rem; font-size: 0.75rem; color: var(--gray-600);
        }
        .doc-actions { display: flex; gap: 0.4rem; align-items: flex-start; }

        /* ── Badges ── */
        .badge { display: inline-block; padding: 0.15rem 0.6rem; border-radius: 20px; font-size: 0.75rem; font-weight: 500; }
        .badge-success { background: #D4EDDA; color: #155724; }
        .badge-danger { background: #F8D7DA; color: #721C24; }
        .badge-warning { background: #FFF3CD; color: #856404; }
        .badge-info { background: #D1ECF1; color: #0C5460; }

        /* ── Hero ── */
        .hero {
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
            border-radius: var(--radius); padding: 3rem 2.5rem; margin-bottom: 2rem; color: white;
        }
        .hero h1 { font-size: 2.2rem; font-weight: 700; margin: 0 0 0.5rem 0; }
        .hero p { font-size: 1.1rem; opacity: 0.9; margin: 0 0 1.5rem 0; max-width: 600px; }

        /* ── Feature cards ── */
        .feature-card {
            background: white; border: 1px solid var(--gray-200); border-radius: var(--radius);
            padding: 1.5rem; text-align: center; box-shadow: var(--shadow);
            transition: all 0.25s;
        }
        .feature-card:hover { box-shadow: var(--shadow-hover); transform: translateY(-3px); }
        .feature-icon { font-size: 2.5rem; margin-bottom: 0.8rem; }
        .feature-card h3 { font-size: 1rem; font-weight: 600; color: var(--primary); margin: 0 0 0.4rem 0; }
        .feature-card p { font-size: 0.85rem; color: var(--gray-600); margin: 0; }

        /* ── KPI cards ── */
        .kpi-card {
            background: white; border: 1px solid var(--gray-200); border-radius: var(--radius);
            padding: 1.2rem; box-shadow: var(--shadow); text-align: center;
        }
        .kpi-value { font-size: 2rem; font-weight: 700; color: var(--primary); }
        .kpi-label { font-size: 0.8rem; color: var(--gray-600); text-transform: uppercase; letter-spacing: 0.5px; }
        .kpi-sub { font-size: 0.85rem; margin-top: 0.3rem; }

        /* ── Auth card ── */
        .auth-card {
            max-width: 440px; margin: 2rem auto; background: white;
            border: 1px solid var(--gray-200); border-radius: var(--radius);
            padding: 2.5rem; box-shadow: var(--shadow);
        }
        .auth-logo { text-align: center; font-size: 3rem; margin-bottom: 0.5rem; }
        .auth-title { text-align: center; font-size: 1.4rem; font-weight: 700; color: var(--primary); margin-bottom: 1.5rem; }

        /* ── Steps ── */
        .step { text-align: center; padding: 1rem; }
        .step-num {
            width: 40px; height: 40px; line-height: 40px; border-radius: 50%;
            background: var(--accent); color: white; font-weight: 700; font-size: 1.1rem;
            margin: 0 auto 0.6rem auto;
        }

        /* ── Button accent ── */
        .stButton > button[kind="primary"] {
            background: var(--accent) !important; color: white !important; border: none !important;
            border-radius: 8px !important; font-weight: 500 !important;
        }
        .stButton > button[kind="primary"]:hover { background: var(--accent-light) !important; }

        /* ── Metrics ── */
        [data-testid="stMetricValue"] { color: var(--primary); font-weight: 700; }
        [data-testid="stMetricDelta"] [data-testid="stMetricDelta"] { font-size: 0.85rem; }

        /* ── Expander ── */
        .streamlit-expanderHeader { font-weight: 600 !important; color: var(--primary) !important; }

        /* ── Divider ── */
        hr { margin: 2rem 0 !important; border-color: var(--gray-200) !important; }

        /* ── Stars ── */
        .stars { color: #FFC107; letter-spacing: 2px; font-size: 1.1rem; }
        .stars-empty { color: var(--gray-200); }
        .rating-text { font-size: 0.85rem; color: var(--gray-600); margin-left: 0.3rem; }
    </style>
    """, unsafe_allow_html=True)


def render_stars(note: float) -> str:
    full = int(round(note))
    empty = 5 - full
    return f"<span class='stars'>{'★' * full}<span class='stars-empty'>{'★' * empty}</span></span><span class='rating-text'>({note})</span>"


def badge(nb: int) -> str:
    if nb > 0:
        return f"<span class='badge badge-success'>✅ {nb} disponible(s)</span>"
    return "<span class='badge badge-danger'>❌ Indisponible</span>"


def status_badge(statut: str) -> str:
    badges_map = {
        "en_cours": "<span class='badge badge-info'>📌 En cours</span>",
        "retourne": "<span class='badge badge-success'>✅ Retourné</span>",
        "retard": "<span class='badge badge-danger'>🔴 En retard</span>",
    }
    return badges_map.get(statut, statut)


ICONES_TYPE = {"livre": "📘", "these": "🎓", "revue": "📰", "dvd": "💿"}


def render_sidebar():
    st.sidebar.markdown("<div style='padding: 0.5rem 0;'>", unsafe_allow_html=True)
    st.sidebar.title("📚 BiblioTech")
    if st.session_state.get("utilisateur"):
        pseudo = st.session_state["utilisateur"]["pseudo"]
        role = st.session_state.get("role", "etudiant")
        role_label = "👤 Bibliothécaire" if role == "bibliothecaire" else "👤 Étudiant"
        st.sidebar.markdown(f"<div style='color:white; padding:0 1rem 0.5rem 1rem;'><strong>{pseudo}</strong><br><span style='opacity:0.6;font-size:0.8rem;'>{role_label}</span></div>", unsafe_allow_html=True)
        st.sidebar.markdown("<div class='sidebar-section'>Navigation</div>", unsafe_allow_html=True)
        st.sidebar.page_link("app.py", label="🏠 Accueil")
        st.sidebar.page_link("pages/catalogue.py", label="📚 Catalogue")
        st.sidebar.page_link("pages/recherche.py", label="🔍 Recherche")
        st.sidebar.page_link("pages/mes_emprunts.py", label="📖 Mes emprunts")
        st.sidebar.page_link("pages/avis.py", label="⭐ Mes avis")
        if role == "bibliothecaire":
            st.sidebar.markdown("<div class='sidebar-section'>Bibliothécaire</div>", unsafe_allow_html=True)
            st.sidebar.page_link("pages/emprunts.py", label="📋 Gestion emprunts")
            st.sidebar.page_link("pages/tableau_de_bord.py", label="📊 Tableau de bord")
        st.sidebar.markdown("<div style='padding:0 1rem;'>", unsafe_allow_html=True)
        if st.sidebar.button("🚪 Se déconnecter"):
            st.session_state["utilisateur"] = None
            st.session_state["role"] = None
            st.rerun()
        st.sidebar.markdown("</div>", unsafe_allow_html=True)
    else:
        st.sidebar.markdown("<div class='sidebar-section'>Accueil</div>", unsafe_allow_html=True)
        st.sidebar.page_link("pages/connexion.py", label="🔐 Connexion")
    st.sidebar.markdown("</div>", unsafe_allow_html=True)
