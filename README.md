# 🔧 Liemo API

> Django + PostgreSQL backend for the Liemo live store link aggregator platform.

## Tech Stack
- **Framework:** Django 5.x + Django REST Framework
- **Database:** PostgreSQL 16
- **Cache:** Redis
- **Task Queue:** Celery + Redis
- **Auth:** JWT (djangorestframework-simplejwt)
- **Docs:** drf-spectacular (OpenAPI 3.0)

## Getting Started

```bash
# Clone and setup
git clone https://github.com/liemo-platform/liemo-api.git
cd liemo-api
cp .env.example .env

# Start with Docker
docker-compose up -d

# Run migrations
docker-compose exec api python manage.py migrate

# Create superuser
docker-compose exec api python manage.py createsuperuser
```

## API Documentation
- Swagger UI: `http://localhost:8000/api/docs/`
- ReDoc: `http://localhost:8000/api/redoc/`

## Branches
| Branch | Purpose |
|--------|---------|
| `main` | Production |
| `develop` | Development |
| `feature/*` | Feature branches |

## Related Repos
- [liemo-mobile](https://github.com/liemo-platform/liemo-mobile) — Flutter app
- [liemo-web-admin](https://github.com/liemo-platform/liemo-web-admin) — Store owner dashboard
- [liemo-web-superadmin](https://github.com/liemo-platform/liemo-web-superadmin) — Super admin panel
- [liemo-infra](https://github.com/liemo-platform/liemo-infra) — Infrastructure
- [liemo-docs](https://github.com/liemo-platform/liemo-docs) — Documentation

---
*Liemo — Live Store Link Aggregator | Philippines 🇵🇭 & Kuwait 🇰🇼*
