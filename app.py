from flask import Flask, render_template
from dao.utilisateur_dao import UtilisateurDAO
from src.service.spotify_service import SpotifyService
from flask import request

app = Flask(__name__, template_folder="src/templates")
# Instance du service Spotify
spotify_service = SpotifyService()

utilisateur_dao = UtilisateurDAO()


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


# Instanciation du service
service = SpotifyService()


@app.route("/map")
def show_map():
    service.create_user_map()  # Crée la carte avec les utilisateurs
    return render_template("map.html")  # Affiche la carte


@app.route("/spotify_analytics")
def spotify_analytics():
    total_songs = spotify_service.get_total_songs()
    total_users = spotify_service.get_total_users()
    average_duration = spotify_service.get_average_session_duration()
    top_artists = spotify_service.get_top_artists()

    return render_template(
        "spotify_analytics.html",
        total_songs=total_songs,
        total_users=total_users,
        average_duration=average_duration,
        top_artists=top_artists,
    )


if __name__ == "__main__":
    app.run(debug=True)
