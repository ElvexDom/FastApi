# backend/modules/df_tools.py
from loguru import logger 
import pandas as pd
import os

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

class Quote(Base):
    __tablename__ = "quotes"

    id = Column(Integer, primary_key=True)
    text = Column(String(100), nullable=False, unique=True)

DB_FILE_PATH = "backend/data/quotes_db.db"
DATABASE_URL = f"sqlite:///{DB_FILE_PATH}"

engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)

def write_db(df: pd.DataFrame):
    session = Session()
    for _, row in df.iterrows():
        # Crée un objet Quote si texte unique
        if not session.query(Quote).filter_by(text=row['text']).first():
            session.add(Quote(id=row['id'], text=row['text']))
    session.commit()
    session.close()

def read_db() -> pd.DataFrame:
    session = Session()
    quotes = session.query(Quote).all()
    session.close()
    # Convertir en DataFrame
    df = pd.DataFrame([{"id": q.id, "text": q.text} for q in quotes])
    df.set_index('id', inplace=True)
    return df

def initialize_db():
    if os.path.exists(DATABASE_URL):
        logger.info("La base de données existe")
    else:
        logger.info(f"impossible de trouver le fichier {DATABASE_URL}")
        Base.metadata.create_all(engine)
        logger.info(f"le fichier {DATABASE_URL} a été créé")
