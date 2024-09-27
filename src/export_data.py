import json

def convert_and_export():
    utilisateurs = []
    contenirs = []
    sessions = []
    songs = []

    song_id_counter = 1
    session_id_counter = 1
    contenir_id_counter = 1

    # Lire le fichier flux.json
    with open('src/donnee/flux.json', 'r') as f:
        for line in f:
            data = json.loads(line.strip())
            
            # Remplissage de la table utilisateurs
            utilisateurs.append({
                "userID": data["userId"],
                "lastName": data["lastName"],
                "firstName": data["firstName"],
                "gender": data["gender"],
                "registration": data["registration"],
                "city": data["city"],
                "zip": data["zip"],
                "state": data["state"],
                "lon": data["lon"],
                "lat": data["lat"]
            })
            
            # Remplissage de la table songs avec auto-incrémentation du songID
            songs.append({
                "songID": song_id_counter,
                "song": data["song"],
                "artist": data["artist"],
                "duration": data["duration"]
            })
            song_id_counter += 1

            # Remplissage de la table sessions avec auto-incrémentation du sessionID
            sessions.append({
                "sessionID": session_id_counter,
                "ts": data["ts"],
                "auth": data["auth"],
                "level": data["level"],
                "userAgent": data["userAgent"],
                "item_in_session": data["itemInSession"],
                "userID_id": data["userId"]
            })
            session_id_counter += 1

            # Remplissage de la table contenir avec auto-incrémentation de l'id
            contenirs.append({
                "id": contenir_id_counter,
                "sessionID_id": session_id_counter - 1,  # sessionID correspond à la dernière session
                "songID_id": song_id_counter - 1  # songID correspond à la dernière chanson
            })
            contenir_id_counter += 1

    # Exporter en fichiers JSON
    with open('src/donnee/utilisateurs.json', 'w') as f:
        json.dump(utilisateurs, f, indent=4)

    with open('src/donnee/contenirs.json', 'w') as f:
        json.dump(contenirs, f, indent=4)

    with open('src/donnee/sessions.json', 'w') as f:
        json.dump(sessions, f, indent=4)

    with open('src/donnee/songs.json', 'w') as f:
        json.dump(songs, f, indent=4)

if __name__ == "__main__":
    convert_and_export()
