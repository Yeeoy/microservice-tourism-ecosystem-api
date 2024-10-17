# Microservice Tourism Ecosystem API

## Project Overview

This project is a tourism ecosystem API based on microservice architecture, aimed at providing a comprehensive tourism service management solution. The system contains multiple independent microservices, each responsible for specific functional areas such as authentication, accommodation, restaurants, local transportation, etc.

## Microservice Architecture

The system includes the following microservices:

1. Auth Service: User authentication and authorization
2. Accommodation Service: Accommodation management
3. Restaurant Service: Restaurant information management
4. Local Transportation Service: Local transportation information management
5. Event Organizers Service: Event organization management
6. Information Center Service: Tourism information center

## Technology Stack

- Backend Framework: Django 3.2.10, Django REST Framework 3.12.4
- Database: SQLite (development environment)
- Containerization: Docker
- Service Orchestration: Docker Compose
- Service Discovery: Consul 1.15.0
- API Documentation: drf-spectacular 0.27.0
- Authentication: JWT (JSON Web Tokens)
- Reverse Proxy: Nginx

## Quick Start

### Prerequisites

- Docker
- Docker Compose

### Installing Docker and Docker Compose

#### Windows:
1. Visit [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop) to download the Docker Desktop installer.
2. Double-click the downloaded installation file and follow the installation wizard's instructions.
3. After installation, Docker Desktop will start automatically. You can see the Docker icon in the system tray.

#### Mac:
1. Visit [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop) to download the Docker Desktop installer.
2. Double-click the downloaded .dmg file and drag Docker to the Applications folder.
3. Open Docker from the Applications folder.
4. The system may ask you to authorize Docker for access permissions, please follow the prompts.

Note: Docker Desktop includes Docker Engine, Docker CLI client, Docker Compose, and other tools.

### Verifying Installation

After installation, open Terminal (Mac) or PowerShell (Windows) and run the following commands to verify the installation:

```
docker --version
docker compose version
```

If version information is displayed, the installation was successful.

### Starting Services

1. Open Terminal (Mac) or PowerShell/Command Prompt (Windows)
2. Clone the repository:
   ```
   git clone https://github.com/Yeeoy/microservice-tourism-ecosystem-api.git
   cd microservice-tourism-ecosystem-api
   ```
3. Build and start services:

   Windows:
   ```
   docker-compose up --build
   ```

   Mac:
   ```
   docker compose up --build
   ```

   Note: If you encounter permission issues on Mac, you may need to use sudo:
   ```
   sudo docker compose up --build
   ```

4. Accessing services:

   All services can be accessed via http://localhost:8000, with specific endpoints as follows:

   - Auth Service: http://localhost:8000/api/customUser/
   - Accommodation Service: http://localhost:8000/api/accommodation/
   - Restaurant Service: http://localhost:8000/api/restaurant/
   - Local Transportation Service: http://localhost:8000/api/local-transportation/
   - Event Organizers Service: http://localhost:8000/api/event-organizers/
   - Information Center Service: http://localhost:8000/api/information-center/

   API documentation and admin interface for each service can be accessed as follows:
   - API Documentation: http://localhost:8000/api/[service-name]/docs/
   - Admin Interface: http://localhost:8000/api/[service-name]/admin/

   For example, for the Auth Service:
   - API Documentation: http://localhost:8000/api/customUser/docs/
   - Admin Interface: http://localhost:8000/api/customUser/admin/

### Stopping Services

To stop all running containers:

- Press Ctrl+C in Terminal/PowerShell/Command Prompt (Use Control+C on Mac)

Or, run the following in the project directory:

Windows:
```
docker-compose down
```

Mac:
```
docker compose down
```

## API Documentation

Each service provides Swagger UI documentation, which can be viewed by accessing `/api/[service-name]/docs/`.

## Authentication

The system uses JWT for authentication. To access protected endpoints, you need to include a valid JWT token in the request header: Authorization: Bearer <your_jwt_token>

## Service Endpoints

The system contains the following main service endpoints:

- Auth Service: `/api/customUser/`
- Accommodation Service: `/api/accommodation/`
- Restaurant Service: `/api/restaurant/`
- Local Transportation Service: `/api/local-transportation/`
- Event Organizers Service: `/api/event-organizers/`
- Information Center Service: `/api/information-center/`

Each service has its specific API endpoints. Please refer to each service's API documentation for detailed endpoint information and usage instructions.

## Development Guide

### Project Structure

Each microservice has its own Dockerfile and Django project structure. The main configuration files include:

- `docker-compose.yml`: Defines container configurations for all microservices
- `nginx.conf`: Nginx reverse proxy configuration
- `[service_name]/Dockerfile`: Docker build files for each service
- `[service_name]/[service_name]/settings.py`: Django settings files

### Adding a New Microservice

1. Create a new service directory in the project root
2. Create a Django project and application in the new directory
3. Create a Dockerfile
4. Update `docker-compose.yml` to add the new service
5. Add routing configuration for the new service in `nginx.conf`

### Running Tests

Each microservice has its own test suite. To run tests, enter the corresponding service directory and execute:

python manage.py test
