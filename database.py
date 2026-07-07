from pymongo import MongoClient, TEXT
from config import MONGODB_URI, DATABASE_NAME

client = MongoClient(MONGODB_URI)

db = client[DATABASE_NAME]

catalogue = db["catalogue"]
utilisateurs = db["utilisateurs"]
emprunts = db["emprunts"]


def create_indexes():
    """Créer les index demandés par le sujet"""

    catalogue.create_index(
        [("titre", TEXT), ("tags", TEXT)],
        name="idx_titre_tags"
    )

    catalogue.create_index("type")
    catalogue.create_index("disponible")

    utilisateurs.create_index("pseudo", unique=True)
    utilisateurs.create_index("email", unique=True)

    emprunts.create_index("utilisateur_id")
    emprunts.create_index("date_retour_prevue")


def test_connection():
    try:
        client.admin.command("ping")
        create_indexes()
        return True
    except Exception as e:
        print(e)
        return False