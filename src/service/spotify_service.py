"""Module providing Spotify analytics services."""

from datetime import datetime
import folium
from dao.utilisateur_dao import UtilisateurDAO
from dao.song_dao import SongDAO
from dao.session_dao import SessionDAO
from dao.db_connection import get_connection

class SpotifyService:
    """Service pour gérer les opérations liées à Spotify Analytics."""

    def __init__(self):
        """Initialise les DAO pour les utilisateurs, les chansons, et les sessions."""
        self.utilisateur_dao = UtilisateurDAO()
        self.song_dao = SongDAO()
        self.session_dao = SessionDAO()

    def create_user_map(self):
        """Crée une carte avec les utilisateurs marqués à leurs coordonnées."""
        utilisateurs = self.utilisateur_dao.get_all_users()
        m = folium.Map(location=[37.0902, -95.7129], zoom_start=4)

        for utilisateur in utilisateurs:
            folium.Marker(
                location=[utilisateur.lat, utilisateur.lon],
                popup=f"{utilisateur.firstName} {utilisateur.lastName}",
            ).add_to(m)

        m.save("src/templates/map.html")

    def get_user_locations(self):
        """Retourne la liste des villes et états des utilisateurs."""
        utilisateurs = self.utilisateur_dao.get_all_users()
        return [(utilisateur.city, utilisateur.state) for utilisateur in utilisateurs]

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

    def get_top_artists(self):
        """Retourne les artistes les plus populaires."""
        return self.song_dao.get_top_artists()

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
        results = []
        with get_connection() as conn, conn.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()

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
        with get_connection() as conn, conn.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
        
        return {row[0]: row[1] for row in results}

    def get_user_coordinates(self, debug=False):
        """Retourne les coordonnées des utilisateurs.

        Args:
            debug (bool): Si vrai, imprime les coordonnées pour déboguer.
        """
        query = "SELECT lat, lon FROM analytics_utilisateur WHERE lat IS NOT NULL AND lon IS NOT NULL"
        
        with get_connection() as conn, conn.cursor() as cursor:
            cursor.execute(query)
            coordinates = cursor.fetchall()
        
        if debug:
            print("Coordonnées des utilisateurs :", coordinates)

        return coordinates
