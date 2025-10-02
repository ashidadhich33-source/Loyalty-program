# ERP API Documentation

## Overview

This document provides comprehensive API documentation for the Odoo-Style ERP system for Kids' Clothing Retail Industry.

## Base URL

```
http://localhost:3000/api
```

## Authentication

The API uses JWT (JSON Web Token) for authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

## Response Format

All API responses follow a consistent format:

```json
{
  "success": true,
  "message": "Operation completed successfully",
  "data": {
    // Response data
  }
}
```

## Error Format

Error responses follow this format:

```json
{
  "success": false,
  "error": {
    "message": "Error description",
    "code": "ERROR_CODE",
    "statusCode": 400,
    "timestamp": "2024-01-01T00:00:00.000Z",
    "path": "/api/endpoint"
  }
}
```

## Status Codes

- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `409` - Conflict
- `429` - Too Many Requests
- `500` - Internal Server Error

---

## Authentication Endpoints

### Register User
**POST** `/auth/register`

Register a new user account.

**Request Body:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepassword123",
  "first_name": "John",
  "last_name": "Doe",
  "company_id": "optional-company-id"
}
```

**Response:**
```json
{
  "success": true,
  "message": "User registered successfully",
  "data": {
    "user": {
      "id": "user-id",
      "username": "john_doe",
      "email": "john@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "role": "employee",
      "status": "active",
      "created_at": "2024-01-01T00:00:00.000Z"
    }
  }
}
```

### Login User
**POST** `/auth/login`

Authenticate user and get access token.

**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "securepassword123",
  "device_info": {
    "device_id": "device-123",
    "device_name": "iPhone 12",
    "device_type": "mobile",
    "browser": "Safari",
    "os": "iOS 15.0",
    "location": "New York, NY"
  }
}
```

**Response:**
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "user": {
      "id": "user-id",
      "username": "john_doe",
      "email": "john@example.com",
      "role": "employee",
      "status": "active"
    },
    "session": {
      "id": "session-id",
      "type": "web",
      "status": "active",
      "device": {
        "id": "device-123",
        "name": "iPhone 12",
        "type": "mobile"
      },
      "last_activity": "2024-01-01T00:00:00.000Z",
      "expires_at": "2024-01-02T00:00:00.000Z"
    },
    "tokens": {
      "access_token": "jwt-access-token",
      "refresh_token": "jwt-refresh-token"
    }
  }
}
```

### Refresh Token
**POST** `/auth/refresh`

Refresh access token using refresh token.

**Request Body:**
```json
{
  "refresh_token": "jwt-refresh-token"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Token refreshed successfully",
  "data": {
    "tokens": {
      "access_token": "new-jwt-access-token",
      "refresh_token": "new-jwt-refresh-token"
    }
  }
}
```

### Logout
**POST** `/auth/logout`

Logout current session.

**Headers:**
```
Authorization: Bearer <access-token>
```

**Response:**
```json
{
  "success": true,
  "message": "Logout successful"
}
```

### Get User Profile
**GET** `/auth/profile`

Get current user profile.

**Headers:**
```
Authorization: Bearer <access-token>
```

**Response:**
```json
{
  "success": true,
  "message": "Profile retrieved successfully",
  "data": {
    "user": {
      "id": "user-id",
      "username": "john_doe",
      "email": "john@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "role": "employee",
      "status": "active",
      "company": {
        "id": "company-id",
        "name": "Example Company"
      }
    }
  }
}
```

---

## User Management Endpoints

### Get Users
**GET** `/users`

Get list of users with pagination and filtering.

**Headers:**
```
Authorization: Bearer <access-token>
```

**Query Parameters:**
- `page` (number): Page number (default: 1)
- `limit` (number): Items per page (default: 10)
- `search` (string): Search term
- `role` (string): Filter by role
- `status` (string): Filter by status
- `company_id` (string): Filter by company
- `sort_by` (string): Sort field (default: created_at)
- `sort_order` (string): Sort order (ASC/DESC, default: DESC)

**Response:**
```json
{
  "success": true,
  "message": "Users retrieved successfully",
  "data": {
    "users": [
      {
        "id": "user-id",
        "username": "john_doe",
        "email": "john@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "role": "employee",
        "status": "active",
        "created_at": "2024-01-01T00:00:00.000Z"
      }
    ],
    "pagination": {
      "total": 100,
      "page": 1,
      "limit": 10,
      "pages": 10
    }
  }
}
```

### Get User by ID
**GET** `/users/:id`

Get specific user by ID.

**Headers:**
```
Authorization: Bearer <access-token>
```

**Response:**
```json
{
  "success": true,
  "message": "User retrieved successfully",
  "data": {
    "user": {
      "id": "user-id",
      "username": "john_doe",
      "email": "john@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "role": "employee",
      "status": "active",
      "company": {
        "id": "company-id",
        "name": "Example Company"
      },
      "user_groups": [
        {
          "id": "group-id",
          "name": "Sales Team",
          "type": "department"
        }
      ]
    }
  }
}
```

### Create User
**POST** `/users`

Create a new user.

**Headers:**
```
Authorization: Bearer <access-token>
```

**Request Body:**
```json
{
  "username": "jane_doe",
  "email": "jane@example.com",
  "password": "securepassword123",
  "first_name": "Jane",
  "last_name": "Doe",
  "phone": "+1234567890",
  "role": "employee",
  "status": "active",
  "company_id": "company-id"
}
```

**Response:**
```json
{
  "success": true,
  "message": "User created successfully",
  "data": {
    "user": {
      "id": "new-user-id",
      "username": "jane_doe",
      "email": "jane@example.com",
      "first_name": "Jane",
      "last_name": "Doe",
      "role": "employee",
      "status": "active",
      "created_at": "2024-01-01T00:00:00.000Z"
    }
  }
}
```

### Update User
**PUT** `/users/:id`

Update user information.

**Headers:**
```
Authorization: Bearer <access-token>
```

**Request Body:**
```json
{
  "first_name": "Jane",
  "last_name": "Smith",
  "phone": "+1234567890",
  "role": "manager"
}
```

**Response:**
```json
{
  "success": true,
  "message": "User updated successfully",
  "data": {
    "user": {
      "id": "user-id",
      "username": "jane_doe",
      "email": "jane@example.com",
      "first_name": "Jane",
      "last_name": "Smith",
      "phone": "+1234567890",
      "role": "manager",
      "updated_at": "2024-01-01T00:00:00.000Z"
    }
  }
}
```

### Delete User
**DELETE** `/users/:id`

Delete user (soft delete).

**Headers:**
```
Authorization: Bearer <access-token>
```

**Response:**
```json
{
  "success": true,
  "message": "User deleted successfully"
}
```

---

## Company Management Endpoints

### Get Companies
**GET** `/companies`

Get list of companies with pagination and filtering.

**Headers:**
```
Authorization: Bearer <access-token>
```

**Query Parameters:**
- `page` (number): Page number (default: 1)
- `limit` (number): Items per page (default: 10)
- `search` (string): Search term
- `type` (string): Filter by company type
- `status` (string): Filter by status
- `sort_by` (string): Sort field (default: created_at)
- `sort_order` (string): Sort order (ASC/DESC, default: DESC)

**Response:**
```json
{
  "success": true,
  "message": "Companies retrieved successfully",
  "data": {
    "companies": [
      {
        "id": "company-id",
        "name": "Example Company",
        "legal_name": "Example Company Ltd.",
        "email": "info@example.com",
        "type": "retail",
        "status": "active",
        "created_at": "2024-01-01T00:00:00.000Z"
      }
    ],
    "pagination": {
      "total": 50,
      "page": 1,
      "limit": 10,
      "pages": 5
    }
  }
}
```

### Get Company by ID
**GET** `/companies/:id`

Get specific company by ID.

**Headers:**
```
Authorization: Bearer <access-token>
```

**Response:**
```json
{
  "success": true,
  "message": "Company retrieved successfully",
  "data": {
    "company": {
      "id": "company-id",
      "name": "Example Company",
      "legal_name": "Example Company Ltd.",
      "email": "info@example.com",
      "phone": "+1234567890",
      "address": "123 Main St",
      "city": "New York",
      "state": "NY",
      "postal_code": "10001",
      "country": "USA",
      "type": "retail",
      "status": "active",
      "currency": "USD",
      "language": "en",
      "timezone": "UTC",
      "gst_enabled": false,
      "pos_enabled": true,
      "ecommerce_enabled": false,
      "users": [
        {
          "id": "user-id",
          "username": "john_doe",
          "email": "john@example.com",
          "role": "admin"
        }
      ]
    }
  }
}
```

### Create Company
**POST** `/companies`

Create a new company.

**Headers:**
```
Authorization: Bearer <access-token>
```

**Request Body:**
```json
{
  "name": "New Company",
  "legal_name": "New Company Ltd.",
  "email": "info@newcompany.com",
  "phone": "+1234567890",
  "address": "456 Oak St",
  "city": "Los Angeles",
  "state": "CA",
  "postal_code": "90210",
  "country": "USA",
  "type": "retail",
  "currency": "USD",
  "language": "en",
  "timezone": "America/Los_Angeles"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Company created successfully",
  "data": {
    "company": {
      "id": "new-company-id",
      "name": "New Company",
      "legal_name": "New Company Ltd.",
      "email": "info@newcompany.com",
      "type": "retail",
      "status": "active",
      "created_at": "2024-01-01T00:00:00.000Z"
    }
  }
}
```

### Update Company
**PUT** `/companies/:id`

Update company information.

**Headers:**
```
Authorization: Bearer <access-token>
```

**Request Body:**
```json
{
  "name": "Updated Company",
  "email": "info@updatedcompany.com",
  "phone": "+1987654321",
  "pos_enabled": true,
  "ecommerce_enabled": true
}
```

**Response:**
```json
{
  "success": true,
  "message": "Company updated successfully",
  "data": {
    "company": {
      "id": "company-id",
      "name": "Updated Company",
      "email": "info@updatedcompany.com",
      "phone": "+1987654321",
      "pos_enabled": true,
      "ecommerce_enabled": true,
      "updated_at": "2024-01-01T00:00:00.000Z"
    }
  }
}
```

### Get Company Users
**GET** `/companies/:id/users`

Get users belonging to a specific company.

**Headers:**
```
Authorization: Bearer <access-token>
```

**Query Parameters:**
- `page` (number): Page number (default: 1)
- `limit` (number): Items per page (default: 10)
- `search` (string): Search term
- `role` (string): Filter by role
- `status` (string): Filter by status

**Response:**
```json
{
  "success": true,
  "message": "Company users retrieved successfully",
  "data": {
    "users": [
      {
        "id": "user-id",
        "username": "john_doe",
        "email": "john@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "role": "admin",
        "status": "active"
      }
    ],
    "pagination": {
      "total": 25,
      "page": 1,
      "limit": 10,
      "pages": 3
    }
  }
}
```

---

## Health Check Endpoints

### Basic Health Check
**GET** `/health`

Get basic health status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00.000Z",
  "uptime": 3600,
  "memory": {
    "rss": 50000000,
    "heapTotal": 20000000,
    "heapUsed": 15000000,
    "external": 1000000
  },
  "version": "v18.0.0",
  "environment": "development",
  "services": {
    "database": "healthy"
  }
}
```

### Detailed Health Check
**GET** `/health/detailed`

Get detailed health information.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00.000Z",
  "uptime": 3600,
  "memory": {
    "rss": 50000000,
    "heapTotal": 20000000,
    "heapUsed": 15000000,
    "external": 1000000
  },
  "cpu": {
    "user": 1000000,
    "system": 500000
  },
  "version": "v18.0.0",
  "environment": "development",
  "services": {
    "database": {
      "status": "healthy",
      "connection": "connected"
    }
  },
  "system": {
    "platform": "linux",
    "arch": "x64",
    "pid": 12345,
    "title": "node"
  }
}
```

---

## Error Codes

| Code | Description |
|------|-------------|
| `MISSING_FIELDS` | Required fields are missing |
| `INVALID_CREDENTIALS` | Invalid email or password |
| `USER_EXISTS` | User already exists |
| `USER_NOT_FOUND` | User not found |
| `COMPANY_EXISTS` | Company already exists |
| `COMPANY_NOT_FOUND` | Company not found |
| `INVALID_TOKEN` | Invalid or expired token |
| `AUTH_REQUIRED` | Authentication required |
| `INSUFFICIENT_PERMISSIONS` | Insufficient permissions |
| `RATE_LIMIT_EXCEEDED` | Rate limit exceeded |

---

## Rate Limiting

The API implements rate limiting to prevent abuse:

- **Authentication endpoints**: 5 requests per 15 minutes per IP
- **API endpoints**: 100 requests per 15 minutes per IP
- **General endpoints**: 1000 requests per 15 minutes per IP

Rate limit headers are included in responses:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640995200
```

---

## Pagination

List endpoints support pagination with the following parameters:

- `page`: Page number (default: 1)
- `limit`: Items per page (default: 10, max: 100)

Response includes pagination metadata:
```json
{
  "pagination": {
    "total": 1000,
    "page": 1,
    "limit": 10,
    "pages": 100
  }
}
```

---

## Filtering and Sorting

List endpoints support filtering and sorting:

**Filtering:**
- Use query parameters to filter results
- String filters support partial matching (case-insensitive)
- Date filters support range queries

**Sorting:**
- `sort_by`: Field to sort by
- `sort_order`: Sort direction (ASC/DESC)

**Example:**
```
GET /api/users?search=john&role=admin&status=active&sort_by=created_at&sort_order=DESC
```

---

## Webhooks

The API supports webhooks for real-time notifications. Webhook endpoints will be documented in future versions.

---

## SDKs and Libraries

Official SDKs and libraries will be provided for:
- JavaScript/Node.js
- Python
- PHP
- Java
- C#

---

## Support

For API support and questions:
- Email: api-support@erpcompany.com
- Documentation: https://docs.erpcompany.com
- Status Page: https://status.erpcompany.com