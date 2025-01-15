import os
import re
from elasticsearch import Elasticsearch

# Chemin des fichiers logs
# Liste des fichiers journaux à analyser
log_files = ["/var/log/user.log", "/var/log/syslog", "/var/log/kern.log"]

# Vérifier que les fichiers existent
# Boucle pour vérifier l'existence de chaque fichier dans la liste
for log_file in log_files:
    if not os.path.exists(log_file):  # Vérifie si le fichier n'existe pas
        print(f"Le fichier {log_file} n'existe pas.")  # Message d'erreur
        exit(1)  # Arrête l'exécution si un fichier est manquant

# Fonction pour analyser une ligne de log et extraire les informations utiles
def parse_log_line(log_line):
    """
    Analyse une ligne de journal pour extraire des informations structurées.

    :param log_line: Ligne brute du fichier log
    :return: Dictionnaire contenant les informations extraites ou None si le format ne correspond pas
    """
    log_pattern = r"^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+\+\d{2}:\d{2}) (\S+) (\S+?)(?:\[(\d+)\])?: (.+)$"
    match = re.match(log_pattern, log_line)
    if match:
        date, hostname, process, id_process, message = match.groups()
        return {
            "Date": date,
            "Hostname": hostname,
            "Process": process,
            "IdProcess": id_process if id_process else "N/A",  # Définit "N/A" si l'ID du processus est absent
            "Message": message
        }
    return None  # Retourne None si la ligne ne correspond pas au modèle

# Lire les fichiers logs et les structurer
data = []
for log_file in log_files:
    with open(log_file, "r") as file:  # Ouvre le fichier en mode lecture
        for line in file:  # Parcourt chaque ligne du fichier
            parsed_line = parse_log_line(line.strip())  # Analyse la ligne
            if parsed_line:  # Ajoute à la liste si l'analyse est réussie
                data.append(parsed_line)

# Vérifier les données extraites
if not data:  # Si aucune donnée n'a été extraite
    print("Aucune donnée n'a été extraite des fichiers logs.")
    exit(1)  # Arrête l'exécution

# Connexion à Elasticsearch
#################################################
es = Elasticsearch(["http://10.78.104.52:9200/"])  # URL du cluster Elasticsearch
#################################################
if not es.ping():  # Vérifie la connectivité au serveur Elasticsearch
    print("Impossible de se connecter à Elasticsearch.")
    exit(1)  # Arrête l'exécution si la connexion échoue

# Indexer les données dans Elasticsearch
index_name = "data_hilbert02"  # Nom de l'index Elasticsearch
for entry in data:  # Parcourt les données extraites
    response = es.index(index=index_name, document=entry)  # Indexe chaque entrée
    if response.get("result") != "created":  # Vérifie le statut de l'indexation
        print(f"Erreur lors de l'indexation de la ligne : {entry}")

print(f"Données indexées avec succès dans l'index '{index_name}'.")

# Vérifier que les données ont été indexées
try:
    response = es.search(index=index_name, body={"query": {"match_all": {}}})  # Recherche tous les documents
    hits = response.get("hits", {}).get("hits", [])  # Récupère les résultats
    if hits:
        print(f"{len(hits)} documents indexés dans Elasticsearch :")
        for hit in hits[:5]:  # Affiche les 5 premiers documents
            print(hit["_source"])
    else:
        print("Aucun document trouvé dans Elasticsearch.")
except Exception as e:
    # Gère les exceptions liées à la recherche dans Elasticsearch
    print(f"Erreur lors de la vérification des données dans Elasticsearch : {e}")
