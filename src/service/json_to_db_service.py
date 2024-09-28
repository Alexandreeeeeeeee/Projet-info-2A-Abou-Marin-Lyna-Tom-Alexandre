import json
from dao.utilisateur_dao import UtilisateurDAO
from dao.song_dao import SongDAO
from dao.session_dao import SessionDAO
from business_object.utilisateur import Utilisateur
from business_object.song import Song
from business_object.session import Session
from business_object.contenir import Contenir

def import_json_to_db(json_file_path):
    # Lecture du fichier JSON
    with open(json_file_path, 'r') as file:
        data = [json.loads(line) for line in file]

    # Initialisation des DAO
    utilisateur_dao = UtilisateurDAO()
    song_dao = SongDAO()
    session_dao = SessionDAO()

    # Parcourir les données JSON
    for entry in data:
        # Création d'une instance Utilisateur
        utilisateur = Utilisateur(
            userID=entry['userId'],
            lastName=entry['lastName'],
            firstName=entry['firstName'],
            gender=entry['gender'],
            lon=entry['lon'],
            lat=entry['lat'],
            city=entry['city'],
            zip_code=entry['zip'],
            state=entry['state'],
            registration=entry['registration']
        )

        # Insertion ou mise à jour de l'utilisateur dans la base de données
        utilisateur_dao.save_or_update(utilisateur)

        # Création d'une instance Song
        song = Song(
            songID=None,  # Assigne un ID unique si nécessaire
            song=entry['song'],
            artist=entry['artist'],
            duration=entry['duration']
        )

        # Insertion ou mise à jour de la chanson dans la base de données
        song_dao.save_or_update(song)

        # Création d'une instance Session
        session = Session(
            sessionID=entry['sessionId'],
            ts=entry['ts'],
            auth=entry['auth'],
            level=entry['level'],
            userAgent=entry['userAgent'],
            item_in_session=entry['itemInSession'],
            user=utilisateur
        )

        # Insertion ou mise à jour de la session dans la base de données
        session_dao.save_or_update(session)

        # Création d'une instance Contenir pour lier la session et la chanson
        contenir = Contenir(session=session, song=song)

        # Insère le lien session-song dans la base de données via ContenirDAO
        # contenu_dao.save_or_update(contenir)  # Crée une DAO pour `Contenir`
