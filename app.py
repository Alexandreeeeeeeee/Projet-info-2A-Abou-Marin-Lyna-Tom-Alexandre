from flask import Flask, render_template, request
from dao.utilisateur_dao import UtilisateurDAO
from service.spotify_service import SpotifyService
from service.openai_service import OpenaiService
import os
#from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder='src/static', template_folder='src/templates')

#app.config['SQLALCHEMY_DATABASE_URI']=environ.get('DB_URL')
#db = SQLAlchemy(app)

# Instance du service Spotify
spotify_service = SpotifyService()
utilisateur_dao = UtilisateurDAO()
openai_service = OpenaiService()


@app.route('/')
def indexx():
    """Affiche la page d'accueil."""
    return render_template('indexx.html')


@app.route("/users", methods=["GET"])
def index():
    """Affiche la liste paginée des utilisateurs."""
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


@app.route('/mapp')
def show_mapp():
    """Affiche la carte avec les positions des utilisateurs."""
    user_locations = spotify_service.get_user_coordinates()  # Récupérer les coordonnées des utilisateurs
    return render_template('map_content.html', user_locations=user_locations)


@app.route('/ask', methods=['GET', 'POST'])
def ask():
    """Affiche et gère le formulaire de requête SQL via OpenAI."""
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
    """Affiche les analyses Spotify."""
    total_songs = spotify_service.get_total_songs()
    total_users = spotify_service.get_total_users()
    average_duration = spotify_service.get_average_session_duration()
    top_artists_by_date = spotify_service.get_top_artists_by_date()
    most_active_users = spotify_service.get_most_active_users()
    activity_peaks = spotify_service.get_activity_peak_times()
    demographics_data = spotify_service.get_user_demographics()
    longest_sessions = spotify_service.get_longest_sessions(top_n=5)

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
        average_items_by_level=spotify_service.get_average_item_in_session_by_level(),
        most_active_users=most_active_users,
        activity_peaks=activity_peaks,
        gender_stats=demographics_data["gender"], 
        longest_sessions=longest_sessions,
        dates=dates
    )


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
