# CiaulaWeb
Questa è un' applicazione per la pianificazione delle proprie vacanze realizzata utilizzando il framework python Django,
presentata come progetto per l'esame del corso di Tecnologie Web a Unimore.


## Tecnologie utilizzate
* Python 3.9.13
* Django 4.2
* django-crispy-forms 2.0
* reportlab 4.0.7


## Installazione/Esecuzione (GNU Linux / Mac)
* (Opzionale) È consigliato utilizzare un ambiente virtuale per Python 3 di fiducia
* Aprire un terminale ed entrare nella cartella del progetto
* Eseguire '''pip install -r requirements.txt''' per installare i pacchetti necessari
* Creare il database con '''touch db.sqlite3'''
* Lanciare '''python manage.py migrate''' per creare tutte le tabelle del database
* Eseguire '''python manage.py runserver''' per lanciare il server
* Aprire un browser a piacimento e scrivere nella barra di ricerca '''127.0.0.1:8000'''

## Installazione/Esecuzione (Windows)
* (Opzionale) È consigliato utilizzare un ambiente virtuale per Python 3 di fiducia
* Aprire un terminale ed entrare nella cartella del progetto
* Eseguire '''pip install -r .\requirements.txt''' per installare i pacchetti necessari
* Creare il database con '''fsutil file createnew db.sqlite3 0'''
* Lanciare '''python .\manage.py migrate''' per creare tutte le tabelle del database
* Eseguire '''python .\manage.py runserver''' per lanciare il server
* Aprire un browser a piacimento e scrivere nella barra di ricerca '''127.0.0.1:8000'''