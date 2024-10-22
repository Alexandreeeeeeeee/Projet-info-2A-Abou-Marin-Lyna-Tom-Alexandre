import unittest
from unittest.mock import MagicMock
from dao.song_dao import SongDAO
from business_object.song import Song


class TestSongDAO(unittest.TestCase):
    def setUp(self):

        # Initialisation de l'utilisateur pour le test
        self.song = Song(
            songID=1,
            song="Little Lover's So Polite",
            artist="Silversun Pickups",
            duration=298.63138,
        )

        self.dao = SongDAO()

        # Mock des méthodes de la DAO
        self.dao.add_song = MagicMock()

    def test_add_songs(self):
        self.dao.add_song(self.song)

        self.dao.add_song.assert_called_once_with(self.song)

        songs = self.dao.get_all_song()

        # THEN
        self.assertGreaterEqual(len(songs), 1)
        self.assertEqual(songs[0].song, "Little Lover's So Polite")

    def test_get_song_by_id_success(self):
        id_song = 150

        song = self.dao.get_song_by_id(id_song)

        self.assertEqual(id_song, song.songID)

    def test_get_song_by_id_fail(self):

        id_song = 1111111111111

        song = self.dao.get_song_by_id(id_song)

        assert song is None

    def test_count_songs(self):
        nb_songs = 2646
        res = self.dao.count_songs()

        self.assertEqual(res, nb_songs)


if __name__ == "__main__":
    unittest.main()
