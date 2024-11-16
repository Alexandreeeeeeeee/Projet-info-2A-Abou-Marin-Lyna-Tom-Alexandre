from dotenv import load_dotenv
import json
import os
from confluent_kafka import Consumer
from dao.db_connection import get_connection  # Assurez-vous que le chemin est correct pour votre projet

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()


def read_config():
    """
    Lit la configuration à partir du fichier client.properties.
    
    :return: Dictionnaire contenant les paramètres de configuration
    """
    config = {}
    with open("client.properties", encoding="utf-8") as fh:  # Ajout de l'encodage explicite
        for line in fh:
            line = line.strip()
            if len(line) != 0 and line[0] != "#":
                parameter, value = line.strip().split("=", 1)
                config[parameter] = value.strip()
    return config


def insert_utilisateur(conn, user_data):
    """
    Insère les données d'un utilisateur dans la base de données.

    :param conn: La connexion à la base de données
    :param user_data: Dictionnaire contenant les données de l'utilisateur
    """
    cursor = conn.cursor()
    query = """
        INSERT INTO public.analytics_utilisateur ("userID", "lastName", "firstName", gender, lon, lat, city, zip, state, registration)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT ("userID") DO NOTHING;
    """
    cursor.execute(query, (
        user_data["userID"],
        user_data["lastName"],
        user_data["firstName"],
        user_data["gender"],
        user_data["lon"],
        user_data["lat"],
        user_data["city"],
        user_data["zip"],
        user_data["state"],
        user_data["registration"]
    ))
    conn.commit()
    cursor.close()


def insert_song(conn, song_data):
    """
    Insère les données d'une chanson dans la base de données.

    :param conn: La connexion à la base de données
    :param song_data: Dictionnaire contenant les données de la chanson
    """
    cursor = conn.cursor()
    query = """
        INSERT INTO public.analytics_song ("song", "artist", "duration")
        VALUES (%s, %s, %s)
        ON CONFLICT ("song", "artist") DO NOTHING;
    """
    cursor.execute(query, (song_data["song"], song_data["artist"], song_data["duration"]))
    conn.commit()
    cursor.close()


def insert_session(conn, session_data):
    """
    Insère les données d'une session dans la base de données et retourne l'ID de la session insérée.

    :param conn: La connexion à la base de données
    :param session_data: Dictionnaire contenant les données de la session
    :return: L'ID de la session insérée
    """
    cursor = conn.cursor()
    query = """
        INSERT INTO public.analytics_session ("ts", "auth", "level", "userAgent", "item_in_session", "userID_id")
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING "sessionID";
    """
    cursor.execute(query, (
        session_data["ts"],
        session_data["auth"],
        session_data["level"],
        session_data["userAgent"],
        session_data["itemInSession"],
        session_data["userID_id"]
    ))
    session_id = cursor.fetchone()[0]  # Récupérer l'ID de la session insérée
    conn.commit()
    cursor.close()
    return session_id


def insert_contenir(conn, session_id, song_id):
    """
    Insère l'association session/chanson dans la table 'contenir'.

    :param conn: La connexion à la base de données
    :param session_id: L'ID de la session
    :param song_id: L'ID de la chanson
    """
    cursor = conn.cursor()
    query = """
        INSERT INTO public.analytics_contenir ("sessionID_id", "songID_id")
        VALUES (%s, %s)
        ON CONFLICT ("sessionID_id", "songID_id") DO NOTHING;
    """
    cursor.execute(query, (session_id, song_id))
    conn.commit()
    cursor.close()


def consume(topic, config):
    """
    Consomme les messages d'un topic Kafka et insère les données dans la base de données.

    :param topic: Le topic Kafka à consommer
    :param config: La configuration du consommateur Kafka
    """
    config["group.id"] = "groupe15"
    config["auto.offset.reset"] = "earliest"
    config["enable.auto.commit"] = True

    # Crée une instance de consommateur
    consumer = Consumer(config)
    # S'abonne au topic spécifié
    consumer.subscribe([topic])

    # Connexion à la base de données
    conn = get_connection()

    try:
        while True:
            # Le consommateur interroge le topic et affiche les messages entrants
            msg = consumer.poll(1.0)
            if msg is not None and msg.error() is None:
                value = msg.value().decode("utf-8")
                value = json.loads(value)  # Charge le message dans un dictionnaire
                print(value)
                # Récupérer les données
                user_data = {
                    "userID": value["userId"],
                    "lastName": value["lastName"],
                    "firstName": value["firstName"],
                    "gender": value["gender"],
                    "lon": value["lon"],
                    "lat": value["lat"],
                    "city": value["city"],
                    "zip": value["zip"],
                    "state": value["state"],
                    "registration": value["registration"]
                }

                song_data = {
                    "song": value["song"],
                    "artist": value["artist"],
                    "duration": value["duration"]
                }

                session_data = {
                    "ts": value["ts"],
                    "auth": value["auth"],
                    "level": value["level"],
                    "userAgent": value["userAgent"],
                    "itemInSession": value["itemInSession"],
                    "userID_id": value["userId"]
                }

                # Insertion dans les tables
                insert_utilisateur(conn, user_data)
                insert_song(conn, song_data)
                session_id = insert_session(conn, session_data)

                # Insertion dans la table contenir (session, chanson)
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT "songID" FROM public.analytics_song WHERE "song" = %s AND "artist" = %s;
                """, (song_data["song"], song_data["artist"]))
                song_id = cursor.fetchone()[0]  # Récupérer l'ID de la chanson
                insert_contenir(conn, session_id, song_id)

    except KeyboardInterrupt:
        pass
    finally:
        # Fermer la connexion du consommateur et de la base de données
        consumer.close()
        conn.close()


def main():
    """
    Fonction principale qui lit la configuration et lance la consommation des messages Kafka.
    """
    config = read_config()
    topic = "listen_events"
    consume(topic, config)


if __name__ == "__main__":
    main()
