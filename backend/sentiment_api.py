# backend/sentiment_api.py
from fastapi import FastAPI, HTTPException
from loguru import logger
import pandas as pd
from pydantic import BaseModel, model_validator
from backend.modules.db_tools import read_db, write_db, initialize_db
from typing import List
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Indiquer à NLTK où trouver les données
nltk.data.path.append("nltk_data")
# Initialiser VADER
sia = SentimentIntensityAnalyzer()

# Configuration de Loguru
logger.add("logs/sentiment_api.log", rotation="500 MB", level="INFO")

# modèles pydantic
class Texte(BaseModel):
    texte: str
    @model_validator(mode='before')
    def check_text(cls, values):
        texte = values.get('texte')
        if not texte or not texte.strip():
            raise ValueError("Le texte ne peut pas être vide")
        return values

# --- Configuration ---
feelApp = FastAPI(title="Feel API")

@feelApp.get("/")
def read_root():
    return {"Hello": "World", "status": "API is running"}

@feelApp.post("/analyse_sentiment/")
async def analyse_sentiment(texte_object: Texte):
    logger.info(f"Analyse du texte: {texte_object.texte}")
    try:
        sentiment = sia.polarity_scores(texte_object.texte)
        logger.info(f"Résultats: {sentiment}")
        # on retourne la réponse
        return {
        "neg": sentiment["neg"],
        "neu": sentiment["neu"],
        "pos": sentiment["pos"],
        "compound": sentiment["compound"],
        }
    except Exception as e:
        logger.error(f"Erreur lors de l'analyse: {e}")
        raise HTTPException(status_code=500, detail=str(e))
