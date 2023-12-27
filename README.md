# User Authentication Service


## Overview

A RESTful API built with FastAPI. It's designed to handle user authentication and management with JWT access and refresh tokens, providing a secure and efficient way to manage user sessions.

## Features

*   User Authentication with JWT (access and refresh tokens).
*   Secure password handling with `bcrypt`.
*   Endpoints for user sign-up, login, logout, profile management, and token refresh.
*   Integration with PostgreSQL for data persistence.

## Getting Started

### Prerequisites

*   Python 3.8+
*   PostgreSQL

### Installation

1.  Clone the repository:
    
    `git clone https://github.com/org-ofirdassa9/user-authentication-service.git cd user-authentication-service`
    
2.  Set up a virtual environment:
    
    `python -m venv venv source venv/bin/activate  # For Unix or MacOS venv\Scripts\activate  # For Windows`
    
3.  Install dependencies:

    `pip install -r requirements.txt`

4. Create the database:

    `python database_init.py`
    
5.  Run the application:
    
    `uvicorn app.main:app --reload`
    

### API Endpoints

*   `POST /api/users_service/users/signup`: Register a new user.
*   `POST /api/users_service/users/login`: Login and receive access and refresh tokens.
*   `POST /api/users_service/users/logout`: Logout and clear tokens.
*   `GET /api/users_service/users/me`: Get the profile of the current user.
*   `POST /api/users_service/users/refresh`: Refresh the access token.
*   `GET /api/users_service/users/{user_id}`: Get user details by ID.
*   `PUT /api/users_service/users/{user_id}`: Update user attributes