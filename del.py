# Script pour supprimer les versions des dépendances dans requirements.txt
with open('requirements.txt', 'r') as file:
    lines = file.readlines()

with open('requirements.txt', 'w') as file:
    for line in lines:
        # Sépare le nom du package et supprime la version
        package = line.split('==')[0]
        file.write(package.strip() + '\n')
