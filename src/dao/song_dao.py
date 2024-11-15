import psycopg2
from dao.db_connection import get_connection
from business_object.song import Song


class SongDAO:
    """Classe pour gérer les opérations CRUD sur les chansons dans la base de données."""

    def __init__(self):
        """Initialise une nouvelle instance de la classe SongDAO."""
        self.connection = get_connection()

    def add_song(self, song):
        """Ajoute une chanson à la base de données ou ignore si la chanson avec le même nom et artiste existe déjà."""
        conn = get_connection()
        cursor = conn.cursor()
        query = """
        INSERT INTO analytics_song ("songID", "song", "artist", "duration")
        VALUES (%s, %s, %s, %s)
        ON CONFLICT ("song", "artist") DO NOTHING
        """
        try:
            cursor.execute(query, (song.song_id, song.song, song.artist, song.duration))
            conn.commit()
        except psycopg2.Error as e:
            print(f"Erreur lors de l'insertion de la chanson : {e}")
            conn.rollback()  # Annule la transaction en cas d'erreur
        finally:
            cursor.close()
            conn.close()

    def get_song_by_id(self, song_id):
        """Récupère une chanson à partir de son ID."""
        conn = get_connection()
        cursor = conn.cursor()
        query = 'SELECT * FROM analytics_song WHERE "songID" = %s'
        cursor.execute(query, (song_id,))
        raw = cursor.fetchone()
        song = None
        if raw:
            song = Song(*raw)
        cursor.close()
        conn.close()
        return song

    def get_all_songs(self):
        """Récupère toutes les chansons de la base de données."""
        conn = get_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM analytics_song"
        cursor.execute(query)
        rows = cursor.fetchall()
        songs = []
        if rows:
            songs = [Song(*row) for row in rows]
        cursor.close()
        conn.close()
        return songs
