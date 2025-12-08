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

DB_FILE_PATH = os.path.join("backend","data", "quotes_db.db")
DATABASE_URL = f"sqlite:///{DB_FILE_PATH}"

engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)

def write_db(df: pd.DataFrame):
    with Session() as session:
        row = df.iloc[-1]
        exists = session.query(Quote).filter_by(text=row['text']).first()
        if not exists:
            session.add(Quote(text=row['text']))
        session.commit()


def read_db() -> pd.DataFrame:
    with Session() as session:
        quotes = session.query(Quote).all()
    df = pd.DataFrame([{"id": q.id, "text": q.text} for q in quotes])
    if not df.empty:
        df.set_index("id", inplace=True)
        print(f"ma valeur est la suivante {df}")
    return df

def initialize_db():
    if os.path.exists(DB_FILE_PATH):
        logger.info("La base de données existe")
    else:
        logger.info(f"impossible de trouver le fichier {DB_FILE_PATH}")
        Base.metadata.create_all(engine)
        logger.info(f"le fichier {DB_FILE_PATH} a été créé")
