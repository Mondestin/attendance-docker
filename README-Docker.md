# Docker Deployment Guide

This guide will help you deploy the AttendanceTrack application using Docker.

## Prerequisites

- Docker installed on your system
- Docker Compose installed
- Firebase project credentials
- Stripe account and API keys

## Quick Start

### 1. Environment Setup

Copy the example environment file and configure it with your credentials:

```bash
cp env.example .env
```

Edit `.env` file with your actual Firebase and Stripe credentials:

```bash
# Firebase Configuration
FIREBASE_SERVICE_ACCOUNT_KEY={"type":"service_account",...}
FIREBASE_CONFIG={"apiKey":"...","authDomain":"...",...}

# Stripe Configuration  
STRIPE_SK=sk_test_your_stripe_secret_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret
```

### 2. Build and Run with Docker Compose

```bash
# Build and start the application
docker-compose up --build

# Or run in detached mode
docker-compose up -d --build
```

### 3. Access the Application

- **API Documentation**: http://localhost:8000/docs
- **API Base URL**: http://localhost:8000

## Alternative: Docker Commands Only

If you prefer using Docker commands directly:

```bash
# Build the image
docker build -t attendancetrack .

# Run the container
docker run -p 8000:8000 --env-file .env attendancetrack
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `FIREBASE_SERVICE_ACCOUNT_KEY` | Firebase service account JSON | Yes |
| `FIREBASE_CONFIG` | Firebase config JSON | Yes |
| `STRIPE_SK` | Stripe secret key | Yes |
| `STRIPE_WEBHOOK_SECRET` | Stripe webhook secret | Yes |

## Troubleshooting

### Common Issues

1. **Port already in use**: Change the port in `docker-compose.yml`
2. **Environment variables not loaded**: Ensure `.env` file exists and is properly formatted
3. **Firebase connection issues**: Verify your Firebase credentials are correct

### View Logs

```bash
# View container logs
docker-compose logs attendancetrack

# Follow logs in real-time
docker-compose logs -f attendancetrack
```

### Stop the Application

```bash
# Stop and remove containers
docker-compose down

# Stop and remove containers + volumes
docker-compose down -v
```

## Production Considerations

For production deployment:

1. Use production Firebase and Stripe keys
2. Set up proper SSL/TLS certificates
3. Configure reverse proxy (nginx)
4. Set up monitoring and logging
5. Use Docker secrets for sensitive data
6. Configure proper backup strategies

## Health Check

The application includes a health check that verifies the API is responding:

```bash
# Check container health
docker-compose ps
```

The health check will restart the container if the API becomes unresponsive. 