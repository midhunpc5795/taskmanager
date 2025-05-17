#  Task Manager – Django Project

A real-time collaborative task management web application built with Django. It supports **Google OAuth2** login, **JWT-based API authentication**, **WebSocket-powered real-time updates**, and standard CRUD operations for tasks and comments.

---

##  Features

-  Google OAuth2 login via **Django Allauth**
-  Secure API access using **JWT authentication**
-  Create, update, delete tasks and comments
-  Assign users to tasks
-  Real-time updates on tasks and comments using **Django Channels**
-  Redis as the Channels backend for message brokering
-  Indexed fields for `status` and `priority` for performance

---

##  Tech Stack

- **Python** 3.13
- **Django** 5.2.1
- **Django REST Framework**
- **Django Allauth + dj-rest-auth** (OAuth2, JWT)
- **Django Channels** (WebSockets)
- **Redis** (Channels layer backend)
- **PostgreSQL** (database)

---

##  Setup Instructions

### 1. Clone & Set Up Environment

```bash
# Unzip or clone the project
cd taskmanager

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the root directory with the following content:

```env
SECRET_KEY=your-django-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# PostgreSQL
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432

# Google OAuth2
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_API_KEY=your_google_api_key
GITHUB_CLIENT_ID=client_id
GITHUB_CLIENT_SECRET=client_secret
```

>  Ensure PostgreSQL and Redis are running locally before starting the app.

### 3. Apply Migrations & Run Server

```bash
python manage.py migrate
python manage.py createsuperuser  # Optional
daphne taskmanager.asgi:application
```

---

##  Access Points

- **HTTP:** `http://127.0.0.1:8000/`
- **WebSocket (Tasks):** `ws://127.0.0.1:8000/ws/task/<task_id>/`

---

##  Running Tests

###  Run All Tests

```bash
python manage.py test core.tests
```

###  Run Only Unit Tests

```bash
python manage.py test core.tests.unit
```

###  Run Only Integration Tests

```bash
python manage.py test core.tests.integration
```


---

##  Project Structure Highlights

```bash
taskmanager/
├── core/
│   ├── models.py           # Task, Comment, UserProfile
│   ├── serializers.py      # DRF serializers
│   ├── views.py            # ViewSets for Task & Comment
│   ├── consumers.py        # WebSocket consumer
│   └── tests/
│       ├── unit/           # Unit tests
│       └── integration/    # Integration & real-time tests
├── taskmanager/
│   ├── settings.py
│   ├── urls.py
│   └── asgi.py
```

---
