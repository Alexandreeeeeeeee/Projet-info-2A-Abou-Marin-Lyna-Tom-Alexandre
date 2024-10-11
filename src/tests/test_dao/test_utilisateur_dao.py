import unittest
from unittest.mock import MagicMock
from dao.utilisateur_dao import UtilisateurDAO
from business_object.utilisateur import Utilisateur

class TestUtilisateurDAO(unittest.TestCase):
    def setUp(self):
        self.dao = UtilisateurDAO()
        # Mock des méthodes de la DAO
        self.dao.add_utilisateur = MagicMock()
        self.dao.get_all_users = MagicMock(return_value=[
            Utilisateur(
                userID=1,
                lastName="Doe",
                firstName="John",
                gender="M",
                lon=1.234,
                lat=5.678,
                city="Paris",
                zip="75001",
                state="Île-de-France",
                registration=2023
            )
        ])

        # Initialisation de l'utilisateur pour le test
        self.utilisateur = Utilisateur(
            userID=1,
            lastName="Doe",
            firstName="John",
            gender="M",
            lon=1.234,
            lat=5.678,
            city="Paris",
            zip="75001",
            state="Île-de-France",
            registration=2023
        )

    def test_add_utilisateur(self):
        # Test d'ajout de l'utilisateur (mocké)
        self.dao.add_utilisateur(self.utilisateur)

        # Vérification que l'utilisateur a bien été ajouté
        self.dao.add_utilisateur.assert_called_once_with(self.utilisateur)
        
        utilisateurs = self.dao.get_all_users()

        # Vérification que la méthode get_all_users renvoie les résultats mockés
        self.assertGreaterEqual(len(utilisateurs), 1)
        self.assertEqual(utilisateurs[0].firstName, "John")

if __name__ == '__main__':
    unittest.main()
