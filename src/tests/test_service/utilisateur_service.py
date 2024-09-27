from dao.utilisateur_dao import UtilisateurDAO

class UtilisateurService:
    def __init__(self):
        self.utilisateur_dao = UtilisateurDAO()

    def ajouter_utilisateur(self, utilisateur):
        """Ajoute un utilisateur via le DAO."""
        self.utilisateur_dao.add_utilisateur(utilisateur)

    def obtenir_tous_les_utilisateurs(self):
        """Récupère tous les utilisateurs via le DAO."""
        return self.utilisateur_dao.get_all_users()

    def obtenir_utilisateur_par_id(self, userID):
        """Récupère un utilisateur spécifique par son ID."""
        return self.utilisateur_dao.find_user_by_id(userID)
