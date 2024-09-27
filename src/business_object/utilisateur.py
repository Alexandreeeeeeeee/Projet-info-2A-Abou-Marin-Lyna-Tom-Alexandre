class Utilisateur:
    def __init__(self, userID, lastName, firstName, gender, lon, lat, city, zip, state, registration):
        self.userID = userID
        self.lastName = lastName
        self.firstName = firstName
        self.gender = gender
        self.lon = lon
        self.lat = lat
        self.city = city
        self.zip = zip
        self.state = state
        self.registration = registration

    def __str__(self):
        return (f"Utilisateur: {self.firstName} {self.lastName}, ID: {self.userID}, "
                f"Gender: {self.gender}, Location: ({self.lon}, {self.lat}), "
                f"City: {self.city}, Zip Code: {self.zip}, State: {self.state}, "
                f"Registration Year: {self.registration}")
    def save_or_update(self, utilisateur):
        connection = get_db_connection()
        cursor = connection.cursor()

        # Vérifie si l'utilisateur existe déjà en utilisant son userID
        cursor.execute("SELECT * FROM utilisateurs WHERE userID = %s", (utilisateur.userID,))
        result = cursor.fetchone()

        if result:
            # Si l'utilisateur existe, on le met à jour
            cursor.execute("""
                UPDATE utilisateurs
                SET lastName = %s, firstName = %s, gender = %s, lon = %s, lat = %s,
                    city = %s, zip_code = %s, state = %s, registration = %s
                WHERE userID = %s
            """, (utilisateur.lastName, utilisateur.firstName, utilisateur.gender,
                  utilisateur.lon, utilisateur.lat, utilisateur.city, utilisateur.zip,
                  utilisateur.state, utilisateur.registration, utilisateur.userID))
        else:
            # Sinon, on insère un nouvel utilisateur
            cursor.execute("""
                INSERT INTO utilisateurs (userID, lastName, firstName, gender, lon, lat, city, zip_code, state, registration)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (utilisateur.userID, utilisateur.lastName, utilisateur.firstName, utilisateur.gender,
                  utilisateur.lon, utilisateur.lat, utilisateur.city, utilisateur.zip,
                  utilisateur.state, utilisateur.registration))

        # Sauvegarde les changements dans la base de données
        connection.commit()
        cursor.close()
        connection.close()
