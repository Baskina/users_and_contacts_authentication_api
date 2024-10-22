# Contacts Management API - README

## Project Overview
This mini-project is a REST API built using FastAPI, designed for managing contacts and their information. The project uses SQLAlchemy as the ORM (Object Relational Mapper) to handle the database interactions, and PostgreSQL as the database. The API allows users to perform CRUD operations (Create, Read, Update, Delete) and includes additional features for searching and filtering contacts based on different attributes.

Additionally, the project now includes user authentication and authorization, ensuring that only registered users can perform operations on their own contacts using JWT tokens. Alembic is used for database migrations.

## Key Features:
- Store contacts with details such as:
    - First Name
    - Last Name
    - Email Address
    - Phone Number
    - Date of Birth
    - Additional Information (optional)
- Full CRUD operations for contacts.
- Search for contacts by:
    - First Name
    - Last Name
    - Email Address
- Retrieve contacts whose birthdays are in the upcoming 7 days.
- **Authentication and Authorization:**
    - User authentication is implemented using hashed passwords and JWT tokens (access and refresh tokens).
    - Users can only manage their own contacts.
    - Registration ensures no duplicate emails.
    - Secure password storage using hashing (passwords are never stored in plain text).

## Technologies Used
- **FastAPI**: For building the REST API.
- **SQLAlchemy**: For database ORM.
- **PostgreSQL**: The database used for storing contact data.
- **Alembic**: For database migrations.
- **Pydantic**: For data validation and serialization.
- **JWT**: For implementing authentication and authorization.
- **Uvicorn**: ASGI server for serving FastAPI applications.

## Installation

### Clone the repository:
```bash
git clone <repository-url>
cd <project-directory>
```

### Set up a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Install the required dependencies:
```bash
pip install -r requirements.txt
```

### Set up the PostgreSQL database:
1. Ensure you have PostgreSQL installed and running.
2. Create a new database for the project:
```bash
psql -U postgres -c "CREATE DATABASE contacts_db;"
```
3. Configure the `config.py` file:
```bash
DATABASE_URL=postgresql://postgres:<password>@localhost:5432/contacts_db
```

### Run database migrations with Alembic:
```bash
alembic upgrade head
```

### Start the FastAPI server:
```bash
uvicorn main:app --reload
```

### API Documentation:
After starting the server, navigate to `http://127.0.0.1:8000/docs` to explore the API documentation via the FastAPI Swagger UI.

## API Endpoints

### Contact Management

- **Create a new contact**
    - `POST /api/contacts/`
    - Create a new contact with the provided details.

- **Get all contacts**
    - `GET /api/contacts/`
    - Retrieve a list of all contacts.

- **Get a contact by ID**
    - `GET /api/contacts/{contact_id}`
    - Retrieve a specific contact by its ID.

- **Update a contact by ID**
    - `PUT /api/contacts/{contact_id}`
    - Update the details of an existing contact.

- **Delete a contact by ID**
    - `DELETE /api/contacts/{contact_id}`
    - Remove a contact from the database.

### Authentication Endpoints

- **Sign up (user registration)**
    - `POST /api/auth/signup`
    - Create a new user account with email and password.

- **Login**
    - `POST /api/auth/login`
    - Authenticate a user with email and password. Returns JWT access and refresh tokens.

- **Refresh Token**
    - `GET /api/auth/refresh_token`
    - Refresh the JWT access token using a valid refresh token.

### Additional Features
- **Search contacts**
    - `GET /api/contacts/search?name=<name>&lastName=<lastName>&email=<email>`
    - Search for contacts based on first name, last name, or email address.

## Authentication & Authorization
The project includes authentication and authorization mechanisms to restrict access to registered users only.

- **User registration**
    - If a user with the provided email already exists, the server returns `HTTP 409 Conflict`.
    - The password is hashed before storage to ensure security.
    - On successful registration, the server responds with `HTTP 201 Created` and returns the new user’s details.

- **Login and JWT Tokens**
    - On login, users provide their email and password. If the credentials are incorrect, the server returns `HTTP 401 Unauthorized`.
    - The authentication mechanism uses a pair of tokens: an `access_token` and a `refresh_token` for authorization.

- **Access Restrictions**
    - Users can only access and modify their own contacts.
    - All POST operations return a `201 Created` status on success.

## General Requirements
- The project is built with FastAPI.
- Uses SQLAlchemy ORM to interact with the PostgreSQL database.
- Includes full CRUD functionality for managing contacts.
- Authentication and authorization using JWT tokens.
- Supports data validation through Pydantic.
- Exposes API documentation through FastAPI’s built-in Swagger interface.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
