# IA POUR LE TRAITEMENT DE LA DONNEE

## pivot.py
  Ce script permet de lire, analyser et indexer des fichiers journaux (logs) dans Elasticsearch. Il extrait des informations structurées à partir de fichiers logs au format prédéfini, puis les stocke dans un index Elasticsearch.
### Prérequis
- Python 3.7 ou supérieur
- Elasticsearch (instance accessible)
- Bibliothèques Python :
  - 'elasticsearch'
  - 'os'
  - 're'
### Fonctionnalités
o Vérifie l'existence des fichiers journaux avant analyse.
o Analyse les lignes de log à l'aide d'expressions régulières pour extraire les informations structurées :
   - Date
   - Nom d'hôte
   - Processus
   - ID de processus
   - Message
o Indexe les données dans Elasticsearch.
o Vérifie les données indexées et affiche un aperçu.
### Exemple de Sortie
Données indexées avec succès dans l'index 'data_hilbert02'.
5 documents indexés dans Elasticsearch :
{'Date': '2024-12-16T14:09:57.761356+01:00', 'Hostname': 'hilbert02', 'Process': 'gnome-keyring-ssh.desktop', 'IdProcess': '2037', 'Message': 'discover_other_daemon: 1GNOME_KEYRING_CONTROL=/run/user/1000/keyring'}

## get.py
  Ce script permet d'extraire les logs de tous les index Elasticsearch et de les exporter dans un fichier CSV structuré. Il utilise l'API scroll d'Elasticsearch pour gérer de grandes quantités de données.
### Prérequis
- Python 3.7 ou supérieur
- Elasticsearch (instance en cours d'exécution)
- Bibliothèques Python :
  - 'elasticsearch'
  - 'csv'
### Fonctionnalités
o Connexion à Elasticsearch : Se connecte au cluster spécifié.
o Requête multi-index : Récupère les documents de tous les index ou d’un index spécifique.
o Extraction sélective : Permet de récupérer uniquement les champs définis.
o Gestion de gros volumes : Utilise la pagination via l'API scroll d'Elasticsearch.
o Exportation CSV : Sauvegarde les données dans un fichier CSV prêt à être analysé.
  ### Exemple de sortie
Date,Hostname,Process,IdProcess,Message

2024-12-11T17:14:51.738480+01:00,hilbert02,gnome-shell,2026,meta_window_set_stack_position_no_sync: assertion 'window->stack_position >= 0' failed

2024-12-11T17:20:14.050043+01:00,hilbert02,gnome-text-edit,6677,Trying to snapshot GtkGizmo 0x559f9a9e7800 without a current allocation
  
## model.ipynb
  
reste à entrainer le modèle avec apprentissage supervisé : classer avec ou sans anomalies
exporter job de prétraitement
exporter job d'entrainement
on hot encoding
