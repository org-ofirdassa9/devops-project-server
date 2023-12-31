# DevOps Project Server

## Overview

A RESTful API built with FastAPI. It's designed to handle user authentication and management with JWT access and refresh tokens, providing a secure and efficient way to manage user sessions. It also includes health metrics tracking and report generation features.

## Features

* User Authentication with JWT (access and refresh tokens).
* Secure password handling with [bcrypt]
* Endpoints for user sign-up, login, logout, profile management, and token refresh.
* Integration with PostgreSQL for data persistence.
* Health metrics tracking for users.
* Report generation for health metrics.

## Getting Started

### Prerequisites

* Python 3.8+
* PostgreSQL

### Installation

1. Clone the repository:

    `git clone https://github.com/org-ofirdassa9/devops-project-server.git cd devops-project-server`

2. Set up a virtual environment:

    `python -m venv venv`
    `source venv/bin/activate For Unix or MacOS`
    `venv\Scripts\activate For Windows`

3. Install dependencies:

    `pip install -r requirements.txt`

4. Create the database:

    `python database_init.py`

5. Run the application:

    `uvicorn users_service:app --reload`
    `uvicorn metrics_process:app --reload --port 8001`
    `uvicorn report_generator:app --reload --port 8002`