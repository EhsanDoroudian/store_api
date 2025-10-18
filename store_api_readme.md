# 🛒 Store API

![Python](https://img.shields.io/badge/python-3.11-blue)
![Django](https://img.shields.io/badge/django-5.2.1-green)
![DRF](https://img.shields.io/badge/DRF-3.16.0-orange)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

**Store API** is a **RESTful e-commerce backend** built with Django & Django REST Framework, supporting products, categories, carts, orders, customers, and comments.  

💡 Includes **JWT authentication**, **Swagger docs**, **custom permissions**, and **advanced admin panel**.  

---

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/EhsanDoroudian/store_api.git
cd store_api

# Create & activate virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment variables in .env
# (SECRET_KEY, DEBUG, ALLOWED_HOSTS, DB_ENGINE, DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run the development server
python manage.py runserver
```

---

## 🗂 Project Structure

```
store_api/
├── config/       # Project settings
├── core/         # Custom user app
├── store/        # Main e-commerce app
├── manage.py
└── requirements.txt
```

---

## 📌 API Endpoints

- `/store/products/` – Products CRUD  
- `/store/categories/` – Categories CRUD  
- `/store/carts/` – Manage carts and items  
- `/store/customers/` – Customer info  
- `/store/orders/` – Orders and order items  
- `/store/products/{id}/comments/` – Product comments  

**Authentication (Djoser & JWT)**:

- `/auth/jwt/create/` – Login  
- `/auth/jwt/refresh/` – Refresh token  
- `/auth/users/` – User registration  

---

## 📖 Swagger / API Docs

Interactive API docs are available at:

- [Swagger UI](http://127.0.0.1:8000/swagger/)  
- [ReDoc](http://127.0.0.1:8000/redoc/)  

Test endpoints directly and explore request/response schemas.

---

## ⚡ Features

- Products, categories, orders, carts, customers, comments  
- JWT authentication & custom permissions  
- Nested routers for related resources  
- Paginated endpoints & filtering  
- Admin panel with inline editing & aggregated data  
- Automatic customer creation on user signup  

---

## 🛠 Technologies

- Python 3.11+, Django 5.2.1, DRF 3.16  
- Djoser, drf-nested-routers, drf-yasg (Swagger)  
- MySQL (via `mysqlclient`)  
- factory_boy & Faker for testing