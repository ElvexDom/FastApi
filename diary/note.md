# Conception du Projet

## Structure du projet
* création d'un dossier de travail  
* création des fichiers  
  * `.venv` (pour l'environnement virtuel)  
  * `.env` (les variables d'environnement)  
  * Procédure d'installation :  
    * `README.md`  
    * `requirements.txt`  
  * `.gitignore` (pour le versionnage)  
* séparation de l'architecture  
  * dossiers :  
    * `APP` : contient toute l'application  
    * `backend` : logique data  
    * `API_IA` : logique IA  
  * architecture en couche  
    * séparation des modules  
    * séparation des modèles  
    * séparation des données  

## Logique / étapes

### Application
* importation des bibliothèques  
* chargement des variables d'environnement  
* création des pages :  
  * accueil  
    * bouton ping API (`hello world`)  
    * GET `'/'`  
  * insérer  
    * formulaire d’insertion  
    * POST `'/insert'`  
    * gestion des exceptions  

### API Backend
* importation des bibliothèques  
* chargement des variables d'environnement  
* création de l'API  
* définition des modèles Pydantic  
* initialisation de la base de données  
* définition des routes :  
  * GET `/` → hello world  
  * POST `/insert` → validation, conversion en df, écriture DB  
  * GET `/read` → lecture complète DB  
  * GET `/read/{id}` → filtre ID et retourne une ligne  

### API Sentiment
* importation des bibliothèques  
* création API  
* définition modèles Pydantic  
* routes :  
  * GET `/` → hello  
  * POST `/analyse_sentiment` → analyse texte et retourne JSON  

### Launcher
* lancement des 2 API sur deux ports différents  

## Tests (pytest)

### Fichiers inclus :
* `tests/test_backend_api.py`  
* `tests/test_sentiment_api.py`  
* `tests/test_backend_orm.py`  

## CI/CD (ICC)

### Actions recommandées :
* lint (ruff/flake8)  
* tests (pytest)  
* coverage  
* build Docker  
* push registry  
* déploiement automatique  

### GitHub Actions : `.github/workflows/projects.yml`

## Architecture
```
mon_projet/
│
├── backend
│   ├── modules
│   │   ├── db_tools.py
│   │   └── df_tools.py
│   ├── data
│   │   ├── quotes_db.csv
│   │   └── quotes_db.db
│   ├── main.py
│   └── sentiment_api.py
│
├── frontend
│   ├── app.py
│   └── pages
│       ├── 0_insérer.py
│       ├── 1_Afficher.py
│       ├── 2_Rechercher.py
│       └── 3_sentiment.py
├── tests
│   ├── test_backend_api.py
│   ├── test_sentiment_api.py
│   └── test_backend_orm.py
│
├── logs
│   └── sentiment_api.log
│
├── .github
│   └── workflows
│       └── projects.yml
│
├── nltk_data
│   └── sentiment
│       └── vader_lexicon.zip
│
├── launcher.py
├── README.md
├── requirements.txt
├── .env
├── .venv
└── .gitignore
```
