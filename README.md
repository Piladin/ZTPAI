# ZTPAI – Platforma Ogłoszeń Korepetycji

## Opis projektu

ZTPAI to aplikacja webowa umożliwiająca publikowanie i wyszukiwanie ogłoszeń korepetycji. Użytkownicy mogą rejestrować się, logować, dodawać, edytować i usuwać ogłoszenia, a także przeglądać oferty innych. System wspiera filtrowanie ogłoszeń po przedmiocie i stawce, a także zarządzanie użytkownikami przez administratora. Powiadomienia e-mail są obsługiwane asynchronicznie przez Celery.

---

## Schemat architektury

+-------------------+        HTTP/REST        +-------------------+        SQL        +-------------------+
|    Frontend       |  <------------------>  |     Backend       | <------------>   |     PostgreSQL    |
|  (React + Vite)   |                        |   (Django REST)   |                  |   (Baza danych)   |
+-------------------+                        +-------------------+                  +-------------------+
         |                                            |
         |                                            | Celery/RabbitMQ
         |                                            v
         |                                 +-------------------+
         |                                 |    Celery Worker  |
         |                                 +-------------------+
         |                                            |
         |                                            v
         |                                 +-------------------+
         |                                 |    RabbitMQ       |
         |                                 +-------------------+

---

## Instrukcja uruchomienia

### Wymagania

- Docker i Docker Compose

### 1. Klonowanie repozytorium

```bash
git clone https://github.com/Piladin/ZTPAI.git
cd ZTPAI
```
### 2. Uruchomienie aplikacji (backend + frontend + bazy)
```bash
docker-compose up --build -d
```

### Rozkład kontenetów
Backend (Django REST API) dostępny pod: http://localhost:8000/api/
Frontend (React) dostępny pod: http://localhost:8080/
Panel administracyjny Django: http://localhost:8000/admin/
Panel RabbitMQ: http://localhost:15672/ (login: user, hasło: password)
Panel pgAdmin: http://localhost:5050/ (login: admin@admin.com, hasło: newpassword)

### Domyślne konta
Admin: admin/admin
User: user/password


### Dobór technologii 

Django + Django REST Framework

React + Vite

PostgreSQL

Celery + RabbitMQ

Docker + Docker Compose
