# Freelance Marketplace (Mini Upwork) API

A clean and beginner-friendly Django REST Framework backend for a mini freelance marketplace.

## Tech Stack
- Python
- Django
- Django REST Framework
- PostgreSQL
- JWT Authentication (SimpleJWT)
- drf-yasg (Swagger)
- django-filter

## Setup (Step-by-step)
1) Create a virtual environment and install dependencies:
```bash
pip install -r requirements.txt
```

2) Configure PostgreSQL (example env values):
```bash
export POSTGRES_DB=freelance_marketplace
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=postgres
export POSTGRES_HOST=localhost
export POSTGRES_PORT=5432
```

3) Run migrations:
```bash
python manage.py makemigrations users projects bids contracts reviews
python manage.py migrate
```

4) Create a superuser (optional):
```bash
python manage.py createsuperuser
```

5) Run the server:
```bash
python manage.py runserver
```

## Authentication (JWT)
- Register: `POST /api/register/`
- Login: `POST /api/login/` (returns `access` and `refresh` tokens)
- Use header: `Authorization: Bearer <access>`

## API Endpoints
### Projects
- `POST /api/projects/` (client only)
- `GET /api/projects/` (open projects, search + filter + pagination)
- `GET /api/projects/{id}/`

### Bids
- `POST /api/projects/{id}/bid/` (freelancer only)
- `GET /api/projects/{id}/bids/` (project owner only)
- `POST /api/bids/{id}/accept/` (client only)

### Contracts
- `GET /api/contracts/` (client/freelancer)
- `POST /api/contracts/{id}/finish/` (client only)

### Reviews
- `POST /api/contracts/{id}/review/` (client only)

## Swagger
- Swagger UI: `/swagger/`
- ReDoc: `/redoc/`

## Test Users (Instructions)
You can create test users via API or Django shell.

Django shell:
```bash
python manage.py shell -c "from django.contrib.auth import get_user_model; User=get_user_model(); client, _ = User.objects.get_or_create(username='client1', defaults={'email':'client1@example.com','role':'client'}); client.set_password('client123'); client.save(); freelancer, _ = User.objects.get_or_create(username='freelancer1', defaults={'email':'freelancer1@example.com','role':'freelancer'}); freelancer.set_password('freelancer123'); freelancer.save();"
```

API (recommended for consistent passwords):
- Client: `username=client1`, `password=client123`
- Freelancer: `username=freelancer1`, `password=freelancer123`

Use `POST /api/register/` twice with the above data.

## Postman
Collection file: `postman/freelance_marketplace.postman_collection.json`
Set `base_url` variable (e.g. `http://127.0.0.1:8000`).

## Project Structure
```
freelance_marketplace/
    users/
    projects/
    bids/
    contracts/
    reviews/
```
