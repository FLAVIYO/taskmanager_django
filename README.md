

## Overview
The **Task Management API** is a RESTful API built with **Django** and **Django REST Framework**. It allows users to manage tasks 

---

## Features
- **User Authentication**:
  - Signup with email and password.
  - Login to receive JWT tokens (access and refresh).
  - Refresh tokens to get new access tokens.
- **Role-Based Access Control**:
  - `ADMIN`: Can access and manage all tasks.
  - `USER`: Can only access and manage their own tasks.
- **Task Management**:
  - Create tasks with a title, description, due date, and status.
  - Retrieve, update, and delete tasks.
- **Structured Error Handling**:
  - Consistent error responses for better debugging.
- **Logging**:
  - All API activity is logged to `api.log`.

---

## Prerequisites
Before running the application, ensure you have the following installed:
- **Python 3.8+**
- **PostgreSQL** (or any other database supported by Django)
- **pip** (Python package manager)

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/FLAVIYO/taskmanager_django.git
cd taskmanager_django
```
### 2. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Create a .env file in the root directory and add the following:

```bash
DB_NAME=taskmanager
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```
### 4. Run Migrations

Apply database migrations:

```bash
python3 manage.py migrate
```
### 5. Create a Superuser (Admin)
Create an admin user to access the Django admin panel:

```bash
python3 manage.py createsuperuser
```
### 6. Start the Development Server
Run the Django development server:

```bash
python3 manage.py runserver
```
- The admin is available at http://localhost:8000/admin/
- The swagger ui is available at http://localhost:8000/doc/
- The API endpoints be available at http://localhost:8000/api/

## Example Requests

### Signup

**Headers:**
- Content-Type: Content-Type

**POST /api/signup/**

```bash
{
  "email": "newuser@example.com",
  "password": "strongpassword",
}
 ```
 ### or  (but not recommended, as its safer to edit roles in the admin ui)

 ```bash
{
  "email": "newuser@example.com",
  "password": "strongpassword",
  "role": "ADMIN",
}
 ```

### Login

**POST /api/login/**

```bash
{
  "email": "newuser@example.com",
  "password": "strongpassword",
}
 ```

### Create Task


**Headers:**
- Content-Type: Content-Type
- Authorization: Bearer <your_access_token>

**POST /api/tasks/**

```bash
{
    "title": "Finish Project",
    "description": "Complete the Task Management API",
    "due_date": "2024-12-31T00:00:00Z",
}
```     


## Running Tests

To run the test suite, use the following command:

```bash
python manage.py test
```
### Test Coverage

- User Authentication: Signup, login, and token refresh.
- Task Management: Create, retrieve, update, and delete tasks.
- Role-Based Access Control: Ensure admins and users have the correct permissions.

## Logging

All API activity is logged to api.log in the root directory. Check this file for detailed logs of requests and errors.

## Contributing

Contributions are welcome! If you find a bug or want to add a feature, please open an issue or submit a pull request.
