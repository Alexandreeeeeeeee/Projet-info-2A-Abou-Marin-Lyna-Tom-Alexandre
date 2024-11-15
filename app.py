from flask import Flask, render_template
from dao.utilisateur_dao import UtilisateurDAO
from service.spotify_service import SpotifyService
from flask import request
from service.openai_service import OpenaiService
#from flask_sqlalchemy import SQLAlchemy
from os import environ
app = Flask(__name__,static_folder='src/static' ,template_folder='src/templates')


#app.config['SQLALCHEMY_DATABASE_URI']=environ.get('DB_URL')
#db = SQLAlchemy(app) 

# Instance du service Spotify
spotify_service = SpotifyService()
utilisateur_dao = UtilisateurDAO()

@app.route('/indexx')
def indexx():
    return render_template('indexx.html')

@app.route("/", methods=["GET"])
def index():
    page = request.args.get("page", 1, type=int)
    per_page = 10

    # Récupérer tous les utilisateurs
    utilisateurs = utilisateur_dao.get_all_users()

    # Calculer le début et la fin de la tranche d'utilisateurs à afficher
    start = (page - 1) * per_page
    end = start + per_page
    utilisateurs_paginated = utilisateurs[start:end]

    return render_template(
        "index.html",
        utilisateurs=utilisateurs_paginated,
        page=page,
        total=len(utilisateurs),
        per_page=per_page,
    )

@app.route("/map")
def show_map():
    service.create_user_map()  # Crée la carte avec les utilisateurs
    return render_template("map.html")  # Affiche la carte




@app.route('/mapp')
def show_mapp():
    user_locations = spotify_service.get_user_coordinates()  # Récupérer les coordonnées des utilisateurs
    return render_template('map_content.html', user_locations=user_locations)

openai_service = OpenaiService()

@app.route('/ask', methods=['GET', 'POST'])
def ask():
    if request.method == 'POST':
        question = request.form.get('question')
        sql_query = openai_service.interpret_question(question)

        if sql_query:
            result = openai_service.execute_query(sql_query)
            return render_template('ask.html', question=question, result=result)
        else:
            return render_template('ask.html', question=question, error="Impossible de générer une requête SQL.")
    
    # Handle GET request to show the ask form without any question or result
    return render_template('ask.html')







@app.route("/spotify_analytics")
def spotify_analytics():
    total_songs = spotify_service.get_total_songs()
    total_users = spotify_service.get_total_users()
    average_duration = spotify_service.get_average_session_duration()
    top_artists_by_date = spotify_service.get_top_artists_by_date()
    average_items_by_level = spotify_service.get_average_item_in_session_by_level()  # Ajout de la moyenne des items par niveau
    
    # Extraire les dates distinctes et les artistes top pour chaque date
    dates = sorted(set(date.strftime('%Y-%m-%d') for date, artist, count in top_artists_by_date))
    top_artists = {
        date: [(artist, count) for d, artist, count in top_artists_by_date if d.strftime('%Y-%m-%d') == date][:10]
        for date in dates
    }

    return render_template(
        "spotify_analytics.html",
        total_songs=total_songs,
        total_users=total_users,
        average_duration=average_duration,
        top_artists=top_artists,
        top_artists_by_date=top_artists_by_date,
        average_items_by_level = spotify_service.get_average_item_in_session_by_level(),
        dates=dates
    )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
