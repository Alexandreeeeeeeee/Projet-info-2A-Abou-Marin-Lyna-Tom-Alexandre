import unittest
from unittest.mock import MagicMock
from dao.utilisateur_dao import UtilisateurDAO
from business_object.utilisateur import Utilisateur


class TestUtilisateurDAO(unittest.TestCase):
    def setUp(self):

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
            registration=2023,
        )

        self.dao = UtilisateurDAO()

        # Mock des méthodes de la DAO
        self.dao.add_utilisateur = MagicMock()
        self.dao.delete_all_users = MagicMock()

        self.dao.get_all_users = MagicMock(
            return_value=[
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
                    registration=2023,
                )
            ]
        )

    def test_add_users(self):
        self.dao.add_utilisateur(self.utilisateur)

        self.dao.add_utilisateur.assert_called_once_with(self.utilisateur)

        utilisateurs = self.dao.get_all_users()

        # THEN
        self.assertGreaterEqual(len(utilisateurs), 1)
        self.assertEqual(utilisateurs[0].firstName, "John")

    def test_delete_all_users(self):
        pass  # attention utiliser le mock sinon pb dans bdd

    def test_get_user_by_id_success(self):
        id_user = 9551

        user = self.dao.get_user_by_id(id_user)

        self.assertEqual(id_user, user.userID)

    def test_get_user_by_id_fail(self):

        id_user = 1111111111111

        user = self.dao.get_user_by_id(id_user)

        assert user is None

    def test_count_users(self):
        nb_users = 587
        res = self.dao.count_users()

        self.assertEqual(res, nb_users)  # erreur


if __name__ == "__main__":
    unittest.main()
