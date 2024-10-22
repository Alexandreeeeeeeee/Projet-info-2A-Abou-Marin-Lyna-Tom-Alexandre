import unittest
from unittest.mock import MagicMock
from dao.session_dao import SessionDAO
from business_object.session import Session


class TestSessionDAO(unittest.TestCase):
    def setUp(self):
        self.dao = SessionDAO()
        self.dao.add_session = MagicMock()
        self.dao.get_all_sessions = MagicMock(
            return_value=[
                Session(
                    sessionID=23358,
                    ts=1726236626000,
                    auth="Logged In",
                    level="paid",
                    userAgent='"Mozilla\/5.0 (Windows NT 6.1; WOW64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/37.0.2062.102 Safari\/537.36"',
                    item_in_session=6,
                    userID_id=760,
                )
            ]
        )
        self.dao.delete_all_sessions = MagicMock()

        self.session = Session(
            sessionID=23358,
            ts=1726236626000,
            auth="Logged In",
            level="paid",
            userAgent='"Mozilla\/5.0 (Windows NT 6.1; WOW64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/37.0.2062.102 Safari\/537.36"',
            item_in_session=6,
            userID_id=760,
        )

    def test_add_session(self):
        self.dao.add_session(self.session)
        self.dao.add_session.assert_called_once_with(self.session)

    def test_get_all_sessions(self):
        sessions = self.dao.get_all_sessions()
        assert len(sessions) == 1
        assert sessions[0].item_in_session == 6

    def test_delete_all_sessions(self):
        self.dao.delete_all_sessions()
        self.dao.delete_all_sessions.assert_called_once_with(None)

    def test_calculate_average_session_duration(self):
        average = self.dao.calculate_average_session_duration()
        assert average == 1726236626000

    def test_calculate_average_sessions_duration_exception(self):
        self.dao.delete_all_sessions()
        average = self.dao.calculate_average_session_duration()
        assert average == 0


if __name__ == "__main__":
    unittest.main()
