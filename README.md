# EShop - backend of online store

## 📖 Project Description

EShop is an e-commerce backend built with FastAPI and modern technology stack. The project provides a REST API for managing products, users, shopping cart, orders, and comments.

## 🚀 Key Features

- **Authentication & Authorization** - JWT tokens, OAuth2, email confirmation
- **Product Management** - CRUD operations for products and categories
- **Shopping Cart** - add, remove, batch operations
- **Order System** - create and manage orders
- **Comments & Reviews** - product comment system
- **User Management** - registration, profiles, roles (admin/user)
- **Caching** - Redis for performance improvement
- **Rate Limiting** - DDoS attack protection
- **Email Notifications** - Celery + ProtonMail for registration confirmation
- **Database Migrations** - Alembic for database schema management

## 🛠 Technology Stack

### Backend
- **FastAPI** - modern Python web framework
- **SQLAlchemy 2.0** - ORM for database operations
- **Alembic** - database migrations
- **Pydantic** - data validation and serialization
- **Uvicorn** - ASGI server
- **Python 3.13** - Python version in Docker

### Database
- **PostgreSQL** - main relational database
- **Redis** - caching

### Authentication & Security
- **JWT** - JSON Web Tokens for authentication
- **bcrypt** - password hashing
- **FastAPI Limiter** - request rate limiting

### Additional Services
- **Celery** - background tasks and message queues
- **ProtonMail API** - email notifications for registration confirmation

### Testing
- **pytest** - testing framework
- **httpx** - HTTP client for tests

## 🔒 Security & Performance

### Security
- **JWT tokens** - secure authentication
- **bcrypt** - password hashing
- **Rate limiting** - DDoS attack protection
- **CORS** - API access control
- **User roles** - admin/user permission separation

### Performance
- **Redis caching** - HTTP response acceleration
- **Asynchronous operations** - FastAPI + async/await
- **Batch operations** - batch CRUD for cart
- **Connection pooling** - efficient database connection management

## 📊 Database Structure

### Main Tables
- **users** - system users (admin/user roles, email confirmation)
- **products** - store products with categories
- **categories** - product categories
- **cart_items** - user shopping carts
- **orders** - user orders
- **comments** - product comments
- **jwt_token_pairs** - JWT tokens for authentication

### Table Relationships
- Users can have multiple products in cart
- Orders are linked to users and products
- Comments are tied to products and users
- Products belong to categories

## 🏗 Project Architecture

```
EShop/
├── app/
│   ├── api/           # API routers (FastAPI endpoints)
│   ├── auth/          # Authentication and OAuth
│   ├── core/          # Configuration and settings
│   ├── database/      # Database and Redis connections
│   ├── models/        # SQLAlchemy models (ORM)
│   ├── schemas/       # Pydantic schemas for validation
│   ├── services/      # Business logic
│   ├── tasks/         # Celery tasks (email, etc.)
│   ├── tests/         # API and service tests
│   └── utils/         # Helper utilities
├── migrations/         # Alembic database migrations
├── docker-compose.yml  # Docker configuration
├── Dockerfile         # Docker image
└── main.py            # Application entry point
```

## 🔧 How the System Works

### 1. API Structure
- **`/api/auth`** - authentication and registration
- **`/api/products`** - product management
- **`/api/categories`** - category management
- **`/api/users`** - user management
- **`/api/cart_items`** - shopping cart
- **`/api/orders`** - order system
- **`/api/comments`** - product comments

### 2. Authentication
- JWT tokens (access + refresh)
- User roles (admin/user)
- OAuth2 integration
- Protected endpoints for administrators

### 3. Caching
- Redis for HTTP responses
- Configurable cache lifetime
- Automatic updates on changes

### 4. Security
- Rate limiting for attack protection
- Input validation (Pydantic)
- Password hashing (bcrypt)
- CORS settings

## 🚀 How to Run the Project

### Prerequisites
- Docker and Docker Compose
- Python 3.13+
- .env file with settings

### 1. Clone and Setup
```bash
git clone https://github.com/marsky0/EShop
cd EShop
```

### 2. Configure .env file
```bash
# .env file already exists in repository
# Fill in the necessary environment variables
```

### 3. Run with Docker (recommended)
```bash
# Run all services in background
docker-compose up -d

# Or run with logs in terminal
docker-compose up

# View logs (if running in background)
docker-compose logs -f

# Stop
docker-compose down
```

### 4. Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Start PostgreSQL and Redis (via Docker)
docker-compose up -d db redis
# Or use local ones

# Apply migrations
alembic upgrade head

# Start application
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Start Celery worker (in separate terminal)
celery -A app.tasks worker --loglevel=info
```

## 🐳 Docker and Deployment

### Dockerfile Features
- **Python 3.13-slim** - lightweight Python image
- **Automatic migrations** - Alembic runs on container start
- **Celery + Uvicorn** - both services run in one container
- **entrypoint.sh** - initialization script with migrations and service startup

### Docker Compose Services
- **web** - main application (FastAPI + Celery)
- **db** - PostgreSQL 15 with persistent storage
- **redis** - Redis 7 for caching and queues

### Environment Variables for Docker
```bash
DATABASE_URL=postgresql://postgres:postgres@db:5432/ESHOP
REDIS_URL=redis://redis:6379/
```

### 5. Check Functionality
```bash
# API available at
http://localhost:8000

# Swagger documentation
http://localhost:8000/docs

# Alternative ReDoc documentation
http://localhost:8000/redoc
```

## 📝 API Endpoints

### 🔐 Authentication
- `POST /api/auth/register` - User registration
- `GET /api/auth/confirm/{token}` - Registration confirmation
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `POST /api/auth/refresh` - Token refresh

### 🛍️ Products
- `GET /api/products/` - List products
- `GET /api/products/{id}` - Get product by ID
- `POST /api/products/` - Create product (admin)
- `PUT /api/products/{id}` - Update product (admin)
- `DELETE /api/products/{id}` - Delete product (admin)

### 📂 Categories
- `GET /api/categories/` - List categories
- `GET /api/categories/{id}` - Get category by ID
- `POST /api/categories/` - Create category (admin)
- `PUT /api/categories/{id}` - Update category (admin)
- `DELETE /api/categories/{id}` - Delete category (admin)

### 🛒 Shopping Cart
- `GET /api/cart_items/` - View cart (admin)
- `GET /api/cart_items/{id}` - Get cart item by ID (admin)
- `GET /api/cart_items/user_id/{user_id}` - User cart
- `POST /api/cart_items/` - Add product to cart
- `POST /api/cart_items/batch/` - Batch add products
- `PUT /api/cart_items/{id}` - Update cart item
- `PUT /api/cart_items/batch/` - Batch update items
- `DELETE /api/cart_items/{id}` - Remove product from cart
- `DELETE /api/cart_items/batch/` - Batch remove products

### 📋 Orders
- `GET /api/orders/` - List orders
- `GET /api/orders/{id}` - Order details
- `POST /api/orders/` - Create order
- `PUT /api/orders/{id}` - Update order
- `DELETE /api/orders/{id}` - Delete order

### 👥 Users
- `GET /api/users/` - List users (admin)
- `GET /api/users/{id}` - User profile
- `POST /api/users/` - Create user (admin)
- `PUT /api/users/{id}` - Update user (admin)
- `DELETE /api/users/{id}` - Delete user (admin)

### 💬 Comments
- `GET /api/comments/` - List comments
- `GET /api/comments/{id}` - Get comment by ID
- `POST /api/comments/` - Create comment
- `PUT /api/comments/{id}` - Update comment
- `DELETE /api/comments/{id}` - Delete comment

## 🚀 Development and Deployment

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Start only DB and Redis
docker-compose up -d db redis

# Apply migrations
alembic upgrade head

# Start application with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Start Celery worker
celery -A app.tasks worker --loglevel=info
```

## 🔒 Environment Variables

Create a `.env` file with the following variables:

```env
# Frontend
FRONTEND_URL=http://localhost:3000

# Rate Limiting
DEFAULT_RATELIMIT_NUM=100
DEFAULT_RATELIMIT_TIME=60

# JWT
SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRES=30
REFRESH_TOKEN_EXPIRES=1440

# Database
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=ESHOP
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

# Redis
REDIS_URL=redis://localhost:6379
CACHE_EXPIRE_HTTP_RESPONSE=300

# Email
EMAIL_USER=your-email@protonmail.com
EMAIL_PASSWORD=your-email-password
```
