"""
Modèles de données MongoDB pour BiblioTech.

Ce fichier documente la structure des collections et centralise
les schémas utilisés dans l'application. Aucune instanciation directe
n'est requise — MongoDB est sans schéma — mais ces classes servent
de référence et de validation documentaire.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


# ─── Sous-documents ───────────────────────────────────────


@dataclass
class Avis:
    utilisateur_pseudo: str
    note: int              # 1 à 5
    commentaire: str
    date: datetime


# ─── Collection : catalogue ───────────────────────────────

# Polymorphisme : le champ `type` détermine les attributs supplémentaires.
#
#   Champs communs : _id, type, titre, annee, tags, nb_exemplaires,
#                    disponible, note_moyenne, avis
#
#   type == "livre"  →  isbn, editeur, nombre_pages
#   type == "these"  →  auteur, universite, annee_soutenance, directeur
#   type == "revue"  →  issn, volume, numero
#   type == "dvd"    →  realisateur, duree


DOCUMENT_TYPES = {"livre", "these", "revue", "dvd"}

LIVRE_SPECIFIC_FIELDS = ["isbn", "editeur", "nombre_pages"]
THESE_SPECIFIC_FIELDS = ["auteur", "universite", "annee_soutenance", "directeur"]
REVUE_SPECIFIC_FIELDS = ["issn", "volume", "numero"]
DVD_SPECIFIC_FIELDS = ["realisateur", "duree"]


# ─── Collection : utilisateurs ────────────────────────────

# Note : le schéma imposé par le sujet est { _id, pseudo, email, date_inscription }.
#        Nous ajoutons mot_de_passe (hash bcrypt) et role ("etudiant"|"bibliothecaire")
#        pour les besoins de l'authentification.


# ─── Collection : emprunts ────────────────────────────────

# Stratégie : embedding de snapshot (titre_snapshot, type_snapshot)
# pour éviter les lectures coûteuses après suppression ou modification
# d'un document du catalogue.
#
#   _id: ObjectId
#   utilisateur_id: ObjectId (ref utilisateurs)
#   document_id: ObjectId (ref catalogue)
#   titre_snapshot: str
#   type_snapshot: str
#   date_emprunt: datetime
#   date_retour_prevue: datetime
#   date_retour_effective: datetime | None


# ─── Helper : construire un document catalogue ────────────


def build_catalogue_document(
    type_doc: str,
    titre: str,
    annee: int,
    tags: list[str],
    nb_exemplaires: int,
    **specific_fields
) -> dict:
    """Construit un document catalogue validé selon le type."""
    if type_doc not in DOCUMENT_TYPES:
        raise ValueError(f"Type inconnu : {type_doc}")
    return {
        "type": type_doc,
        "titre": titre,
        "annee": annee,
        "tags": tags,
        "nb_exemplaires": nb_exemplaires,
        "disponible": nb_exemplaires > 0,
        "note_moyenne": 0.0,
        "avis": [],
        **specific_fields,
    }
