# NexusStudent — International Student Support Platform (Russia)

## Overview

NexusStudent is a web-based platform built with Flask to support international students studying in Russia.
It centralizes essential information on visa compliance, housing, work regulations, healthcare access, and emergency services into a single, user-friendly interface.

The platform is designed to reduce confusion and provide reliable, structured guidance for students adapting to a new legal and social environment.

---

## Key Features

### 1. AI Assistant

Interactive chatbot that provides instant responses to common student queries related to:

* Visa and migration procedures
* Work regulations
* Healthcare access
* Housing rules

### 2. Resource Library

Structured and practical guides covering:

* Visa extension and registration requirements
* Accommodation and rental practices
* Legal work conditions for students
* Health insurance and medical services

### 3. Community Module

* Students can post questions and share experiences
* Encourages peer-to-peer support
* Simple discussion interface backed by SQLite

### 4. Emergency Support

* Quick access to essential emergency contacts in Russia
* Includes medical, police, and general assistance

---

## Technology Stack

| Layer    | Technology            |
| -------- | --------------------- |
| Backend  | Python (Flask)        |
| Frontend | HTML, CSS, JavaScript |
| Database | SQLite                |

---

## System Architecture

The application follows a simple client-server architecture:

* Flask handles routing, backend logic, and API endpoints
* Templates render dynamic content using Jinja2
* Static assets (CSS/JS) manage UI and interactions
* SQLite stores community posts

---

## Project Structure

```
Nexus_student/
│
├── .env
├── .gitignore
├── run.py
├── config.py
├── requirements.txt
├── README.md
│
├── database/
│   ├── __init__.py
│   ├── models.py
│   └── users.db
│
├── routes/
│   ├── __init__.py
│   ├── main_routes.py
│   ├── api_routes.py
│   ├── auth_routes.py
│   ├── profile_routes.py
│   └── admin_routes.py
│
├── services/
│   ├── __init__.py
│   ├── chatbot_service.py
│   ├── email_service.py
│   └── intents.json
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── chatbot.html
│   ├── resources.html
│   ├── community.html
│   ├── emergency.html
│   ├── profile.html
│   ├── admin.html
│   └── auth/
│       ├── login.html
│       ├── register.html
│       ├── forgot.html
│       └── reset.html
│
└── static/
    ├── style.css
    ├── main.js
    └── uploads/
        └── default.png
```

---

## Installation & Setup

### 1. Install dependencies

```
pip install flask
```

### 2. Run the application

```
python app.py
```

### 3. Access the application

Open:

```
http://127.0.0.1:5000
```

---

## Current Limitations

* Chatbot uses rule-based logic (no external AI integration)
* No authentication system (community is open)
* Local SQLite database (not scalable for production use)

---

## Future Improvements

* Integration with OpenAI API for advanced chatbot responses
* User authentication and profile system
* Deployment on cloud (AWS / Render / Railway)
* PostgreSQL database for scalability

---

## Purpose

This project was developed as part of a Flask-based assignment to demonstrate:

* Full-stack web development
* Backend API design
* Frontend UI/UX implementation
* Practical problem-solving for real-world users

---
