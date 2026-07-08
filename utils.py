import bcrypt
import streamlit as st
import random


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())


# ── Particle generator ──────────────────────────────────

def _generate_particles(count: int = 100) -> str:
    """Generate box-shadow values for CSS-only particles."""
    items = []
    for _ in range(count):
        x = random.uniform(0, 100)
        y = random.uniform(0, 100)
        size = random.uniform(0.8, 2.5)
        opacity = random.uniform(0.08, 0.35)
        items.append(f"{x:.1f}vw {y:.1f}vh 0 {size:.1f}px rgba(255,255,255,{opacity:.3f})")
    return ", ".join(items)


# ── CSS + Background effects ─────────────────────────────

PARTICLES_1 = _generate_particles(90)
PARTICLES_2 = _generate_particles(70)


def apply_custom_css():
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Georgia:wght@400;700&display=swap');

        * {{ font-family: Georgia, 'Times New Roman', serif; }}

        :root {{
            --bg-dark: #07070d;
            --bg-card: rgba(255, 255, 255, 0.03);
            --bg-card-hover: rgba(255, 255, 255, 0.06);
            --glass-border: rgba(255, 255, 255, 0.06);
            --glass-border-hover: rgba(255, 255, 255, 0.12);
            --text-primary: #e4e4ed;
            --text-secondary: #9494a8;
            --text-muted: #6b6b80;
            --accent: #60a5fa;
            --accent-hover: #93bbfd;
            --accent-glow: rgba(96, 165, 250, 0.15);
            --secondary: #a78bfa;
            --success: #34d399;
            --success-bg: rgba(52, 211, 153, 0.1);
            --success-dark: #34d399;
            --danger: #f87171;
            --danger-bg: rgba(248, 113, 113, 0.1);
            --danger-dark: #f87171;
            --warning: #fbbf24;
            --warning-bg: rgba(251, 191, 36, 0.1);
            --info: #60a5fa;
            --info-bg: rgba(96, 165, 250, 0.1);
            --radius: 16px;
            --radius-sm: 10px;
            --radius-xs: 8px;
            --glass-bg: rgba(255, 255, 255, 0.03);
            --glass-blur: blur(20px);
            --transition: 0.35s cubic-bezier(0.22, 1, 0.36, 1);
        }}

        /* ── Animated Background ── */
        html, body, .stApp {{
            background: var(--bg-dark) !important;
        }}
        .stApp::before {{
            content: '';
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background:
                radial-gradient(ellipse at 20% 30%, rgba(96, 165, 250, 0.10) 0%, transparent 50%),
                radial-gradient(ellipse at 80% 20%, rgba(167, 139, 250, 0.08) 0%, transparent 50%),
                radial-gradient(ellipse at 60% 85%, rgba(52, 211, 153, 0.06) 0%, transparent 50%),
                radial-gradient(ellipse at 10% 70%, rgba(251, 191, 36, 0.04) 0%, transparent 50%),
                radial-gradient(ellipse at 50% 50%, rgba(96, 165, 250, 0.03) 0%, transparent 70%);
            animation: bgShift 35s ease-in-out infinite;
            z-index: 0;
            pointer-events: none;
        }}
        @keyframes bgShift {{
            0%, 100% {{ transform: scale(1) rotate(0deg); opacity: 0.8; }}
            25% {{ transform: scale(1.08) rotate(0.8deg); opacity: 1; }}
            50% {{ transform: scale(0.95) rotate(-0.5deg); opacity: 0.85; }}
            75% {{ transform: scale(1.04) rotate(0.3deg); opacity: 0.95; }}
        }}

        /* ── Floating Orbs ── */
        .orb {{
            position: fixed;
            border-radius: 50%;
            filter: blur(80px);
            pointer-events: none;
            z-index: 0;
            opacity: 0.6;
        }}
        .orb-1 {{
            width: 400px; height: 400px;
            background: rgba(96, 165, 250, 0.08);
            top: -10%; left: -8%;
            animation: orbFloat1 28s ease-in-out infinite;
        }}
        .orb-2 {{
            width: 350px; height: 350px;
            background: rgba(167, 139, 250, 0.07);
            bottom: -10%; right: -8%;
            animation: orbFloat2 32s ease-in-out infinite;
        }}
        .orb-3 {{
            width: 280px; height: 280px;
            background: rgba(52, 211, 153, 0.05);
            top: 45%; left: 55%;
            animation: orbFloat3 24s ease-in-out infinite;
        }}
        .orb-4 {{
            width: 200px; height: 200px;
            background: rgba(251, 191, 36, 0.04);
            top: 70%; left: 15%;
            animation: orbFloat1 26s ease-in-out infinite reverse;
        }}
        @keyframes orbFloat1 {{
            0%, 100% {{ transform: translate(0, 0) scale(1); }}
            33% {{ transform: translate(30px, -40px) scale(1.05); }}
            66% {{ transform: translate(-20px, 20px) scale(0.95); }}
        }}
        @keyframes orbFloat2 {{
            0%, 100% {{ transform: translate(0, 0) scale(1); }}
            33% {{ transform: translate(-30px, 30px) scale(0.95); }}
            66% {{ transform: translate(20px, -40px) scale(1.05); }}
        }}
        @keyframes orbFloat3 {{
            0%, 100% {{ transform: translate(0, 0) scale(1); }}
            50% {{ transform: translate(15px, -25px) scale(1.03); }}
        }}

        /* ── CSS Particles ── */
        .particles {{
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            pointer-events: none;
            z-index: 0;
        }}
        .particles::before {{
            content: '';
            position: absolute;
            width: 1px; height: 1px;
            border-radius: 50%;
            box-shadow: {PARTICLES_1};
            animation: particleDrift 40s linear infinite;
        }}
        .particles::after {{
            content: '';
            position: absolute;
            width: 1px; height: 1px;
            border-radius: 50%;
            box-shadow: {PARTICLES_2};
            animation: particleDrift2 55s linear infinite;
        }}
        @keyframes particleDrift {{
            0% {{ transform: translate(0, 0); }}
            25% {{ transform: translate(0.5vw, -0.3vh); }}
            50% {{ transform: translate(-0.3vw, 0.5vh); }}
            75% {{ transform: translate(0.4vw, 0.2vh); }}
            100% {{ transform: translate(0, 0); }}
        }}
        @keyframes particleDrift2 {{
            0% {{ transform: translate(0, 0); }}
            25% {{ transform: translate(-0.4vw, 0.5vh); }}
            50% {{ transform: translate(0.5vw, -0.2vh); }}
            75% {{ transform: translate(-0.2vw, -0.4vh); }}
            100% {{ transform: translate(0, 0); }}
        }}

        /* ── Typography ── */
        h1, h2, h3, h4, h5, h6 {{ font-family: Georgia, serif; letter-spacing: -0.01em; }}
        .stApp h1 {{ font-weight: 700; color: var(--text-primary); font-size: 1.65rem; margin-bottom: 0.5rem; }}
        .stApp h2 {{ font-weight: 600; color: var(--text-primary); font-size: 1.3rem; }}
        .stApp h3 {{ font-weight: 600; color: var(--text-primary); font-size: 1.1rem; }}
        p, li, span, div {{ color: var(--text-secondary); }}
        strong {{ color: var(--text-primary); }}

        hr {{ margin: 2rem 0 !important; border: none !important; height: 1px !important;
            background: linear-gradient(to right, transparent, rgba(255,255,255,0.06), transparent) !important; }}

        /* ── Glassmorphism Base ── */
        .glass {{
            background: var(--glass-bg);
            backdrop-filter: var(--glass-blur);
            -webkit-backdrop-filter: var(--glass-blur);
            border: 1px solid var(--glass-border);
            border-radius: var(--radius);
        }}

        /* ── Sidebar ── */
        section[data-testid="stSidebar"] {{
            background: rgba(10, 10, 18, 0.88) !important;
            backdrop-filter: blur(24px) !important;
            -webkit-backdrop-filter: blur(24px) !important;
            border-right: 1px solid rgba(255,255,255,0.04);
        }}
        section[data-testid="stSidebar"] .stTitle {{
            color: var(--text-primary) !important;
            font-size: 1.1rem !important;
            font-weight: 700 !important;
            padding: 0.5rem 0 0.2rem 0;
        }}
        .sidebar-section {{
            color: var(--text-muted);
            font-size: 0.6rem;
            text-transform: uppercase;
            letter-spacing: 1.8px;
            padding: 1.5rem 1rem 0.3rem 1rem;
            font-weight: 600;
            opacity: 0.6;
        }}
        section[data-testid="stSidebar"] a {{
            color: rgba(255,255,255,0.55) !important;
            font-size: 0.82rem;
            padding: 0.4rem 0.7rem;
            border-radius: var(--radius-xs);
            transition: var(--transition);
            text-decoration: none;
            display: block;
            margin: 0.05rem 0.5rem;
            border-left: 2px solid transparent;
            font-family: Georgia, serif;
        }}
        section[data-testid="stSidebar"] a:hover {{
            color: white !important;
            background: rgba(255,255,255,0.05);
            border-left-color: var(--accent);
        }}
        section[data-testid="stSidebar"] a:active, section[data-testid="stSidebar"] a:focus {{
            color: white !important;
            background: rgba(96,165,250,0.1);
            border-left-color: var(--accent);
        }}
        section[data-testid="stSidebar"] .stButton button {{
            background: rgba(255,255,255,0.04);
            color: rgba(255,255,255,0.6);
            border: 1px solid rgba(255,255,255,0.05);
            border-radius: var(--radius-xs);
            padding: 0.3rem 1rem;
            font-size: 0.8rem;
            width: calc(100% - 1rem);
            margin: 0 0.5rem;
            transition: var(--transition);
            font-family: Georgia, serif;
        }}
        section[data-testid="stSidebar"] .stButton button:hover {{
            background: rgba(255,255,255,0.08);
            color: white;
        }}
        .sidebar-user {{
            color: var(--text-primary);
            padding: 0.2rem 1rem 0.3rem 1rem;
        }}
        .sidebar-user strong {{ font-size: 0.9rem; font-weight: 600; color: white; }}
        .sidebar-user span {{ opacity: 0.4; font-size: 0.7rem; color: var(--text-secondary); }}
        .sidebar-divider {{
            height: 1px;
            background: linear-gradient(to right, transparent, rgba(255,255,255,0.06), transparent);
            margin: 0.3rem 1rem;
        }}
        .sidebar-logo {{
            padding: 0.3rem 1rem 0.8rem 1rem;
            border-bottom: 1px solid rgba(255,255,255,0.04);
            margin-bottom: 0.3rem;
        }}
        .sidebar-logo-text {{
            font-size: 1.15rem;
            font-weight: 700;
            color: white;
            letter-spacing: -0.3px;
            font-family: Georgia, serif;
        }}
        .sidebar-logo-sub {{
            font-size: 0.62rem;
            color: rgba(255,255,255,0.3);
            letter-spacing: 0.6px;
            margin-top: 0.1rem;
            font-family: Georgia, serif;
        }}

        /* ── Glass Cards ── */
        .doc-card {{
            background: var(--glass-bg);
            backdrop-filter: var(--glass-blur);
            -webkit-backdrop-filter: var(--glass-blur);
            border: 1px solid var(--glass-border);
            border-radius: var(--radius);
            padding: 1rem 1.25rem;
            box-shadow: 0 4px 24px rgba(0,0,0,0.2);
            transition: var(--transition);
            display: flex;
            align-items: flex-start;
            gap: 1rem;
            margin-bottom: 0.7rem;
            position: relative;
        }}
        .doc-card::before {{
            content: '';
            position: absolute;
            left: 0;
            top: 20%;
            height: 60%;
            width: 3px;
            border-radius: 0 3px 3px 0;
            background: var(--glass-border);
            transition: var(--transition);
            opacity: 0;
        }}
        .doc-card:hover {{
            background: var(--bg-card-hover);
            border-color: var(--glass-border-hover);
            box-shadow: 0 8px 40px rgba(0,0,0,0.3), 0 0 40px rgba(96,165,250,0.05);
            transform: translateY(-2px);
        }}
        .doc-card:hover::before {{
            background: var(--accent);
            opacity: 1;
            height: 70%;
            top: 15%;
        }}
        .doc-type-badge {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            min-width: 40px;
            height: 40px;
            border-radius: var(--radius-xs);
            font-size: 0.7rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.3px;
            flex-shrink: 0;
            transition: var(--transition);
            font-family: Georgia, serif;
        }}
        .doc-card:hover .doc-type-badge {{ transform: scale(1.06); }}
        .type-livre {{ background: rgba(167, 139, 250, 0.15); color: #a78bfa; }}
        .type-these {{ background: rgba(244, 114, 182, 0.15); color: #f472b6; }}
        .type-revue {{ background: rgba(96, 165, 250, 0.15); color: #60a5fa; }}
        .type-dvd {{ background: rgba(52, 211, 153, 0.15); color: #34d399; }}
        .doc-body {{ flex: 1; min-width: 0; }}
        .doc-title {{ font-size: 0.95rem; font-weight: 600; color: var(--text-primary); margin: 0 0 0.2rem 0; line-height: 1.4; font-family: Georgia, serif; }}
        .doc-meta {{ font-size: 0.8rem; color: var(--text-secondary); margin: 0 0 0.35rem 0; display: flex; flex-wrap: wrap; gap: 0.4rem; align-items: center; }}
        .doc-tags {{ display: flex; flex-wrap: wrap; gap: 0.25rem; }}
        .doc-tag {{
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.05);
            border-radius: 20px;
            padding: 0.05rem 0.5rem;
            font-size: 0.7rem;
            color: var(--text-muted);
            transition: var(--transition);
        }}
        .doc-tag:hover {{ background: rgba(255,255,255,0.07); border-color: rgba(255,255,255,0.1); }}

        /* ── Badges ── */
        .badge {{
            display: inline-flex;
            align-items: center;
            gap: 0.3rem;
            padding: 0.1rem 0.6rem;
            border-radius: 20px;
            font-size: 0.73rem;
            font-weight: 500;
            font-family: Georgia, serif;
        }}
        .badge::before {{
            content: '';
            display: inline-block;
            width: 6px;
            height: 6px;
            border-radius: 50%;
            flex-shrink: 0;
        }}
        .badge-success {{ background: var(--success-bg); color: var(--success-dark); }}
        .badge-success::before {{ background: var(--success); }}
        .badge-danger {{ background: var(--danger-bg); color: var(--danger-dark); }}
        .badge-danger::before {{ background: var(--danger); }}
        .badge-warning {{ background: var(--warning-bg); color: var(--warning); }}
        .badge-warning::before {{ background: var(--warning); }}
        .badge-info {{ background: var(--info-bg); color: var(--info); }}
        .badge-info::before {{ background: var(--info); }}
        .badge-neutral {{ background: rgba(255,255,255,0.04); color: var(--text-muted); }}
        .badge-neutral::before {{ background: var(--text-muted); }}

        /* ── Hero ── */
        .hero {{
            background: rgba(255,255,255,0.02);
            backdrop-filter: blur(24px);
            -webkit-backdrop-filter: blur(24px);
            border: 1px solid rgba(255,255,255,0.06);
            border-radius: var(--radius);
            padding: 2.75rem 2.5rem;
            margin-bottom: 2rem;
            color: white;
            position: relative;
            overflow: hidden;
        }}
        .hero::after {{
            content: '';
            position: absolute;
            top: -60%;
            right: -15%;
            width: 500px;
            height: 500px;
            background: radial-gradient(circle, rgba(96,165,250,0.06) 0%, transparent 60%);
            border-radius: 50%;
            pointer-events: none;
        }}
        .hero h1 {{
            font-size: 2rem;
            font-weight: 700;
            margin: 0 0 0.4rem 0;
            letter-spacing: -0.5px;
            position: relative;
            z-index: 1;
            color: white;
            font-family: Georgia, serif;
            background: linear-gradient(135deg, #f0f0ff, #93bbfd);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        .hero p {{
            font-size: 1rem;
            opacity: 0.7;
            margin: 0;
            max-width: 550px;
            line-height: 1.65;
            position: relative;
            z-index: 1;
            color: rgba(255,255,255,0.8);
        }}

        /* ── Feature cards ── */
        .feature-card {{
            background: var(--glass-bg);
            backdrop-filter: var(--glass-blur);
            -webkit-backdrop-filter: var(--glass-blur);
            border: 1px solid var(--glass-border);
            border-radius: var(--radius);
            padding: 1.75rem 1.25rem 1.5rem;
            text-align: center;
            box-shadow: 0 4px 24px rgba(0,0,0,0.15);
            transition: var(--transition);
            position: relative;
            overflow: hidden;
        }}
        .feature-card::after {{
            content: '';
            position: absolute;
            bottom: 0;
            left: 15%;
            width: 70%;
            height: 2px;
            border-radius: 2px 2px 0 0;
            opacity: 0;
            transition: var(--transition);
            background: linear-gradient(90deg, transparent, var(--accent), transparent);
        }}
        .feature-card:hover {{
            background: var(--bg-card-hover);
            border-color: var(--glass-border-hover);
            box-shadow: 0 12px 48px rgba(0,0,0,0.25), 0 0 40px rgba(96,165,250,0.04);
            transform: translateY(-4px);
        }}
        .feature-card:hover::after {{ opacity: 1; }}
        .feature-card h3 {{ font-size: 0.92rem; font-weight: 600; color: var(--text-primary); margin: 0 0 0.35rem 0; font-family: Georgia, serif; }}
        .feature-card p {{ font-size: 0.8rem; color: var(--text-secondary); margin: 0; line-height: 1.55; }}
        .feature-icon {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 50px;
            height: 50px;
            border-radius: 14px;
            margin-bottom: 0.9rem;
            font-size: 1.05rem;
            font-weight: 700;
            transition: var(--transition);
            font-family: Georgia, serif;
        }}
        .feature-card:hover .feature-icon {{ transform: scale(1.1); border-radius: 12px; }}
        .fi-catalogue {{ background: rgba(167, 139, 250, 0.15); color: #a78bfa; }}
        .fi-recherche {{ background: rgba(96, 165, 250, 0.15); color: #60a5fa; }}
        .fi-emprunts {{ background: rgba(52, 211, 153, 0.15); color: #34d399; }}
        .fi-avis {{ background: rgba(251, 191, 36, 0.15); color: #fbbf24; }}

        /* ── KPI cards ── */
        .kpi-card {{
            background: var(--glass-bg);
            backdrop-filter: var(--glass-blur);
            -webkit-backdrop-filter: var(--glass-blur);
            border: 1px solid var(--glass-border);
            border-radius: var(--radius);
            padding: 1.25rem 1rem;
            box-shadow: 0 4px 24px rgba(0,0,0,0.15);
            text-align: center;
            transition: var(--transition);
        }}
        .kpi-card:hover {{
            background: var(--bg-card-hover);
            border-color: var(--glass-border-hover);
            box-shadow: 0 8px 32px rgba(0,0,0,0.25);
            transform: translateY(-2px);
        }}
        .kpi-value {{ font-size: 1.8rem; font-weight: 700; color: var(--text-primary); letter-spacing: -0.5px; font-family: Georgia, serif; }}
        .kpi-label {{ font-size: 0.7rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.8px; margin-top: 0.15rem; font-weight: 600; }}

        /* ── Auth card ── */
        .auth-card {{
            max-width: 400px;
            margin: 2rem auto;
            background: var(--glass-bg);
            backdrop-filter: var(--glass-blur);
            -webkit-backdrop-filter: var(--glass-blur);
            border: 1px solid var(--glass-border);
            border-radius: var(--radius);
            padding: 2rem 2rem 0.5rem;
            box-shadow: 0 8px 40px rgba(0,0,0,0.2);
        }}
        .auth-title {{ text-align: center; font-size: 1.3rem; font-weight: 700; color: var(--text-primary); margin-bottom: 1.5rem; letter-spacing: -0.3px; font-family: Georgia, serif; }}

        /* ── Steps ── */
        .step {{ text-align: center; padding: 0.8rem; }}
        .step-num {{
            width: 36px; height: 36px; line-height: 36px; border-radius: 50%;
            background: linear-gradient(135deg, var(--accent), var(--secondary));
            color: white; font-weight: 700; font-size: 0.85rem;
            margin: 0 auto 0.6rem auto;
            box-shadow: 0 4px 16px rgba(96,165,250,0.2);
        }}
        .step strong {{ font-size: 0.88rem; color: var(--text-primary); font-weight: 600; font-family: Georgia, serif; }}

        /* ── Buttons ── */
        .stButton > button {{
            border-radius: var(--radius-xs) !important;
            font-weight: 500 !important;
            transition: var(--transition) !important;
            font-size: 0.85rem !important;
            font-family: Georgia, serif !important;
            letter-spacing: 0.02em;
        }}
        .stButton > button[kind="primary"] {{
            background: linear-gradient(135deg, rgba(96,165,250,0.2), rgba(167,139,250,0.15)) !important;
            color: var(--text-primary) !important;
            border: 1px solid rgba(96,165,250,0.25) !important;
            box-shadow: 0 4px 16px rgba(96,165,250,0.1) !important;
            backdrop-filter: blur(8px) !important;
        }}
        .stButton > button[kind="primary"]:hover {{
            background: linear-gradient(135deg, rgba(96,165,250,0.3), rgba(167,139,250,0.25)) !important;
            border-color: rgba(96,165,250,0.4) !important;
            box-shadow: 0 8px 32px rgba(96,165,250,0.2) !important;
            transform: translateY(-1px);
        }}
        .stButton > button[kind="secondary"] {{
            background: rgba(255,255,255,0.03) !important;
            border: 1px solid var(--glass-border) !important;
            color: var(--text-secondary) !important;
        }}
        .stButton > button[kind="secondary"]:hover {{
            border-color: var(--glass-border-hover) !important;
            background: rgba(255,255,255,0.06) !important;
        }}

        /* ── Expander ── */
        .streamlit-expanderHeader {{
            font-weight: 600 !important;
            color: var(--text-primary) !important;
            font-size: 0.88rem !important;
            border-radius: var(--radius-xs) !important;
            padding: 0.5rem 0.75rem !important;
            background: rgba(255,255,255,0.02) !important;
            border: 1px solid var(--glass-border) !important;
            transition: var(--transition) !important;
            font-family: Georgia, serif !important;
        }}
        .streamlit-expanderHeader:hover {{ background: rgba(255,255,255,0.05) !important; }}
        .streamlit-expanderContent {{
            border: 1px solid var(--glass-border) !important;
            border-top: none !important;
            border-radius: 0 0 var(--radius-xs) var(--radius-xs) !important;
            padding: 0.5rem 1rem !important;
            background: rgba(255,255,255,0.01) !important;
        }}

        /* ── Stars ── */
        .stars {{ color: #fbbf24; letter-spacing: 1px; font-size: 0.95rem; }}
        .stars-empty {{ opacity: 0.15; color: white; }}
        .rating-text {{ font-size: 0.78rem; color: var(--text-muted); margin-left: 0.25rem; }}

        /* ── Tabs ── */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 0;
            border-bottom: 1px solid var(--glass-border);
            padding: 0;
        }}
        .stTabs [data-baseweb="tab"] {{
            font-size: 0.82rem;
            font-weight: 500;
            color: var(--text-muted);
            padding: 0.5rem 1.2rem;
            border-bottom: 2px solid transparent;
            transition: var(--transition);
            margin-bottom: -1px;
            font-family: Georgia, serif;
        }}
        .stTabs [data-baseweb="tab"]:hover {{ color: var(--text-primary); background: rgba(255,255,255,0.02); }}
        .stTabs [aria-selected="true"] {{
            color: var(--accent) !important;
            border-bottom-color: var(--accent) !important;
        }}

        /* ── Form inputs ── */
        .stTextInput input, .stSelectbox div[data-baseweb="select"] > div,
        .stTextArea textarea, .stNumberInput input {{
            background: rgba(255,255,255,0.03) !important;
            border: 1px solid var(--glass-border) !important;
            border-radius: var(--radius-xs) !important;
            font-size: 0.82rem !important;
            transition: var(--transition) !important;
            color: var(--text-primary) !important;
            font-family: Georgia, serif !important;
        }}
        .stTextInput input:focus, .stSelectbox div[data-baseweb="select"] > div:focus,
        .stTextArea textarea:focus, .stNumberInput input:focus {{
            border-color: var(--accent) !important;
            background: rgba(255,255,255,0.05) !important;
            box-shadow: 0 0 0 3px var(--accent-glow) !important;
        }}
        .stSelectbox div[data-baseweb="select"] > div {{ color: var(--text-primary) !important; }}
        .stSelectbox svg {{ fill: var(--text-muted) !important; }}

        /* Label styling */
        .stTextInput label, .stSelectbox label, .stTextArea label, .stNumberInput label {{
            color: var(--text-secondary) !important;
            font-size: 0.8rem !important;
            font-family: Georgia, serif !important;
        }}

        /* ── Checkbox / Radio ── */
        .stCheckbox label {{ font-size: 0.82rem; color: var(--text-secondary); font-family: Georgia, serif; }}
        .stRadio label {{ font-size: 0.82rem; color: var(--text-secondary); font-family: Georgia, serif; }}
        .stCheckbox svg {{ fill: var(--accent) !important; }}

        /* ── Metrics ── */
        div[data-testid="stMetric"] {{
            background: var(--glass-bg);
            backdrop-filter: var(--glass-blur);
            border: 1px solid var(--glass-border);
            border-radius: var(--radius);
            padding: 0.8rem 1rem;
            box-shadow: 0 4px 20px rgba(0,0,0,0.12);
        }}
        div[data-testid="stMetricValue"] {{ color: var(--text-primary); font-weight: 700; font-size: 1.6rem; font-family: Georgia, serif; }}
        div[data-testid="stMetricLabel"] {{ font-size: 0.72rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.6px; font-weight: 600; }}

        /* ── Alerts ── */
        .stAlert {{
            border-radius: var(--radius-xs) !important;
            border: 1px solid var(--glass-border) !important;
            font-size: 0.82rem !important;
            background: rgba(255,255,255,0.02) !important;
            font-family: Georgia, serif !important;
        }}
        .stAlert > div:first-child {{ border-radius: var(--radius-xs) !important; }}

        /* ── Progress bar ── */
        .stProgress > div {{
            background: rgba(255,255,255,0.05) !important;
            border-radius: 20px !important;
        }}
        .stProgress > div > div > div {{
            background: linear-gradient(90deg, var(--accent), var(--secondary)) !important;
            border-radius: 20px !important;
        }}

        /* ── Container ── */
        div.st-emotion-cache-1r6slb0,
        div[data-testid="stVerticalBlockBorder"] > div {{
            border-color: var(--glass-border) !important;
            border-radius: var(--radius-xs) !important;
        }}

        /* ── Popover ── */
        div[data-baseweb="popover"] div {{
            background: rgba(15,15,25,0.95) !important;
            backdrop-filter: blur(24px) !important;
            border: 1px solid var(--glass-border) !important;
            border-radius: var(--radius-xs) !important;
            box-shadow: 0 8px 40px rgba(0,0,0,0.4) !important;
        }}

        /* ── Spinner ── */
        .stSpinner > div {{ border-color: var(--accent) transparent transparent transparent !important; }}

        /* ── Select Slider ── */
        div[data-baseweb="slider"] div {{ background: var(--accent) !important; }}

        /* ── Dataframe ── */
        .stDataFrame {{ border: 1px solid var(--glass-border) !important; border-radius: var(--radius-xs) !important; }}
        .stDataFrame thead tr th {{ background: rgba(255,255,255,0.03) !important; font-size: 0.78rem !important; font-weight: 600 !important; color: var(--text-secondary) !important; }}
        .stDataFrame tbody tr td {{ color: var(--text-secondary) !important; }}
    </style>
    """, unsafe_allow_html=True)

    # Inject floating orbs + particles (visible background elements)
    st.markdown("""
    <div class="orb orb-1"></div>
    <div class="orb orb-2"></div>
    <div class="orb orb-3"></div>
    <div class="orb orb-4"></div>
    <div class="particles"></div>
    """, unsafe_allow_html=True)


# ── Helpers ──────────────────────────────────────────────

def render_stars(note: float) -> str:
    full = int(round(note))
    empty = 5 - full
    return f"<span class='stars'>{'★' * full}<span class='stars-empty'>{'★' * empty}</span></span><span class='rating-text'>({note})</span>"


def badge(nb: int) -> str:
    if nb > 0:
        return f"<span class='badge badge-success'>{nb} disponible(s)</span>"
    return "<span class='badge badge-danger'>Indisponible</span>"


def status_badge(statut: str) -> str:
    badges_map = {
        "en_cours": "<span class='badge badge-info'>En cours</span>",
        "retourne": "<span class='badge badge-success'>Retourne</span>",
        "retard": "<span class='badge badge-danger'>En retard</span>",
    }
    return badges_map.get(statut, statut)


def type_badge(type_doc: str) -> str:
    classes_map = {
        "livre": "type-livre",
        "these": "type-these",
        "revue": "type-revue",
        "dvd": "type-dvd",
    }
    labels_map = {
        "livre": "L",
        "these": "T",
        "revue": "R",
        "dvd": "D",
    }
    cls = classes_map.get(type_doc, "type-livre")
    label = labels_map.get(type_doc, "?")
    return f"<span class='doc-type-badge {cls}'>{label}</span>"


def feature_icon(name: str) -> str:
    icons = {
        "catalogue": ("fi-catalogue", "C"),
        "recherche": ("fi-recherche", "R"),
        "emprunts": ("fi-emprunts", "E"),
        "avis": ("fi-avis", "A"),
    }
    cls, letter = icons.get(name, ("fi-catalogue", "?"))
    return f"<div class='feature-icon {cls}'>{letter}</div>"


def render_sidebar():
    st.sidebar.markdown("<div style='padding: 0.5rem 0;'>", unsafe_allow_html=True)
    st.sidebar.markdown("""
    <div class="sidebar-logo">
        <div class="sidebar-logo-text">BiblioTech</div>
        <div class="sidebar-logo-sub">Gestion de bibliotheque</div>
    </div>
    """, unsafe_allow_html=True)
    if st.session_state.get("utilisateur"):
        pseudo = st.session_state["utilisateur"]["pseudo"]
        role = st.session_state.get("role", "etudiant")
        role_label = "Bibliothecaire" if role == "bibliothecaire" else "Etudiant"
        st.sidebar.markdown(
            f"<div class='sidebar-user'><strong>{pseudo}</strong><br><span>{role_label}</span></div>",
            unsafe_allow_html=True
        )
        st.sidebar.markdown("<div class='sidebar-divider'></div>", unsafe_allow_html=True)
        st.sidebar.markdown("<div class='sidebar-section'>Navigation</div>", unsafe_allow_html=True)
        st.sidebar.page_link("app.py", label="Accueil")
        st.sidebar.page_link("pages/catalogue.py", label="Catalogue")
        st.sidebar.page_link("pages/recherche.py", label="Recherche")
        st.sidebar.page_link("pages/mes_emprunts.py", label="Mes emprunts")
        st.sidebar.page_link("pages/avis.py", label="Mes avis")
        if role == "bibliothecaire":
            st.sidebar.markdown("<div class='sidebar-section'>Bibliothecaire</div>", unsafe_allow_html=True)
            st.sidebar.page_link("pages/emprunts.py", label="Gestion des emprunts")
            st.sidebar.page_link("pages/tableau_de_bord.py", label="Tableau de bord")
        st.sidebar.markdown("<div class='sidebar-divider'></div>", unsafe_allow_html=True)
        if st.sidebar.button("Se deconnecter"):
            st.session_state["utilisateur"] = None
            st.session_state["role"] = None
            st.rerun()
    else:
        st.sidebar.markdown("<div class='sidebar-section'>Accueil</div>", unsafe_allow_html=True)
        st.sidebar.page_link("pages/connexion.py", label="Connexion")
    st.sidebar.markdown("</div>", unsafe_allow_html=True)
