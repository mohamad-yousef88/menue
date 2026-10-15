# Djaj Wa Toom — Menu Management Backend

A professional, scalable FastAPI backend for restaurant menu management with Clean Architecture, JWT authentication, image hosting via Cloudinary, a web-based admin dashboard, and a customer-facing public menu page accessible via QR code.

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Architecture](#-architecture)
- [Project Structure](#-project-structure)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Environment Variables](#-environment-variables)
- [Running the Application](#-running-the-application)
- [First-Time Setup](#-first-time-setup)
- [API Documentation](#-api-documentation)
- [Web Pages](#-web-pages)
- [Authentication Flow](#-authentication-flow)
- [Cloudinary Integration](#-cloudinary-integration)
- [Database Management](#-database-management)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Brand Identity](#-brand-identity)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

**Djaj Wa Toom** is a complete backend solution for restaurant menu management. It provides:

- A **REST API** for programmatic access and future expansion.
- A **Web-based admin dashboard** built with Jinja2 + Tailwind CSS, protected by JWT authentication.
- A **Public menu page** accessible via QR code — customers scan the QR code placed on tables to browse the live menu instantly.

The application follows **Clean Architecture** principles and **SOLID** design patterns, making it easy to maintain, test, and extend.

---

## ✨ Features

### Admin Features

- 🔐 JWT-based authentication with HTTP-only cookies
- 📋 Create, update, delete, and manage multiple menus
- 🍔 Full CRUD for menu items with categories, prices, and descriptions
- 🖼️ Image upload with automatic Cloudinary hosting
- 🎨 Featured items and availability flags
- 🔢 Custom sort order for items
- 🔳 QR code generator for printing on tables
- 📅 Date-based menus (seasonal / holiday menus)

### Customer Features

- 📱 Mobile-responsive public menu page
- 🔍 Category-based filtering
- ⚡ Fast loading (lightweight HTML + Tailwind CSS)
- 🚫 No authentication required
- 🔄 Always shows the latest menu (no reprint needed)

### Technical Features

- 🏗️ Clean Architecture (Models → Repositories → Services → API)
- 🔑 Password hashing with bcrypt + SHA-256
- 🌐 CORS support
- 📝 Full OpenAPI / Swagger documentation
- 🐳 Docker-ready
- 🗄️ Support for both PostgreSQL (production) and SQLite (development)

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|------------|
| Backend Framework | FastAPI 0.109 |
| Server | Uvicorn |
| ORM | SQLAlchemy 2.0 |
| Database | PostgreSQL / SQLite |
| Authentication | PyJWT + bcrypt |
| Image Hosting | Cloudinary |
| Templating | Jinja2 |
| CSS Framework | Tailwind CSS (CDN) |
| Interactivity | HTMX + Alpine.js |
| Fonts | Google Fonts (Cairo) |
| Language | Python 3.11+ |

---

## 🏛 Architecture

The project follows **Clean Architecture** with strict separation of concerns:

```
┌─────────────────────────────────────────────────┐
│                  API Layer                       │
│  (FastAPI routers — HTTP handling only)         │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│               Service Layer                      │
│  (Business logic — no HTTP, no SQL)             │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│             Repository Layer                     │
│  (Data access — SQL queries only)                │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│               Model Layer                        │
│  (SQLAlchemy — database tables)                  │
└─────────────────────────────────────────────────┘
```

### SOLID Principles Applied

- **S** — Single Responsibility: Each layer has one job.
- **O** — Open/Closed: Repositories are extensible without modification.
- **L** — Liskov Substitution: `BaseRepository` works with any model.
- **I** — Interface Segregation: Specialized repositories per entity.
- **D** — Dependency Inversion: Services depend on repositories, not the reverse.

---

## 📁 Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                       # App entry point
│   │
│   ├── core/                         # Cross-cutting concerns
│   │   ├── config.py                 # Settings via pydantic-settings
│   │   ├── database.py               # SQLAlchemy engine & session
│   │   ├── security.py               # JWT + password hashing
│   │   └── exceptions.py             # Custom HTTP exceptions
│   │
│   ├── models/                       # SQLAlchemy models
│   │   ├── menu.py
│   │   ├── menu_item.py
│   │   └── user.py
│   │
│   ├── schemas/                      # Pydantic schemas (DTOs)
│   │   ├── menu.py
│   │   ├── menu_item.py
│   │   └── auth.py
│   │
│   ├── repositories/                 # Data access layer
│   │   ├── base.py
│   │   ├── menu_repository.py
│   │   ├── menu_item_repository.py
│   │   └── user_repository.py
│   │
│   ├── services/                     # Business logic
│   │   ├── menu_service.py
│   │   ├── menu_item_service.py
│   │   ├── image_service.py
│   │   └── auth_service.py
│   │
│   ├── api/                          # REST API (JSON)
│   │   ├── deps.py
│   │   └── v1/
│   │       ├── router.py
│   │       ├── auth.py
│   │       ├── menus.py
│   │       └── items.py
│   │
│   ├── web/                          # Jinja2 Web UI
│   │   ├── deps.py
│   │   ├── routes/
│   │   │   ├── public.py
│   │   │   ├── auth.py
│   │   │   ├── dashboard.py
│   │   │   ├── menus.py
│   │   │   └── items.py
│   │   └── templates/
│   │       ├── base.html
│   │       ├── components/
│   │       ├── public/
│   │       └── admin/
│   │
│   └── static/
│       └── img/
│           └── logo.png
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 📦 Requirements

- **Python** 3.11 or higher
- **PostgreSQL** 14+ (or SQLite for development)
- **Cloudinary** account (free tier works)
- **pip** and **venv**

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/djaj-wa-toom-backend.git
cd djaj-wa-toom-backend
```

### 2. Create and activate a virtual environment

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file at the project root (next to `requirements.txt`):

```env
# ─── Database ───
DATABASE_URL=postgresql://user:password@host:5432/menudb
# For local development with SQLite:
# DATABASE_URL=sqlite:///./menu.db

# ─── Cloudinary ───
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

# ─── Application ───
APP_NAME=Djaj Wa Toom Menu API
DEBUG=True

# ─── JWT ───
JWT_SECRET_KEY=generate-a-random-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=10080
```

### Generate a strong JWT secret key

```bash
python -c "import secrets; print(secrets.token_urlsafe(64))"
```

Copy the output and paste it as `JWT_SECRET_KEY`.

### Cloudinary credentials

1. Sign up at [cloudinary.com](https://cloudinary.com/)
2. Go to **Console → Dashboard**
3. Copy **Cloud Name**, **API Key**, and **API Secret**

---

## ▶️ Running the Application

### Development mode (with auto-reload)

```bash
uvicorn app.main:app --reload --port 8000
```

### Development mode with LAN access (for testing QR from phone)

```bash
uvicorn app.main:app --reload --port 8000 --host 0.0.0.0
```

### Production mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

The application will be available at:

| URL | Description |
|-----|-------------|
| `http://localhost:8000` | Root (redirects to `/menu`) |
| `http://localhost:8000/docs` | Swagger UI (interactive API docs) |
| `http://localhost:8000/redoc` | ReDoc API documentation |
| `http://localhost:8000/health` | Health check |

---

## 🎬 First-Time Setup

The very first user must be created **once** through the setup endpoint, otherwise no one can access the admin panel.

### Option 1: Using Swagger UI

1. Open `http://localhost:8000/docs`
2. Find `POST /api/v1/auth/setup`
3. Click **Try it out**
4. Send:

```json
{
  "username": "admin",
  "password": "your_secure_password",
  "full_name": "Restaurant Owner"
}
```

### Option 2: Using cURL

```bash
curl -X POST http://localhost:8000/api/v1/auth/setup \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"your_secure_password","full_name":"Restaurant Owner"}'
```

After this, the admin panel is accessible at `http://localhost:8000/admin/login`.

⚠️ **Note:** `/auth/setup` works **only once**. It returns `409 Conflict` if a user already exists.

---

## 📡 API Documentation

### Base URL

```
http://localhost:8000/api/v1
```

### Authentication Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/auth/setup-required` | ❌ | Check if first-time setup is needed |
| POST | `/auth/setup` | ❌ | Create first admin (one-time only) |
| POST | `/auth/login` | ❌ | Login and receive JWT |
| POST | `/auth/register` | ✅ | Register a new user |
| GET | `/auth/me` | ✅ | Get current user info |
| POST | `/auth/change-password` | ✅ | Change current user password |
| GET | `/auth/users` | ✅ | List all users |

### Menu Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/menus/visible` | ❌ | **Public** — Menu shown to customers |
| GET | `/menus/` | ✅ | List all menus |
| GET | `/menus/default` | ✅ | Get default menu |
| GET | `/menus/{id}` | ✅ | Get menu with items |
| POST | `/menus/` | ✅ | Create a menu |
| PUT | `/menus/{id}` | ✅ | Update a menu |
| DELETE | `/menus/{id}` | ✅ | Delete a menu |

### Menu Item Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/menus/{id}/items/public` | ❌ | **Public** — Available items only |
| GET | `/menus/{id}/items/categories/public` | ❌ | **Public** — Unique categories |
| GET | `/menus/{id}/items/` | ✅ | List items (with filters) |
| GET | `/menus/{id}/items/categories` | ✅ | List categories |
| GET | `/menus/{id}/items/search?q=X` | ✅ | Search items |
| POST | `/menus/{id}/items/` | ✅ | Create item (multipart with image) |
| PUT | `/menus/{id}/items/{item_id}` | ✅ | Update item (multipart) |
| DELETE | `/menus/{id}/items/{item_id}` | ✅ | Delete item |

### Example Request: Create Menu

```bash
curl -X POST http://localhost:8000/api/v1/menus/ \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Ramadan Menu",
    "description": "Special Ramadan items",
    "is_default": false,
    "is_active": true
  }'
```

### Example Request: Create Item with Image

```bash
curl -X POST http://localhost:8000/api/v1/menus/1/items/ \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -F "name=Chicken Shawarma" \
  -F "description=Chicken + garlic + pickles" \
  -F "price=9000" \
  -F "category=Sandwiches" \
  -F "is_available=true" \
  -F "is_featured=true" \
  -F "sort_order=1" \
  -F "image=@/path/to/image.jpg"
```

---

## 🌐 Web Pages

The application exposes beautiful Jinja2-rendered pages:

| Page | URL | Access | Description |
|------|-----|--------|-------------|
| Public Menu | `/menu` | Public | Customer menu (QR destination) |
| Admin Login | `/admin/login` | Public | Login form |
| Dashboard | `/admin` | Auth | Stats overview |
| Menus List | `/admin/menus` | Auth | Manage menus |
| New Menu | `/admin/menus/new` | Auth | Create menu |
| Edit Menu | `/admin/menus/{id}/edit` | Auth | Update menu |
| Items List | `/admin/menus/{id}/items` | Auth | Manage items |
| New Item | `/admin/menus/{id}/items/new` | Auth | Create item |
| Edit Item | `/admin/menus/{id}/items/{id}/edit` | Auth | Update item |
| QR Generator | `/admin/qr` | Auth | Generate QR for printing |

### QR Code Workflow

1. Admin creates/updates menu items in the dashboard.
2. Admin opens `/admin/qr` and prints the QR code.
3. Place printed QR on restaurant tables.
4. Customer scans QR → opens `/menu` with the **current** menu.
5. **No reprinting is needed** — the QR is a fixed URL and always shows the latest content.

---

## 🔐 Authentication Flow

### For API Clients

```
1. POST /api/v1/auth/login  →  { access_token }
2. Store token securely
3. Add header to all protected requests:
   Authorization: Bearer <token>
4. On 401 → refresh or re-login
```

### For Web Admin Panel (Jinja2)

```
1. POST /admin/login  →  Set-Cookie: access_token=<JWT>; HttpOnly
2. Browser automatically sends cookie with every request
3. Server reads cookie via get_current_user_from_cookie()
4. On /admin/logout → cookie is cleared
```

### Password Security

Passwords are hashed using **SHA-256 → bcrypt** (double hashing):

1. SHA-256 normalizes any password to 32 bytes.
2. bcrypt applies salt and slow hashing.
3. This avoids bcrypt's 72-byte limit while preserving security.

---

## 🖼 Cloudinary Integration

### Upload Flow

1. Admin submits form with image file.
2. `ImageService.upload()` sends file to Cloudinary.
3. Cloudinary returns:
   - `secure_url` — stored in `image_url`
   - `public_id` — stored in `image_public_id` (for deletion)
4. Both are saved with the menu item.

### Delete Flow

1. Admin deletes item or uploads a new image.
2. `ImageService.delete(public_id)` removes the old image from Cloudinary.
3. This prevents orphaned files and wasted storage.

### Folder Structure in Cloudinary

```
menu_items/
├── abc123xyz.jpg
├── def456uvw.jpg
└── ...
```

---

## 🗄 Database Management

### Automatic Table Creation

Tables are created automatically at startup via:

```python
Base.metadata.create_all(bind=engine)
```

### Recommended: Use Alembic (Production)

For production, use migrations:

```bash
# Initialize (only once)
alembic init alembic

# Create migration
alembic revision --autogenerate -m "add new field"

# Apply migration
alembic upgrade head
```

### Database Schema

#### `users`

| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER | Primary key |
| username | VARCHAR(50) | Unique |
| password_hash | VARCHAR(255) | bcrypt hash |
| full_name | VARCHAR(100) | Nullable |
| role | VARCHAR(20) | admin / manager |
| is_active | BOOLEAN | Default true |
| last_login | DATETIME | Nullable |
| created_at | DATETIME | Auto |

#### `menus`

| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER | Primary key |
| name | VARCHAR(100) | |
| description | TEXT | Nullable |
| is_default | BOOLEAN | Only one true |
| is_active | BOOLEAN | |
| start_date | DATETIME | Nullable |
| end_date | DATETIME | Nullable |
| created_at | DATETIME | |
| updated_at | DATETIME | |

#### `menu_items`

| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER | Primary key |
| name | VARCHAR(150) | |
| description | TEXT | Nullable |
| price | INTEGER | In smallest unit |
| category | VARCHAR(50) | Indexed |
| image_url | VARCHAR(500) | Cloudinary URL |
| image_public_id | VARCHAR(200) | Cloudinary public ID |
| is_available | BOOLEAN | |
| is_featured | BOOLEAN | |
| sort_order | INTEGER | |
| menu_id | INTEGER | Foreign key |
| created_at | DATETIME | |
| updated_at | DATETIME | |

---

## 🧪 Testing

### Manual API Testing

Use the interactive Swagger UI at `http://localhost:8000/docs`.

### Recommended Testing Tools

- **Postman** — For API collection testing
- **Insomnia** — Alternative to Postman
- **httpx / pytest** — For automated tests (to be added)

### Sample Test Flow

1. `POST /auth/setup` — Create admin
2. `POST /auth/login` — Get token
3. `GET /auth/me` — Verify token works
4. `POST /menus/` — Create menu
5. `POST /menus/{id}/items/` — Add item with image
6. `GET /menus/{id}/items/` — Verify item appears
7. `GET /menus/visible` — Confirm public visibility
8. `DELETE /menus/{id}/items/{item_id}` — Clean up

---

## 🚢 Deployment

### Render.com (Recommended)

1. Create a **PostgreSQL** database on Render.
2. Create a **Web Service** and connect your GitHub repo.
3. Set environment variables in the Render dashboard.
4. Set **Start Command**:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

5. Deploy.

### Docker

**`Dockerfile`:**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Build and run:**

```bash
docker build -t djaj-menu-api .
docker run -p 8000:8000 --env-file .env djaj-menu-api
```

### Docker Compose

```yaml
version: "3.9"

services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: menu
      POSTGRES_PASSWORD: menu
      POSTGRES_DB: menudb
    volumes:
      - pgdata:/var/lib/postgresql/data

  api:
    build: .
    depends_on:
      - db
    environment:
      DATABASE_URL: postgresql://menu:menu@db:5432/menudb
      CLOUDINARY_CLOUD_NAME: ${CLOUDINARY_CLOUD_NAME}
      CLOUDINARY_API_KEY: ${CLOUDINARY_API_KEY}
      CLOUDINARY_API_SECRET: ${CLOUDINARY_API_SECRET}
    ports:
      - "8000:8000"

volumes:
  pgdata:
```

### Production Checklist

- [ ] Set `DEBUG=False`
- [ ] Use a strong `JWT_SECRET_KEY` (64+ random chars)
- [ ] Restrict `allow_origins` in CORS to your real domain
- [ ] Use HTTPS (automatic on Render)
- [ ] Set `secure=True` in cookie flags
- [ ] Enable database backups
- [ ] Use Alembic for migrations instead of `create_all`
- [ ] Set up error monitoring (Sentry, etc.)
- [ ] Configure logging
- [ ] Add rate limiting (Slowapi)

---

## 🎨 Brand Identity

The application follows a strict brand palette:

| Color | Hex | Usage |
|-------|-----|-------|
| Primary Red | `#E10600` | CTAs, headers, accents |
| Dark Red | `#B80500` | Hover states |
| Yellow | `#FFD600` | Featured badges, highlights (used sparingly) |
| Black | `#1A1A1A` | Text, sidebar |
| Background | `#F7F7F5` | Page background |
| Border | `#E9E9E9` | Subtle dividers |

**Typography:** Cairo (Google Fonts) for Arabic, system UI for fallback.

**Design Principles:**

- White space is a primary element — do not overcrowd.
- Yellow is used only for accents (stars, "featured" badges).
- Red is reserved for CTAs and identity elements.
- Rounded corners (18–22px) and soft shadows for a modern feel.

---

## 🤝 Contributing

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/amazing-feature`.
3. Follow Clean Architecture principles.
4. Ensure `pip install -r requirements.txt` succeeds.
5. Write clear commit messages.
6. Push your branch: `git push origin feature/amazing-feature`.
7. Open a Pull Request.

### Code Style

- Follow **PEP 8**.
- Use **type hints** everywhere.
- Keep services free of HTTP/SQL concerns.
- Keep repositories free of business logic.
- One responsibility per file.

---

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## 📞 Support

For questions or issues:

- Open an issue on GitHub
- Contact: [your-email@example.com](mailto:your-email@example.com)

---

## 🗺 Roadmap

- [ ] Alembic migrations for production
- [ ] Automated tests (pytest + httpx)
- [ ] Rate limiting with Slowapi
- [ ] Multi-language support (AR / EN / TR)
- [ ] Analytics dashboard (views, popular items)
- [ ] Export menu as PDF
- [ ] Bulk import from CSV/Excel
- [ ] Audit log for admin actions

---

