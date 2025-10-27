# Store API

A **Django REST API** for an e-commerce platform, providing functionalities for managing products, categories, carts, orders, customers, and comments.

## Project Structure

```
store_api/
├── config/                 # Project settings and configuration
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core/                   # Custom user app
│   ├── __init__.py
│   ├── admin.py
│   ├── models.py
│   └── serializers.py
├── store/                  # Main e-commerce app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── filters.py
│   ├── models.py
│   ├── paginations.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── signals.py
│   ├── urls.py
│   └── views.py
├── manage.py
└── requirements.txt
```

## Features

- **Products & Categories**
  - CRUD operations for products and categories.
  - Inventory management with critical stock filters.
  - Automatic slug generation for products.

- **Cart & Cart Items**
  - Create and manage carts.
  - Add, update, and remove items.
  - Total price calculation.

- **Orders & Order Items**
  - Create orders from carts.
  - Staff and customer-specific order views.
  - Admin can view all orders with detailed items and customer info.

- **Customer Management**
  - Automatic customer profile creation upon user registration.
  - Retrieve and update own customer profile.
  - Admin functionalities for managing customers.

- **Comments**
  - Nested comments under products.
  - Comment approval workflow.

- **Authentication & Permissions**
  - JWT authentication via `djangorestframework-simplejwt`.
  - Custom permissions like `IsAdminOrReadOnly`.
  - Djoser integration for user registration and management.

- **Pagination & Filtering**
  - Default pagination for listing endpoints.
  - Product filtering by category and inventory.
  - Search and ordering capabilities.

- **Admin Panel**
  - Advanced admin customization for products, orders, customers, and comments.
  - Inline editing and aggregated information (like number of comments).

- **Swagger / API Documentation**
  - Interactive API documentation available via Swagger.
  - Access it at `/swagger/` or `/api/docs/` depending on configuration.

## Installation

1. Clone the repository:

```bash
git clone <https://github.com/EhsanDoroudian/store_api.git>
cd store_api
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # Linux / macOS
venv\Scripts\activate     # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up environment variables in `.env`:

```
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_ENGINE=django.db.backends.mysql
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=3306
```

5. Apply migrations:

```bash
python manage.py migrate
```

6. Create a superuser:

```bash
python manage.py createsuperuser
```

7. Run the development server:

```bash
python manage.py runserver
```

Access the API at `http://127.0.0.1:8000/` and the admin panel at `http://127.0.0.1:8000/admin/`.  
Swagger documentation is available at:

- `/swagger/` – Interactive Swagger UI  
- `/redoc/` (optional) – ReDoc documentation if configured

## API Endpoints

- `/store/products/` – Products CRUD  
- `/store/categories/` – Categories CRUD  
- `/store/carts/` – Manage carts and items  
- `/store/customers/` – Customer info  
- `/store/orders/` – Orders and order items  
- `/store/products/{id}/comments/` – Product comments  

Authentication endpoints (via Djoser):

- `/auth/jwt/create/` – Login and obtain JWT token  
- `/auth/jwt/refresh/` – Refresh JWT token  
- `/auth/users/` – User registration  

## Technologies Used

- Python 3.11+
- Django 5.2.1
- Django REST Framework
- Djoser
- drf-nested-routers
- drf-yasg (Swagger API docs)
- Django Debug Toolbar (for development)
- MySQL (via `mysqlclient`)
- environs for environment variables
- factory_boy & Faker for testing

## Notes

- The project uses a **custom user model** (`core.CustomUser`) with email as unique field.  
- The folder `store_api/` is the **root project folder** containing `config/`, `core/`, and the main app `store/`.  
- The API is designed with RESTful principles, and most list endpoints are paginated.  
- Swagger UI provides an interactive interface to test all endpoints and see request/response schemas.