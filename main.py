import openai
import psycopg2
from dotenv import load_dotenv
import os

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Obtenir la clé API OpenAI depuis les variables d'environnement
openai.api_key = os.getenv("OPENAI_API_KEY")


# Connexion à la base de données PostgreSQL
def connect_to_db():
    try:
        connection = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        return connection
    except Exception as e:
        print(f"Erreur lors de la connexion à la base de données : {e}")
        return None


# Fonction pour interpréter la question et générer une requête SQL
def interpret_question(question):
    # Instructions spécifiques sur la base de données
    table_info = """
    La base de données contient les tables suivantes :
    - Table 'analytics_utilisateur' : contient les colonnes "userID", "lastName", "firstName", "gender", "lon", "lat", "city", "zip", "state", "registration".
    - Table 'analytics_song' : contient les colonnes "songID", "song", "artist", "duration".
    - Table 'analytics_session' : contient les colonnes "sessionID", "ts", "auth", "level", "userAgent", "item_in_session", "userID_id" (clé étrangère vers analytics_utilisateur).
    - Table 'analytics_contenir' : contient les colonnes "id", "sessionID_id" (clé étrangère vers analytics_session), "songID_id" (clé étrangère vers analytics_song).
    
    exemple de jointure :
    SELECT DISTINCT u."userID", u."firstName", u."lastName"
    FROM public.analytics_utilisateur u
    JOIN public.analytics_session s ON u."userID" = s."userID_id"
    JOIN public.analytics_contenir c ON s."sessionID" = c."sessionID_id"
    JOIN public.analytics_song song ON c."songID_id" = song."songID"
    WHERE song.artist = 'Coldplay';

    exemple pour nombre totale des femmes :
            SELECT COUNT(*)
            FROM public.analytics_utilisateur
            WHERE gender = 'F';

    exemple pour nombre totale des hommes :
             SELECT COUNT(*) 
            FROM public.analytics_utilisateur
            WHERE gender = 'M';


    Relations :
    - Un utilisateur (analytics_utilisateur) peut participer à plusieurs sessions (analytics_session).
    - Une session peut contenir plusieurs chansons (analytics_contenir), et chaque chanson est liée à un artiste dans la table analytics_song.
    
    execute le requettes sql tu es connectee avec la base de donnes retrourne direcement le resultats et sans utiliser de formatage ou de balises Markdown. Ne donne aucune explication.
    et commentes le resultats en quelques lignes

    N'inclut aucun formatage, balise Markdown ou d'explication et commentes le resultats en quelques lignes.
    avec toutes ces information fais effort de bien executer les code sql.
    """

    # Enrichir le prompt avec les instructions et la question de l'utilisateur
    prompt = f"{table_info}\nGénère une requête SQL appropriée pour répondre à la question suivante : '{question}'"

    
    

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant who helps generate SQL queries."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            n=1,
            temperature=0
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"Erreur lors de l'appel à l'API OpenAI : {e}")
        return None


def execute_query(query):
    connection = connect_to_db()
    if connection is None:
        return None

    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            return result  # Retournez le résultat brut
    except Exception as e:
        print(f"Erreur lors de l'exécution de la requête : {e}")
        return None
    finally:
        connection.close()


def main():
    question = input("Posez une question à la base de données : ")

    # Interpréter la question pour obtenir une requête SQL
    sql_query = interpret_question(question)

    if sql_query:
        print(f"Requête SQL générée : {sql_query}")
        # Exécuter la requête SQL générée
        results = execute_query(sql_query)

        if results is not None:
            # Afficher les résultats
            for row in results:
                print(row)
            # Ajoutez un commentaire après avoir affiché les résultats
            print(f"Le nombre total de résultats est : {len(results)}")
        else:
            print("Aucun résultat trouvé ou erreur d'exécution de la requête.")
    else:
        print("Impossible de générer une requête SQL.")