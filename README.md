# Advox v1

Advox v1 is a multi-service legal support platform with:
- a React + Vite frontend
- a Spring Cloud Gateway entry point
- Spring Boot microservices for authentication and ticketing
- a separate scraping service (routed through the gateway)

## Repository Structure

- `frontend/advox-frontend`: React 19 + TypeScript UI
- `services/gateway-service`: API gateway, JWT verification, request routing
- `services/login-service`: authentication and user profile APIs
- `services/ticket-service`: ticketing service skeleton

## Current Architecture and Flow

1. Frontend calls `http://localhost:8080/login/api/...` via Axios.
2. Gateway routes:
   - `/login/**` -> login-service (`http://localhost:8081`)
   - `/tickets/**` -> ticket-service (`http://localhost:8082`)
   - `/scrape/**` -> scraping-service (`http://localhost:8000`)
3. Gateway validates JWT on protected routes and injects user headers (`X-USER-ID`, etc).
4. Login service validates `X-GATEWAY-AUTH` for incoming requests from gateway.
5. Login/profile endpoints support:
   - `POST /api/auth/login`
   - `POST /api/auth/register`
   - `GET /api/auth/me`
   - `PUT /api/auth/me`

## Ports

- Frontend dev server: `5173`
- Gateway service: `8080`
- Login service: `8081`
- Ticket service: `8082`
- Scraping service (expected): `8000`

## Tech Stack

- Frontend: React, TypeScript, React Router, Axios, Vite
- Backend: Java 17+, Spring Boot, Spring Cloud Gateway
- Datastores:
  - Login service -> PostgreSQL (`advox_ticketing`)
  - Ticket service -> MongoDB (`advox_tickets`)
- Auth: JWT (HS512)

## Prerequisites

- Node.js 20+ and npm
- Java 17+
- Maven (or use each service's Maven wrapper)
- PostgreSQL running locally
- MongoDB running locally

## Run the Project Locally

### 1) Start backend services

In separate terminals:

- Gateway:
  - `cd services/gateway-service`
  - `./mvnw spring-boot:run`
- Login service:
  - `cd services/login-service`
  - `./mvnw spring-boot:run`
- Ticket service:
  - `cd services/ticket-service`
  - `./mvnw spring-boot:run`

### 2) Start frontend

- `cd frontend/advox-frontend`
- `npm install`
- `npm run dev`

### 3) Open app

- `http://localhost:5173`

## Notes and Current Status

- Frontend is wired to gateway endpoint `http://localhost:8080/login/api`.
- Route protection is implemented in frontend using auth context and token presence.
- Gateway CORS is configured for local frontend usage.
- Ticket service is currently a minimal skeleton with health endpoint.

## Next Recommended Improvements

- Move secrets and DB credentials to environment variables.
- Add Docker Compose for one-command local startup.
- Add module-level README files for each service.
- Add tests for auth flow (gateway + login-service integration).
