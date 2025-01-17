# IA POUR LE TRAITEMENT DE LA DONNÉE

Le projet a pour objectif principal de gérer les logs d’une machine en les chargeant dans un cluster Elasticsearch afin de faciliter leur stockage, leur analyse et leur visualisation. En complément, des logs spécifiques contenant des anomalies sont également intégrés dans le cluster pour enrichir les données disponibles et permettre une meilleure détection des anomalies.

Ensuite, l’ensemble des logs provenant de différentes machines est récupéré pour constituer un jeu de données global. Sur ce jeu de données, un modèle d’apprentissage est entraîné en identifiant les logs contenant des anomalies. Ce modèle est par la suite testé sur un fichier dédié contenant des logs marqués comme anormaux, afin d’évaluer sa capacité à détecter efficacement ces anomalies.

## **pivot.py**

Ce script lit, analyse et indexe des fichiers journaux (logs) dans Elasticsearch. Il extrait des informations structurées à partir de fichiers logs au format prédéfini, puis les stocke dans un index Elasticsearch.

### **Prérequis**

| Composant            | Description                                      |
|-----------------------|--------------------------------------------------|
| **Python**           | Version 3.7 ou supérieure                        |
| **Elasticsearch**    | Instance accessible                              |
| **Bibliothèques Python** | `elasticsearch`, `os`, `re`                  |

### **Fonctionnalités**

- Vérification de l'existence des fichiers journaux avant analyse.
- Analyse des lignes de log à l'aide d'expressions régulières pour extraire :
  - Date
  - Nom d'hôte
  - Processus
  - ID de processus
  - Message
- Indexation des données dans Elasticsearch.
- Vérification des données indexées et affichage d'un aperçu.

### **Exemple de Sortie**

```
Données indexées avec succès dans l'index 'data_hilbert02'.

5 documents indexés dans Elasticsearch :
{'Date': '2024-12-16T14:09:57.761356+01:00', 'Hostname': 'hilbert02', 'Process': 'gnome-keyring-ssh.desktop', 'IdProcess': '2037', 'Message': 'discover_other_daemon: 1GNOME_KEYRING_CONTROL=/run/user/1000/keyring'}
```

---

## **get.py**

Ce script extrait les logs de tous les index Elasticsearch et les exporte dans un fichier CSV structuré.

### **Prérequis**

| Composant            | Description                                      |
|-----------------------|--------------------------------------------------|
| **Python**           | Version 3.7 ou supérieure                        |
| **Elasticsearch**    | Instance en cours d'exécution                    |
| **Bibliothèques Python** | `elasticsearch`, `csv`                       |

### **Fonctionnalités**

- **Connexion à Elasticsearch** : Se connecte au cluster spécifié.
- **Requête multi-index** : Récupère les documents de tous les index ou d’un index spécifique.
- **Extraction sélective** : Récupère uniquement les champs définis.
- **Gestion de gros volumes** : Utilise l'API `scroll` pour paginer les résultats.
- **Exportation CSV** : Sauvegarde les données dans un fichier CSV prêt à être analysé.

### **Exemple de Sortie**

| Date                          | Hostname  | Process        | IdProcess | Message                                                                           |
|-------------------------------|-----------|----------------|-----------|-----------------------------------------------------------------------------------|
| 2024-12-11T17:14:51.738480+01:00 | hilbert02 | gnome-shell    | 2026      | meta_window_set_stack_position_no_sync: assertion 'window->stack_position >= 0' failed |
| 2024-12-11T17:20:14.050043+01:00 | hilbert02 | gnome-text-edit | 6677      | Trying to snapshot GtkGizmo 0x559f9a9e7800 without a current allocation          |

---

## **model.ipynb**

Ce projet propose un cadre pour détecter des anomalies dans les fichiers logs grâce à un classificateur **Random Forest**.

### **Prérequis**

| Bibliothèque        | Description                        |
|---------------------|------------------------------------|
| `pandas`            | Manipulation de données           |
| `numpy`             | Calculs numériques                |
| `scikit-learn`      | Machine learning                  |
| `joblib`            | Sauvegarde des modèles            |

### **Fichiers**

| Nom du fichier               | Description                                       |
|------------------------------|---------------------------------------------------|
| `logs_corrompu_label.csv`    | Logs pour le prétraitement et l'entraînement      |
| `all_logs.csv`               | Logs pour la détection des anomalies             |

### **Utilisation**

1. **Prétraitement des Données**

   Nettoyez les données et appliquez un encodage OneHotEncoding.

   ```python
   from script import preprocess_data
   df_encoded = preprocess_data('logs_corrompu_label.csv')
   ```

2. **Entraînement du Modèle**

   Entraînez un modèle Random Forest optimisé.

   ```python
   from script import train_model_opti
   model, accuracy = train_model_opti(df_encoded)
   ```

3. **Test du Modèle**

   Utilisez le modèle entraîné pour détecter les anomalies.

   ```python
   from script import test_model
   anomalies = test_model('all_logs.csv')
   print(anomalies)
   ```

### **Fonctionnalités**

- **Prétraitement** : Nettoie les données et encode les caractéristiques catégorielles.
- **Optimisation des Hyperparamètres** : Ajuste les paramètres avec `GridSearchCV`.
- **Détection d'Anomalies** : Identifie les entrées considérées comme des anomalies.

### **Résultats**

- Précision : **~99.53%** sur l'ensemble d'entraînement.
