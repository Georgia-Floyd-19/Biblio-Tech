from bson import ObjectId
from datetime import datetime, timedelta
from database import catalogue, utilisateurs, emprunts
from utils import hash_password, verify_password


# ─── Utilisateurs ───────────────────────────────────────

def creer_utilisateur(pseudo: str, email: str, mot_de_passe: str, role="etudiant"):
    if utilisateurs.find_one({"pseudo": pseudo}):
        raise Exception("Ce pseudo est déjà utilisé.")
    if utilisateurs.find_one({"email": email}):
        raise Exception("Cet email est déjà utilisé.")
    document = {
        "pseudo": pseudo,
        "email": email,
        "mot_de_passe": hash_password(mot_de_passe),
        "role": role,
        "date_inscription": datetime.now()
    }
    return utilisateurs.insert_one(document).inserted_id


def authentifier_utilisateur(pseudo: str, mot_de_passe: str):
    utilisateur = utilisateurs.find_one({"pseudo": pseudo})
    if utilisateur and verify_password(mot_de_passe, utilisateur["mot_de_passe"]):
        utilisateur["_id"] = str(utilisateur["_id"])
        return utilisateur
    return None


def obtenir_utilisateur_par_id(utilisateur_id):
    return utilisateurs.find_one({"_id": ObjectId(utilisateur_id)})


def obtenir_utilisateur_par_pseudo(pseudo: str):
    return utilisateurs.find_one({"pseudo": pseudo})


# ─── Catalogue ──────────────────────────────────────────

def ajouter_document(document: dict):
    return catalogue.insert_one(document).inserted_id


def recuperer_catalogue(trier_par=None):
    query = catalogue.find()
    if trier_par == "note_desc":
        query = query.sort("note_moyenne", -1)
    elif trier_par == "note_asc":
        query = query.sort("note_moyenne", 1)
    elif trier_par == "titre_asc":
        query = query.sort("titre", 1)
    elif trier_par == "annee_desc":
        query = query.sort("annee", -1)
    return list(query)


def recuperer_document(document_id):
    return catalogue.find_one({"_id": ObjectId(document_id)})


def modifier_document(document_id, nouveau_document):
    catalogue.update_one(
        {"_id": ObjectId(document_id)},
        {"$set": nouveau_document}
    )


def supprimer_document(document_id):
    actif = emprunts.find_one({
        "document_id": ObjectId(document_id),
        "date_retour_effective": None
    })
    if actif:
        raise Exception("Impossible de supprimer : un emprunt est en cours sur ce document.")
    catalogue.delete_one({"_id": ObjectId(document_id)})


# ─── Recherche ──────────────────────────────────────────

def rechercher_documents(texte="", type_doc="", annee_min=None, annee_max=None, dispo_only=False, mode_recherche="regex"):
    query = {}
    if texte:
        if mode_recherche == "text":
            query["$text"] = {"$search": texte}
        else:
            query["$or"] = [
                {"titre": {"$regex": texte, "$options": "i"}},
                {"tags": {"$regex": texte, "$options": "i"}}
            ]
    if type_doc:
        query["type"] = type_doc
    if annee_min is not None or annee_max is not None:
        clause_annee = {}
        if annee_min is not None:
            clause_annee["$gte"] = annee_min
        if annee_max is not None:
            clause_annee["$lte"] = annee_max
        query["annee"] = clause_annee
    if dispo_only:
        query["nb_exemplaires"] = {"$gt": 0}
    return list(catalogue.find(query))


# ─── Emprunts ───────────────────────────────────────────

def emprunter_document(utilisateur_id: str, document_id: str):
    doc_id = ObjectId(document_id)
    deja_emprunte = emprunts.find_one({
        "utilisateur_id": ObjectId(utilisateur_id),
        "document_id": doc_id,
        "date_retour_effective": None
    })
    if deja_emprunte:
        raise Exception("Vous avez déjà emprunté ce document.")
    doc = catalogue.find_one_and_update(
        {"_id": doc_id, "nb_exemplaires": {"$gt": 0}},
        {"$inc": {"nb_exemplaires": -1}}
    )
    if not doc:
        raise Exception("Document non disponible ou inexistant.")
    catalogue.update_one(
        {"_id": doc_id, "nb_exemplaires": {"$lte": 0}},
        {"$set": {"disponible": False}}
    )
    utilisateur = obtenir_utilisateur_par_id(utilisateur_id)
    maintenant = datetime.now()
    emprunt = {
        "utilisateur_id": ObjectId(utilisateur_id),
        "document_id": doc_id,
        "titre_snapshot": doc["titre"],
        "type_snapshot": doc["type"],
        "date_emprunt": maintenant,
        "date_retour_prevue": maintenant + timedelta(days=21),
        "date_retour_effective": None
    }
    return emprunts.insert_one(emprunt).inserted_id


def retourner_document(emprunt_id: str):
    emp_id = ObjectId(emprunt_id)
    emp = emprunts.find_one_and_update(
        {"_id": emp_id, "date_retour_effective": None},
        {"$set": {"date_retour_effective": datetime.now()}}
    )
    if not emp:
        raise Exception("Emprunt introuvable ou déjà retourné.")
    doc_id = emp["document_id"]
    catalogue.update_one(
        {"_id": doc_id},
        {"$inc": {"nb_exemplaires": 1}}
    )
    catalogue.update_one(
        {"_id": doc_id, "nb_exemplaires": {"$gt": 0}},
        {"$set": {"disponible": True}}
    )


def emprunts_par_utilisateur(utilisateur_id: str):
    return list(emprunts.find({"utilisateur_id": ObjectId(utilisateur_id)}).sort("date_emprunt", -1))


def emprunts_en_cours():
    return list(emprunts.find({"date_retour_effective": None}).sort("date_emprunt", -1))


def emprunts_en_retard():
    return list(emprunts.find({
        "date_retour_prevue": {"$lt": datetime.now()},
        "date_retour_effective": None
    }).sort("date_retour_prevue", 1))


def tous_les_emprunts():
    return list(emprunts.find().sort("date_emprunt", -1))


# ─── Avis ───────────────────────────────────────────────

def ajouter_avis(document_id: str, utilisateur_pseudo: str, note: int, commentaire: str):
    if not commentaire.strip():
        raise Exception("Le commentaire ne peut pas être vide.")
    doc_id = ObjectId(document_id)
    doc = catalogue.find_one({"_id": doc_id})
    if not doc:
        raise Exception("Document introuvable.")
    for avis in doc.get("avis", []):
        if avis["utilisateur_pseudo"] == utilisateur_pseudo:
            raise Exception("Vous avez déjà laissé un avis sur ce document.")
    nouvel_avis = {
        "utilisateur_pseudo": utilisateur_pseudo,
        "note": note,
        "commentaire": commentaire,
        "date": datetime.now()
    }
    catalogue.update_one(
        {"_id": doc_id},
        {"$push": {"avis": nouvel_avis}}
    )
    pipeline = [
        {"$match": {"_id": doc_id}},
        {"$unwind": "$avis"},
        {"$group": {"_id": "$_id", "moyenne": {"$avg": "$avis.note"}}}
    ]
    resultats = list(catalogue.aggregate(pipeline))
    moyenne = resultats[0]["moyenne"] if resultats else note
    catalogue.update_one(
        {"_id": doc_id},
        {"$set": {"note_moyenne": round(moyenne, 2)}}
    )


# ─── Statistiques (Aggregation Pipeline) ────────────────

def top_5_documents_plus_empruntes():
    return list(emprunts.aggregate([
        {"$group": {"_id": "$document_id", "total": {"$sum": 1}}},
        {"$sort": {"total": -1}},
        {"$limit": 5},
        {"$lookup": {
            "from": "catalogue",
            "localField": "_id",
            "foreignField": "_id",
            "as": "document"
        }},
        {"$unwind": "$document"},
        {"$project": {"titre": "$document.titre", "type": "$document.type", "total": 1}}
    ]))


def emprunts_par_type():
    return list(emprunts.aggregate([
        {"$group": {"_id": "$type_snapshot", "total": {"$sum": 1}}},
        {"$sort": {"total": -1}}
    ]))


def taux_retour():
    total = emprunts.count_documents({})
    if total == 0:
        return 0, 0
    a_temps = emprunts.count_documents({
        "$expr": {
            "$and": [
                {"$ne": ["$date_retour_effective", None]},
                {"$lte": ["$date_retour_effective", "$date_retour_prevue"]}
            ]
        }
    })
    en_retard = emprunts.count_documents({
        "$expr": {
            "$or": [
                {"$and": [
                    {"$ne": ["$date_retour_effective", None]},
                    {"$gt": ["$date_retour_effective", "$date_retour_prevue"]}
                ]},
                {"$and": [
                    {"$eq": ["$date_retour_effective", None]},
                    {"$lt": ["$date_retour_prevue", datetime.now()]}
                ]}
            ]
        }
    })
    return a_temps, en_retard


def top_5_utilisateurs_plus_actifs():
    return list(emprunts.aggregate([
        {"$group": {"_id": "$utilisateur_id", "total": {"$sum": 1}}},
        {"$sort": {"total": -1}},
        {"$limit": 5},
        {"$lookup": {
            "from": "utilisateurs",
            "localField": "_id",
            "foreignField": "_id",
            "as": "utilisateur"
        }},
        {"$unwind": "$utilisateur"},
        {"$project": {"pseudo": "$utilisateur.pseudo", "total": 1}}
    ]))
