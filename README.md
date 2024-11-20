# Projet info groupe 15 : Spotify Analytics

Spotify Analytics est une application permettant à des companies, des maisons de disque ou des particuliers de mieux connaître les utilisateurs d'un site de musique, notamment :

- Leurs caractéristiques
- Leur localisation
- Leurs goûts musicaux

## :arrow_forward: Logiciels requis

- [Visual Studio Code](https://code.visualstudio.com/)
- [Python 3.10](https://www.python.org/)
- [PostgreSQL](https://www.postgresql.org/)

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
OPEN_API_KEY=sk-proj-63d5n15RLPJysk4gEa8uT3BlbkFJGs4OWoLxKS6C5vMjah5
```

---

## :arrow_forward: Lancez les tests unitaires

Dans le terminal :

- `python -m pytest -v`

---

## :arrow_forward: Les logs (À ENLEVER ?)

L'initalisation se fait dans le module `src/utils/log_init.py` :

- Celui-ci est appelé au démarrage de l'application ou du webservice
- Il utilise le fichier `logging_config.yml` pour la configuration
  - pour modifier le niveau de logs :arrow_right: balise *level*

Un décorateur a été créé dans `src/utils/log_decorator.py`.

Appliqué à une méthode, il permettra d'afficher dans les logs :

- les paramétres d'entrée
- la sortie

Les logs sont consultables dans le dossier `logs`.

---

## :arrow_forward: Utilisez l'application

### Lancez l'application (À MODIFIER)

Vous pouvez maintenant lancer l'application, le webservice ou les tests unitaires

- `python src/__main__.py` (puis commencez par ré-initialiser la bdd)
- `python src/app.py` (à tester)
- `pytest -v`

### Lancez les services

Vous pouvez accéder aux différentes fonctionnalités en cliquant sur les options présentes dans le header
