# backend/main.py
from fastapi import FastAPI, HTTPException
import pandas as pd
from pydantic import BaseModel, model_validator
from backend.modules.db_tools import read_db, write_db, initialize_db
from typing import List
import random

# modèles pydantic
class QuoteRequest(BaseModel):
    text : str
    @model_validator(mode='before')
    def check_text(cls, values):
        text = values.get('text')
        if not text or not text.strip():
            raise ValueError("Le texte ne peut pas être vide")
        return values
    
class QuoteResponse(BaseModel):
    id : int
    text : str

class QuoteIdResponse(BaseModel):
    id : int

# creation si besoin de la base de données
initialize_db()

# --- Configuration ---
app = FastAPI(title="API")

@app.get("/")
def read_root():
    return {"Hello": "World", "status": "API is running"}

@app.post("/insert/", response_model= QuoteResponse)
def insert_quote(quote : QuoteRequest):
    """Insère une nouvelle citation"""

    # 1. trouver le dernier id dans le csv
    df = read_db()

    # 2. donne un id a ma citation
    if df.empty :
        new_id = 1
    elif df.index.max() <= 0 :
        new_id = 1
    else :
        new_id = 1 + df.index.max()

    # 3.1 créer la nouvelle ligne
    objet = {"text": [quote.text]}
    new_row = pd.DataFrame(objet, index = [new_id])

    # 3.2 enregistrer le fichier csv
    df = pd.concat([df, new_row])
    write_db(df)

    # 4. pour la confirmation je vais envoyer à l'application
    # la citation avec son id
    return {"id":new_id, "text":quote.text}

@app.get("/read/", response_model=List[QuoteResponse])
def read_all_quotes():
    df = read_db()
    return df.reset_index().rename(columns={'id':'id','text':'text'}).to_dict('records')


@app.get("/read/{id}", response_model=QuoteResponse)
def read_specific_quotes(id : int):
    # il me faut toutes les citations pour les connaitres
    df = read_db()
    # filtre par l'id concerné
    if id not in df.index:
        raise HTTPException(status_code=404, detail=f"Citation avec ID {id} non trouvée")
    quote_data = df.loc[id].to_dict()
    quote_data['id'] = id
    # retourne les résultats
    return quote_data

@app.get("/read/random/", response_model=QuoteResponse)
def read_random_quotes():
    # il me faut toutes les citations pour les connaitres
    df = read_db()
    # filtre par l'id concerné  
    if df.empty:
        raise HTTPException(status_code=404, detail=f"Citation avec aléatoire non trouvée")
    
    random_id = random.choice(df.index)
    quote_data = df.loc[random_id].to_dict()
    quote_data['id'] = random_id
    # retourne les résultats
    return quote_data

@app.get("/read/all_ids/", response_model=List[QuoteIdResponse])
def read_all_id():
    # il me faut toutes les citations pour les connaitres
    df = read_db()
    # filtre par l'id concerné  
    if df.empty:
        raise HTTPException(status_code=404, detail=f"Citation avec aléatoire non trouvée")
    # transformer l'index en colonne et convertir en liste de dicts
    ids = df.index.to_frame(name='id').to_dict(orient='records')
    
    return ids
