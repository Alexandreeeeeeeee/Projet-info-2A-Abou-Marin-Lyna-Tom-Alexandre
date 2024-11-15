class Song:
    """Classe pour représenter une chanson."""

    def __init__(self, song_id, song, artist, duration):
        """
        Initialise une nouvelle instance de la classe Song.

        :param song_id: ID de la chanson.
        :param song: Nom de la chanson.
        :param artist: Nom de l'artiste.
        :param duration: Durée de la chanson en secondes.
        """
        self.song_id = song_id
        self.song = song
        self.artist = artist
        self.duration = duration

    def __repr__(self):
        """Retourne une représentation en chaîne de caractères de la chanson."""
        return f"Song(song_id={self.song_id}, song='{self.song}', artist='{self.artist}', duration={self.duration})"
