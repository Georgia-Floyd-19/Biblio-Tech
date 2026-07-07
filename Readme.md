# BiblioTech 📚

Plateforme de gestion de bibliothèque collaborative — projet NoSQL (Session 4).

## Stack technique

- **Langage :** Python 3.10+
- **Interface :** Streamlit
- **Base de données :** MongoDB Atlas (cluster M0 gratuit)
- **Versionnage :** GitHub

## Installation

1. **Cloner le dépôt**

```bash
git clone <url-du-depot>
cd bibliotech
```

2. **Créer un environnement virtuel**

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
source .venv/bin/activate  # Linux/Mac
```

3. **Installer les dépendances**

```bash
pip install -r requirements.txt
```

4. **Configurer les variables d'environnement**

Copier le fichier `.env.example` vers `.env` et renseigner les vraies valeurs :

```bash
cp .env.example .env
```

Éditer `.env` :
```
MONGODB_URI=mongodb+srv://<utilisateur>:<motdepasse>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
DATABASE_NAME=bibliotech
```

5. **Lancer l'application**

```bash
streamlit run app.py
```

## Structure du projet

```
bibliotech/
├── app.py                  # Point d'entrée Streamlit
├── config.py               # Configuration (variables d'environnement)
├── database.py             # Connexion MongoDB et index
├── models.py               # Modèles de données
├── services.py             # Logique métier
├── utils.py                # Fonctions utilitaires
├── pages/
│   ├── catalogue.py        # Gestion du catalogue (CRUD)
│   ├── connexion.py        # Authentification
│   ├── recherche.py        # Recherche avancée
│   ├── emprunts.py         # Gestion des emprunts (bibliothécaire)
│   ├── mes_emprunts.py     # Mes emprunts (étudiant)
│   └── tableau_de_bord.py  # Statistiques (bibliothécaire)
├── requirements.txt        # Dépendances Python
├── .env.example            # Variables d'environnement (template)
├── .gitignore
└── README.md
```

## Fonctionnalités

1. **Catalogue hétérogène** — Ajout, modification, suppression de documents (livres, thèses, revues, DVD)
2. **Recherche avancée** — Filtres textuels, par type, année, disponibilité
3. **Gestion des emprunts** — Emprunt, retour, suivi des retards
4. **Avis et notes** — Notation des documents empruntés
5. **Tableau de bord** — Statistiques via aggregation pipeline MongoDB

## Déploiement

L'application est déployée sur [Streamlit Community Cloud](https://bibliotech.streamlit.app).
