# Access Control Matrix

## 1. Purpose

The Apex Manufacturing Intelligence & Predictive Operations Platform uses role-based access control (RBAC) to restrict API functionality according to user responsibilities.

Authentication verifies the identity of the user, while authorization determines which business capabilities the authenticated user can access.

The authorization model is implemented using roles stored in PostgreSQL and role claims included in JWT access tokens.

---

## 2. Application Roles

| Role                 | Primary Responsibility                                                          |
| -------------------- | ------------------------------------------------------------------------------- |
| Executive            | Monitor business performance and operational KPIs                               |
| Production Manager   | Monitor production performance and operational efficiency                       |
| Maintenance Manager  | Monitor machine health, maintenance activity, and predictive maintenance alerts |
| Data Analyst         | Perform business and operational analytics                                      |
| Data Scientist       | Perform analytics and machine-learning operations                               |
| Data Administrator   | Monitor and manage data-quality activities                                      |
| System Administrator | Manage and monitor the overall application environment                          |

---

## 3. API Access Matrix

| API Area                  | Executive | Production Manager | Maintenance Manager | Data Analyst | Data Scientist | Data Administrator | System Administrator |
| ------------------------- | :-------: | :----------------: | :-----------------: | :----------: | :------------: | :----------------: | :------------------: |
| KPI Dashboard             |     ✓     |          ✓         |          —          |       ✓      |        ✓       |          —         |           ✓          |
| Production Performance    |     ✓     |          ✓         |          —          |       ✓      |        ✓       |          —         |           ✓          |
| Facility Performance      |     ✓     |          ✓         |          —          |       ✓      |        ✓       |          —         |           ✓          |
| Machine Risk Distribution |     ✓     |          —         |          ✓          |       ✓      |        ✓       |          —         |           ✓          |
| Machine Health            |     —     |          —         |          ✓          |       ✓      |        ✓       |          —         |           ✓          |
| Maintenance Alerts        |     —     |          —         |          ✓          |       —      |        ✓       |          —         |           ✓          |
| Machine Prediction        |     —     |          —         |          ✓          |       —      |        ✓       |          —         |           ✓          |
| Production Analytics      |     ✓     |          ✓         |          —          |       ✓      |        ✓       |          —         |           ✓          |
| Downtime Analytics        |     ✓     |          ✓         |          —          |       ✓      |        ✓       |          —         |           ✓          |
| Quality Analytics         |     ✓     |          ✓         |          —          |       ✓      |        ✓       |          —         |           ✓          |
| Machine Analytics         |     ✓     |          —         |          ✓          |       ✓      |        ✓       |          —         |           ✓          |
| Data Quality Summary      |     —     |          —         |          —          |       ✓      |        ✓       |          ✓         |           ✓          |
| Data Quality Issues       |     —     |          —         |          —          |       ✓      |        ✓       |          ✓         |           ✓          |
| Validation Run History    |     —     |          —         |          —          |       ✓      |        ✓       |          ✓         |           ✓          |

`✓` = Authorized
`—` = Not authorized

---

## 4. Authentication

All protected API endpoints require a valid JWT access token.

The authentication flow is:

```text
User
  ↓
Login Request
  ↓
Username and Password Validation
  ↓
Password Hash Verification
  ↓
User Role Lookup
  ↓
JWT Access Token Generation
  ↓
Authenticated API Request
```

The JWT contains:

* User ID
* Username
* Role
* Expiration time

Example JWT claims:

```json
{
    "sub": "2",
    "username": "analyst",
    "role": "Data Analyst",
    "exp": "token expiration timestamp"
}
```

---

## 5. Authorization

After authentication, the API extracts the user's role from the JWT.

The authorization process is:

```text
API Request
     ↓
JWT Validation
     ↓
Token Decoded
     ↓
Role Extracted
     ↓
Role Permission Check
     ↓
 ┌───────────────┐
 │ Authorized?   │
 └───────┬───────┘
       Yes│       │No
          ↓       ↓
      API Data   HTTP 403
```

Users who are authenticated but do not have permission for a specific endpoint receive:

```http
403 Forbidden
```

with:

```json
{
    "detail": "Insufficient permissions"
}
```

---

## 6. Authentication vs Authorization

Authentication and authorization are separate security controls.

### Authentication

Answers:

> Who is the user?

The system verifies the username and password and generates a JWT access token.

### Authorization

Answers:

> What is the user allowed to access?

The system checks the role contained in the JWT against the permissions configured for the API endpoint.

---

## 7. Security Controls

The application implements the following security controls:

| Control                 | Implementation                     |
| ----------------------- | ---------------------------------- |
| Password hashing        | Argon2 through `pwdlib`            |
| Authentication          | Username and password              |
| Session mechanism       | JWT access tokens                  |
| Token algorithm         | HS256                              |
| Token expiration        | 60 minutes                         |
| API authentication      | HTTP Bearer authentication         |
| Authorization           | Role-based access control          |
| Unauthorized request    | HTTP 401                           |
| Insufficient permission | HTTP 403                           |
| Account status          | Active/inactive account validation |
| Login tracking          | Last-login timestamp               |

---

## 8. RBAC Validation

RBAC was validated using multiple application users.

### Data Analyst

The Data Analyst user was successfully authorized to access:

```text
GET /analytics/production
```

The same user was denied access to:

```text
GET /maintenance-alerts
```

The API returned:

```http
403 Forbidden
```

with:

```json
{
    "detail": "Insufficient permissions"
}
```

### Maintenance Manager

A Maintenance Manager test user was successfully authenticated and authorized to access:

```text
GET /maintenance-alerts
```

This confirms that authorization is based on the user's assigned role rather than authentication alone.

---

## 9. Security Architecture

The overall security architecture is:

```text
                    ┌──────────────────────┐
                    │      Application     │
                    │       User           │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    POST /auth/login  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    PostgreSQL        │
                    │    app_user          │
                    │    user_role         │
                    │    role              │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Password Verify    │
                    │      Argon2           │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    JWT Access Token  │
                    │   User + Role + Exp  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │     Protected API    │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   JWT Verification   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    RBAC Permission   │
                    │        Check         │
                    └───────┬───────┬──────┘
                            │       │
                     Authorized    Denied
                            │       │
                            ▼       ▼
                         HTTP 200  HTTP 403
```

---

## 10. Design Principles

The authorization model follows these principles:

1. Users receive permissions through roles rather than individual endpoint assignments.
2. Authentication is required before accessing protected business APIs.
3. Authorization is evaluated for each protected endpoint.
4. Sensitive maintenance and predictive operations are restricted to appropriate technical roles.
5. Data-quality functionality is restricted to data-oriented roles and system administrators.
6. Executive access focuses on business-level analytics and KPIs.
7. System administrators have broad operational access.
8. Unauthorized users receive a `403 Forbidden` response.
9. Invalid or expired authentication tokens receive a `401 Unauthorized` response.
10. Passwords are never stored in plaintext.

---

## 11. Future Security Enhancements

Potential future improvements include:

* Refresh tokens
* Secure secret management using environment variables or a secrets manager
* Token revocation
* Login rate limiting
* Account lockout after repeated failed login attempts
* Audit logging for sensitive API operations
* HTTPS/TLS in production
* More granular permission-based authorization
* Multi-factor authentication
* Security monitoring and alerting

---

## 12. Summary

The Apex Manufacturing platform implements authentication and role-based authorization using PostgreSQL, Argon2 password hashing, JWT access tokens, FastAPI security dependencies, and role-based permission checks.

The RBAC implementation has been validated with both authorized and unauthorized role scenarios, providing a security layer appropriate for the platform's business and operational API architecture.
