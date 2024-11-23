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

# Lancer l'application

Vous avez deux possibilités pour lancer l'application : **avec Python** ou **avec Docker**.

## 1. Lancer avec Python

1. Ouvrez le terminal dans **VSCode**.
2. Exécutez la commande suivante :  
   ```bash
   python app.py

## 2. Lancer avec Docker

### Étape 1 : Préparer l'application

- Modifiez le fichier `app.py` :
  - Retirez les commentaires (`#`) devant les lignes suivantes :
    - `from flask_sqlalchemy import SQLAlchemy`
    - `app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("DB_URL")`
    - `db = SQLAlchemy(app)`

- Modifiez le fichier `.env` pour changer le nom de la base de données en : flask_db

### Étape 2 : Construire et exécuter Docker

1. Ouvrez le terminal et exécutez la commande suivante pour construire et démarrer les conteneurs :  
 `docker compose up --build`
 
 ### Étape 3 : Démarrer l'application
Une fois l'installation terminée, choisissez l'une des options suivantes pour démarrer l'application :  

- **Option 1** : Lancer le conteneur via l'interface graphique de Docker Desktop.  
- **Option 2** : Utiliser le terminal pour démarrer le conteneur en arrière-plan :  
  `docker compose up -d flask_app`

### Lancez les services

Vous pouvez accéder aux différentes fonctionnalités en cliquant sur les options présentes dans le header
