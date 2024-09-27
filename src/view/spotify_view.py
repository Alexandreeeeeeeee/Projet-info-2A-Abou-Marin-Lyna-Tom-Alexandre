from service.spotify_service import SpotifyService

def display_average_session_duration():
    service = SpotifyService()
    avg_duration = service.get_average_session_duration()
    print(f"Durée moyenne d'une session : {avg_duration}")

def display_user_locations():
    service = SpotifyService()
    locations = service.get_user_locations()
    for user in locations:
        print(f"Utilisateur : {user.firstName} {user.lastName} - Ville : {user.city}")
