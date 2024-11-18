import unittest
from unittest.mock import MagicMock, patch
from src.service.spotify_service import SpotifyService

class TestSpotifyService(unittest.TestCase):
    
    def setUp(self):
        # Initialisation du service avec des DAO mockés
        self.spotify_service = SpotifyService()

        # Mock de la classe UtilisateurDAO
        self.utilisateur_dao_mock = MagicMock()
        self.song_dao_mock = MagicMock()
        self.session_dao_mock = MagicMock()
        self.contenir_dao_mock = MagicMock()

        # Assignation des mocks aux attributs du service
        self.spotify_service.utilisateur_dao = self.utilisateur_dao_mock
        self.spotify_service.song_dao = self.song_dao_mock
        self.spotify_service.session_dao = self.session_dao_mock
        self.spotify_service.contenir_dao = self.contenir_dao_mock

    @patch('dao.utilisateur_dao.UtilisateurDAO.connection')
    def test_get_total_songs(self, mock_connection):
        # Mock de la méthode `connection` pour retourner un curseur mocké
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = [100]  # Valeur simulée pour le total des chansons

        total_songs = self.spotify_service.get_total_songs()
        self.assertEqual(total_songs, 100)

    @patch('dao.utilisateur_dao.UtilisateurDAO.connection')
    def test_get_total_users(self, mock_connection):
        # Mock de la méthode `connection` pour retourner un curseur mocké
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = [200]  # Valeur simulée pour le total des utilisateurs

        total_users = self.spotify_service.get_total_users()
        self.assertEqual(total_users, 200)

    @patch('dao.utilisateur_dao.UtilisateurDAO.connection')
    def test_get_average_session_duration(self, mock_connection):
        # Mock de la méthode `connection` pour retourner un curseur mocké
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = [1500]  # Valeur simulée pour la durée moyenne de session

        avg_duration = self.spotify_service.get_average_session_duration()
        self.assertEqual(avg_duration, 1500)

    @patch('dao.utilisateur_dao.UtilisateurDAO.connection')
    def test_get_top_artists_by_date(self, mock_connection):
        # Mock des résultats de la requête SQL
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            ('2024-11-18', 'Artist 1', 10),
            ('2024-11-18', 'Artist 2', 5)
        ]
        
        top_artists = self.spotify_service.get_top_artists_by_date()
        self.assertEqual(top_artists, [
            (datetime(2024, 11, 18), 'Artist 1', 10),
            (datetime(2024, 11, 18), 'Artist 2', 5)
        ])

    @patch('dao.utilisateur_dao.UtilisateurDAO.connection')
    def test_get_average_item_in_session_by_level(self, mock_connection):
        # Mock des résultats de la requête SQL
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            ('premium', 25),
            ('basic', 15)
        ]
        
        avg_items_by_level = self.spotify_service.get_average_item_in_session_by_level()
        self.assertEqual(avg_items_by_level, {'premium': 25, 'basic': 15})

    @patch('dao.utilisateur_dao.UtilisateurDAO.connection')
    def test_get_user_coordinates(self, mock_connection):
        # Mock des résultats de la requête SQL
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            (48.8566, 2.3522),
            (34.0522, -118.2437)
        ]
        
        coordinates = self.spotify_service.get_user_coordinates(debug=True)
        self.assertEqual(coordinates, [(48.8566, 2.3522), (34.0522, -118.2437)])

    @patch('dao.utilisateur_dao.UtilisateurDAO.connection')
    def test_get_most_active_users(self, mock_connection):
        # Mock des résultats de la requête SQL
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            (1, 'John', 'Doe', 5),
            (2, 'Jane', 'Doe', 3)
        ]
        
        most_active_users = self.spotify_service.get_most_active_users(top_n=2)
        self.assertEqual(most_active_users, [
            {"userID": 1, "name": "John Doe", "sessions": 5},
            {"userID": 2, "name": "Jane Doe", "sessions": 3}
        ])

    @patch('dao.utilisateur_dao.UtilisateurDAO.connection')
    def test_get_activity_peak_times(self, mock_connection):
        # Mock des résultats de la requête SQL pour l'heure et le jour
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.fetchall.side_effect = [
            [('12', 100), ('14', 80)],  # Hourly query
            [('Mon', 200), ('Tue', 150)]  # Daily query
        ]
        
        peak_times = self.spotify_service.get_activity_peak_times()
        self.assertEqual(peak_times, {
            "hourly": [{"hour": '12', "count": 100}, {"hour": '14', "count": 80}],
            "daily": [{"day": 'Mon', "count": 200}, {"day": 'Tue', "count": 150}]
        })

    @patch('dao.utilisateur_dao.UtilisateurDAO.connection')
    def test_get_user_demographics(self, mock_connection):
        # Mock des résultats de la requête SQL
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            ('male', 100),
            ('female', 120)
        ]
        
        demographics = self.spotify_service.get_user_demographics()
        self.assertEqual(demographics, {
            "gender": {'male': 100, 'female': 120}
        })

    @patch('dao.utilisateur_dao.UtilisateurDAO.connection')
    def test_get_longest_sessions(self, mock_connection):
        # Mock des résultats de la requête SQL
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            (1, 'John', 'Doe', 1600, 10),
            (2, 'Jane', 'Doe', 1500, 8)
        ]
        
        longest_sessions = self.spotify_service.get_longest_sessions(top_n=2)
        self.assertEqual(longest_sessions, [
            {"sessionID": 1, "user": "John Doe", "timestamp": 1600, "song_count": 10},
            {"sessionID": 2, "user": "Jane Doe", "timestamp": 1500, "song_count": 8}
        ])

if __name__ == '__main__':
    unittest.main()
