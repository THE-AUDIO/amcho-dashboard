# AMCHO Dashboard 📊

Un tableau de bord interactif pour l'analyse et la visualisation des données de prix du cacao et de l'indice des prix à la production (PPI). Application web moderne construite avec **Streamlit**, incluant un système d'authentification et des visualisations avancées.

🌐 **[Accédez à l'application en ligne](https://amcho-dashboard.onrender.com)**

---

## 🎯 Fonctionnalités principales

- **Authentification sécurisée** : Système de login/register pour les utilisateurs
- **Tableau récapitulatif** : Vue d'ensemble des données clés avec KPIs
- **Analyse des prix du cacao** : Historique et tendances des prix du cacao
- **Indice PPI** : Visualisation de l'indice des prix à la production
- **Comparaison** : Comparaison interactive entre plusieurs indicateurs
- **Pipeline ETL** : Extraction, transformation et chargement automatique des données

---

## 📁 Structure du projet

```
amcho-dashboard/
├── app/                          # Application Streamlit principale
│   ├── main.py                   # Point d'entrée principal
│   ├── core/                     # Fonctionnalités métier
│   │   ├── auth.py               # Gestion de l'authentification
│   │   ├── dashboard.py          # Logique du dashboard
│   │   └── register.py           # Enregistrement d'utilisateurs
│   ├── pages/                    # Pages de l'application
│   │   ├── 01_Login.py           # Page de connexion
│   │   ├── 02_Register.py        # Page d'inscription
│   │   └── dashboard/            # Pages du dashboard
│   │       ├── 01_Tableau.py     # Tableau récapitulatif
│   │       ├── 02_Cocoa.py       # Prix du cacao
│   │       ├── 03_PPI.py         # Indice PPI
│   │       └── 04_Comparaison.py # Comparaison d'indicateurs
│   └── service/                  # Services et utilitaires
│       └── db.py                 # Interactions avec la base de données
├── etl/                          # Pipeline ETL
│   ├── main.py                   # Point d'entrée ETL
│   ├── core/                     # Configuration
│   │   ├── base.py               # Modèles de base SQLAlchemy
│   │   ├── bd.py                 # Configuration base de données
│   │   └── config.py             # Configuration ETL
│   ├── extract/                  # Extraction des données
│   │   └── extractor.py          # Extracteurs de données
│   ├── load/                     # Chargement des données
│   │   └── loader.py             # Chargeur de données
│   ├── model/                    # Modèles de données
│   │   ├── cocoa.py              # Modèle pour les prix du cacao
│   │   ├── ppi.py                # Modèle pour l'indice PPI
│   │   └── users.py              # Modèle pour les utilisateurs
│   └── transform/                # Transformation des données
│       └── transformer.py        # Transformateurs de données
├── data/                         # Fichiers de données brutes
│   ├── cocoa_price.csv           # Historique des prix du cacao
│   └── ppi.csv                   # Données PPI
├── requirements.txt              # Dépendances Python
├── run.py                        # Lanceur principal
├── run.sh                        # Script d'exécution (Linux/Mac)
└── run.bat                       # Script d'exécution (Windows)
```

---

## 🚀 Installation

### Prérequis
- Python 3.12.3
- pip (gestionnaire de paquets Python)
- Base de données supportée (PostgreSQL recommandé)

### Étapes d'installation

1. **Cloner le projet**
   ```bash
   git clone https://github.com/THE-AUDIO/amcho-dashboard.git
   cd amcho-dashboard
   ```

2. **Créer un environnement virtuel**
   ```bash
   python -m venv venv
   ```

3. **Activer l'environnement virtuel**
   - **Linux/Mac** :
     ```bash
     source venv/bin/activate
     ```
   - **Windows** :
     ```bash
     venv\Scripts\activate
     ```

4. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configurer les variables d'environnement**
   
   Créez un fichier `.env` à la racine du projet :
   ```env
   DATABASE_URL=postgresql://user:password@localhost:5432/amcho_db
   ```

---

## 🏃 Lancement de l'application

### Méthode 1 : Script Python (recommandé)
```bash
python run.py
```
Cette commande exécute automatiquement l'ETL, puis lance l'application Streamlit.

### Méthode 2 : Scripts natifs
- **Linux/Mac** :
  ```bash
  ./run.sh
  ```
- **Windows** :
  ```bash
  run.bat
  ```

### Méthode 3 : Lancer l'ETL et l'app séparément
```bash
# Exécuter l'ETL
python etl/main.py

# Lancer l'application
streamlit run app/main.py
```

### Méthode 4 : Docker Compose (recommandé pour production) 🐳
La solution la plus simple et la plus fiable pour déployer l'application en production.

#### Prérequis
- Docker et Docker Compose installés
- Vérifier l'installation :
  ```bash
  docker --version
  docker compose version
  ```

#### Lancer l'application avec Docker Compose
```bash
# Démarrer les services (app + base de données)
docker compose up -d

# Consulter les logs
docker compose logs -f

# Arrêter les services
docker compose down
```

#### Accès à l'application
- **Application Streamlit** : http://localhost:8501
- **Base de données PostgreSQL** : localhost:5432
  - Utilisateur : `amcho_user`
  - Mot de passe : `amcho_password`
  - Nom de la BD : `amcho_db`

#### Gestion des conteneurs
```bash
# Voir les conteneurs en cours d'exécution
docker compose ps

# Redémarrer les services
docker compose restart

# Reconstruire les images
docker compose up -d --build

# Supprimer les données persistantes
docker compose down -v

# Voir les logs d'un service spécifique
docker compose logs -f app
docker compose logs -f postgres
```

#### Personnaliser la configuration
Modifiez le fichier `docker-compose.yml` pour :
- Changer les ports (modifier `8501:8501` ou `5432:5432`)
- Modifier les identifiants PostgreSQL
- Ajouter des variables d'environnement
- Configurer les volumes de persistance

---

## 🔄 Pipeline ETL

Le pipeline ETL automatise l'extraction, la transformation et le chargement des données :

1. **Extraction** : Récupération des données brutes depuis les fichiers CSV
2. **Transformation** : Nettoyage, normalisation et enrichissement des données
3. **Chargement** : Insertion des données dans la base de données

### Exécuter l'ETL manuellement
```bash
python etl/main.py
```

---

## 🔐 Authentification

L'application inclut un système d'authentification sécurisé :

- **Inscription** : Créer un nouveau compte utilisateur
- **Connexion** : Se connecter avec vos identifiants
- **Gestion de session** : Contrôle d'accès aux pages du dashboard

### Exemple d'utilisation
1. Lancez l'application
2. Accédez à la page d'inscription pour créer un compte
3. Connectez-vous avec vos identifiants
4. Naviguez vers le tableau de bord

---

## 📊 Pages du Dashboard

### 1. 📋 Tableau Récapitulatif
Vue d'ensemble avec les KPIs principaux et les indicateurs clés du moment.

### 2. 🍫 Prix du Cacao
Historique détaillé des prix du cacao avec analyses et tendances.

### 3. 📈 Indice PPI
Visualisation de l'indice des prix à la production et ses évolutions.

### 4. 🔀 Comparaison
Comparaison interactive entre différents indicateurs et périodes.

---

## 📦 Dépendances principales

- **Streamlit** : Framework web pour l'interface utilisateur
- **Pandas** : Manipulation et analyse de données
- **SQLAlchemy** : ORM pour la gestion de la base de données
- **Plotly** : Visualisations interactives
- **Pydantic** : Validation de données
- **psycopg2-binary** : Connecteur PostgreSQL

Voir [requirements.txt](requirements.txt) pour la liste complète.

---

## 🔧 Configuration

### Variables d'environnement

```env
# Base de données
DATABASE_URL=postgresql://user:password@localhost:5432/amcho_db

```

---

## 📝 Notes développeur

- Les modèles de données se trouvent dans `etl/model/`
- Les transformations de données se font dans `etl/transform/`
- La logique métier du dashboard est dans `app/core/dashboard.py`
- L'authentification est gérée dans `app/core/auth.py`

---

## 🐛 Troubleshooting

### L'app ne démarre pas
```bash
# Vérifier que toutes les dépendances sont installées
pip install -r requirements.txt

# Vérifier la connexion à la base de données
python -c "from etl.core.bd import engine; print(engine)"
```

### Erreurs de base de données
- Vérifier que la base de données est en cours d'exécution
- Vérifier la variable `DATABASE_URL` dans le fichier `.env`
- S'assurer que les tables sont bien créées : `python etl/main.py`

---
