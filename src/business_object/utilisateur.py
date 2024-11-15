"""
Module contenant la classe Utilisateur pour représenter les utilisateurs de la base de données.
"""

class Utilisateur:
    """Classe représentant un utilisateur avec ses attributs associés dans la base de données."""

    def __init__(self, user_id, last_name, first_name, gender, lon, lat, city, zip_code, state, registration):
        """
        Initialise une instance de la classe Utilisateur.

        :param user_id: L'ID de l'utilisateur
        :param last_name: Nom de famille de l'utilisateur
        :param first_name: Prénom de l'utilisateur
        :param gender: Genre de l'utilisateur
        :param lon: Longitude de la localisation de l'utilisateur
        :param lat: Latitude de la localisation de l'utilisateur
        :param city: Ville de l'utilisateur
        :param zip_code: Code postal de l'utilisateur
        :param state: État ou région de l'utilisateur
        :param registration: Date d'inscription de l'utilisateur
        """
        self.user_id = user_id
        self.last_name = last_name
        self.first_name = first_name
        self.gender = gender
        self.lon = lon  # Longitude
        self.lat = lat  # Latitude
        self.city = city
        self.zip_code = zip_code
        self.state = state
        self.registration = registration

    def __repr__(self):
        """
        Représentation de l'objet Utilisateur en chaîne de caractères.
        
        :return: Représentation textuelle de l'utilisateur
        """
        return (
            f"Utilisateur(user_id={self.user_id}, last_name='{self.last_name}', "
            f"first_name='{self.first_name}', gender='{self.gender}', "
            f"lon={self.lon}, lat={self.lat}, city='{self.city}', "
            f"zip_code='{self.zip_code}', state='{self.state}', "
            f"registration='{self.registration}')"
        )
