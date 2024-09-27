# business_object/song.py

class Song:
    def __init__(self, songID, song, artist, duration):
        self.songID = songID
        self.song = song
        self.artist = artist
        self.duration = duration

# Ajoutez la classe SongDAO ici


class SongDAO:
    def __init__(self):
        # Initialisez votre connexion à la base de données ici
        pass

    def get_song_by_id(self, songID):
        # Implémentez la logique pour récupérer une chanson par son ID
        pass
