from flask import Flask, render_template, request,jsonify
from dao.utilisateur_dao import UtilisateurDAO
from dao.song_dao import SongDAO
from service.spotify_service import SpotifyService
from service.openai_service import OpenaiService
from datetime import datetime
# from flask_sqlalchemy import SQLAlchemy
from os import environ
import os
from dotenv import load_dotenv
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__, static_folder="src/static", template_folder="src/templates")
# app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("DB_URL")
# db = SQLAlchemy(app)
load_dotenv()
app = Flask(__name__, static_folder="src/static", template_folder="src/templates")
# app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("DB_URL")
# db = SQLAlchemy(app)

# Instance du service Spotify
spotify_service = SpotifyService()
utilisateur_dao = UtilisateurDAO()
song_dao = SongDAO()
openai_service = OpenaiService()


@app.errorhandler(404)
def page_not_found(e):
    """Gestion des erreurs 404 : Page non trouvée."""
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server_error(e):
    """Gestion des erreurs 500 : Erreur interne du serveur."""
    return render_template("500.html"), 500


@app.errorhandler(Exception)
def handle_exception(e):
    """Gestion des erreurs générales."""
    return render_template("error.html", error_message=str(e)), 500


@app.route("/test_404")

@app.route("/test_404")
def test_404():
    return render_template("404.html")


@app.route("/")

@app.route("/")
def indexx():
    """Affiche la page d'accueil."""
    try:
        return render_template("indexx.html")
        return render_template("indexx.html")
    except Exception as e:
        return render_template("error.html", error_message=str(e)), 500


@app.route("/users", methods=["GET"])
def index():
    """Affiche la liste paginée des utilisateurs."""
    try:
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
    except Exception as e:
        return render_template("error.html", error_message=str(e)), 500


@app.route("/mapp")
@app.route("/mapp")
def show_mapp():
    """Affiche la carte avec les positions des utilisateurs."""
    try:
        user_locations = (
            spotify_service.get_user_coordinates()
        )  # Récupérer les coordonnées des utilisateurs
        return render_template("map_content.html", user_locations=user_locations)
        user_locations = (
            spotify_service.get_user_coordinates()
        )  # Récupérer les coordonnées des utilisateurs
        return render_template("map_content.html", user_locations=user_locations)
    except Exception as e:
        return render_template("error.html", error_message=str(e)), 500


@app.route("/ask", methods=["GET", "POST"])
@app.route("/ask", methods=["GET", "POST"])
def ask():
    """Affiche et gère le formulaire de requête SQL via OpenAI."""
    try:
        if request.method == "POST":
            question = request.form.get("question")
        if request.method == "POST":
            question = request.form.get("question")
            sql_query = openai_service.interpret_question(question)

            if sql_query:
                result = openai_service.execute_query(sql_query)
                return render_template("ask.html", question=question, result=result)
                return render_template("ask.html", question=question, result=result)
            else:
                return render_template(
                    "ask.html", question=question, error="Impossible de générer une requête SQL."
                )

                return render_template(
                    "ask.html", question=question, error="Impossible de générer une requête SQL."
                )

        # Handle GET request to show the ask form without any question or result
        return render_template("ask.html")
        return render_template("ask.html")
    except Exception as e:
        return render_template("error.html", error_message=str(e)), 500


@app.route("/spotify_analytics")
def spotify_analytics():
    """Affiche les analyses Spotify."""
    try:
        total_songs = spotify_service.get_total_songs()
        total_users = spotify_service.get_total_users()
        average_duration = spotify_service.get_average_session_duration()
        top_artists_by_date = spotify_service.get_top_artists_by_date()
        active_users = spotify_service.get_most_active_users()
        activity_peaks = spotify_service.get_activity_peak_times()
        demographics_data = spotify_service.get_user_demographics()
        longest_sessions = spotify_service.get_longest_sessions(top_n=5)

        # Extraire les dates distinctes et les artistes top pour chaque date
        dates = sorted(
            set(date.strftime("%Y-%m-%d") for date, artist, count in top_artists_by_date)
        )
        top_artists = {
            date: [
                (artist, count)
                for d, artist, count in top_artists_by_date
                if d.strftime("%Y-%m-%d") == date
            ][:10]
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
            most_active_users=active_users,
            activity_peaks=activity_peaks,
            gender_stats=demographics_data["gender"],
            longest_sessions=longest_sessions,
            dates=dates,
        )
    except Exception as e:
        return render_template("error.html", error_message=str(e)), 500


# Routes REST API ajoutées
@app.route('/api/users', methods=['GET'])
def api_get_users():
    """API pour récupérer la liste des utilisateurs."""
    try:
        users = utilisateur_dao.get_all_users()
        return jsonify([user.to_dict() for user in users])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/users/<int:user_id>', methods=['GET'])
def api_get_user(user_id):
    """API pour récupérer un utilisateur spécifique."""
    try:
        user = utilisateur_dao.get_user_by_id(user_id)
        if not user:
            return jsonify({'error': 'Utilisateur non trouvé'}), 404
        return jsonify(user.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/songs', methods=['GET'])
def api_get_songs():
    """API pour récupérer toutes les chansons."""
    try:
        songs = song_dao.get_all_songs()
        return jsonify([song.to_dict() for song in songs])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analytics/summary', methods=['GET'])
def api_spotify_summary():
    """API pour obtenir un résumé des analyses Spotify."""
    try:
        summary = {
            'total_songs': spotify_service.get_total_songs(),
            'total_users': spotify_service.get_total_users(),
            'average_session_duration': spotify_service.get_average_session_duration(),
        }
        return jsonify(summary)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analytics/top_artist', methods=['GET'])
def api_spotify_top_artist():
    """API pour obtenir un résumé des analyses Spotify."""
    try:
        # Fetch the raw data from the spotify_service
        raw_data = spotify_service.get_top_artists_by_date()

        # Process the raw data to organize it by date
        grouped_data = {}

        for record in raw_data:
            # Assuming the date is a datetime object, format it as a string
            date, artist, count = record

            if isinstance(date, datetime):  # Ensure the date is a datetime object
                date_str = date.strftime("%a, %d %b %Y")  # Format the datetime to a string
            else:
                date_str = str(date)  # If already a string, just use it

            # If the date is not already in the dictionary, initialize it with an empty list
            if date_str not in grouped_data:
                grouped_data[date_str] = []

            # Append the artist and count to the corresponding date
            grouped_data[date_str].append({'artist': artist, 'count': count})

        # Limit the results to top 10 artists for each day
        for date_str, artists in grouped_data.items():
            # Sort the artists by count in descending order and take the top 10
            sorted_artists = sorted(artists, key=lambda x: x['count'], reverse=True)
            grouped_data[date_str] = sorted_artists[:10]  # Take only the top 10

        # Prepare the summary response
        summary = {'top_artists_by_date': grouped_data}

        return jsonify(summary)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)