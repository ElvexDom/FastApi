#### Installation des bibliothèques

```bash
pip install fastapi uvicorn streamlit pandas requests
```

#### Un mini programme complet

* **frontend** (Streamlit)

  * **pages**

* **backend** :

  * **modules** (contenir nos propres modules)
  * **data** (nos CSV et la base SQLite `quotes_db.db`)

#### Ma base de données "quotes_db.csv" et "quotes_db.db"

Colonnes :

* `id`
* `text`

> Il est également possible de consulter le fichier `diary/note.md` pour des notes complémentaires.

#### Commandes pour lancer le serveur FastAPI avec uvicorn

```bash
uvicorn backend.main:app --reload --log-level debug
```

#### Commandes pour le terminal pour faire un GET

* **Powershell** :

```powershell
Invoke-WebRequest -Method GET "http://127.0.0.1:8000/citation"
```

* **Mac / Linux** :

```bash
curl -X GET "http://127.0.0.1:8000/citation"
```

#### Commandes pour lancer le frontend Streamlit

```bash
streamlit run frontend/app.py
```

#### Commandes pour lancer mes API Python avec `launcher.py`

```bash
python launcher.py
```

> Le `launcher.py` contient la logique pour lancer les 2 API (FastAPI backend et API sentiment) sur des ports distincts.
