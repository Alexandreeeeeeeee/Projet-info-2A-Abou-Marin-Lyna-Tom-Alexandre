import folium
from dao.utilisateur_dao import UtilisateurDAO
from dao.song_dao import SongDAO
from dao.session_dao import SessionDAO


class SpotifyService:
    def __init__(self):
        self.utilisateur_dao = UtilisateurDAO()
        self.song_dao = SongDAO()  # Si vous avez un DAO pour les chansons
        self.session_dao = SessionDAO()  # Si vous avez un DAO pour les sessions

    def create_user_map(self):
        utilisateurs = self.utilisateur_dao.get_all_users()  # Récupérer les utilisateurs
        # Créer la carte centrée sur les États-Unis
        m = folium.Map(location=[37.0902, -95.7129], zoom_start=4)  # Centre sur les États-Unis
        for utilisateur in utilisateurs:
            folium.Marker(
                location=[utilisateur.lat, utilisateur.lon],
                popup=f"{utilisateur.firstName} {utilisateur.lastName}",
            ).add_to(m)
        m.save("src/templates/map.html")  # Sauvegarder dans le dossier templates

    def get_user_locations(self):
        utilisateurs = self.utilisateur_dao.get_all_users()  # Récupérer les utilisateurs
        return [(utilisateur.city, utilisateur.state) for utilisateur in utilisateurs]

    def get_total_songs(self):
        # Récupérer toutes les chansons et compter
        return self.song_dao.count_songs()

    def get_total_users(self):
        # Récupérer tous les utilisateurs et compter
        return self.utilisateur_dao.count_users()

    def get_average_session_duration(self):
        # Calculer la durée moyenne des sessions
        return self.session_dao.calculate_average_session_duration()

    def get_top_artists(self):
        # Récupérer les artistes les plus populaires
        return self.song_dao.get_top_artists()
