# src/dao/contenir_dao.py
from dao.db_connection import get_connection
from business_object.contenir import Contenir

class ContenirDAO:
    def add_contenir(self, contenir):
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO analytics_contenir ("sessionID_id", "songID_id")
            VALUES (%s, %s)
        """
        try:
            cursor.execute(query, (
                contenir.sessionID_id,
                contenir.songID_id  # Assurez-vous d'utiliser songID
            ))
            conn.commit()
        except Exception as e:
            print(f"Error inserting contenir: {e}")
        finally:
            cursor.close()
            conn.close()

    def delete_all_contenirs(self):
        conn = get_connection()
        cursor = conn.cursor()
        query = "DELETE FROM analytics_contenir"
        cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()

    def get_all_contenirs(self):
        conn = get_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM analytics_contenir"
        cursor.execute(query)
        rows = cursor.fetchall()
        contenirs = [Contenir(*row) for row in rows]
        cursor.close()
        conn.close()
        return contenirs
