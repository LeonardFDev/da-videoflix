# Videoflix

[🇬🇧 English version](README.MD)

## Beschreibung

Dieses Projekt wurde als Lernprojekt entwickelt, um die Entwicklung einer modernen Webanwendung mit Django und dem Django REST Framework praxisnah zu erlernen. Im Fokus steht die Entwicklung eines Backends mit einer REST API, über die ein bereitgestelltes Frontend mit dem Backend kommuniziert.

Dabei werden HTTP-Anfragen verarbeitet und geschützte Endpunkte mithilfe einer JWT-basierten Authentifizierung abgesichert. Hierfür kommen Access- und Refresh-Tokens zum Einsatz, die über Cookies zwischen Frontend und Backend übertragen und verwaltet werden.

Das Backend wird mit Docker betrieben und über Docker Desktop verwaltet. Für die Datenbankverwaltung kommt PostgreSQL zum Einsatz, das ebenfalls in einem eigenen Docker-Container ausgeführt wird.

Zusätzlich wird Redis als In-Memory-Datenspeicher für die Verwaltung und Ausführung von Hintergrundaufgaben (Background Tasks) verwendet. Dadurch können zeitintensive Prozesse asynchron und unabhängig von der eigentlichen HTTP-Anfrage verarbeitet werden. Auch Redis wird als separater Docker-Container bereitgestellt.

Außerdem werden Videodateien mithilfe von FFmpeg verarbeitet und konvertiert. Die zeitintensiven Verarbeitungsschritte werden über Redis asynchron im Hintergrund ausgeführt.

Die benötigten Dienste, darunter das Backend, PostgreSQL und Redis, werden mithilfe von Docker und einer docker-compose.yml-Datei gemeinsam konfiguriert und verwaltet. Dadurch entsteht eine übersichtliche, voneinander getrennte und reproduzierbare Entwicklungsumgebung.

---

## Quickstart

### 1. Repository klonen

```bash
git clone https://github.com/LeonardFDev/da-videoflix.git .
```

### 2. .env
Erstellt eine `.env`-Datei mit dem Inhalt von `.env.template`

```bash
cp .env.template .env
```

### 3. Erstellen und starten des Projekts mit docker-compose
Hinweise: 
- Der Docker-Desktop muss geöffnet sein
- Bitte stelle sicher, dass die Datei backend.entrypoint.sh mit der End of Line Sequence LF abgespeichert ist.

```bash
docker-compose up --build
```

-> falls das nicht funktioniert, verwende (ohne "-")
```bash
docker compose up --build
```

---

# Features

* Django REST API
* JWT-basierte Authentifizierung mit Access- und Refresh-Tokens
* Asynchrone Verarbeitung von Hintergrundaufgaben
* Verwaltung und Speicherung von Anwendungsdaten in PostgreSQL
* Videodateien konvertieren und verarbeiten

---

# Technologien

| Technologie           | Version                        |
| --------------------- | ------------------------------ |
| Python                | 3.13.3                         |
| Django                | 6.1.2                          |
| Django REST Framework | 3.18.3                         |
| Django Cors Headers   | 4.9.0                          |
| Django Rq             | 4.2.0                          |
| Django-redis          | 7.0.0                          |
| Gunicorn              | 26.2.0                         |
| Psycopg2-binary       | 2.9.13                         |
| Python dotenv         | 1.2.4                          |
| Whitenoise            | 6.12.0                         |
| Datenbank             | PostgreSQL                     |
| Authentifizierung     | JWT-basierte Authentifizierung |

---

# Voraussetzungen

Folgende Software wird benötigt:

* Docker Desktop
* Python 3.13.3 oder höher
* pip
* Git

Das Projekt wurde unter Windows entwickelt.

Da es sich um eine Django Web API handelt, sollte die Anwendung grundsätzlich auch unter anderen Betriebssystemen mit Python-Unterstützung lauffähig sein.

Mögliche Betriebssysteme:

* Windows
* Linux
* macOS

---

# Django Apps

Das Projekt verwendet folgende Django Apps:

| App                   | Beschreibung                                                                                          |
| --------------------- | ----------------------------------------------------------------------------------------------------- |
| `auth_app`            | Stellt die API-Endpunkte für Registrierung, Registrierung bestätigen, Anmeldung, Abmeldung, Token Aktualisieren, Passwort zurücksetzen und neues passwort setzten bereit.   |
| `video_app`           | Stellt die API-Endpunkte für Video bereit.                                                            |

Zusätzlich werden folgende Django-Komponenten verwendet:

* `rest_framework`
* `rest_framework_simplejwt`
* `rest_framework_simplejwt.token_blacklist`
* `django_rq`

---

# Datenbank

Das Projekt verwendet PostgreSQL als relationales Datenbankmanagementsystem. Die Datenbank wird über Docker Desktop in einem Container betrieben und ermöglicht eine vom Django-Projekt getrennte, lokal verwaltete Datenbankumgebung.

PostgreSQL wird verwendet, um eine realitätsnahe Entwicklungsumgebung zu schaffen und den Umgang mit einer externen Datenbank zu erlernen.

Die Verbindung zwischen Django und PostgreSQL erfolgt über das Python-Paket psycopg2-binary.

Die Datenbank wird lokal über einen Docker-Container bereitgestellt und verwaltet. Die Konfiguration erfolgt über eine docker-compose.yml-Datei.

Die Datenbankdaten werden über ein Docker-Volume persistent gespeichert, sodass sie auch nach dem Neustart oder Entfernen des Containers erhalten bleiben.

---

# Migrationen

Migrationen verwalten Änderungen an der Datenbankstruktur.

Neue Migration erstellen:

```bash
docker-compose exec web python manage.py makemigrations
```

Migrationen anwenden:

```bash
docker-compose exec web python manage.py migrate
```

---

# Superuser

Beim Erstellen der Docker-Images wird ein Superuser erstellt, Benutzername und Passwort befinden sich in der .env-Datei

Falls man einen seperaten superuser erstellen möchte, geht das wie folgt:
```bash
docker-compose exec web python manage.py createsuperuser
```

Danach ist der Admin-Bereich erreichbar unter:

```text
admin/
```

---

# Docker Container

Der Docker-Container wird wie folgt gestartet, gestoppt und neu gestartet:

## Docker-Container Starten
```bash
docker start backend
```

## Docker-Container Stoppen
```bash
docker stop  backend
```

## Docker-Container Neustarten
```bash
docker restart backend
```

oder über Docker desktop


Standardmäßig ist die Anwendung erreichbar unter:

```text
http://127.0.0.1:8000/
```

---

# Authentifizierung

Die API verwendet eine JWT-basierte Authentifizierung über das Django REST Framework. Für die Authentifizierung werden Access- und Refresh-Tokens verwendet, die über Cookies zwischen Frontend und Backend übertragen werden.

Verwendete JWT-Komponenten:

```text
Access Token
Refresh Token
```

## Token-Erstellung

Bei der Anmeldung eines Benutzers werden ein Access Token und ein Refresh Token erstellt. Diese werden in Cookies gespeichert und für die Authentifizierung bzw. Erneuerung der Authentifizierung verwendet.

## Authentifizierte Anfragen

Geschützte API-Anfragen werden mithilfe des Access Tokens authentifiziert. Das Token wird über das Cookie an das Backend übermittelt und vom Backend auf seine Gültigkeit überprüft.

Ist das Access Token abgelaufen, kann mithilfe des Refresh Tokens ein neues Access Token angefordert werden.

Die Authentifizierung erfolgt somit nicht über einen Authorization-Header, sondern über die zwischen Frontend und Backend übertragenen Cookies.

---

# API Endpunkte

Die Anwendung stellt folgende API-Endpunkte bereit:

| Nr. | Methode  | Endpunkt                                        | Name               | Beschreibung                                                         |
| --- | -------- | ----------------------------------------------- | ------------------ | -------------------------------------------------------------------- |
| 1   | POST     | `api/register/`                                 | registration       | Benutzer registrieren                                                |
| 2   | GET      | `api/activate/<uidb64>/<token>`                 | activate           | Benutzerregistrierung bestätigen                                     |
| 3   | POST     | `api/login/`                                    | login              | Benutzer einloggen                                                   |
| 4   | POST     | `api/logout/`                                   | logout             | Benutzer ausloggen                                                   |
| 5   | POST     | `api/token/refresh/`                            | token_refresh      | mit Hilfe des Refresh-Tokens einen neuen Zugriffstoken angefordert   |
| 6   | POST     | `api/password_rest`                             | password_reset     | Benutzerpasswort zurücksetzen                                        |
| 7   | POST     | `api/password_confirm/<uidb64>/<token>`         | password_confirm   | Ein neues Benutzerpasswort setzen                                    |
| 8   | GET      | `api/video/`                                    | video-list         | Eine Liste aller bereits verarbeiteten Videos wird ausgegeben        |
| 9   | GET      | `api/video/<movie_id>/<resolution>/<segment>`   | video-detail       | Das Video / der Film wird ausgegeben                                 |

---

# Projektstruktur

```text
Videoflix
│
├── .dogerignore
├── .gitignore
├── .env
├── .env.template
├── backend.Dockerfile
├── backend.entrypoint.sh
├── docker-compose.yml
├── manage.py
├── requirements.txt
├── README.MD
├── README_DE.MD
|
├── services/tasks
|    ├── convert_video.py
|    ├── create_confirm_email.py
|    ├── create_password_reset_email.py
|    ├── create_thumbnail.py
|    └── delete_unactivated_user.py
|
├── templates/emails
|    ├── confirm_email.py
|    └── password_reset_email.py
│
├── tests
|    └── helpers.py
|
├── core
│   ├── settings.py
|   ├── authentication.py
|   ├── test_runner.py
│   └── urls.py
│
├── auth_app
│   ├── migrations/
│   ├── tests
|   |   ├── test_activate_user.py
|   |   ├── test_login.py
|   |   ├── test_logout.py
|   |   ├── test_password_confirm.py
|   |   ├── test_password_reset.py
|   |   ├── test_registration.py
|   |   ├── test_token_refresh.py
|   |
|   └── api
|       ├── serializers.py
|       ├── urls.py
|       └── views.py
│
└── video_app
    ├── models.py
    ├── admin.py
    ├── migrations/
    ├── api
    |   ├── serializers.py
    |   ├── urls.py
    |   └── views.py
    |
    └── tests
        ├── test_video_detail.py
        ├── test_video_list.py
        └── file_to_test
             └── test_video.mp4
```

---

# Tests

Das Projekt enthält automatisierte Tests.

Alle Tests ausführen:

```bash
docker-compose exec web python manage.py test
```

Nur die Tests einer bestimmten Testdatei ausführen:

```bash
docker-compose exec web python manage.py test "auth_app.tests.test_activate_user"
```

```bash
docker-compose exec web python manage.py test "auth_app.tests.test_login
```

```bash
docker-compose exec web python manage.py test "auth_app.tests.test_logout
```

```bash
docker-compose exec web python manage.py test "auth_app.tests.test_password_confirm
```

```bash
docker-compose exec web python manage.py test "auth_app.tests.test_password_reset
```

```bash
docker-compose exec web python manage.py test "auth_app.tests.test_registration
```

```bash
docker-compose exec web python manage.py test "auth_app.tests.test_token_refresh
```

```bash
docker-compose exec web python manage.py test "auth_app.tests.test_video_detail
```

```bash
docker-compose exec web python manage.py test "auth_app.tests.test_video_list
```

---

# Technische Besonderheiten

* Kommunikation zwischen Frontend und Backend über eine REST API
* JWT-Authentifizierung über HTTP-Cookies
* Verwendung von Access- und Refresh-Tokens zur Verwaltung der Authentifizierung
* PostgreSQL als relationales Datenbanksystem
* Redis als In-Memory-Datenspeicher für Hintergrundaufgaben
* Docker-basierte Entwicklungsumgebung mit Docker Compose, Dockerfile und Entrypoint-Skript für Backend, PostgreSQL und Redis
* FFmpeg zur Videoverarbeitung

---

# Lizenz

© 2026 Leonard Fritzmann

Alle Rechte vorbehalten.

Dieses Projekt dient ausschließlich Lern- und Portfoliozwecken. Eine Nutzung, Vervielfältigung oder Weitergabe des Quellcodes ist ohne ausdrückliche Genehmigung nicht gestattet.

---

# Kontakt

Bei Fragen oder Anmerkungen:

* E-Mail: contact@leonard-fritzmann.de