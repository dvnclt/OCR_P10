# Installation et Lancement du Projet Softdesk API en local

## TOC

- [Versions](#versions)
- [Installation du Projet](#installation-du-projet)
  - [Cloner le dépôt](#étape-1-cloner-le-dépôt)
  - [Dépendances et création de l'environnement virtuel](#étape-2-dépendances-et-création-de-lenvironnement-virtuel)
    - [Si vous utilisez Poetry](#si-vous-utilisez-poetry)
    - [Si vous utilisez pip](#si-vous-utilisez-pip)
  - [Appliquer les migrations](#étape-3-appliquer-les-migrations)
  - [Créer un superuser](#étape-4-créer-un-superuser)
- [Lancement du projet en local](#lancement-du-projet-en-local)
  - [Démarrer le serveur Django](#démarrer-le-serveur-django)
  - [Accéder à l'application](#accéder-à-lapplication)

## Versions

Le projet a été réalisé avec Poetry :
- **Python 3.13**

## Installation du Projet

### Étape 1 : Cloner le dépôt

Commencez par cloner le dépôt du projet et rendez-vous à sa racine :
```bash
git clone https://github.com/dvnclt/OCR_P10
cd OCR_P10
```

### Étape 2 : Dépendances et création de l'environnement virtuel

#### Si vous utilisez Poetry :

Installez directement les dépendances depuis pyproject.toml et créer un environnement :
```bash
poetry install
```

Activez l'environnement virtuel :
```bash
poetry shell
```

#### Si vous utilisez pip :

Créez un environnement virtuel :
```bash
python -m venv env
```

Activez-le :

(Sous MacOS)
```bash
source env/bin/activate
```

(Sous Windows)
```bash
.\env\Scripts\activate
```

Installez les dépendances à partir de requirements.txt :
```bash
pip install -r requirements.txt
```

### Étape 3 : Appliquer les migrations

Une fois les dépendances installées, appliquez les migrations de la base de données
pour configurer la structure de la base de données :
```bash
python manage.py migrate
```

### Étape 4 : Créer un superuser
Si vous souhaitez accéder à l'interface d'administration Django, créez
un superutilisateur avec la commande suivante :
```bash
python manage.py createsuperuser
```

## Lancement du projet en local

### Démarrer le serveur Django

Pour lancer le serveur de développement Django, utilisez la commande suivante :
```bash
python manage.py runserver
```

### Accéder à l'application

Une fois le serveur démarré, ouvrez votre navigateur et allez à l'adresse suivante :
http://127.0.0.1:8000/

Vous pouvez également accéder à l'interface d'administration à l'adresse suivante :
http://127.0.0.1:8000/admin/