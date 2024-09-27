from dao.db_connection import get_connection
from dao.utilisateur_dao import UtilisateurDAO
from dao.song_dao import SongDAO

from dao.utilisateur_dao import UtilisateurDAO

def main():
    dao = UtilisateurDAO()
    utilisateurs = dao.get_all_users()
    print("Liste des utilisateurs:")
    for utilisateur in utilisateurs:
        print(utilisateur)  # Cela utilise la méthode __str__

if __name__ == "__main__":
    main()

