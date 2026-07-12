from dotenv import load_dotenv
import os
import sys

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")

if not MONGODB_URI:
    try:
        import streamlit as st
        MONGODB_URI = st.secrets.get("MONGODB_URI")
        os.environ["DATABASE_NAME"] = st.secrets.get("DATABASE_NAME", "bibliotech")
    except Exception:
        pass

if not MONGODB_URI:
    sys.exit("ERREUR: MONGODB_URI non defini. Copie .env.example en .env et configure-le.")

DATABASE_NAME = os.getenv("DATABASE_NAME", "bibliotech")