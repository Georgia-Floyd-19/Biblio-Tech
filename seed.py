from database import client, catalogue, utilisateurs, emprunts
from utils import hash_password
from datetime import datetime, timedelta
from bson import ObjectId
import random

def seed():
    print("🗑️  Nettoyage des collections...")
    catalogue.delete_many({})
    utilisateurs.delete_many({})
    emprunts.delete_many({})

    # ─── Utilisateurs ───────────────────────────────
    users_data = [
        ("admin", "admin@bibliotech.com", "admin123", "bibliothecaire"),
        ("alice", "alice@etudiant.fr", "pass123", "etudiant"),
        ("bob", "bob@etudiant.fr", "pass123", "etudiant"),
        ("charlie", "charlie@etudiant.fr", "pass123", "etudiant"),
        ("diana", "diana@etudiant.fr", "pass123", "etudiant"),
        ("emma", "emma@etudiant.fr", "pass123", "etudiant"),
    ]
    user_ids = {}
    for pseudo, email, mdp, role in users_data:
        uid = utilisateurs.insert_one({
            "pseudo": pseudo,
            "email": email,
            "mot_de_passe": hash_password(mdp),
            "role": role,
            "date_inscription": datetime.now() - timedelta(days=random.randint(1, 90))
        }).inserted_id
        user_ids[pseudo] = uid
        print(f"  ✅ Utilisateur {pseudo} ({role}) créé")

    # ─── Livres ─────────────────────────────────────
    livres = [
        {"titre": "Les Misérables", "annee": 1862, "tags": ["roman", "classique", "histoire"], "isbn": "978-2253006332", "editeur": "Hachette", "nombre_pages": 1488},
        {"titre": "Le Petit Prince", "annee": 1943, "tags": ["roman", "philosophie", "jeunesse"], "isbn": "978-2070612758", "editeur": "Gallimard", "nombre_pages": 96},
        {"titre": "1984", "annee": 1949, "tags": ["roman", "dystopie", "politique"], "isbn": "978-2070368228", "editeur": "Gallimard", "nombre_pages": 328},
        {"titre": "L’Étranger", "annee": 1942, "tags": ["roman", "existentialisme", "philosophie"], "isbn": "978-2070360024", "editeur": "Gallimard", "nombre_pages": 120},
        {"titre": "Fondation", "annee": 1951, "tags": ["science-fiction", "roman"], "isbn": "978-2253006333", "editeur": "Denoël", "nombre_pages": 320},
        {"titre": "Sapiens : Une brève histoire de l’humanité", "annee": 2011, "tags": ["essai", "histoire", "anthropologie"], "isbn": "978-2757870990", "editeur": "Points", "nombre_pages": 512},
        {"titre": "Astrophysics for People in a Hurry", "annee": 2017, "tags": ["sciences", "astrophysique", "vulgarisation"], "isbn": "978-0393356501", "editeur": "Norton", "nombre_pages": 192},
        {"titre": "Clean Code", "annee": 2008, "tags": ["informatique", "programmation", "agile"], "isbn": "978-0132350884", "editeur": "Prentice Hall", "nombre_pages": 464},
        {"titre": "Les Fleurs du Mal", "annee": 1857, "tags": ["poésie", "classique", "littérature"], "isbn": "978-2253006340", "editeur": "Poulet-Malassis", "nombre_pages": 256},
        {"titre": "Le Rouge et le Noir", "annee": 1830, "tags": ["roman", "classique", "psychologique"], "isbn": "978-2253006357", "editeur": "Le Livre de Poche", "nombre_pages": 544},
        {"titre": "Une brève histoire du temps", "annee": 1988, "tags": ["sciences", "physique", "vulgarisation"], "isbn": "978-2080812383", "editeur": "Flammarion", "nombre_pages": 256},
        {"titre": "Le Nom de la Rose", "annee": 1980, "tags": ["roman", "polar", "histoire", "médiéval"], "isbn": "978-2253057440", "editeur": "Grasset", "nombre_pages": 672},
        {"titre": "L’Alchimiste", "annee": 1988, "tags": ["roman", "philosophie", "aventure"], "isbn": "978-2290357657", "editeur": "J’ai Lu", "nombre_pages": 192},
        {"titre": "La Peste", "annee": 1947, "tags": ["roman", "existentialisme", "allégorie"], "isbn": "978-2070360420", "editeur": "Gallimard", "nombre_pages": 256},
        {"titre": "Introduction to Algorithms", "annee": 1990, "tags": ["informatique", "algorithmique", "référence"], "isbn": "978-0262033848", "editeur": "MIT Press", "nombre_pages": 1312},
        {"titre": "Les Trois Mousquetaires", "annee": 1844, "tags": ["roman", "aventure", "histoire"], "isbn": "978-2253006371", "editeur": "Baudry", "nombre_pages": 768},
        {"titre": "Vingt mille lieues sous les mers", "annee": 1870, "tags": ["roman", "aventure", "science-fiction"], "isbn": "978-2253006388", "editeur": "Hetzel", "nombre_pages": 480},
        {"titre": "L’Écume des jours", "annee": 1947, "tags": ["roman", "fantastique", "amour"], "isbn": "978-2070360031", "editeur": "Gallimard", "nombre_pages": 192},
        {"titre": "Design Patterns : Elements of Reusable Object-Oriented Software", "annee": 1994, "tags": ["informatique", "design patterns", "référence"], "isbn": "978-0201633610", "editeur": "Addison-Wesley", "nombre_pages": 416},
        {"titre": "La Ferme des animaux", "annee": 1945, "tags": ["roman", "satire", "politique"], "isbn": "978-2070360048", "editeur": "Gallimard", "nombre_pages": 112},
    ]

    # ─── Thèses ─────────────────────────────────────
    theses = [
        {"titre": "Apprentissage profond pour la reconnaissance d’images médicales", "annee": 2022, "tags": ["ia", "deep learning", "médecine"], "auteur": "Jean Dupont", "universite": "Sorbonne Université", "annee_soutenance": 2022, "directeur": "Prof. Marie Curie"},
        {"titre": "Optimisation des réseaux de neurones pour le traitement du langage naturel", "annee": 2023, "tags": ["ia", "nlp", "optimisation"], "auteur": "Amel Benali", "universite": "Université Paris-Saclay", "annee_soutenance": 2023, "directeur": "Prof. Luc Moreau"},
        {"titre": "Impact du changement climatique sur la biodiversité marine", "annee": 2021, "tags": ["écologie", "climat", "biodiversité"], "auteur": "Paul Lefèvre", "universite": "Université de Montpellier", "annee_soutenance": 2021, "directeur": "Prof. Claire Fontaine"},
        {"titre": "Analyse des inégalités économiques en Afrique subsaharienne", "annee": 2023, "tags": ["économie", "inégalités", "afrique"], "auteur": "Fatima Diallo", "universite": "Université Cheikh Anta Diop", "annee_soutenance": 2023, "directeur": "Prof. Thomas Sankara"},
        {"titre": "Nouvelles approches thérapeutiques contre le cancer du poumon", "annee": 2024, "tags": ["médecine", "cancer", "thérapie"], "auteur": "Dr. Sarah Cohen", "universite": "Université de Genève", "annee_soutenance": 2024, "directeur": "Prof. Alain Bernard"},
        {"titre": "Étude des supraconducteurs à haute température critique", "annee": 2022, "tags": ["physique", "supraconducteurs", "matériaux"], "auteur": "Hiroshi Tanaka", "universite": "Université Grenoble Alpes", "annee_soutenance": 2022, "directeur": "Prof. Élise Durand"},
        {"titre": "Sociologie des communautés virtuelles dans les jeux en ligne", "annee": 2023, "tags": ["sociologie", "jeux vidéo", "communautés"], "auteur": "Lucas Petit", "universite": "Université Lyon 2", "annee_soutenance": 2023, "directeur": "Prof. Sophie Morel"},
        {"titre": "Synthèse de nanomatériaux pour le stockage d’énergie", "annee": 2024, "tags": ["chimie", "nanomatériaux", "énergie"], "auteur": "Aïcha Koné", "universite": "Université Félix Houphouët-Boigny", "annee_soutenance": 2024, "directeur": "Prof. Pierre Dubois"},
    ]

    # ─── Revues ─────────────────────────────────────
    revues = [
        {"titre": "Science & Vie — Mars 2024", "annee": 2024, "tags": ["sciences", "vulgarisation", "actualité"], "issn": "0036-8369", "volume": "1280", "numero": "3"},
        {"titre": "Nature — Vol 635", "annee": 2024, "tags": ["sciences", "recherche", "biologie"], "issn": "0028-0836", "volume": "635", "numero": "8038"},
        {"titre": "Pour la Science — Avril 2024", "annee": 2024, "tags": ["sciences", "vulgarisation", "maths"], "issn": "0153-4092", "volume": "558", "numero": "4"},
        {"titre": "The Lancet — Janvier 2025", "annee": 2025, "tags": ["médecine", "recherche", "clinique"], "issn": "0140-6736", "volume": "405", "numero": "10472"},
        {"titre": "IEEE Transactions on Pattern Analysis and Machine Intelligence", "annee": 2024, "tags": ["informatique", "ia", "vision"], "issn": "0162-8828", "volume": "46", "numero": "7"},
        {"titre": "Research in African Literatures", "annee": 2023, "tags": ["littérature", "afrique", "culture"], "issn": "0034-5210", "volume": "54", "numero": "2"},
        {"titre": "Journal of Climate Change Research", "annee": 2024, "tags": ["climat", "environnement", "recherche"], "issn": "2589-4567", "volume": "12", "numero": "1"},
        {"titre": "La Recherche — Hors-série IA", "annee": 2023, "tags": ["ia", "sciences", "dossier"], "issn": "0029-5671", "volume": "589", "numero": "HS"},
        {"titre": "Communications of the ACM — June 2024", "annee": 2024, "tags": ["informatique", "acm", "recherche"], "issn": "0001-0782", "volume": "67", "numero": "6"},
        {"titre": "Science — Special Issue on Quantum Computing", "annee": 2024, "tags": ["physique", "quantique", "sciences"], "issn": "0036-8075", "volume": "385", "numero": "6712"},
        {"titre": "Harvard Business Review — France", "annee": 2024, "tags": ["management", "économie", "business"], "issn": "0017-8012", "volume": "102", "numero": "5"},
        {"titre": "Les Cahiers de la Recherche en Éducation", "annee": 2023, "tags": ["éducation", "pédagogie", "recherche"], "issn": "2569-4567", "volume": "18", "numero": "2"},
    ]

    # ─── DVD ─────────────────────────────────────────
    dvds = [
        {"titre": "Cosmos : Une odyssée à travers l’univers", "annee": 2014, "tags": ["documentaire", "astrophysique", "vulgarisation"], "realisateur": "Neil deGrasse Tyson", "duree": 540},
        {"titre": "La Marche de l’Empereur", "annee": 2005, "tags": ["documentaire", "nature", "antarctique"], "realisateur": "Luc Jacquet", "duree": 86},
        {"titre": "Les Algorithmes au quotidien", "annee": 2023, "tags": ["documentaire", "informatique", "ia"], "realisateur": "Clément Baudry", "duree": 120},
        {"titre": "L’Histoire de l’écriture", "annee": 2020, "tags": ["documentaire", "histoire", "écriture"], "realisateur": "Marie-Anne Chabin", "duree": 92},
        {"titre": "Into the Abyss : Les fonds marins", "annee": 2021, "tags": ["documentaire", "océan", "biologie marine"], "realisateur": "James Cameron", "duree": 95},
        {"titre": "La Grande Histoire de la physique quantique", "annee": 2022, "tags": ["documentaire", "physique", "quantique"], "realisateur": "Étienne Klein", "duree": 110},
        {"titre": "L’Économie pour tous", "annee": 2023, "tags": ["documentaire", "économie", "pédagogique"], "realisateur": "Philippe Aghion", "duree": 75},
        {"titre": "Biodiversité : l’alerte", "annee": 2024, "tags": ["documentaire", "écologie", "biodiversité"], "realisateur": "Yann Arthus-Bertrand", "duree": 88},
        {"titre": "Python : de zéro à pro", "annee": 2025, "tags": ["cours", "informatique", "python"], "realisateur": "Dr. Sarah Cohen", "duree": 360},
        {"titre": "Les Grandes Civilisations Africaines", "annee": 2022, "tags": ["documentaire", "histoire", "afrique"], "realisateur": "Joseph Ki-Zerbo", "duree": 130},
    ]

    # ─── Insertion documents ─────────────────────────
    all_docs = []
    doc_ids = {}

    for data in livres:
        doc = {"type": "livre", **data, "nb_exemplaires": random.randint(1, 5), "note_moyenne": 0.0, "avis": []}
        doc["disponible"] = doc["nb_exemplaires"] > 0
        doc_ids[doc["titre"]] = catalogue.insert_one(doc).inserted_id
        all_docs.append(doc)

    for data in theses:
        doc = {"type": "these", **data, "nb_exemplaires": random.randint(1, 3), "note_moyenne": 0.0, "avis": []}
        doc["disponible"] = doc["nb_exemplaires"] > 0
        doc_ids[doc["titre"]] = catalogue.insert_one(doc).inserted_id
        all_docs.append(doc)

    for data in revues:
        doc = {"type": "revue", **data, "nb_exemplaires": random.randint(1, 10), "note_moyenne": 0.0, "avis": []}
        doc["disponible"] = doc["nb_exemplaires"] > 0
        doc_ids[doc["titre"]] = catalogue.insert_one(doc).inserted_id
        all_docs.append(doc)

    for data in dvds:
        doc = {"type": "dvd", **data, "nb_exemplaires": random.randint(1, 4), "note_moyenne": 0.0, "avis": []}
        doc["disponible"] = doc["nb_exemplaires"] > 0
        doc_ids[doc["titre"]] = catalogue.insert_one(doc).inserted_id
        all_docs.append(doc)

    print(f"  ✅ {len(all_docs)} documents insérés")

    # ─── Emprunts ────────────────────────────────────
    utilisateur_list = ["alice", "bob", "charlie", "diana", "emma"]
    titres_docs = list(doc_ids.keys())
    maintenant = datetime.now()
    emprunt_count = 0

    for i, pseudo in enumerate(utilisateur_list):
        nb_emprunts = random.randint(2, 5)
        docs_choisis = random.sample(titres_docs, min(nb_emprunts, len(titres_docs)))
        for titre in docs_choisis:
            doc_id = doc_ids[titre]
            doc = catalogue.find_one({"_id": doc_id})
            if doc and doc["nb_exemplaires"] > 0:
                date_emprunt = maintenant - timedelta(days=random.randint(5, 60))
                date_retour_prevue = date_emprunt + timedelta(days=21)
                date_retour_effective = None
                if random.random() < 0.5:
                    date_retour_effective = date_retour_prevue + timedelta(days=random.randint(-5, 15))
                    if date_retour_effective > maintenant:
                        date_retour_effective = None

                emprunts.insert_one({
                    "utilisateur_id": user_ids[pseudo],
                    "document_id": doc_id,
                    "titre_snapshot": doc["titre"],
                    "type_snapshot": doc["type"],
                    "date_emprunt": date_emprunt,
                    "date_retour_prevue": date_retour_prevue,
                    "date_retour_effective": date_retour_effective
                })
                catalogue.update_one(
                    {"_id": doc_id},
                    {"$inc": {"nb_exemplaires": -1}}
                )
                catalogue.update_one(
                    {"_id": doc_id, "nb_exemplaires": {"$lte": 0}},
                    {"$set": {"disponible": False}}
                )
                emprunt_count += 1

    print(f"  ✅ {emprunt_count} emprunts créés")

    # ─── Avis ────────────────────────────────────────
    commentaires = [
        "Excellent ouvrage, très instructif !",
        "Un peu difficile à suivre mais très complet.",
        "Parfait pour les débutants comme pour les experts.",
        "Je recommande vivement cette lecture.",
        "Bien écrit et très clair.",
        "Contenu un peu daté mais toujours pertinent.",
        "Une référence incontournable dans le domaine.",
        "Très bonne introduction au sujet.",
        "J’ai beaucoup apprécié la clarté des explications.",
        "Quelques passages complexes mais globalement excellent.",
    ]
    avis_count = 0
    for titre in random.sample(titres_docs, min(25, len(titres_docs))):
        doc_id = doc_ids[titre]
        nb_avis = random.randint(1, 4)
        auteurs = random.sample(utilisateur_list, min(nb_avis, len(utilisateur_list)))
        notes_liste = []
        for auteur in auteurs:
            note = random.randint(2, 5)
            commentaire = random.choice(commentaires)
            date_avis = maintenant - timedelta(days=random.randint(1, 30))
            catalogue.update_one(
                {"_id": doc_id},
                {"$push": {"avis": {
                    "utilisateur_pseudo": auteur,
                    "note": note,
                    "commentaire": commentaire,
                    "date": date_avis
                }}}
            )
            notes_liste.append(note)
            avis_count += 1
        if notes_liste:
            moyenne = round(sum(notes_liste) / len(notes_liste), 2)
            catalogue.update_one(
                {"_id": doc_id},
                {"$set": {"note_moyenne": moyenne}}
            )

    print(f"  ✅ {avis_count} avis ajoutés")
    print(f"\n🎉 Seed terminé !")
    print(f"   📚 {len(all_docs)} documents")
    print(f"   👥 {len(users_data)} utilisateurs")
    print(f"   📖 {emprunt_count} emprunts")
    print(f"   ⭐ {avis_count} avis")
    print(f"\n🔐 Identifiants : admin / admin123 (bibliothécaire)")
    print(f"                 alice, bob, charlie, diana, emma — pass123 (étudiants)")

seed()
