# Chemistry Shop 

![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-ff1709?style=for-the-badge&logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![Celery](https://img.shields.io/badge/Celery-37B24D?style=for-the-badge&logo=celery&logoColor=white)
![Stripe](https://img.shields.io/badge/Stripe-008CDD?style=for-the-badge&logo=stripe&logoColor=white)
- jwt authentication with email confirmation via djoser
- stripe payment processing with webhooks
- shopping cart and order management
- product catalog with categories and search
- admin panel for inventory management
- background tasks with celery (session and tokens cleanup)
- redis caching for images and sessions
- email notifications for orders and confirmations

## tech stuff

- django 4.2
- django-rest-framework
- djoser
- htmx
- celery
- redis
- nginx
- docker

## run it

### quick start

```bash
git clone this
cd backend
```

make a `.env` in `chemistry_shop/`:

```bash
SECRET_KEY=your-super-secret-key
DEBUG=False
POSTGRES_DB=chemistry_shop
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-db-password
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
REDIS_URL=redis://redis:6379/0
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password
STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_key
STRIPE_SECRET_KEY=sk_test_your_stripe_secret
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret
```

setup database:
```bash
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
```
browse to localhost

## api

```bash
GET /api/ingredients/    
GET /api/categories/
```

also added standart djoser api's as /auth/users/me/, /auth/users/ etc.

## background tasks
celery handles:

session cleanup (removes expired sessions)
token blacklist cleanup (clears old jwt tokens)
image caching (manages product images)
email sending (order confirmations, notifications)

redis acts as both cache and celery message broker.
## docker details

postgres stores all data
redis handles caching + celery tasks
backend runs django api
celery processes background tasks
nginx serves static files + proxies api requests

nginx config handles proxy headers for django's cors/csrf stuff.
volumes persist database, redis data, static files, and media uploads.
## stripe setup

create stripe account
get api keys from dashboard
set webhook endpoint: https://yourdomain.com/api/payments/webhook/ or you can use stripe-cli on your local machine

add webhook secret to env file

webhook handles payment confirmations and order status updates.
## email setup
uses gmail smtp:

enable 2fa on gmail account
generate app password
use app password in EMAIL_HOST_PASSWORD

sends confirmation emails for registration and order notifications.
