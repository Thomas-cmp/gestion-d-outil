# Gestion des Outils - Projet Python

## Description
Ce projet est une application de gestion des outils pour les Team Leaders, permettant l'affectation et le retour des outils utilisés par les opérateurs. L'interface utilisateur est développée en Python avec `tkinter`, et les données sont stockées dans une base SQLite.

## Fonctionnalités principales
- **Connexion Team Leader** : Accès sécurisé via un identifiant.
- **Gestion des outils** : Affectation et retour d'outils.
- **Gestion des utilisateurs** : Recherche et validation des opérateurs.
- **Base de données SQLite** : Stockage des informations des utilisateurs, outils et affectations.
- **Interface graphique (GUI)** : Développée avec `tkinter`.
- **Envoi d'e-mails** : Notifications via `win32com.client` pour Outlook.

## Installation
### Prérequis
- Python 3.x installé

### Installation du projet
1. Clonez le dépôt ou téléchargez le projet.
2. Lancez la commande pour installer les dependances depuis le terminal :
   ```bash
   python pip install -r requirements.txt
   ```
4. Placez l'image `cmp_logo.png` dans le dossier principal.
5. Lancez le script principal :
   ```bash
   python C:\Users\votre_non\Desktop\gestion d'outil> python ajouter_operateur.py.py
   ```

## Utilisation
### Connexion
- L'utilisateur doit scanner son badge ou entrer son ID.
- Seuls les `Team Leaders` ont accès à l'application.

### Menu principal
Une fois connecté, l'utilisateur peut :
- Affecter un outil
- Retourner un outil
- Gérer les outils et utilisateurs
- Se déconnecter

### Affectation d'un outil
1. Rechercher un opérateur par son ID ou son nom.
2. Filtrer et sélectionner un outil disponible.
3. Confirmer l'affectation.

## Technologies utilisées
- **Langage** : Python
- **GUI** : Tkinter
- **Base de données** : SQLite
- **Gestion des images** : PIL (Pillow)
- **Emails** : `win32com.client` (Outlook)

## Licence
Ce projet est sous licence MIT.

## Auteur
- [Votre Nom]

# Projet de Gestion des Retours d'Outils

## Description
Ce projet est une interface graphique en Python utilisant Tkinter pour gérer le retour des outils prêtés aux opérateurs. Il permet :
- La recherche d'un opérateur via son ID
- L'affichage des outils actuellement affectés à un opérateur
- Le retour d'un outil avec mise à jour de la base de données
- La déclaration d'un outil en réparation avec notification par e-mail

## Technologies utilisées
- **Langage** : Python
- **Bibliothèques** :
  - Tkinter (Interface utilisateur)
  - SQLite3 (Base de données)
  - Win32com (Envoi d'email via Outlook)

## Installation
### Prérequis
- Python 3.x installé
- Outlook configuré sur la machine (pour l'envoi des e-mails)

### Étapes d'installation
1. **Cloner le dépôt**
```bash
   git clone <URL_DU_REPO>
   cd <NOM_DU_PROJET>
```

2. **Installer les dépendances**
```bash
   pip install pywin32
```

3. **Exécuter le programme**
```bash
   python main.py
```

## Fonctionnalités principales
### 1. Recherche d'un opérateur
- L'utilisateur entre l'ID de l'opérateur.
- La liste des outils affectés est affichée.

### 2. Retour d'un outil
- Sélection de l'outil à retourner.
- Mise à jour automatique de la base de données.

### 3. Déclaration d'un outil à réparer
- Sélection de l'outil à déclarer en réparation.
- Mise à jour de la base de données et envoi d'un e-mail à la maintenance.

## Base de données
- **Table `outils`** : Contient les informations sur les outils.
- **Table `affectations`** : Gère les prêts et retours des outils.

## Auteur
[Votre Nom]  
[Votre Email]  

## Licence
Ce projet est sous licence [Nom de la licence].

# Gestion des Utilisateurs - Application Python

## Description
Cette application permet de gérer les utilisateurs d'un système de gestion des outils. Elle offre des fonctionnalités pour afficher, ajouter, modifier et supprimer des utilisateurs à l'aide d'une interface graphique développée avec Tkinter et d'une base de données SQLite.

## Fonctionnalités
- Affichage d'une liste des utilisateurs avec un tableau interactif (Treeview).
- Ajout d'un nouvel utilisateur avec un identifiant, un nom, un prénom et un rôle.
- Modification des informations d'un utilisateur existant.
- Suppression d'un utilisateur après confirmation.
- Interface intuitive avec des boutons d'action et un design agréable.

## Prérequis
Avant d'exécuter l'application, assurez-vous d'avoir les éléments suivants installés :

- Python 3.x
- Tkinter (inclus par défaut avec Python)
- SQLite3 (inclus par défaut avec Python)

## Installation
1. Clonez le dépôt ou téléchargez les fichiers sources :
   ```bash
   git clone https://github.com/votre-repository.git
   cd votre-repository
   ```
2. Assurez-vous que votre base de données SQLite (`gestion_outils.db`) contient une table `utilisateurs` avec la structure suivante :
   ```sql
   CREATE TABLE utilisateurs (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       nom TEXT NOT NULL,
       prenom TEXT NOT NULL,
       role TEXT NOT NULL
   );
   ```
3. Exécutez le script principal :
   ```bash
   python gestion_utilisateurs.py
   ```

## Utilisation
1. Lancez l'application.
2. Ajoutez, modifiez ou supprimez des utilisateurs selon vos besoins.
3. Naviguez facilement entre les pages grâce aux boutons de gestion.

## Technologies utilisées
- **Langage** : Python
- **Bibliothèques** : Tkinter, SQLite3
- **Base de données** : SQLite

## Auteur
- Nom : [Votre Nom]
- Contact : [Votre Email]

## Licence
Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.

