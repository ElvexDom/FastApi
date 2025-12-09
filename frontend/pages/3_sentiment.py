# frontend/pages/0_insérer.py
import streamlit as st
import requests 
import os 
from dotenv import load_dotenv

load_dotenv()

FAST_API_PORT = int(os.getenv("FAST_API_PORT", "8080"))+1
API_BASE_URL = os.getenv('API_BASE_URL')

API_ROOT_URL =  f"http://{API_BASE_URL}:{FAST_API_PORT}"
API_URL =  API_ROOT_URL + "/analyse_sentiment"

st.title("Ecire un texte pour analyse (English)")

with st.form("insert_form"):
    new_quote_text = st.text_area("Texte :", height = 150)
    submitted = st.form_submit_button("Soumettre le etxte")

    if submitted:
        data = {"texte":new_quote_text}
        st.info("envoi à l'API")

        try : 
            response = requests.post(API_URL, json=data)

            if response.status_code == 200:
                sentiment = response.json()
                if sentiment['compound'] >= 0.05 :
                    st.write("Sentiment global : Positif 😀")
                elif sentiment['compound'] <= -0.05 :
                    st.write("Sentiment global : Négatif 🙁")
                else :
                    st.write("Sentiment global : Neutre 😐")
            else:
                st.error(f"Erreur de l'API avec le code {response.status_code}")


        except requests.exceptions.ConnectionError:
            st.error(f"ERREUR : Impossible de se connecter à l'API à {API_URL}")
            st.warning("Veuillez vous assurer que le serveur Uvicorn est bien lancé en arrière-plan.")
