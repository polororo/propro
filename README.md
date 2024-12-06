# Système de Gestion de Catalogue 🏪

## Description
Application de gestion de catalogue développée en Python avec interface graphique PyQt6. Cette application permet de gérer un catalogue de produits avec un système d'authentification sécurisé.

## Fonctionnalités ✨

### Authentification et Sécurité 🔐
- Connexion utilisateur
- Inscription
- Authentification à deux facteurs
- Vérification sécurisée des mots de passe

### Gestion des Produits 📦
- Affichage du catalogue complet
- Création de nouveaux produits
- Modification des produits existants
- Suppression de produits
- Recherche et filtrage

## Installation 🚀

### Prérequis
- Python 3.x
- Gestionnaire de paquets pip

```bash
pip install -r requirements.txt
```

## Démarrage ▶️

Pour lancer l'application :
```bash
python projet_python/menu.py
```

## Structure du Projet 📁
```
projet_python/
├── menu.py                    # Point d'entrée de l'application
├── database.db               # Base de données SQLite
├── afficher_catalogue.py     # Gestion de l'affichage
├── create_product.py         # Création de produits
├── update_product.py         # Mise à jour des produits
├── delete_product.py         # Suppression de produits
├── login.py                  # Système de connexion
└── sign_up.py               # Système d'inscription
```

## Dépendances 📚
requirements.txt

## Sécurité 🛡️
- Authentification à deux facteurs intégrée
- Système de logs pour le suivi des opérations
- Vérification sécurisée des mots de passe

## Login
- Mot de passe admin : SA9tV94zTtDz6mOf
- Mot de passe editor : b9re42OgC2OloG6m
-Mot de passe user : iTVwUeZQYsVHrJV1
- Mot de passe user_test : fgRJ5ThDRiwkbIog

## Base de données 💾
- Utilisation de SQLite
- Structure optimisée pour la gestion des produits
- Sauvegarde automatique des données

## Journalisation 📝
Toutes les opérations sont enregistrées dans le fichier `logs.log` 