from database import client, utilisateurs, catalogue
from utils import hash_password

try:
    client.admin.command("ping")
    print("✅ Connexion MongoDB réussie")

    admin = utilisateurs.find_one({"pseudo": "admin"})
    if not admin:
        utilisateurs.insert_one({
            "pseudo": "admin",
            "email": "admin@bibliotech.com",
            "mot_de_passe": hash_password("admin123"),
            "role": "bibliothecaire",
            "date_inscription": __import__('datetime').datetime.now()
        })
        print("✅ Compte bibliothécaire créé (admin / admin123)")
    else:
        print("ℹ️ Compte admin déjà existant")

    utilisateurs.create_index("pseudo", unique=True)
    utilisateurs.create_index("email", unique=True)

    print("✅ Index vérifiés")
    print(f"📚 Documents dans catalogue : {catalogue.count_documents({})}")
    print(f"👥 Utilisateurs : {utilisateurs.count_documents({})}")

except Exception as e:
    print("❌", repr(e))
