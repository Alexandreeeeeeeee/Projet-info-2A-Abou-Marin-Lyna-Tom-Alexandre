import os
from dotenv import load_dotenv
import psycopg2

"""Module pour établir une connexion à la base de données PostgreSQL."""

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()

def get_connection():
    """Établit et retourne une connexion à la base de données PostgreSQL en utilisant les variables d'environnement."""
    # Création de la connexion à la base de données avec les paramètres d'environnement
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    return conn
