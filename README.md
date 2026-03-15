# Freelance Marketplace API

Mini Upwork-style backend built with Django REST Framework. It supports clients posting projects, freelancers bidding, contracts, and reviews.

## Tech Stack
- Python
- Django
- Django REST Framework
- PostgreSQL
- SimpleJWT (JWT authentication)
- drf-yasg (Swagger)
- django-filter

## Setup
1) Create a virtual environment and install dependencies:
```bash
pip install -r requirements.txt
```

2) Configure environment variables (examples):
```bash
export DJANGO_SECRET_KEY=change-me
export DJANGO_DEBUG=1
export DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost

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
- Header: `Authorization: Bearer <access>`

## Roles
- `client`: can create projects, accept bids, finish contracts, leave reviews
- `freelancer`: can place bids

## API Endpoints
### Projects
- `POST /api/projects/` (client only)
- `GET /api/projects/` (auth required, only open projects)
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
- Swagger UI: `/swagger/`
- ReDoc: `/redoc/`

## Notes
- Accepting a bid creates a contract and moves the project to `in_progress`.
- Finishing a contract marks the project as `completed`.
