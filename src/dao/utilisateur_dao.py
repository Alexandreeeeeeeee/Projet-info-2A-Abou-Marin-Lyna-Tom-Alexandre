from dao.db_connection import get_connection
from business_object.utilisateur import Utilisateur


class UtilisateurDAO:
    def __init__(self):
        self.connection = get_connection()

    def add_utilisateur(self, utilisateur):
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
                    utilisateur.userID,
                    utilisateur.lastName,
                    utilisateur.firstName,
                    utilisateur.gender,
                    utilisateur.lon,
                    utilisateur.lat,
                    utilisateur.city,
                    utilisateur.zip,
                    utilisateur.state,
                    utilisateur.registration,
                ),
            )
            conn.commit()
        except Exception as e:
            print(f"Error inserting utilisateur: {e}")
            conn.rollback()  # Annule la transaction en cas d'erreur
        finally:
            cursor.close()
            conn.close()

    def delete_all_users(self):
        conn = get_connection()
        cursor = conn.cursor()
        query = "DELETE FROM analytics_utilisateur"
        cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()

    def get_all_users(self):
        conn = get_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM analytics_utilisateur"
        cursor.execute(query)
        rows = cursor.fetchall()
        if rows:
            users = [Utilisateur(*row) for row in rows]
        cursor.close()
        conn.close()
        return users

    def get_user_by_id(self, userID):
        conn = get_connection()
        cursor = conn.cursor()
        query = 'SELECT * FROM analytics_utilisateur WHERE "userID" = %s'
        cursor.execute(query, (userID,))
        row = cursor.fetchone()
        user = None
        if row:
            user = Utilisateur(*row)
        cursor.close()
        conn.close()
        return user

    def count_users(self):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM analytics_utilisateur")
            res = cursor.fetchone()[0]
            return res
