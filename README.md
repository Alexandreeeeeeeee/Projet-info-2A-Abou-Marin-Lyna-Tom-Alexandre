# Projet info groupe 15 : Spotify Analytics

Spotify Analytics est une application permettant à des companies, des maisons de disque ou des particuliers de mieux connaître les utilisateurs d'un site de musique, notamment :

- Leurs caractéristiques
- Leur localisation
- Leurs goûts musicaux

## :arrow_forward: Logiciels requis

- [Visual Studio Code](https://code.visualstudio.com/)
- [Python 3.10](https://www.python.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [Docker](https://www.docker.com/)

---

## :arrow_forward: Téléchargez ou clonez le projet

### Clonez le projet :

- [ ] Ouvrez **Git Bash**
- [ ] Positionnez-vous dans le dossier dans lequel vous souhaitez importer le dépôt
  - `mkdir -p /chemin/sous-chemin/dossier && cd $_`
- [ ] Clonez ce dépôt
  - `git clone https://github.com/Alexandreeeeeeeee/Projet-info-2A-Abou-Marin-Lyna-Tom-Alexandre.git`

### Téléchargez le projet :

- [ ] Téléchargez [le dossier sur Github](https://github.com/Alexandreeeeeeeee/Projet-info-2A-Abou-Marin-Lyna-Tom-Alexandre)
- [ ] Décompressez-le dans la destination de votre choix

---

## :arrow_forward: Ouvrez le dépôt avec VSCode

- [ ] Ouvrez **Visual Studio Code**
- [ ] File > Open Folder
- [ ] Cliquez une seule fois sur *Projet-info-2A-Abou-Marin-Lyna-Tom-Alexandre* et cliquez sur `Sélectionner un dossier`
  - Assurez-vous alors que le dossier parent dans l'explorer VSCode *Projet-info-2A-Abou-Marin-Lyna-Tom-Alexandre*

---

## :arrow_forward: Installez les packages nécessaires

Dans Visual Studio Code :

- [ ] Ouvrez un terminal *Git Bash*
- [ ] Exécutez les commandes suivantes

```bash
pip install -r requirements.txt
pip list
```

---

## :arrow_forward: Variables d'environnement

À la racine du projet le fichier :

- [ ] Créez un fichier nommé `.env` 
- [ ] Collez les éléments ci-dessous

```
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=postgres
OPEN_API_KEY=sk-proj-63d5n15RLPJysk4gEa8uT3BlbkFJGvs4OWoLxKS6C5vMjah5
```

---

## :arrow_forward: Utilisez l'application

### Lancez l'application

Avec VSCode : (EST-CE IMPORTANT DE FAIRE ```python main.py``` ?)

- [ ] Dans le terminal, exécuter ```python main.py```
- [ ] Exécuter ```python app.py```

Avec Docker : (Où METTRE L'INFO LOCALHOST:8000 ?)
Avant de lancer la commande docker-compose up --build, il est nécessaire de modifier le fichier app.py en retirant les commentaires (#) devant les lignes suivantes :

from flask_sqlalchemy import SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("DB_URL")
db = SQLAlchemy(app)
Ensuite, il faut accéder au fichier .env et changer le nom de la base de données en flask_db.
- [ ] Dans le terminal, exécuter ```docker compose up --build``` puis attendre que l'installation se termine
- [ ] 2 possibilités :
  - Lancer le conteneur
  - exécuter ```docker compose up -d flask_app```

### Lancez les services

Vous pouvez accéder aux différentes fonctionnalités en cliquant sur les options présentes dans le header
