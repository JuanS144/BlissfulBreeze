# BlissfulBreeze - Hair Salon Management System

A web application for managing a hair salon business, built with Python, Flask, Jinja, HTML/CSS, JS, PostgreSQL.

## Features

### Core Functionality
- **Appointment Management**: Schedule, view, and manage client appointments
- **User Management**: Handle client and staff profiles with different access levels
- **Report System**: Generate and track reports for appointments and services
- **Service Management**: Organize and display salon services with pricing

### Technical Implementation
- **Flask Blueprint Architecture**: Modular application structure for scalability
- **Role-Based Access Control**: Different interfaces for clients, staff, and administrators
- **Secure Authentication**: Password hashing with bcrypt and session management
- **RESTful API**: JWT-authenticated endpoints for third-party integrations
- **Responsive Design**: Modern UI that works across devices

## Technologies Used
- **Backend**: Python, Flask, SQLAlchemy, Flask-Login
- **Frontend**: HTML, CSS, JavaScript
- **Security**: JWT, Bcrypt
- **Database**: SQLite (development) / PostgreSQL (production)

## Project Structure
The application follows a blueprint-based architecture, separating concerns into:
- User authentication
- Appointment management
- Reporting system
- Admin controls
- API endpoints

## Installation & Setup
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set environment variables
4. Initialize the database: `flask db upgrade`
5. Run the application: `flask run`
