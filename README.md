# Freelance Marketplace API (DRF)

Mini Upwork-style backend built with Django REST Framework. Clients post projects, freelancers bid, clients accept bids to create contracts, and clients leave reviews after completion.

## Tech Stack
- Python
- Django
- Django REST Framework
- SQLite
- JWT (SimpleJWT)
- drf-yasg (Swagger)
- django-filter
- Git

## Project Scope Note
- This repository contains the DRF implementation (`freelance-marketplace-drf`).
- The Django MVT (template-based) implementation should live in a separate repository as required by the spec.

## Setup
1. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
2. SQLite is used by default (`db.sqlite3`).
3. Run migrations:
```bash
python manage.py makemigrations users projects bids contracts reviews
python manage.py migrate
```
4. Seed test users:
```bash
python manage.py seed_test_users
```
5. (Optional) Create a superuser:
```bash
python manage.py createsuperuser
```
6. Run the server:
```bash
python manage.py runserver
```

## Authentication (JWT)
- Register: `POST /api/register/`
- Login: `POST /api/login/`
- Long-lived login: `POST /api/login/long/`
- Logout: `POST /api/logout/` (blacklists refresh token)
- Header: `Authorization: Bearer <access>`

## Test Users
- Client: `client1` / `client123`
- Freelancer: `freelancer1` / `freelancer123`

## API Endpoints
### Projects
- `POST /api/projects/` (client only)
- `GET /api/projects/` (auth required, open projects only)
- `GET /api/projects/{id}/`

Filters for project list:
- `?search=keyword`
- `?budget__gte=100&budget__lte=1000`

### Bids
- `POST /api/projects/{id}/bid/` (freelancer only)
- `GET /api/projects/{id}/bids/` (project owner only)
- `POST /api/bids/{id}/accept/` (project owner only)

### Contracts
- `GET /api/contracts/` (client/freelancer)
- `POST /api/contracts/{id}/finish/` (client only)

### Reviews
- `POST /api/contracts/{id}/review/` (client only, contract must be finished)

## Swagger
- Swagger UI: `http://127.0.0.1:8000/swagger/`
- ReDoc: `http://127.0.0.1:8000/redoc/`

## Postman
- Postman collection: [Freelance-Marketplace.postman_collection.json](postman/Freelance-Marketplace.postman_collection.json)
- Import the collection and set variables:
  - `baseUrl` (example: `http://127.0.0.1:8000`)
  - `token` (JWT access token)

## Business Logic Notes
- Accepting a bid creates a contract and moves the project to `in_progress`.
- Finishing a contract marks the project as `completed`.
- Freelancers can bid only once per project.
