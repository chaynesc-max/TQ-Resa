import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Réservation de bureaux", layout="wide")

# Connexion à la base SQLite
conn = sqlite3.connect("data.db")

# Choix du site
site = st.selectbox("Sélectionnez un site :", ["Montréal", "Québec"])

# Chargement des bureaux
rooms = pd.read_sql_query(f"SELECT * FROM rooms WHERE site='{site}'", conn)

# Affichage du plan
st.image(f"static/images/{site}_plan.png", use_container_width=True)

# Liste des bureaux disponibles
available = rooms[rooms["available"] == 1]
st.write("Bureaux disponibles :")
st.dataframe(available[["name", "type", "capacity"]])

# Réservation rapide
with st.form("booking_form"):
    selected = st.selectbox("Choisissez un bureau :", available["name"])
    user = st.text_input("Votre nom")
    date = st.date_input("Date")
    submit = st.form_submit_button("Réserver")

    if submit:
        conn.execute(
            "INSERT INTO bookings (room_id, user, date) VALUES (?, ?, ?)",
            (int(available[available["name"] == selected]["id"].iloc[0]), user, str(date))
        )
        conn.commit()
        st.success(f"✅ Réservation confirmée pour {user} le {date} ({selected})")

conn.close()
