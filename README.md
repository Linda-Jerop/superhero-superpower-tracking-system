# Superheroes API 🦸‍♀️

A Flask REST API for tracking superheroes and their superpowers. This application allows you to manage heroes, their associated powers, and relationships between them.

## Table of Contents

- [Features](#features)
- [Project Overview](#project-overview)
- [Setup Instructions](#setup-instructions)
- [Database Models](#database-models)
- [API Endpoints](#api-endpoints)
- [Testing with Postman](#testing-with-postman)
- [Email Configuration](#email-configuration)
- [Author](#author)
- [License](#license)

---

## Features

✨ **Complete CRUD Operations** - Create, read, and update heroes and powers
🔗 **Relationship Management** - Associate heroes with multiple powers with strength levels
✅ **Data Validation** - Built-in validation for power descriptions and hero-power strength levels
📧 **Email Notifications** - Send email alerts when heroes acquire new powers
🗄️ **SQLite Database** - Lightweight, serverless database with automatic migrations
🔄 **RESTful API Design** - Follows REST naming conventions and HTTP standards
⚡ **Error Handling** - Comprehensive error responses with appropriate HTTP status codes

---

## Project Overview

This API manages three main entities:

1. **Heroes** - Superheroes with names and secret identities
2. **Powers** - Superpowers with descriptions
3. **HeroPowers** - The relationship between heroes and powers, with strength levels

### Entity Relationship Diagram

```
Hero (1) ──────────────(M) HeroPower (M)──────────────(1) Power
```

- A Hero has many Powers through HeroPower
- A Power has many Heroes through HeroPower
- HeroPower includes the strength level of the power for each hero

---

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation Steps

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd superheroes
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database:**
   ```bash
   flask db upgrade
   ```

5. **Seed the database with sample data:**
   ```bash
   python -c "from app import create_app, db; from seed import seed_database; app = create_app(); app.app_context().push(); seed_database()"
   ```

6. **Run the application:**
   ```bash
   python run.py
   ```

The API will be available at `http://localhost:5000`

---

## Database Models

### Hero Model

```python
{
  "id": 1,
  "name": "Kamala Khan",
  "super_name": "Ms. Marvel"
}
```

**Fields:**
- `id` (Integer, Primary Key)
- `name` (String, Required) - Real name
- `super_name` (String, Required) - Superhero alias

---

### Power Model

```python
{
  "id": 1,
  "name": "super strength",
  "description": "gives the wielder super-human strengths"
}
```

**Fields:**
- `id` (Integer, Primary Key)
- `name` (String, Required) - Power name
- `description` (String, Required) - Must be at least 20 characters long

**Validation:**
- Description must be present and at least 20 characters long

---

### HeroPower Model

```python
{
  "id": 1,
  "hero_id": 1,
  "power_id": 1,
  "strength": "Strong",
  "hero": { /* Hero object */ },
  "power": { /* Power object */ }
}
```

**Fields:**
- `id` (Integer, Primary Key)
- `hero_id` (Integer, Foreign Key) - Reference to Hero
- `power_id` (Integer, Foreign Key) - Reference to Power
- `strength` (String, Required) - Strength level of the power

**Validation:**
- `strength` must be one of: `'Strong'`, `'Weak'`, `'Average'`

**Cascade Delete:**
- When a Hero or Power is deleted, all associated HeroPowers are automatically deleted

---

## API Endpoints

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
Retrieve a specific hero with all their associated powers.

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
      "hero": {
        "id": 1,
        "name": "Kamala Khan",
        "super_name": "Ms. Marvel"
      },
      "power": {
        "id": 2,
        "name": "flight",
        "description": "gives the wielder the ability to fly through the skies at supersonic speed"
      }
    }
  ]
}
```

**Error Response (404 Not Found):**
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
Retrieve a specific power.

**Response (200 OK):**
```json
{
  "id": 1,
  "name": "super strength",
  "description": "gives the wielder super-human strengths"
}
```

**Error Response (404 Not Found):**
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
  "description": "Valid Updated Description - This must be at least 20 characters long!"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "name": "super strength",
  "description": "Valid Updated Description - This must be at least 20 characters long!"
}
```

**Error Response (404 Not Found):**
```json
{
  "error": "Power not found"
}
```

**Error Response (400 Bad Request) - Validation Failed:**
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
  "strength": "Average",
  "power_id": 1,
  "hero_id": 3
}
```

**Response (201 Created):**
```json
{
  "id": 11,
  "hero_id": 3,
  "power_id": 1,
  "strength": "Average",
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

**Error Response (400 Bad Request) - Validation Failed:**
```json
{
  "errors": ["strength must be one of ['Strong', 'Weak', 'Average']"]
}
```

**Error Response (404 Not Found) - Invalid IDs:**
```json
{
  "errors": ["Invalid hero_id or power_id"]
}
```

---

### POST /send_power_email
Send an email notification about a new power acquisition.

**Request Body:**
```json
{
  "hero_name": "Kamala Khan",
  "power_name": "flight",
  "recipient_email": "user@example.com"
}
```

**Response (200 OK):**
```json
{
  "message": "Email sent successfully"
}
```

**Error Response (400 Bad Request):**
```json
{
  "errors": ["hero_name, power_name, and recipient_email are required"]
}
```

---

## Testing with Postman

1. Import the Postman collection (`challenge-2-superheroes.postman_collection.json`) into Postman
2. Ensure the application is running on `http://localhost:5000`
3. Execute the requests in the collection to test all endpoints
4. Verify responses match the expected JSON format and HTTP status codes

---

## Email Configuration

The application supports sending emails via SMTP. Configure email settings using environment variables in a `.env` file:

```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
MAIL_DEFAULT_SENDER=superheroes@example.com
```

### Gmail Setup

1. Enable 2-Factor Authentication on your Gmail account
2. Generate an [App Password](https://myaccount.google.com/apppasswords)
3. Use the App Password in the `MAIL_PASSWORD` environment variable

---

## Project Structure

```
superheroes/
├── app/
│   ├── __init__.py          # Flask app factory and configuration
│   ├── models.py            # Database models (Hero, Power, HeroPower)
│   ├── routes.py            # API endpoints
│   └── email.py             # Email utility functions
├── migrations/              # Database migrations (auto-generated)
├── run.py                   # Application entry point
├── seed.py                  # Database seeding script
├── requirements.txt         # Python dependencies
├── README.md                # This file
└── superheroes.db           # SQLite database (auto-created)
```

---

## Best Practices Implemented

✅ **MVC Pattern** - Separation of Models, Views (Routes), and Configuration
✅ **Environment Variables** - Secure configuration management
✅ **Database Migrations** - Version control of schema changes with Alembic
✅ **Validation Layer** - Built-in validators using SQLAlchemy's `@validates`
✅ **Error Handling** - Comprehensive error responses with appropriate HTTP status codes
✅ **Serialization Control** - Prevent circular references using `to_dict()` methods
✅ **Cascade Deletes** - Automatic cleanup of orphaned records
✅ **RESTful Design** - Proper HTTP verbs and status codes
✅ **DRY Principle** - Reusable methods to avoid code duplication
✅ **Documentation** - Comprehensive docstrings and this README

---

## Author

**Linda Jerop**
- GitHub: [@linda-jerop](https://github.com/linda-jerop)
- Email: linda@example.com

---

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## Support

If you encounter any issues or have questions, please:
1. Check the API endpoints documentation above
2. Review the error messages in the API response
3. Verify database connectivity with `flask db current`
4. Check environment variables are correctly configured

Happy coding! 🚀
