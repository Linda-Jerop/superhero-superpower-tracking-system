# 🦸 Superheroes API

A robust Flask REST API for managing superheroes and their superpowers. Track hero-power associations with full CRUD functionality, validations, and email notifications.

**Owner:** Linda Jerop  
**Repository:** [GitHub - Superheroes](https://github.com/yourusername/superheroes)

---

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Setup Instructions](#setup-instructions)
- [Database Schema](#database-schema)
- [API Endpoints](#api-endpoints)
- [Validation Rules](#validation-rules)
- [Email Configuration](#email-configuration)
- [Usage Examples](#usage-examples)
- [License](#license)
- [Support](#support)

---

## ✨ Features

✅ **Full CRUD Operations** - Create, read, update hero and power records  
✅ **Relationship Management** - Associate heroes with powers through HeroPower model  
✅ **Data Validation** - Built-in validations for power descriptions and strength levels  
✅ **Cascade Deletes** - Automatically clean up orphaned records  
✅ **Email Notifications** - Send alerts when heroes are assigned powers or powers are updated  
✅ **RESTful Design** - Follows REST conventions with proper HTTP status codes  
✅ **Serialization Control** - Prevents circular references with depth-limited serialization  
✅ **Database Migrations** - SQLAlchemy Alembic for version control of schema changes

---

## 🛠️ Tech Stack

- **Framework:** Flask 2.3.3
- **Database:** SQLite with SQLAlchemy ORM
- **Migrations:** Flask-Migrate (Alembic)
- **Email:** Flask-Mail with SMTP support
- **Environment:** Python 3.x with virtual environment

---

## 🚀 Setup Instructions

### Prerequisites

- Python 3.8+
- pip package manager
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/superheroes.git
cd superheroes
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory:

```env
# Flask Configuration
FLASK_ENV=development
FLASK_APP=run.py

# Database
DATABASE_URL=sqlite:///superheroes.db

# Email Configuration (Gmail example)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=noreply@superheroes.com
```

**Note:** For Gmail, use an [App Password](https://support.google.com/accounts/answer/185833) instead of your regular password.

### 5. Initialize Database

```bash
# Create database tables
flask db init          # First time only
flask db migrate -m "Initial migration"
flask db upgrade

# Seed with sample data
python -c "from app import create_app, db; from seed import seed_database; app = create_app(); app.app_context().push(); seed_database()"
```

### 6. Run the Application

```bash
python run.py
```

The API will be available at `http://localhost:5000`

---

## 📊 Database Schema

### Entity Relationship Diagram

```
┌─────────────┐       ┌──────────────┐       ┌────────────┐
│    Hero     │───────│  HeroPower   │───────│   Power    │
├─────────────┤       ├──────────────┤       ├────────────┤
│ id (PK)     │       │ id (PK)      │       │ id (PK)    │
│ name        │◄──────│ hero_id (FK) │       │ name       │
│ super_name  │       │ power_id (FK)├──────►│ description│
└─────────────┘       │ strength     │       └────────────┘
      ▲               └──────────────┘            ▲
      │                                           │
      └───────────────── One-to-Many ─────────────┘
                    (through HeroPower)
```

### Models

**Hero**
- `id` (Integer, PK)
- `name` (String, required)
- `super_name` (String, required)
- `hero_powers` (Relationship to HeroPower)

**Power**
- `id` (Integer, PK)
- `name` (String, required)
- `description` (String, required, min 20 chars)
- `hero_powers` (Relationship to HeroPower)

**HeroPower**
- `id` (Integer, PK)
- `hero_id` (Integer, FK to Hero)
- `power_id` (Integer, FK to Power)
- `strength` (String, enum: 'Strong', 'Weak', 'Average')

---

## 🔌 API Endpoints

### GET /heroes
Retrieve all heroes with basic information.

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Kamala Khan",
    "super_name": "Ms. Marvel"
  },
  {
    "id": 2,
    "name": "Doreen Green",
    "super_name": "Squirrel Girl"
  }
]
```

---

### GET /heroes/:id
Retrieve a specific hero with all associated powers.

**Response (200 OK):**
```json
{
  "id": 1,
  "name": "Kamala Khan",
  "super_name": "Ms. Marvel",
  "hero_powers": [
    {
      "id": 1,
      "hero_id": 1,
      "power_id": 2,
      "strength": "Strong",
      "power": {
        "id": 2,
        "name": "flight",
        "description": "gives the wielder the ability to fly through the skies at supersonic speed"
      }
    }
  ]
}
```

**Response (404 Not Found):**
```json
{
  "error": "Hero not found"
}
```

---

### GET /powers
Retrieve all available powers.

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "super strength",
    "description": "gives the wielder super-human strengths"
  },
  {
    "id": 2,
    "name": "flight",
    "description": "gives the wielder the ability to fly through the skies at supersonic speed"
  }
]
```

---

### GET /powers/:id
Retrieve a specific power by ID.

**Response (200 OK):**
```json
{
  "id": 1,
  "name": "super strength",
  "description": "gives the wielder super-human strengths"
}
```

**Response (404 Not Found):**
```json
{
  "error": "Power not found"
}
```

---

### PATCH /powers/:id
Update a power's description.

**Request Body:**
```json
{
  "description": "New description that is at least 20 characters long",
  "notification_email": "admin@superheroes.com"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "name": "super strength",
  "description": "New description that is at least 20 characters long"
}
```

**Response (404 Not Found):**
```json
{
  "error": "Power not found"
}
```

**Response (400 Bad Request):**
```json
{
  "errors": ["description must be present and at least 20 characters long"]
}
```

---

### POST /hero_powers
Create a new hero-power association.

**Request Body:**
```json
{
  "strength": "Strong",
  "power_id": 1,
  "hero_id": 3,
  "notification_email": "admin@superheroes.com"
}
```

**Response (201 Created):**
```json
{
  "id": 11,
  "hero_id": 3,
  "power_id": 1,
  "strength": "Strong",
  "hero": {
    "id": 3,
    "name": "Gwen Stacy",
    "super_name": "Spider-Gwen"
  },
  "power": {
    "id": 1,
    "name": "super strength",
    "description": "gives the wielder super-human strengths"
  }
}
```

**Response (400 Bad Request):**
```json
{
  "errors": ["strength must be one of ['Strong', 'Weak', 'Average']"]
}
```

**Response (404 Not Found):**
```json
{
  "errors": ["Invalid hero_id or power_id"]
}
```

---

### POST /send-test-email
Test email sending capability.

**Request Body:**
```json
{
  "recipient_email": "test@example.com"
}
```

**Response (200 OK):**
```json
{
  "message": "Test email sent successfully",
  "recipient": "test@example.com"
}
```

---

## ✓ Validation Rules

### Power Model
- **description** must be present and at least 20 characters long
- Attempting to create/update with invalid description returns 400 with error message

### HeroPower Model
- **strength** must be one of: `'Strong'`, `'Weak'`, `'Average'`
- Invalid strength values return 400 with error message
- Both `hero_id` and `power_id` must reference existing records

---

## 📧 Email Configuration

The API supports sending email notifications for:

1. **Hero Power Assignment** - Notified when a hero is assigned a new power
2. **Power Update** - Notified when a power description is updated
3. **Test Emails** - Verify email functionality via `/send-test-email` endpoint

### Email Providers Supported

- **Gmail SMTP** (recommended for development)
- **Office 365 SMTP**
- **SendGrid**
- **Custom SMTP servers**

### Setting Up Gmail SMTP

1. Enable 2-factor authentication on your Google account
2. Generate an [App Password](https://support.google.com/accounts/answer/185833)
3. Add to `.env`:
   ```env
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=xxxx xxxx xxxx xxxx
   ```

---

## 💡 Usage Examples

### Using cURL

```bash
# Get all heroes
curl http://localhost:5000/heroes

# Get specific hero with powers
curl http://localhost:5000/heroes/1

# Get all powers
curl http://localhost:5000/powers

# Create new hero-power association
curl -X POST http://localhost:5000/hero_powers \
  -H "Content-Type: application/json" \
  -d '{
    "strength": "Strong",
    "power_id": 1,
    "hero_id": 3,
    "notification_email": "admin@superheroes.com"
  }'

# Update power description
curl -X PATCH http://localhost:5000/powers/1 \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Grants superhuman strength and durability to the wielder",
    "notification_email": "admin@superheroes.com"
  }'

# Send test email
curl -X POST http://localhost:5000/send-test-email \
  -H "Content-Type: application/json" \
  -d '{"recipient_email": "test@example.com"}'
```

### Using Postman

1. Download the [Postman Collection](./challenge-2-superheroes.postman_collection.json)
2. Import into Postman
3. Set base URL to `http://localhost:5000`
4. Execute requests from the collection

### Using Python Requests

```python
import requests

BASE_URL = "http://localhost:5000"

# Get all heroes
response = requests.get(f"{BASE_URL}/heroes")
heroes = response.json()

# Create hero-power association
payload = {
    "strength": "Average",
    "power_id": 2,
    "hero_id": 5,
    "notification_email": "admin@superheroes.com"
}
response = requests.post(f"{BASE_URL}/hero_powers", json=payload)
new_association = response.json()
```

---

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🤝 Support

For issues, feature requests, or questions:

- **Email:** linda.jerop@flatiron.school
- **GitHub Issues:** [Create an issue](https://github.com/yourusername/superheroes/issues)
- **Discord:** Available on the Flatiron Community Server

---

## 🎯 Best Practices Implemented

### Code Quality
✅ **DRY Principle** - Reusable methods and functions  
✅ **SOLID Principles** - Single responsibility per function/class  
✅ **Type Hints** - Clear function signatures  
✅ **Error Handling** - Try-catch blocks with meaningful messages  

### Database
✅ **Migrations** - Tracked schema changes  
✅ **Cascade Deletes** - Referential integrity  
✅ **Validations** - Database-level constraints  
✅ **Relationships** - Proper foreign keys and joins  

### API Design
✅ **REST Conventions** - Standard HTTP methods and status codes  
✅ **Serialization** - Depth control to prevent circular references  
✅ **Status Codes** - 200, 201, 400, 404, 500 as appropriate  
✅ **Error Responses** - Consistent JSON error format  

### Security
✅ **Environment Variables** - Sensitive config not in code  
✅ **Input Validation** - All user inputs validated  
✅ **Email Protection** - Credentials never exposed  

---

**Last Updated:** January 5, 2026  
**Version:** 1.0.0
