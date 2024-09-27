import unittest
from service.spotify_service import SpotifyService
from dao.utilisateur_dao import UtilisateurDAO
from business_object.utilisateur import Utilisateur
import os

class TestSpotifyService(unittest.TestCase):
    def setUp(self):
        self.service = SpotifyService()
        
        # Mock de l'utilisateur
        self.mock_utilisateur_dao = UtilisateurDAO()
        self.mock_utilisateur_dao.get_all_users = lambda: [
            Utilisateur(1, "Doe", "John", "M", 1.234, 5.678, "Paris", "75001", "Île-de-France", 2023),
            Utilisateur(2, "Smith", "Jane", "F", 2.345, 6.789, "Lyon", "69001", "Auvergne-Rhône-Alpes", 2023)
        ]
        self.service.utilisateur_dao = self.mock_utilisateur_dao

    def test_get_user_locations(self):
        locations = self.service.get_user_locations()
        self.assertEqual(len(locations), 2)
        self.assertIn(("Paris", "Île-de-France"), locations)
        self.assertIn(("Lyon", "Auvergne-Rhône-Alpes"), locations)

    def test_create_user_map(self):
        self.service.create_user_map()
        # Vérifie si le fichier map.html a été créé
        self.assertTrue(os.path.exists('src/templates/map.html'))
        # Optionnel : Vous pouvez également vérifier le contenu du fichier
        with open('src/templates/map.html', 'r') as file:
            content = file.read()
            self.assertIn("Map", content)  # Vérifie que le contenu contient "Map"

if __name__ == '__main__':
    unittest.main()
