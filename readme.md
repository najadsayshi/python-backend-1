# FastAPI Auth + CRUD App

A full stack backend app with authentication and item management, deployed on Render with a PostgreSQL database on Neon.

🔗 **Live Demo:** [https://python-backend-1-d4t3.onrender.com/](https://python-backend-1-d4t3.onrender.com/)

---

## Features

- 📝 Signup & Login with JWT authentication
- 🔐 Protected routes using Bearer tokens
- 📦 Full CRUD for items (Create, Read, Update, Delete)
- 🗄️ PostgreSQL database via Neon
- 🖥️ Frontend served directly from FastAPI (HTML/CSS/JS)
- ☁️ Deployed on Render

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI |
| Database | PostgreSQL (Neon) |
| ORM | SQLModel |
| Auth | JWT (python-jose) |
| Frontend | HTML, CSS, Vanilla JS |
| Deployment | Render |

---

## API Endpoints

| Method | Endpoint | Auth Required | Description |
|--------|----------|--------------|-------------|
| POST | `/signup` | ❌ | Register a new user |
| POST | `/login` | ❌ | Login and get JWT token |
| GET | `/profile` | ✅ | Get current user info |
| GET | `/items` | ✅ | Get all items for current user |
| POST | `/items` | ✅ | Create a new item |
| PUT | `/items/{id}` | ✅ | Update an item |
| DELETE | `/items/{id}` | ✅ | Delete an item |

---

## Getting Started

### 1. Clone the repo
```bash
git clone <your-repo-url>
cd <your-repo-name>
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

Create a `.env` file in the root directory:
```
DATABASE_URL=your_neon_postgresql_url
SECRET_KEY=your_secret_key
```

### 4. Run the app
```bash
fastapi dev main.py
```

Visit `http://127.0.0.1:8000`

---

## Project Structure

```
├── main.py          # FastAPI app, all routes
├── models.py        # SQLModel database models
├── auth.py          # JWT token creation & verification
├── db.py            # Database connection
├── requirements.txt
├── .env             # Environment variables (don't commit!)
└── frontend/        # HTML, CSS, JS files
    ├── index.html
    ├── dashboard.html
    └── style.css
```

---

## Deployment

This app is deployed on **Render** with environment variables set in the Render dashboard. The database is hosted on **Neon** (serverless PostgreSQL).