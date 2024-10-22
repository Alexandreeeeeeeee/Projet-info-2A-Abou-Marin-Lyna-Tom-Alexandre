from business_object.utilisateur import Utilisateur

# business_object/session.py


class Session:
    def __init__(self, sessionID, ts, auth, level, userAgent, item_in_session, userID_id):
        self.sessionID = sessionID
        self.ts = ts
        self.auth = auth
        self.level = level
        self.userAgent = userAgent
        self.item_in_session = item_in_session
        self.userID_id = userID_id


# Ajoutez la classe SessionDAO ici
class SessionDAO:
    def __init__(self):
        # Initialisez votre connexion à la base de données ici
        pass

    def get_user_by_id(self, sessionID):
        # Implémentez la logique pour récupérer une session par son ID
        pass
