import psycopg2
from psycopg2 import OperationalError


def test_connection():
    try:
        # Connexion à la base de données
        connection = psycopg2.connect(
            dbname="postgres", user="postgres", password="postgres", host="localhost", port="5432"
        )
        # Création d'un curseur
        cursor = connection.cursor()
        print("Connexion réussie à la base de données PostgreSQL")

        # Vérifie la version de PostgreSQL
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        print("Version de PostgreSQL:", db_version)

        # Fermeture du curseur et de la connexion
        cursor.close()
        connection.close()

    except OperationalError as e:
        print("Erreur de connexion à la base de données PostgreSQL")
        print(e)


# Appel de la fonction pour tester la connexion
if __name__ == "__main__":
    test_connection()
