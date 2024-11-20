import unittest
from unittest.mock import patch, MagicMock
from src.service.spotify_service import SpotifyService
from datetime import datetime  

class TestSpotifyService(unittest.TestCase):

    @patch('src.service.spotify_service.UtilisateurDAO')
    @patch('src.service.spotify_service.SongDAO')
    @patch('src.service.spotify_service.SessionDAO')
    @patch('src.service.spotify_service.ContenirDAO')
    def setUp(self, MockContenirDAO, MockSessionDAO, MockSongDAO, MockUtilisateurDAO):
        self.mock_utilisateur_dao = MockUtilisateurDAO.return_value
        self.mock_song_dao = MockSongDAO.return_value
        self.mock_session_dao = MockSessionDAO.return_value
        self.mock_contenir_dao = MockContenirDAO.return_value
        self.service = SpotifyService()

    def test_get_total_songs(self):
        mock_cursor = MagicMock()
        self.mock_song_dao.connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchone.return_value = [3755]

        total_songs = self.service.get_total_songs()
        self.assertEqual(total_songs, 3755)
        mock_cursor.execute.assert_called_once_with("SELECT COUNT(*) FROM analytics_song")

    def test_get_total_users(self):
        mock_cursor = MagicMock()
        self.mock_utilisateur_dao.connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchone.return_value = [939]

        total_users = self.service.get_total_users()
        self.assertEqual(total_users, 939)
        mock_cursor.execute.assert_called_once_with("SELECT COUNT(*) FROM analytics_utilisateur")

    def test_get_average_session_duration(self):
        mock_cursor = MagicMock()
        self.mock_session_dao.connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchone.return_value = [1731714514541.5612]

        average_duration = self.service.get_average_session_duration()
        self.assertEqual(average_duration, 1731714514541.5612)
        mock_cursor.execute.assert_called_once_with("SELECT AVG(ts) FROM analytics_session")

    def test_get_top_artists_by_date(self):
        mock_cursor = MagicMock()
        self.mock_session_dao.connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            ('2024-11-16', 'Coldplay', 16),
            ('2024-11-15', 'Coldplay', 28)
        ]

        top_artists = self.service.get_top_artists_by_date()
        expected_results = [
            (datetime.strptime('2024-11-16', '%Y-%m-%d'), 'Coldplay', 16),
            (datetime.strptime('2024-11-15', '%Y-%m-%d'), 'Coldplay', 28)
        ]
        self.assertEqual(top_artists, expected_results)

    def test_get_average_item_in_session_by_level(self):
        mock_cursor = MagicMock()
        self.mock_session_dao.connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            ('free', 31.8),
            ('paid', 139.6)
        ]

        average_items = self.service.get_average_item_in_session_by_level()
        expected_results = {'free': 31.8, 'paid': 139.6}
        self.assertEqual(average_items, expected_results)

if __name__ == '__main__':
    unittest.main()
