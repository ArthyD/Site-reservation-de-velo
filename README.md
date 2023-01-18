# Boite Clef BDD IMT Atlantique

Projet étudiant pour la réservation de vélos mis à disposition par l'association : bureau du développement durable de IMT Atlantique

## Pour commencer

La partie Arduino est faite pour un Arduino MKR1010 en connexion avec un réseau nécessitant une authetification WPA/WPA2 d'entreprise. 

### Installation

Partie serveur 

_Python_: Executez la commande ``pip install -r ./requirements.txt``

Avant de lancer le serveur il faut initialiser certaines variables d'environnement :
  - ``export ADMIN_NAME="nameAdmin"``
  - ``export ADMIN_PWD="passwordAdmin"``
  - ``export HASH_METHOD="sha256"``

Partie Arduino

_Library nécessaire_ :
  - SPI.h
  - WiFiNINA.h
  - WiFiUdp.h

Le type de carte est Arduino SAMD, pour programmer ces cartes : [documentation officielle arduino](https://docs.arduino.cc/hardware/mkr-wifi-1010)



## Démarrage

Démarrer le serveur : Executez la commande ``python ./veloBDD/main.py``

Démarrer Arduino : entrer le nom du réseau et les identifiants et mot de passe dans le fichier _arduino_secrets.h_ puis téléverser les codes

## Fabriqué avec

* [Python Flask](https://flask.palletsprojects.com/en/2.0.x/) - Framework python (back-end)
* [Bootsrap](https://getbootstrap.com/) - Framework CSS et JavaScript (front-end)
* [IDE Arduino](https://www.arduino.cc/en/software) - IDE pour Arduino

