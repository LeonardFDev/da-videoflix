# Videoflix

[🇩🇪 Deutsche Version](README_DE.MD)

## Description

This project was developed as a learning project to gain practical experience in building a modern web application using Django and the Django REST Framework. The main focus is on developing a backend with a REST API through which a provided frontend communicates with the backend.

HTTP requests are processed, and protected endpoints are secured using JWT-based authentication. Access and refresh tokens are used for this purpose and are transferred and managed between the frontend and backend via cookies.

The backend runs in a Docker container and is managed through Docker Desktop. PostgreSQL is used for database management and runs in its own dedicated Docker container.

Additionally, Redis is used as an in-memory data store for managing and executing background tasks. This allows time-consuming processes to be handled asynchronously and independently of the actual HTTP request. Redis is also deployed as a separate Docker container.

Furthermore, video files are processed and converted using FFmpeg. Time-consuming processing tasks are executed asynchronously in the background using Redis.

All required services, including the backend, PostgreSQL, and Redis, are configured and managed together using Docker and a docker-compose.yml file. This creates a structured, isolated, and reproducible development environment.

---

## Quickstart

### 1. Clone the repository

```bash
git clone https://github.com/LeonardFDev/da-videoflix.git .
```

### 2. .env
Creates a '.env' file with the contents of '.env.template'

```bash
cp .env.template .env
```

### 3. Create and start the project with docker-compose
Notes: 
- Docker desktop must be open
- Please make sure that the file is backend.entrypoint.sh saved with the End of Line Sequence LF.

```bash
docker-compose up --build
```

-> if that doesn't work, use (without "-")
```bash
docker compose up --build
```

---

# Features

* Django REST API
* JWT-based authentication using access and refresh tokens

---

# Technologies

| Technology            | Version                     |
| --------------------- | --------------------------- |
| Python                | 3.13.3                      |
| Django                | 6.1.2                       |
| Django REST Framework | 3.18.3                      |
| Django Cors Headers   | 4.9.0                       |
| Django Rq             | 4.2.0                       |
| Django-redis          | 7.0.0                       |
| Gunicorn              | 26.2.0                      |
| Psycopg2-binary       | 2.9.13                      |
| Python dotenv         | 1.2.4                       |
| Whitenoise            | 6.12.0                      |
| Database              | PostgreSQL                  |
| Authentication        | JWT-basierte Authentication |

---

# Requirements

The following software is required:

* Docker Desktop
* Python 3.13.3 or later
* pip
* Git

The project was developed on Windows.

Since this is a Django Web API, the application should generally run on other operating systems that support Python.

Supported operating systems include:

* Windows
* Linux
* macOS

---

# Django Apps

The project uses the following Django apps:

| App                   | Description                                                                                                                                     |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| `auth_app`            | Provides the API endpoints for Registration, Confirm Registration, Login, Login, Logout, refresh Token, Reset Password, and Set New Password.   |
| `video_app`           | Provides the API endpoints for video.                                                                                                           |

Additionally, the following Django components are used:

* `rest_framework`
* `rest_framework_simplejwt`
* `rest_framework_simplejwt.token_blacklist`
* `django_rq`

---

# Database

The project uses PostgreSQL as its relational database management system. The database runs in a Docker container managed through Docker Desktop, providing a locally managed database environment that is separate from the Django project.

PostgreSQL is used to create a realistic development environment and to gain practical experience working with an external database system.

The connection between Django and PostgreSQL is established using the Python package psycopg2-binary.

The database is provided and managed locally through a Docker container. Its configuration is defined in a docker-compose.yml file.

The database data is stored in a Docker volume to ensure persistence. This means that the data remains available even after the container is restarted, removed, or recreated.

---

# Migrations

Migrations manage changes to the database schema.

Create new migrations:

```bash
docker-compose exec web python manage.py makemigrations
```

Apply migrations:

```bash
docker-compose exec web python manage.py migrate
```

---

# Superuser

When creating the Docker images, a superuser is created, username and password are in the .env file

If you want to create a separate superuser, you can do it as follows:
```bash
docker-compose exec web python manage.py createsuperuser
```

The admin interface will then be available at:

```text
admin/
```

---

# Docker Container

The Docker container is started, stopped, and restarted as follows:

## Launch Docker container
```bash
docker start backend
```

## Stop Docker containers
```bash
docker stop  backend
```

## Restart Docker containers
```bash
docker restart backend
```

or via Docker desktop


By default, the application is available at:

```text
http://127.0.0.1:8000/
```

---

# Authentication

The API uses JWT-based authentication with the Django REST Framework. Access and refresh tokens are used for authentication and are transmitted between the frontend and backend via cookies.

JWT components used:

```text
Access Token
Refresh Token
```

## Token Creation

When a user logs in, an access token and a refresh token are generated. These tokens are stored in cookies and are used for authentication and renewing the authentication session.

## Authenticated Requests

Protected API requests are authenticated using the access token. The token is transmitted to the backend via a cookie and its validity is verified by the backend.

If the access token expires, the refresh token can be used to request a new access token.

Authentication is therefore handled through cookies transmitted between the frontend and backend rather than through an Authorization header.

---

# API Endpoints

The application provides the following API endpoints:

| No. | Method   | Endpoint                                        | Name               | Description                                                            |
| --- | -------- | ----------------------------------------------- | ------------------ | ---------------------------------------------------------------------- |
| 1   | POST     | `api/register/`                                 | registration       | Register user                                                          |
| 2   | GET      | `api/activate/<uidb64>/<token>`                 | activate           | Confirm user registration                                              |
| 3   | POST     | `api/login/`                                    | login              | Log in user                                                            |
| 4   | POST     | `api/logout/`                                   | logout             | Log out user                                                           |
| 5   | POST     | `api/token/refresh/`                            | token_refresh      | requested a new access token using the refresh token                   |
| 6   | POST     | `api/password_rest`                             | password_reset     | Reset user password                                                    |
| 7   | POST     | `api/password_confirm/<uidb64>/<token>`         | password_confirm   | Set a new user password                                                |
| 8   | GET      | `api/video/`                                    | video-list         | A list of all videos that have already been processed will be output   |
| 9   | GET      | `api/video/<movie_id>/<resolution>/<segment>`   | video-detail       | The video / movie is output                                            |

---

# Project Structure

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

The project contains automated tests.

Run all tests:

```bash
docker-compose exec web python manage.py test
```

Run the tests from a specific test file:

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

# Technical Highlights

* Communication between frontend and backend via a REST API
* JWT authentication using HTTP cookies
* Use of access and refresh tokens for authentication management

---

# License

© 2026 Leonard Fritzmann

All rights reserved.

This project is intended solely for learning and portfolio purposes. Use, reproduction, or redistribution of the source code is not permitted without explicit permission.

---

# Contact

For questions or feedback:

* Email: E-Mail: contact@leonard-fritzmann.de