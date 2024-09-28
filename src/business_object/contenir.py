# business_object/contenir.py
from business_object.session import SessionDAO
from business_object.song import SongDAO

class Contenir:
    def __init__(self, id, sessionID_id, songID_id):
        self.id = id
        self.sessionID_id = sessionID_id
        self.songID_id = songID_id

    def get_session(self):
        session_dao = SessionDAO()
        return session_dao.get_user_by_id(self.sessionID_id)

    def get_song(self):
        song_dao = SongDAO()
        return song_dao.get_song_by_id(self.songID_id)

    def __str__(self):
        session = self.get_session()
        song = self.get_song()
        return f"Session ID {self.sessionID_id} contains song ID {self.songID_id}: {song.title} by {song.artist}"  # Ajustez selon les attributs de votre classe Song
