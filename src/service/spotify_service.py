"""Module providing Spotify analytics services."""

from datetime import datetime
import folium
from dao.utilisateur_dao import UtilisateurDAO
from dao.song_dao import SongDAO
from dao.session_dao import SessionDAO
from dao.db_connection import get_connection
from dao.contenir_dao import ContenirDAO

class SpotifyService:
    """Service pour gérer les opérations liées à Spotify Analytics."""

    def __init__(self):
        """Initialise les DAO pour les utilisateurs, les chansons, et les sessions."""
        self.utilisateur_dao = UtilisateurDAO()
        self.song_dao = SongDAO()
        self.session_dao = SessionDAO()
        self.contenir_dao = ContenirDAO()

    def get_total_songs(self):
        """Retourne le nombre total de chansons dans la base de données."""
        with self.song_dao.connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM analytics_song")
            return cursor.fetchone()[0]

    def get_total_users(self):
        """Retourne le nombre total d'utilisateurs dans la base de données."""
        with self.utilisateur_dao.connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM analytics_utilisateur")
            return cursor.fetchone()[0]

    def get_average_session_duration(self):
        """Retourne la durée moyenne des sessions en millisecondes."""
        with self.session_dao.connection.cursor() as cursor:
            cursor.execute("SELECT AVG(ts) FROM analytics_session")
            return cursor.fetchone()[0]

    def get_top_artists_by_date(self):
        """Retourne les artistes les plus populaires par date."""
        query = """
        SELECT TO_CHAR(TO_TIMESTAMP(s."ts" / 1000), 'YYYY-MM-DD') AS session_date, 
               a."artist", COUNT(a."songID") AS song_count
        FROM public.analytics_session AS s
        JOIN public.analytics_contenir AS c ON s."sessionID" = c."sessionID_id"
        JOIN public.analytics_song AS a ON c."songID_id" = a."songID"
        GROUP BY session_date, a."artist"
        ORDER BY session_date DESC, song_count DESC;
        """
        with self.session_dao.connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()

        # Transformation des résultats pour inclure les dates formatées
        return [
            (datetime.strptime(row[0], '%Y-%m-%d'), row[1], row[2]) for row in results
        ]


    def get_average_item_in_session_by_level(self):
        """Retourne la moyenne des éléments par session, groupée par niveau d'abonnement."""
        query = """
        SELECT s.level, AVG(s.item_in_session) AS average_items
        FROM public.analytics_session AS s
        GROUP BY s.level
        ORDER BY s.level;
        """
        # Utilisation du DAO Session pour exécuter la requête
        with self.session_dao.connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()

        return {row[0]: row[1] for row in results}


    def get_user_coordinates(self, debug=False):
        """Retourne les coordonnées des utilisateurs.

        Args:
            debug (bool): Si vrai, imprime les coordonnées pour déboguer.
        """
        query = "SELECT lat, lon FROM analytics_utilisateur WHERE lat IS NOT NULL AND lon IS NOT NULL"
    
        with self.utilisateur_dao.connection.cursor() as cursor:
            cursor.execute(query)
            coordinates = cursor.fetchall()
    
        if debug:
            print("Coordonnées des utilisateurs :", coordinates)

        return coordinates


    def get_most_active_users(self, top_n=10):
        """Retourne les utilisateurs les plus actifs."""
        query = """
        SELECT u."userID", u."firstName", u."lastName", COUNT(s."sessionID") AS session_count
        FROM public.analytics_utilisateur AS u
        JOIN public.analytics_session AS s ON u."userID" = s."userID_id"
        GROUP BY u."userID", u."firstName", u."lastName"
        ORDER BY session_count DESC
        LIMIT %s;
        """
        with self.utilisateur_dao.connection.cursor() as cursor:
            cursor.execute(query, (top_n,))
            results = cursor.fetchall()

        return [{"userID": row[0], "name": f"{row[1]} {row[2]}", "sessions": row[3]} for row in results]


    def get_activity_peak_times(self):
        """Analyse les pics d'activité par heure et par jour."""
        query_hourly = """
        SELECT TO_CHAR(TO_TIMESTAMP(s."ts" / 1000), 'HH24') AS hour, COUNT(*) AS activity_count
        FROM public.analytics_session AS s
        GROUP BY hour
        ORDER BY activity_count DESC;
        """
        with self.session_dao.connection.cursor() as cursor:
            cursor.execute(query_hourly)
            hourly_activity = cursor.fetchall()

        query_daily = """
        SELECT TO_CHAR(TO_TIMESTAMP(s."ts" / 1000), 'DY') AS day, COUNT(*) AS activity_count
        FROM public.analytics_session AS s
        GROUP BY day
        ORDER BY activity_count DESC;
        """
        with self.session_dao.connection.cursor() as cursor:
            cursor.execute(query_daily)
            daily_activity = cursor.fetchall()

        return {
            "hourly": [{"hour": row[0], "count": row[1]} for row in hourly_activity],
            "daily": [{"day": row[0], "count": row[1]} for row in daily_activity],
        }


    def get_user_demographics(self):
        """Retourne les statistiques par genre."""
        query = """
        SELECT gender, COUNT(*) AS user_count
        FROM public.analytics_utilisateur
        GROUP BY gender;
        """
        with self.utilisateur_dao.connection.cursor() as cursor:
            cursor.execute(query)
            gender_stats = cursor.fetchall()

        return {
            "gender": {row[0]: row[1] for row in gender_stats},
        }


    def get_longest_sessions(self, top_n=5):
        """Retourne les sessions les plus longues."""
        query = """
        SELECT s."sessionID", u."firstName", u."lastName", s."ts", COUNT(c."songID_id") AS song_count
        FROM public.analytics_session AS s
        JOIN public.analytics_utilisateur AS u ON s."userID_id" = u."userID"
        JOIN public.analytics_contenir AS c ON s."sessionID" = c."sessionID_id"
        GROUP BY s."sessionID", u."firstName", u."lastName", s."ts"
        ORDER BY song_count DESC
        LIMIT %s;
        """
        # Utilisation du DAO pour la connexion et l'exécution de la requête
        with self.session_dao.connection.cursor() as cursor:
            cursor.execute(query, (top_n,))
            results = cursor.fetchall()

        return [
            {
                "sessionID": row[0],
                "user": f"{row[1]} {row[2]}",
                "timestamp": row[3],
                "song_count": row[4],
            }
            for row in results
        ]
