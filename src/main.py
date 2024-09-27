from service.json_to_db_service import import_json_to_db

if __name__ == "__main__":
    # Spécifie le chemin vers le fichier JSON contenant les données
    json_file_path ='src/donnee/flux.json'

    
    # Appel de la fonction pour importer les données du fichier JSON dans la base de données
    import_json_to_db(json_file_path)
