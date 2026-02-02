
# Playto Community Feed

A prototype **Community Feed** application built as part of the **Playto Engineering Challenge**.  
The app supports text posts, threaded comments, likes with karma-based gamification, and a dynamic leaderboard that ranks users based on karma earned in the **last 24 hours**.

---

## Tech Stack

### Backend
- Django
- Django REST Framework (DRF)
- SQLite (default, can be switched to PostgreSQL)

### Frontend
- React
- Tailwind CSS

---

## Deployed URL:
- https://playto-challenge-frontend.onrender.com/

## Screenshots

### Community Feed
![Community Feed](screenshots/feed.png)

### Leaderboard (Last 24h)
![Leaderboard](screenshots/leaderboard.png)


## How to Run Locally

---

## 1. Backend Setup (Django)

### Navigate to the backend directory
```bash
cd playto_backend
````

### Create and activate a virtual environment

```bash
python -m venv venv
```

**Windows**

```bash
venv\Scripts\activate
```

**macOS / Linux**

```bash
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is missing, install dependencies manually:

```bash
pip install django djangorestframework django-cors-headers
```

### Apply database migrations

```bash
python manage.py migrate
```

### Create a superuser (for admin access)

```bash
python manage.py createsuperuser
```

### Start the backend server

```bash
python manage.py runserver
```

The backend will be available at:

```
http://127.0.0.1:8000
```

---

## 2. Frontend Setup (React)

### Open a new terminal and navigate to the frontend directory

```bash
cd playto_frontend
```

### Install frontend dependencies

```bash
npm install
```

### Start the frontend development server

```bash
npm start
```

The frontend will be available at:

```
http://localhost:3000
```

---

## Authentication Notes

* Authentication is handled using **Django Session Authentication**
* You must be logged in via the Django Admin panel:

```
http://127.0.0.1:8000/admin/
```

* Frontend API requests include credentials to support session-based authentication:

```js
credentials: "include"
```

---

## Testing the Application

1. Log in via **Django Admin**
2. Create users, posts, and comments from the admin panel
3. Open the frontend:

   ```
   http://localhost:3000
   ```
4. Like posts and comments from the UI
5. Observe leaderboard updates (karma aggregated for the **last 24 hours only**)

---

## Features Implemented

* Text-based community posts
* Threaded (nested) comments
* Like system with concurrency-safe logic
* Karma-based gamification:

  * Post Like → +5 Karma
  * Comment Like → +1 Karma
* Dynamic leaderboard (Top 5 users, last 24 hours)

---

## Notes

* The backend remains the **source of truth** for all data
* Karma is calculated dynamically from activity history (not stored as a static field)
* Designed to avoid N+1 query issues when loading nested comments

---

