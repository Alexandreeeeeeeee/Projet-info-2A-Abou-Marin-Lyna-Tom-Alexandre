import os
from dao.db_connection import get_connection
from business_object.utilisateur import Utilisateur
import psycopg2


class UtilisateurDAO:
    """Classe pour gérer les opérations CRUD sur les utilisateurs dans la base de données."""
    
    def __init__(self):
        """Initialise une nouvelle instance de la classe UtilisateurDAO."""
        self.connection = get_connection()

    def add_utilisateur(self, utilisateur):
        """Ajoute un utilisateur à la base de données ou met à jour ses informations si l'utilisateur existe déjà."""
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO analytics_utilisateur ("userID", "lastName", "firstName", "gender", "lon", "lat", "city", "zip", "state", "registration")
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT ("userID")
            DO UPDATE SET
                "lastName" = EXCLUDED."lastName",
                "firstName" = EXCLUDED."firstName",
                "gender" = EXCLUDED."gender",
                "lon" = EXCLUDED."lon",
                "lat" = EXCLUDED."lat",
                "city" = EXCLUDED."city",
                "zip" = EXCLUDED."zip",
                "state" = EXCLUDED."state",
                "registration" = EXCLUDED."registration"
        """
        try:
            cursor.execute(
                query,
                (
                    utilisateur.user_id,
                    utilisateur.last_name,
                    utilisateur.first_name,
                    utilisateur.gender,
                    utilisateur.lon,
                    utilisateur.lat,
                    utilisateur.city,
                    utilisateur.zip_code,
                    utilisateur.state,
                    utilisateur.registration,
                ),
            )
            conn.commit()
        except psycopg2.Error as e:
            print(f"Erreur lors de l'insertion de l'utilisateur : {e}")
            conn.rollback()  # Annule la transaction en cas d'erreur
        finally:
            cursor.close()
            conn.close()

    def delete_all_users(self):
        """Supprime tous les utilisateurs de la base de données."""
        conn = get_connection()
        cursor = conn.cursor()
        query = "DELETE FROM analytics_utilisateur"
        cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()

    def get_all_users(self):
        """Récupère tous les utilisateurs de la base de données."""
        conn = get_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM analytics_utilisateur"
        cursor.execute(query)
        rows = cursor.fetchall()
        users = []
        if rows:
            users = [Utilisateur(*row) for row in rows]
        cursor.close()
        conn.close()
        return users

    def get_user_by_id(self, user_id):
        """Récupère un utilisateur à partir de son ID."""
        conn = get_connection()
        cursor = conn.cursor()
        query = 'SELECT * FROM analytics_utilisateur WHERE "userID" = %s'
        cursor.execute(query, (user_id,))
        row = cursor.fetchone()
        user = None
        if row:
            user = Utilisateur(*row)
        cursor.close()
        conn.close()
        return user
