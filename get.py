from elasticsearch import Elasticsearch
import csv

# Configuration Elasticsearch
ELASTICSEARCH_HOST = "http://10.78.104.59:9200"  # Adresse de votre cluster Elasticsearch
FIELDS = [
    "Date",  
    "Hostname",
    "Process",
    "IdProcess",
    "Message",
]  # Liste des champs à extraire et à inclure dans le fichier CSV

# Connexion à Elasticsearch
es = Elasticsearch(ELASTICSEARCH_HOST)

# Fonction pour récupérer les logs
def fetch_logs(index_pattern="*", fields=None, size=1000):
    """
    Récupère les logs de tous les index Elasticsearch.

    :param index_pattern: Modèle d'index à interroger (par défaut '*', tous les index)
    :param fields: Liste des champs à inclure (None pour tous les champs)
    :param size: Nombre maximum de documents à récupérer par requête
    :return: Liste de documents contenant les logs
    """
    query = {
        "_source": fields,  # Champs à inclure dans les résultats
        "query": {"match_all": {}},  # Requête pour récupérer tous les documents
        "size": size  # Limite de documents par requête
    }

    # Première requête avec une session scroll pour gérer de gros volumes de données
    response = es.search(index=index_pattern, body=query, scroll="1m")
    scroll_id = response["_scroll_id"]  # Identifiant de la session scroll
    hits = response["hits"]["hits"]  # Liste des documents récupérés

    documents = []  # Liste pour stocker tous les documents
    while hits:  # Tant qu'il reste des documents à récupérer
        documents.extend([hit["_source"] | {"_index": hit["_index"], "_id": hit["_id"]} for hit in hits])
        response = es.scroll(scroll_id=scroll_id, scroll="1m")  # Requête pour obtenir les documents suivants
        hits = response["hits"]["hits"]

    return documents  # Retourne tous les documents récupérés

# Fonction pour écrire les logs dans un fichier CSV
def write_to_csv(file_name, documents, fields):
    """
    Écrit les logs dans un fichier CSV.

    :param file_name: Nom du fichier CSV
    :param documents: Liste des documents à écrire
    :param fields: Champs à inclure dans le fichier CSV
    """
    with open(file_name, "w", newline='', encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fields)  # Crée un writer CSV avec les champs spécifiés
        writer.writeheader()  # Écrit l'en-tête des colonnes

        for doc in documents:
            # Complète avec des valeurs vides si un champ est manquant
            row = {field: doc.get(field, "") for field in fields}
            writer.writerow(row)  # Écrit chaque document comme une ligne dans le fichier CSV

# Exécution principale
if __name__ == "__main__":
    print("Fetching logs from all Elasticsearch indices...")
    logs = fetch_logs(fields=FIELDS)  # Récupère les logs avec les champs spécifiés
    print(f"Fetched {len(logs)} logs.")  # Affiche le nombre de logs récupérés

    print("Writing logs to CSV...")
    write_to_csv("all_logs.csv", logs, FIELDS)  # Écrit les logs dans un fichier CSV
    print("Logs written to all_logs.csv.")  # Confirmation d'écriture
