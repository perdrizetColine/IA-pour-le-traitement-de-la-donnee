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

Ce projet propose un cadre pour la détection d'anomalies dans les fichiers de logs à l'aide d'un classificateur Random Forest. Les étapes incluent le prétraitement des données, l'entraînement du modèle avec optimisation des hyperparamètres et le test pour détecter les anomalies.

### Prérequis

- pandas
  
- numpy
  
- scikit-learn
  
- joblib

### Fichiers

o 'logs_corrompu_label.csv' : Fichier de logs pour le prétraitement et l'entraînement.

o 'all_logs.csv' : Fichier de test pour la détection des anomalies.

### Utilisation

logs_corrompu_label.csv : Fichier de logs pour le prétraitement et l'entraînement.

all_logs.csv : Fichier de test pour la détection des anomalies.

Utilisation

1. Prétraitement des Données

Le prétraitement nettoie les données et applique un encodage OneHotEncoding. Il sauvegarde également le pipeline de prétraitement pour une réutilisation ultérieure.

from script import preprocess_data
df_encoded = preprocess_data('logs_corrompu_label.csv')

2. Entraîner le Modèle

Cette étape entraîne un modèle Random Forest avec une recherche des meilleurs hyperparamètres. Le modèle optimisé est sauvegardé.

from script import train_model_opti
model, accuracy = train_model_opti(df_encoded)

3. Tester le Modèle

Utilisez le modèle entraîné pour prédire les anomalies dans un fichier de test.

from script import test_model
anomalies = test_model('all_logs.csv')
print(anomalies)

### Fonctionnalités

Prétraitement : Gère les valeurs manquantes et encode les caractéristiques catégorielles.

Optimisation des Hyperparamètres : Ajuste les hyperparamètres de Random Forest avec GridSearchCV.

Détection d'Anomalies : Identifie les entrées considérées comme des anomalies.

Résultats

Le meilleur modèle atteint une précision de ~99.95% sur l'ensemble d'entraînement.
