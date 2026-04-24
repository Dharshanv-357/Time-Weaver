# ⏳ TimeWeaver – AI-Powered Timetable Generation System

TimeWeaver is an **AI-powered academic timetable generation system** designed for universities.  
It uses a **Genetic Algorithm** to generate conflict-free schedules while satisfying constraints such as faculty availability, room capacity, and workload limits.

---

## 🚀 Project Overview

TimeWeaver consists of three main components:

| Component | Description |
|----------|-------------|
| **Frontend** | User interface for admin, faculty, and students |
| **Backend** | REST API with scheduling logic and business rules |
| **Database** | PostgreSQL for persistent storage |


## 🧩 System Architecture (Current)
Frontend (Express - Port 3000)
|
| pg (direct DB access)
v
PostgreSQL

Backend (FastAPI - Port 8000)
|
| asyncpg
v
PostgreSQL


---

## 🎯 Target Architecture (After Integration)
Frontend (Static UI)
|
| Axios API calls
v
Backend (FastAPI)
|
v
PostgreSQL


---

## 🛠 Tech Stack

### 🔹 Backend
- Python 3.12
- FastAPI
- Uvicorn
- PostgreSQL
- SQLAlchemy (Async)
- Alembic (Migrations)
- Pydantic
- JWT Authentication (python-jose)
- Password hashing (passlib + bcrypt)
- Testing: pytest, pytest-asyncio, pytest-cov
- Linting: Ruff

### 🔹 Frontend
- HTML, CSS, JavaScript (Vanilla)
- Express.js (Node.js)
- PostgreSQL (node-postgres)
- bcrypt
- Axios
- dotenv
- Testing: Jest, @testing-library/dom

---

## 🗄 Database

- Engine: PostgreSQL  
- Default DB: `timeweaver_db`  
- Port: 5432  
- Migration Tool: Alembic  

---

## ⚙️ Setup Instructions

### 🔹 Backend Setup

```bash
git clone https://github.com/Pranathi-N-47/timeweaver_backend.git
cd timeweaver_backend

python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate   # Linux/Mac

pip install -r requirements.txt
pip install -e .

# Setup PostgreSQL and update .env
alembic upgrade head

uvicorn app.main:app --reload
