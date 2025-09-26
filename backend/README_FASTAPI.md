# MashinMan - FastAPI Migration

This document describes the migration of the MashinMan project from Django to FastAPI.

## Overview

The original MashinMan project was built using Django with MongoDB (via mongoengine). This migration re-implements the backend using FastAPI, providing:

1. Asynchronous performance improvements
2. Modern Python typing support
3. Improved API documentation with Swagger/OpenAPI
4. Better development experience

## Key Changes

### Framework Migration
- Replaced Django with FastAPI
- Replaced Django REST Framework with native FastAPI features
- Replaced mongoengine with Beanie ODM for MongoDB
- Replaced Django's synchronous ORM with Motor (async MongoDB driver)

### Authentication & Security
- Replaced `djangorestframework-simplejwt` with custom JWT implementation
- Maintained similar token structure (access and refresh tokens)
- Kept password hashing using bcrypt through passlib

### Configuration Management
- Replaced Django settings with Pydantic Settings
- Environment variable support maintained
- Similar structure with development/production environments

### Database Models
- Converted mongoengine models to Beanie Documents
- Maintained the same data structure and relationships
- Added Pydantic models for request/response validation

## New Structure

```
backend/
├── core/                 # Core utilities and configurations
│   ├── config.py         # Application settings
│   ├── database.py       # Database connection
│   └── security.py       # Authentication and security utilities
├── users/                # Users module
│   ├── api.py            # API routes
│   ├── models.py         # Data models and Pydantic schemas
│   ├── service.py        # Business logic
│   └── dependencies.py   # FastAPI dependencies
├── main.py               # FastAPI application entry point
└── requirements-fastapi.txt  # Dependencies
```

## Installation

1. Install dependencies:
```bash
pip install -r requirements-fastapi.txt
```

2. Set up environment variables in a `.env` file:
```env
ENVIRONMENT=development
SECRET_KEY=your-secret-key
MONGODB_DB=mashinman
MONGODB_HOST=localhost
MONGODB_PORT=27017
```

3. Run the application:
```bash
uvicorn main:app --reload
```

## API Documentation

FastAPI automatically generates interactive API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Migration Status

This is a partial migration focusing on:
- [x] Core infrastructure (database, auth, config)
- [x] User management module
- [ ] Vehicles module
- [ ] Services module
- [ ] History module
- [ ] Pricing module
- [ ] Emergency module

To complete the migration, similar patterns would need to be applied to the remaining modules.

## Benefits of Migration

1. **Performance**: Asynchronous architecture improves throughput
2. **Type Safety**: Full Python typing support reduces bugs
3. **Developer Experience**: Automatic API documentation and validation
4. **Modern Standards**: Uses current best practices in Python web development
5. **Scalability**: Better suited for microservices architecture