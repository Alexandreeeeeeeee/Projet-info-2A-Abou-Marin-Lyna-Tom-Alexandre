import openai
from dao.db_connection import get_connection  # Importer get_connection
from dotenv import load_dotenv
import os

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Obtenir la clé API OpenAI depuis les variables d'environnement
openai.api_key = os.getenv("OPENAI_API_KEY")


class OpenaiService:
    def __init__(self):
        # Vous pouvez ajouter d'autres initialisations si nécessaire
        pass

    def interpret_question(self, question):
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

    def execute_query(self, query):
        connection = get_connection()  # Utiliser get_connection pour obtenir la connexion
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
