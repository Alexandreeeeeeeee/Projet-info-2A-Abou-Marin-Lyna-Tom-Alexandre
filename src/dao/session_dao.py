from dao.db_connection import get_connection
from business_object.session import Session

class SessionDAO:
    from dao.db_connection import get_connection
from business_object.session import Session

class SessionDAO:
    def __init__(self):
        self.connection = get_connection()



    def add_session(self, session):
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO analytics_session ("sessionID", "ts", "auth", "level", "userAgent", "item_in_session", "userID_id")
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        try:
            cursor.execute(query, (
                session.sessionID,
                session.ts,
                session.auth,
                session.level,
                session.userAgent,
                session.item_in_session,
                session.userID_id
            ))
            conn.commit()
        except Exception as e:
            print(f"Error inserting session: {e}")
        finally:
            cursor.close()
            conn.close()

    def delete_all_sessions(self):
        conn = get_connection()
        cursor = conn.cursor()
        query = "DELETE FROM analytics_session"
        cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()

    def get_all_sessions(self):
        conn = get_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM analytics_session"
        cursor.execute(query)
        rows = cursor.fetchall()
        sessions = [Session(*row) for row in rows]
        cursor.close()
        conn.close()
        return sessions

    def calculate_average_session_duration(self):
        with self.connection.cursor() as cursor:
            try:
                cursor.execute("SELECT AVG(ts) FROM analytics_session")  # Supposons que 'ts' représente la durée
                return cursor.fetchone()[0]  # Renvoie la durée moyenne des sessions
            except Exception as e:
                print(f"Erreur lors du calcul de la durée moyenne des sessions : {e}")
                return 0  # Retourne 0 en cas d'erreur
