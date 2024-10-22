from dao.db_connection import get_connection
from business_object.song import Song


class SongDAO:
    def __init__(self):
        self.connection = get_connection()

    def add_song(self, song):
        conn = get_connection()
        cursor = conn.cursor()
        query = """
        INSERT INTO analytics_song ("songID", "song", "artist", "duration")
        VALUES (%s, %s, %s, %s)
        ON CONFLICT ("songID") DO NOTHING
    """
        try:
            cursor.execute(query, (song.songID, song.song, song.artist, song.duration))
            conn.commit()
        except Exception as e:
            print(f"Error inserting song: {e}")
        finally:
            cursor.close()
            conn.close()

    def get_song_by_id(self, songID):
        conn = get_connection()
        cursor = conn.cursor()
        query = 'SELECT * FROM analytics_song WHERE "songID" = %s'
        cursor.execute(query, (songID,))
        raw = cursor.fetchone()
        song = None
        if raw:
            song = Song(*raw)
        cursor.close()
        conn.close()
        return song

    def count_songs(self):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM analytics_song")
            return cursor.fetchone()[0]

    def get_top_artists(self):
        with self.connection.cursor() as cursor:
            cursor.execute(
                "SELECT artist, COUNT(*) as count FROM analytics_song GROUP BY artist ORDER BY count DESC LIMIT 5"
            )
            return cursor.fetchall()

    def get_all_song(self):
        conn = get_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM analytics_song"
        cursor.execute(query)
        rows = cursor.fetchall()
        if rows:
            songs = [Song(*row) for row in rows]
        cursor.close()
        conn.close()
        return songs
