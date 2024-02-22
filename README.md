<p align="center">
  <img src="https://cdn-icons-png.flaticon.com/512/6295/6295417.png" width="100" />
</p>
<p align="center">
    <h1 align="center">DEVOPS-PROJECT-SERVER</h1>
</p>
<p align="center">
    <em>Empowering DevOps Efficiency with Seamless Server Solutions</em>
</p>
<p align="center">
	<img src="https://img.shields.io/github/last-commit/org-ofirdassa9/devops-project-server?style=flat&logo=git&logoColor=white&color=0080ff" alt="last-commit">
	<img src="https://img.shields.io/github/languages/top/org-ofirdassa9/devops-project-server?style=flat&color=0080ff" alt="repo-top-language">
	<img src="https://img.shields.io/github/languages/count/org-ofirdassa9/devops-project-server?style=flat&color=0080ff" alt="repo-language-count">
<p>
<p align="center">
		<em>Developed with the software and tools below.</em>
</p>
<p align="center">
	<img src="https://img.shields.io/badge/Python-3776AB.svg?style=flat&logo=Python&logoColor=white" alt="Python">
	<img src="https://img.shields.io/badge/Docker-2496ED.svg?style=flat&logo=Docker&logoColor=white" alt="Docker">
	<img src="https://img.shields.io/badge/GitHub%20Actions-2088FF.svg?style=flat&logo=GitHub-Actions&logoColor=white" alt="GitHub%20Actions">
</p>
<hr>

##  Overview

The `devops-project-server` project provides a robust API architecture for handling user management, health metrics processing, and report generation. Key functionalities include dynamic endpoint imports with FastAPI, middleware setup for user authentication, and health metric updates. The project enhances modularity and scalability through modular routers, enabling efficient data management and secure user interactions. By automating build and push operations for Docker images and enabling user CRUD testing, the project ensures reliability and effectiveness in app deployment.

---

##  Features

|    |   Feature         | Description |
|----|-------------------|---------------------------------------------------------------|
| ⚙️  | **Architecture**  | This project follows a modular design with components like user services, metrics processing, and report generation. It uses FastAPI for API endpoints and Docker for containerization, promoting scalability and maintainability. Configuration settings are handled in a structured manner. |
| 🔩 | **Code Quality**  | The codebase maintains a good level of quality with clear structure and separation of concerns. It follows PEP8 conventions for Python code, ensuring readability and consistency. Functions and classes are well-organized, promoting easier maintenance and collaboration. |
| 📄 | **Documentation** | The project has detailed documentation within the codebase, explaining the purpose and functionality of key components like user services, metrics processing, and report generation. Additionally, configuration files and Dockerfiles are documented to aid in setup and deployment. |
| 🔌 | **Integrations**  | Key integrations include FastAPI for RESTful APIs, SQLAlchemy for database interactions, Pydantic for data validation, and Matplotlib for data visualization. External dependencies like Docker and GitHub Actions are utilized for containerization and CI/CD workflows. |
| 🧩 | **Modularity**    | The project exhibits high modularity with separate modules for user services, metrics processing, and report generation. Each module can be independently developed, tested, and scaled, promoting code reusability and maintainability. Dependencies are managed efficiently. |
| 🧪 | **Testing**       | The project uses pytest for automated testing of user service endpoints. Test scenarios cover user CRUD operations and authentication functionalities, ensuring the reliability and robustness of the API services. Testing is integrated into the CI workflow for continuous validation. |
| ⚡️  | **Performance**   | The architecture emphasizes efficiency and speed, utilizing lightweight base images for Docker containers and Uvicorn server for API deployment. Code optimizations help manage resource consumption effectively, enhancing the overall performance of the application. |
| 🛡️ | **Security**      | Security measures include password encryption with bcrypt, token-based authentication with JWT, and data validation with Pydantic. Access control is enforced at both user service and metrics processing endpoints, ensuring data protection and user privacy. Logging configurations enhance security monitoring. |
| 📦 | **Dependencies**  | Key external libraries and dependencies include FastAPI, SQLAlchemy, Pydantic, Matplotlib, and bcrypt. These libraries support various functionalities like API development, database interactions, data validation, and data visualization within the project. |


---
##  Modules

<details closed><summary>.</summary>

| File                                                                                                                           | Summary                                                                                                                                                                                                                                                                                                                     |
| ---                                                                                                                            | ---                                                                                                                                                                                                                                                                                                                         |
| [logging.conf](https://github.com/org-ofirdassa9/devops-project-server/blob/master/logging.conf)                               | Code in `metrics.py` under `api/metrics_process/endpoints` calculates and updates health metrics for users. This functionality is crucial for monitoring and analyzing user health data in the application's overall architecture.                                                                                          |
| [users_service.py](https://github.com/org-ofirdassa9/devops-project-server/blob/master/users_service.py)                       | Summary: users_service.py dynamically imports FastAPI endpoint modules, adding routers for each to /api/users_service. Key features include middleware setup and exception handling for AuthJWT.                                                                                                                            |
| [users_service.Dockerfile](https://github.com/org-ofirdassa9/devops-project-server/blob/master/users_service.Dockerfile)       | Code Summary:**`users_service.Dockerfile` sets up Python environment for `users_service` API using Debian. It installs required dependencies and defines entrypoint to run the service.                                                                                                                                     |
| [logger.py](https://github.com/org-ofirdassa9/devops-project-server/blob/master/logger.py)                                     | Summary:** `logger.py` configures JSON logging format for all loggers based on `logging.conf`. Enhances log readability and structure in the `devops-project-server` architecture.                                                                                                                                          |
| [init.Dockerfile](https://github.com/org-ofirdassa9/devops-project-server/blob/master/init.Dockerfile)                         | init.Dockerfile: Execute Database Initialization****Code Snippet:** Initializes database using Python.**Role:** Bootstrap database on container start.**Supports:** `devops-project-server` architecture.                                                                                                                   |
| [report_generator.py](https://github.com/org-ofirdassa9/devops-project-server/blob/master/report_generator.py)                 | Summary:**`report_generator.py` in `devops-project-server` dynamically imports and adds FastAPI router modules for report generation endpoints, enhancing modularity and scalability of the server architecture.                                                                                                            |
| [init-requirements.txt](https://github.com/org-ofirdassa9/devops-project-server/blob/master/init-requirements.txt)             | Code snippet in `user.py` under `users_service` builds user-related endpoints using FastAPI, enhancing user management in the application.                                                                                                                                                                                  |
| [metrics_process.py](https://github.com/org-ofirdassa9/devops-project-server/blob/master/metrics_process.py)                   | Code Summary:**`metrics_process.py` in `devops-project-server` dynamically imports and adds FastAPI routers for metrics processing endpoints, enhancing modular architecture and API scalability in the repository.                                                                                                         |
| [metrics_process.Dockerfile](https://github.com/org-ofirdassa9/devops-project-server/blob/master/metrics_process.Dockerfile)   | metrics_process.Dockerfile** builds and packages metric processing application for deployment. Utilizes multiple stages and lightweight base image for efficiency. Entry point starts Uvicorn server.                                                                                                                       |
| [database_init.py](https://github.com/org-ofirdassa9/devops-project-server/blob/master/database_init.py)                       | Code Summary:** `init_db()` creates database tables, adds a sample user, and their health metrics. Logs actions and handles errors. Supports database initialization in the app's architecture.                                                                                                                             |
| [report_generator.Dockerfile](https://github.com/org-ofirdassa9/devops-project-server/blob/master/report_generator.Dockerfile) | Code Summary:**The `report_generator.Dockerfile` builds and configures a lightweight container to run the report generation service using Uvicorn. It handles Python dependencies and sets the entrypoint for the application.---For further information, please refer to the detailed repository structure provided above. |

</details>

<details closed><summary>.github.workflows</summary>

| File                                                                                                                     | Summary                                                                                                                                                                                          |
| ---                                                                                                                      | ---                                                                                                                                                                                              |
| [build-push.yaml](https://github.com/org-ofirdassa9/devops-project-server/blob/master/.github/workflows/build-push.yaml) | Code Summary:****Role:** Automates build and push operations for Docker images.**Features:** Defines CI workflow for server components deployment.                                               |
| [pytest.yaml](https://github.com/org-ofirdassa9/devops-project-server/blob/master/.github/workflows/pytest.yaml)         | Role:** Automated testing for users service endpoints. **Features:** Authorizes and tests user CRUD operations. **Context:** Located in `devops-project-server/app/api/users_service/endpoints`. |

</details>

<details closed><summary>app</summary>

| File                                                                                                 | Summary                                                                                                                                                                                                                      |
| ---                                                                                                  | ---                                                                                                                                                                                                                          |
| [___init__.py](https://github.com/org-ofirdassa9/devops-project-server/blob/master/app/___init__.py) | Code Summary:**`app/__init__.py` initializes core modules for API services like metric processing, reporting, and user management. Crucial for coordinating service functionality within the parent repository architecture. |

</details>

<details closed><summary>app.models</summary>

| File                                                                                                        | Summary                                                                                                                                                                                       |
| ---                                                                                                         | ---                                                                                                                                                                                           |
| [models.py](https://github.com/org-ofirdassa9/devops-project-server/blob/master/app/models/models.py)       | Code Summary:**Defines User and HealthMetrics models for storing user details and health metrics with relationships, contributing to data management in the parent repository's architecture. |
| [___init__.py](https://github.com/org-ofirdassa9/devops-project-server/blob/master/app/models/___init__.py) | Code Summary:**Manages app data models to store entities for the application's business logic and relationships between various components..                                                  |

</details>

<details closed><summary>app.core</summary>

| File                                                                                                    | Summary                                                                                                                                                                                                                     |
| ---                                                                                                     | ---                                                                                                                                                                                                                         |
| [database.py](https://github.com/org-ofirdassa9/devops-project-server/blob/master/app/core/database.py) | Database Connection Utility**In `app/core/database.py`, this code manages database connection setup and resources, crucial for data interaction across the application's modules in the `devops-project-server` repository. |
| [security.py](https://github.com/org-ofirdassa9/devops-project-server/blob/master/app/core/security.py) | Summary: Code snippet in app/core/security.py enforces password and email validation rules using bcrypt. Enhances user authentication and security for users_service endpoints in the repository architecture.              |
| [config.py](https://github.com/org-ofirdassa9/devops-project-server/blob/master/app/core/config.py)     | Feature Summary:**The `config.py` file in `app/core` defines project settings like project name, database URL, JWT configuration, and CORS origin. It sets security configurations and retrieves settings via Pydantic.     |

</details>

<details closed><summary>app.api.users_service</summary>

| File                                                                                                                   | Summary                                                                                                                                                                                              |
| ---                                                                                                                    | ---                                                                                                                                                                                                  |
| [___init__.py](https://github.com/org-ofirdassa9/devops-project-server/blob/master/app/api/users_service/___init__.py) | Code Summary:**Handles user-related API endpoints with authentication mechanisms. Ensures secure user operations within the app's core structure. Promotes robust user management in the repository. |

</details>

<details closed><summary>app.api.users_service.endpoints</summary>

| File                                                                                                                             | Summary                                                                                                                                                                                                                                       |
| ---                                                                                                                              | ---                                                                                                                                                                                                                                           |
| [auth.py](https://github.com/org-ofirdassa9/devops-project-server/blob/master/app/api/users_service/endpoints/auth.py)           | Code Summary:** Authentication and authorization endpoints for user signup, login, token refresh, and logout in the users_service module. Integrates with FastAPI, sqlalchemy, and JWT for secure user interactions.                          |
| [user.py](https://github.com/org-ofirdassa9/devops-project-server/blob/master/app/api/users_service/endpoints/user.py)           | Code snippet in user.py handles user endpoints, including fetching and updating user data with permissions validation, using FastAPI and SQLAlchemy. Deploys robust user and health metrics integration for complete user information access. |
| [___init__.py](https://github.com/org-ofirdassa9/devops-project-server/blob/master/app/api/users_service/endpoints/___init__.py) | Code Snippet Summary:**Manages user-related HTTP routes in the `users_service` API, facilitating user data retrieval and updates. Key role in handling user operations within the system architecture.                                        |

</details>

<details closed><summary>app.api.metrics_process.endpoints</summary>

| File                                                                                                                           | Summary                                                                                                                                                                                               |
| ---                                                                                                                            | ---                                                                                                                                                                                                   |
| [metrics.py](https://github.com/org-ofirdassa9/devops-project-server/blob/master/app/api/metrics_process/endpoints/metrics.py) | Summary:This code snippet within the parent repository's architecture updates a user's health metrics securely, ensuring data integrity and access control in a FastAPI application using SQLAlchemy. |

</details>

<details closed><summary>app.api.report_generator</summary>

| File                                                                                                                      | Summary                                                                                                      |
| ---                                                                                                                       | ---                                                                                                          |
| [generator.py](https://github.com/org-ofirdassa9/devops-project-server/blob/master/app/api/report_generator/generator.py) | Generates user health overview and trend reports based on stored metrics in the app's health tracker module. |

</details>

<details closed><summary>app.api.report_generator.endpoints</summary>

| File                                                                                                                            | Summary                                                                                                                                                                         |
| ---                                                                                                                             | ---                                                                                                                                                                             |
| [reports.py](https://github.com/org-ofirdassa9/devops-project-server/blob/master/app/api/report_generator/endpoints/reports.py) | Code in `reports.py` generates user health reports using FastAPI and Matplotlib. It ensures data privacy and visualizes metrics in bar and trend chart formats for downloading. |

</details>

<details closed><summary>app.crud</summary>

| File                                                                                                      | Summary                                                                                                                                                                                                                      |
| ---                                                                                                       | ---                                                                                                                                                                                                                          |
| [user_crud.py](https://github.com/org-ofirdassa9/devops-project-server/blob/master/app/crud/user_crud.py) | Code Summary-user_crud.py:**The code creates and authenticates users, storing health metrics. It adds new users and default metrics to the database, enhancing user data management in the parent repository's architecture. |
| [___init__.py](https://github.com/org-ofirdassa9/devops-project-server/blob/master/app/crud/___init__.py) | Code snippet in `app/crud/__init__.py` initializes CRUD operations for users. It defines user CRUD endpoints for read and update functionalities, contributing to the API layer of the parent repository's architecture.     |

</details>

<details closed><summary>app.schemas</summary>

| File                                                                                                                   | Summary                                                                                                                                                                                                                      |
| ---                                                                                                                    | ---                                                                                                                                                                                                                          |
| [user_schema.py](https://github.com/org-ofirdassa9/devops-project-server/blob/master/app/schemas/user_schema.py)       | Code Summary:**`user_schema.py` defines user data models for updates, creation, and access tokens. Crucial for maintaining user information in the project's API architecture.                                               |
| [___init__.py](https://github.com/org-ofirdassa9/devops-project-server/blob/master/app/schemas/___init__.py)           | Summary:**`app/schemas/__init__.py` defines data schemas for user authentication and health metrics. Essential for data validation and security in user-related functionalities within the parent repository's architecture. |
| [login_request.py](https://github.com/org-ofirdassa9/devops-project-server/blob/master/app/schemas/login_request.py)   | Code snippet in `app/schemas/login_request.py` defines `LoginRequest` schema with email and password fields. It plays a critical role in user authentication within the parent repository's architecture.                    |
| [health_metrics.py](https://github.com/org-ofirdassa9/devops-project-server/blob/master/app/schemas/health_metrics.py) | Summary:**`health_metrics.py` defines Pydantic models for basic and detailed user health metrics. Supports structured data validation for health-related information in user profiles within the server app.                 |

</details>

---

##  Getting Started

***Requirements***

Ensure you have the following dependencies installed on your system:

* **Python**: `version 3.8+`
* **PostgreSQL**

### Installation

1. Clone the repository:

    `git clone https://github.com/org-ofirdassa9/devops-project-server.git cd devops-project-server`

2. Set up a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate For Unix or MacOS
    venv\Scripts\activate For Windows
    ```

3. Install dependencies:

    `pip install -r requirements.txt`

4. Init the database:

    `python database_init.py`

5. Run the application:

    ```sh
    uvicorn users_service:app --reload
    uvicorn metrics_process:app --reload --port 8001
    uvicorn report_generator:app --reload --port 8002
    ```

###  Tests

Use the following command to run tests:

```sh
pytest tests
```

---
