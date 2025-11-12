# Digital Bank

ApiRest built with Django Rest Framework 3.14.0 and Django 4.2.5

# ERD

<p align="center">
           <img src="https://lucid.app/publicSegments/view/f56589fc-8908-4c80-9de7-cb3e682dfdb9/image.png"/>
</p>

# Getting Started

## Prerequisites

- Git
- **Option A (Docker):** Docker and Docker Compose installed
- **Option B (Local):** Python 3.8+, PostgreSQL 12+, and pip

## Clone Repository

```bash
git clone https://github.com/jewelazo/digital_bank.git
cd digital_bank
```

## Option A: Docker Setup (Recommended)

### 1. Configure Environment Variables

Create a `.env` file following the `.env.example` template:

```bash
cp .env.example .env
```

**Important:** For Docker, set `DATABASE_HOST=db` in your `.env` file.

### 2. Build and Start Services

```bash
docker compose up --build
```

This will start:

- **Web application** on [http://localhost:8000](http://localhost:8000)
- **PostgreSQL database** on port 5434 (internal: 5432)

### 3. Run Migrations

In a new terminal, run:

```bash
docker compose exec web python manage.py migrate
```

### 4. Create Superuser

```bash
docker compose exec web python manage.py createsuperuser
```

### 5. Access the Application

- **API Documentation (Swagger):** [http://127.0.0.1:8000/apidocs/](http://127.0.0.1:8000/apidocs/)
- **Admin Panel:** [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

### Useful Docker Commands

```bash
# Stop services
docker compose down

# View logs
docker compose logs -f

# Rebuild after dependency changes
docker compose up --build

# Run tests
docker compose exec web pytest
```

---

## Option B: Local Development Setup

### 1. Create Virtual Environment

```bash
python -m venv .venv
```

### 2. Activate Virtual Environment

**Linux/Mac:**

```bash
source .venv/bin/activate
```

**Windows:**

```bash
.\.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Database

Create a PostgreSQL database and configure your `.env` file following `.env.example` as template.

**Important:** For local development, set `DATABASE_HOST=localhost` in your `.env` file.

### 5. Run Migrations

```bash
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

### 7. Start Development Server

```bash
python manage.py runserver
```

### 8. Access the Application

- **API Documentation (Swagger):** [http://127.0.0.1:8000/apidocs/](http://127.0.0.1:8000/apidocs/)
- **Admin Panel:** [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

---

## API Authentication

All endpoints require JWT authentication (except `/api/token/` and documentation).

Add your token in this format:

```
Authorization: Bearer {{your_token}}
```

## Running Tests

**Docker:**

```bash
docker compose exec web pytest
```

**Local:**

```bash
pytest
```

## Internationalization (i18n)

This project supports multiple languages. Translation files are located in the `locale/` directory.

### Compile Translations

After modifying translation files (`.po` files), you need to compile them to `.mo` files:

**Docker:**

```bash
docker compose exec web python manage.py compilemessages
```

**Local:**

```bash
python manage.py compilemessages
```

### Update Translation Files

To extract new translatable strings from the codebase:

**Docker:**

```bash
docker compose exec web python manage.py makemessages -l es
```

**Local:**

```bash
python manage.py makemessages -l es
```

**Note:** Available languages: Spanish (es)
