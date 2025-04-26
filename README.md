# Iseya Task Management API

## Introduction
Iseya Task Management API is a robust and secure backend service built with **FastAPI** and **PostgreSQL** to handle task management efficiently. It supports **JWT-based authentication**, **Role-Based Access Control (RBAC)**, and **full CRUD operations** with **asynchronous database queries** for high performance.

This API is designed for both **administrators** and **regular users**, enforcing proper authorization to protect data integrity. It also includes **detailed error handling, validation**, and **Swagger API documentation**.

---

## Features
- **User Authentication & JWT Authorization**
- **Role-Based Access Control (RBAC)** (Admin vs. User)
- **Task Management** (Create, Retrieve, Update, Delete)
- **Secure Password Hashing**
- **Detailed Error Handling & Validation**
- **Database Integration with PostgreSQL**
- **Fully Documented OpenAPI (Swagger UI)**
- **Modular & Scalable Code Structure**
- **Dockerized for Seamless Deployment**

---

## ⚙️ Tech Stack
- **FastAPI** (Backend Framework)
- **PostgreSQL** (Relational Database)
- **SQLAlchemy + Async Support**
- **Pydantic** (Data Validation)
- **JWT (JSON Web Tokens)** (Authentication)
- **Docker** (Containerization)
- **Render** (Deployment Platform)

---

## 🛠 Installation & Setup
### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Stormz99/iseya-task-api.git
cd iseya-task-api
```

### Create & Activate Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Configure Environment Variables
Create a `.env` file in the root directory:
```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost/iseya_db
SECRET_KEY=your_jwt_secret
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### Run Database Migrations
```bash
alembic upgrade head
```

### Start the API Server
```bash
uvicorn app.main:app --reload
```

API will be running at: `http://127.0.0.1:8000`

---

## Authentication & User Roles
- **Admin**: Full access to all tasks and users.
- **User**: Can only manage their own tasks.

### User Registration
```http
POST /auth/register
```
#### Request Body:
```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```
#### Response:
```json
{
  "id": 1,
  "email": "user@example.com",
  "role": "user"
}
```


###  User Login (JWT Token Generation)
```http
POST /auth/login
```
#### Request Body:
```json
{
  "email": "user5example.com",
  "password": "securepassword"
}
```
#### Response:
```json
{
  "access_token": "your.jwt.token",
  "token_type": "bearer"
}
```

---

## Task Management Endpoints
###  Create a Task (Authenticated User)
```http
POST /tasks/
```
#### Request Body:
```json
{
  "title": "New Task",
  "description": "Task description here",
  "due_date": "2024-04-01T12:00:00",
  "priority": "medium",
  "status": "pending"
}
```
#### Response:
```json
{
  "id": 1,
  "title": "New Task",
  "owner_id": 1
}
```

###  Retrieve All Tasks (Admin Only)
```http
GET /tasks/
```

###  Retrieve Own Tasks (Authenticated User)
```http
GET /tasks/user-tasks
```

###  Retrieve a Single Task (Owner or Admin)
```http
GET /tasks/{task_id}
```

###  Update a Task (Owner or Admin)
```http
PUT /tasks/{task_id}
```

###  Delete a Task (Owner or Admin)
```http
DELETE /tasks/{task_id}
```

---

## 🏗 Project Structure
```
app/
│── auth/          # Authentication (JWT, Hashing, Login)
│── models/        # Database Models (User, Task, Enums)
│── schemas/       # Pydantic Schemas (Validation)
│── routes/        # API Endpoints (Tasks, Auth)
│── services/      # Business Logic (Task Operations)
│── database/      # Database Connection
│── utils/         # Error Handling, Helpers
│── main.py        # Application Entry Point
```

---

##  Deployment Guide
###  Docker Setup
```bash
docker build -t iseya-task-api .
docker run -p 8000:8000 iseya-task-api
```

### 2️⃣ Deploy on Render
- Push to GitHub
- Connect Repository to Render
- Set up PostgreSQL Database
- Deploy

---

## 📄 Postman Collection
A Postman collection is available for testing authentication and task operations.
[Download Postman Collection](#)

---

## 👨‍💻 Contributing
1. Fork the repo.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit changes (`git commit -m 'Add feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Submit a Pull Request.

---

## 📜 License
This project is licensed under the **MIT License**.

---

## 🎯 Author
Developed by **Ijiola Abiodun** — Passionate about building scalable and secure APIs!


