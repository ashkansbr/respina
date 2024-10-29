A Django REST API for managing ads and comments. This project allows users to register, create ads, add comments, and manage their content, with permissions and authentication managed through JSON Web Tokens (JWT).

Features

User Registration: Register users with a unique email and password.
JWT Authentication: Token-based authentication for secure access.
Ad Management: CRUD operations for ads, with owner-only permissions for updates and deletes.
Comment Management: Users can post one comment per ad, viewable by anyone.
Containerized: Easily deployable with Docker and Docker Compose.


Getting Started

Prerequisites
Docker and Docker Compose
Python 3.8+ (if running locally)

git clone https://github.com/ashkansbr/respina.git

Use Docker Compose to build and start the containers:

docker-compose up --build


Run Database Migrations:

After the containers are running, apply the database migrations with:

docker-compose exec web python manage.py migrate

Testing the API
You can run the test suite using pytest with Docker:

docker-compose run web pytest

