import psycopg2
from dao.db_connection import get_connection
from business_object.contenir import Contenir


# Module docstring
"""Module pour la gestion des opérations CRUD sur la table 'contenir' dans la base de données PostgreSQL."""

class ContenirDAO:
    """Classe pour gérer les opérations CRUD sur la table 'contenir' dans la base de données."""

    def add_contenir(self, contenir):
        """
        Ajoute une nouvelle ligne dans la table 'contenir'.
        
        :param contenir: Instance de la classe Contenir contenant les données à insérer.
        """
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO analytics_contenir ("sessionID_id", "songID_id")
            VALUES (%s, %s)
        """
        try:
            cursor.execute(query, (
                contenir.session_id,
                contenir.song_id
            ))
            conn.commit()
        except psycopg2.Error as e:
            print(f"Erreur lors de l'insertion de contenir : {e}")
            conn.rollback()  # Annule la transaction en cas d'erreur
        finally:
            cursor.close()
            conn.close()

    def delete_all_contenirs(self):
        """
        Supprime toutes les lignes de la table 'contenir'.
        """
        conn = get_connection()
        cursor = conn.cursor()
        query = "DELETE FROM analytics_contenir"
        try:
            cursor.execute(query)
            conn.commit()
        except psycopg2.Error as e:
            print(f"Erreur lors de la suppression des contenus : {e}")
            conn.rollback()  # Annule la transaction en cas d'erreur
        finally:
            cursor.close()
            conn.close()

    def get_all_contenirs(self):
        """
        Récupère toutes les lignes de la table 'contenir'.
        
        :return: Liste d'instances de la classe Contenir correspondant aux lignes récupérées.
        """
        conn = get_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM analytics_contenir"
        cursor.execute(query)
        rows = cursor.fetchall()
        contenirs = [Contenir(*row) for row in rows] if rows else []
        cursor.close()
        conn.close()
        return contenirs
