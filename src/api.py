from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from dao.db_connection import get_connection
from business_object.song import Song  # Assurez-vous que le chemin est correct

app = FastAPI()

# DAO pour interagir avec la base de données
class SongDAO:
    def __init__(self):
        self.connection = get_connection()

    def add_song(self, song: Song):
        conn = self.connection
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
            raise HTTPException(status_code=500, detail="Error inserting song")
        finally:
            cursor.close()

    def get_all_songs(self) -> List[Song]:
        conn = self.connection
        cursor = conn.cursor()
        query = 'SELECT * FROM analytics_song'
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return [Song(songID=row[0], song=row[1], artist=row[2], duration=row[3]) for row in result]

# Instance de SongDAO
song_dao = SongDAO()

@app.get("/songs", response_model=List[Song])
async def get_songs():
    return song_dao.get_all_songs()  # Retourne la liste des chansons

# Endpoint pour ajouter une nouvelle chanson
@app.post("/songs", response_model=Song)
async def add_song(song: Song):
    song_dao.add_song(song)  # Utilise le DAO pour ajouter la chanson
    return song
