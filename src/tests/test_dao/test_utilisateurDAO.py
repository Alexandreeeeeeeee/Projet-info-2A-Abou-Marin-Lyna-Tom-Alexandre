import unittest
from unittest.mock import patch, MagicMock
from dao.utilisateur_dao import UtilisateurDAO
from business_object.utilisateur import Utilisateur


class TestUtilisateurDAO(unittest.TestCase):

    @patch("dao.utilisateur_dao.get_connection")
    def test_get_user_by_id(self, mock_get_connection):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()

        mock_cursor.fetchone.return_value = (
            1,
            "Catoire",
            "Tom",
            "M",
            1725822274000,
            "Paris",
            "75001",
            "",
            1.234,
            5.678,
        )

        mock_conn.cursor.return_value = mock_cursor
        mock_get_connection.return_value = mock_conn

        utilisateur_dao = UtilisateurDAO()
        result = utilisateur_dao.get_user_by_id(1)

        self.assertIsNotNone(result)
        self.assertEqual(result.user_id, 1)
        self.assertEqual(result.first_name, "Tom")

        mock_cursor.execute.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch("dao.utilisateur_dao.get_connection")
    def test_get_all_users(self, mock_get_connection):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()

        mock_cursor.fetchall.return_value = [
            (1, "Catoire", "Tom", "M", 1725822274000, "Paris", "75001", "", 1.234, 5.678),
            (2, "Boucher", "Alex", "M", 1725822274001, "Lyon", "69001", "", 2.345, 6.789),
        ]

        mock_conn.cursor.return_value = mock_cursor
        mock_get_connection.return_value = mock_conn

        utilisateur_dao = UtilisateurDAO()
        result = utilisateur_dao.get_all_users()

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].user_id, 1)
        self.assertEqual(result[0].first_name, "Tom")
        self.assertEqual(result[1].first_name, "Alex")

        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()


if __name__ == "__main__":
    unittest.main()
