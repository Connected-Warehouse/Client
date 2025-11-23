# Python Socket Client - Gestion de Scénarios de Packages

## Description

Ce projet fournit un **client Python** pour interagir avec un serveur via sockets. Il permet d'exécuter différents scénarios de gestion de colis (`ADD`, `READ`, `MODIFY`, `DELETE`) pour tester ou automatiser les flux de traitement des packages.

Le client inclut :

* Gestion automatique de la connexion au serveur.
* Gestion des erreurs et messages reçus.
* Plusieurs scénarios prêts à l'emploi pour tester différentes situations.
* Support pour des scénarios complexes ou des envois volumineux.

## Prérequis

* Python 3.8 ou supérieur
* Modules Python utilisés :

  * `time`
  * `datetime`
  * `client.SocketClient` (votre module de client socket)
  * `client.listener.MyListener` (classe de listener pour gérer les événements)

## Installation

1. Clonez le dépôt ou téléchargez les fichiers du projet.
2. Assurez-vous que le serveur cible est accessible à l'adresse définie (`HOST` et `PORT` dans le code).
3. Installez les dépendances nécessaires si votre `SocketClient` en requiert (non incluses dans ce projet par défaut).

## Structure du projet

```
client/
│
├─ SocketClient.py        # Classe principale de communication avec le serveur
├─ listener/
│   └─ MyListener.py      # Classe de base pour écouter les événements
main.py                   # Script principal avec scénarios et CLI
```

## Utilisation

Lancez le client avec :

```bash
python main.py
```

Vous serez alors invité à choisir un scénario depuis le menu :

```
=== MENU SCÉNARIOS ===
1: Ajout puis suppression d'un colis
2: Ajout, modification, lecture, suppression
3: Lire un colis inexistant
4: Tentative d'ajout sans infos obligatoires
5: Ajout, puis suppression d'un colis sans source ni destination
6: Envoi d'une trop grosse requête
q: Quitter
```

### Exemple de scénario

**Scénario 1** :

1. Ajout d’un colis.
2. Lecture du colis ajouté.
3. Suppression du colis.

Chaque étape attend une validation de l'utilisateur avant de continuer (`Appuyez sur Entrée pour continuer...`).

## Fonctions principales

### `ScenarioListener`

* Gère les événements :

  * `on_connected()` : affichage de la connexion au serveur
  * `on_disconnected()` : affichage de la déconnexion
  * `on_received(message)` : affichage des messages reçus
  * `on_error(error)` : affichage des erreurs

### `safe_send(client, listener, message, host, port, timeout)`

* Envoie un message au serveur en s’assurant que le client est connecté.
* Tente une reconnexion automatique en cas de besoin.
* Gère les erreurs d’envoi.

## Scénarios disponibles

| N° | Description                                                |
| -- | ---------------------------------------------------------- |
| 1  | Ajout puis suppression d’un colis                          |
| 2  | Ajout, modification, lecture, suppression                  |
| 3  | Lecture d’un colis inexistant                              |
| 4  | Tentative d’ajout sans informations obligatoires           |
| 5  | Ajout et suppression d’un colis sans source ni destination |
| 6  | Envoi d’une requête volumineuse pour tester le serveur     |

## Personnalisation

* `TERMINAL_NAME` : Identifiant du terminal client
* `PACKAGE_CODE` : Code du colis utilisé dans les scénarios
* `HOST` / `PORT` : Adresse et port du serveur

Vous pouvez modifier ces constantes directement dans le script `main.py` pour l’adapter à votre environnement.

## Remarques

* Les scénarios utilisent des pauses (`input()`) pour permettre de suivre les étapes pas à pas.
* Le client peut être adapté pour des scripts automatisés en supprimant les `input()` si nécessaire.
* Ce client est conçu pour des tests et des démonstrations et suppose que le serveur respecte le protocole attendu.
* On part ici du principe que le serveur se trouve en "127.0.0.1" au port 8888
