import psycopg2
from dao.db_connection import get_connection
from business_object.session import Session

# Module docstring
"""Module pour la gestion des sessions dans la base de données PostgreSQL."""

class SessionDAO:
    """Classe pour gérer les opérations CRUD sur les sessions dans la base de données."""

    def __init__(self):
        """Initialise une nouvelle instance de la classe SessionDAO."""
        self.connection = get_connection()

    def add_session(self, session):
        """Ajoute une session à la base de données."""
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO analytics_session ("sessionID", "ts", "auth", "level", "userAgent", "item_in_session", "userID_id")
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        try:
            cursor.execute(
                query,
                (
                    session.session_id,
                    session.ts,
                    session.auth,
                    session.level,
                    session.user_agent,
                    session.item_in_session,
                    session.user_id_id,
                ),
            )
            conn.commit()
        except psycopg2.Error as e:
            print(f"Erreur lors de l'insertion de la session : {e}")
            conn.rollback()  # Annule la transaction en cas d'erreur
        finally:
            cursor.close()
            conn.close()

    def delete_all_sessions(self):
        """Supprime toutes les sessions de la base de données."""
        conn = get_connection()
        cursor = conn.cursor()
        query = "DELETE FROM analytics_session"
        try:
            cursor.execute(query)
            conn.commit()
        except psycopg2.Error as e:
            print(f"Erreur lors de la suppression des sessions : {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

    def get_all_sessions(self):
        """Récupère toutes les sessions de la base de données."""
        conn = get_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM analytics_session"
        cursor.execute(query)
        rows = cursor.fetchall()
        sessions = [Session(*row) for row in rows] if rows else []
        cursor.close()
        conn.close()
        return sessions
