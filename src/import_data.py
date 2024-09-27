import json
from dao.utilisateur_dao import UtilisateurDAO
from dao.contenir_dao import ContenirDAO
from dao.session_dao import SessionDAO
from dao.song_dao import SongDAO
from business_object.utilisateur import Utilisateur
from business_object.contenir import Contenir
from business_object.session import Session
from business_object.song import Song

def import_utilisateurs():
    utilisateur_dao = UtilisateurDAO()
    with open('src/donnee/utilisateurs.json', 'r') as f:
        utilisateurs = json.load(f)
        for data in utilisateurs:
            utilisateur = Utilisateur(
                userID=data['userID'],
                lastName=data['lastName'],
                firstName=data['firstName'],
                gender=data['gender'],
                registration=data['registration'],
                city=data['city'],
                zip=data['zip'],
                state=data['state'],
                lon=data['lon'],
                lat=data['lat']
            )
            utilisateur_dao.add_utilisateur(utilisateur)

def import_songs():
    song_dao = SongDAO()
    with open('src/donnee/songs.json', 'r') as file:
        songs = json.load(file)
        for song_data in songs:
            song = Song(
                songID=song_data['songID'],
                song=song_data['song'],
                artist=song_data['artist'],
                duration=song_data['duration']
            )
            try:
                song_dao.add_song(song)
            except Exception as e:
                print(f"Error inserting song: {e}")

def import_sessions():
    session_dao = SessionDAO()
    with open('src/donnee/sessions.json', 'r') as file:
        sessions = json.load(file)
        for session_data in sessions:
            session = Session(
                sessionID=session_data['sessionID'],
                ts=session_data['ts'],
                auth=session_data['auth'],
                level=session_data['level'],
                userAgent=session_data['userAgent'],
                item_in_session=session_data['item_in_session'],
                userID_id=session_data['userID_id']
            )
            try:
                session_dao.add_session(session)
            except Exception as e:
                print(f"Error inserting session: {e}")

def import_contenirs():
    contenir_dao = ContenirDAO()
    with open('src/donnee/contenirs.json', 'r') as file:
        contenirs = json.load(file)
        for contenir_data in contenirs:
            contenir = Contenir(
                id=contenir_data['id'],
                sessionID_id=contenir_data['sessionID_id'],
                songID_id=contenir_data['songID_id']  # Utilisation correcte de songID_id
            )
            try:
                contenir_dao.add_contenir(contenir)
            except Exception as e:
                print(f"Error inserting contenir: {e}")



if __name__ == "__main__":
    import_utilisateurs()
    import_songs()
    import_sessions()
    import_contenirs()
