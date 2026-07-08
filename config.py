from dotenv import load_dotenv
import os
import sys

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
if not MONGODB_URI:
    sys.exit("ERREUR: MONGODB_URI non defini. Copie .env.example en .env et configure-le.")

DATABASE_NAME = os.getenv("DATABASE_NAME", "bibliotech")