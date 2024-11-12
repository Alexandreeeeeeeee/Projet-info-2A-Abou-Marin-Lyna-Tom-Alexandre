from dao.db_connection import get_connection
from business_object.song import Song
from datetime import datetime

class SongDAO:
    def __init__(self):
        self.connection = get_connection()

    def add_song(self, song):
        conn = get_connection()
        cursor = conn.cursor()
        query = """
        INSERT INTO analytics_song ("songID", "song", "artist", "duration")
        VALUES (%s, %s, %s, %s)
        ON CONFLICT ("song", "artist") DO NOTHING
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
    
    def get_top_artists_by_date(self):
        # Ouvrir une connexion à la base de données
        conn = get_connection()
        cursor = conn.cursor()
        
        query = """
        SELECT TO_CHAR(TO_TIMESTAMP(s."ts" / 1000), 'YYYY-MM-DD') AS session_date, 
            a."artist", 
            COUNT(a."songID") AS song_count
        FROM public.analytics_session AS s
        JOIN public.analytics_contenir AS c ON s."sessionID" = c."sessionID_id"
        JOIN public.analytics_song AS a ON c."songID_id" = a."songID"
        GROUP BY session_date, a."artist"
        ORDER BY session_date DESC, song_count DESC;
        """
        
        # Exécuter la requête
        cursor.execute(query)
        results = cursor.fetchall()

        # Fermer le curseur et la connexion
        cursor.close()
        conn.close()

        # Formater les résultats
        formatted_results = []
        for row in results:
            session_date_str = row[0]  # Assumant que la date est la première colonne
            artist = row[1]
            song_count = row[2]

            # Convertir la chaîne de date en datetime
            session_date = datetime.strptime(session_date_str, '%Y-%m-%d')
            formatted_results.append((session_date, artist, song_count))
        
        return formatted_results



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
