# OMNEXA AI — Django Backend

Complete production-ready Django backend for OMNEXA AI website with REST API, admin panel, and all content management features.

## 🛠️ Tech Stack

- **Language**: Python 3.11+
- **Framework**: Django 5.x
- **REST API**: Django REST Framework (DRF)
- **Database**: PostgreSQL (production) / SQLite (development)
- **Media Storage**: Django's default `MEDIA_ROOT` (configurable for AWS S3/Cloudinary)
- **Email**: Django's SMTP backend (configurable for SendGrid/Mailgun)
- **Authentication**: Django's built-in auth (staff/admin only)
- **CORS**: `django-cors-headers`
- **Environment**: `python-decouple` for `.env` management

## 📁 Project Structure

```
omnexa_ai/
├── manage.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
│
├── omnexa_ai/               ← Django project config
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── core/                    ← Shared utilities, base models
│   ├── models.py
│   ├── utils.py
│   └── context_processors.py
│
├── home/                    ← Home page backend
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── services/                ← Services page backend
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── solutions/               ← Solutions page backend
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── case_studies/            ← Case studies backend
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── blog/                    ← Blog backend
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── about/                   ← About page backend
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── contact/                 ← Contact/lead capture backend
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── chatbot/                 ← Chatbot widget backend
│   ├── models.py
│   ├── views.py
│   └── urls.py
│
├── careers/                 ← Careers page backend
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── templates/               ← Django HTML templates
│   ├── base.html
│   ├── home/
│   ├── services/
│   ├── solutions/
│   ├── case_studies/
│   ├── blog/
│   ├── about/
│   ├── contact/
│   └── careers/
│
├── media/                  ← User uploaded files
├── static/                 ← Static assets
└── logs/                   ← Application logs
```

## 🚀 Quick Start

### 1. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

```bash
cp .env.example .env
# Edit .env with your configuration
```

### 4. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser (for Django Admin)

```bash
python manage.py createsuperuser
```

### 6. Run Development Server

```bash
python manage.py runserver
```

### 7. Access Django Admin

```
http://127.0.0.1:8000/admin/
```

## 🌐 API Endpoints

### Contact & Leads
- `POST /api/v1/contact/book/` - Submit consultation booking
- `POST /api/v1/contact/newsletter/` - Newsletter signup

### Services
- `GET /api/v1/services/` - List all services
- `GET /api/v1/services/<slug>/` - Single service detail

### Solutions
- `GET /api/v1/solutions/` - List all industry solutions
- `GET /api/v1/solutions/<industry>/` - Single industry solution

### Case Studies
- `GET /api/v1/case-studies/` - List all case studies
- `GET /api/v1/case-studies/<slug>/` - Single case study

### Blog
- `GET /api/v1/blog/` - List blog posts (with `?category=` filter)
- `GET /api/v1/blog/<slug>/` - Single blog post

### Chatbot
- `POST /api/v1/chatbot/message/` - Send/receive chatbot message
- `GET /api/v1/chatbot/history/?session_key=xxx` - Get chat history
- `DELETE /api/v1/chatbot/clear/?session_key=xxx` - Clear chat history

### Careers
- `GET /api/v1/careers/` - Get careers page content
- `GET /api/v1/careers/jobs/` - List all job openings
- `GET /api/v1/careers/jobs/<slug>/` - Single job detail
- `POST /api/v1/careers/apply/` - Submit job application
- `GET /api/v1/careers/benefits/` - List company benefits

## 🔒 Security Checklist

For production deployment, ensure:

1. **Set `DEBUG = False`** in `.env`
2. **Generate secure `SECRET_KEY`**
3. **Configure PostgreSQL database**
4. **Set up proper `ALLOWED_HOSTS`**
5. **Configure email backend**
6. **Enable HTTPS** (SSL/TLS)
7. **Set up static file serving** (Whitenoise or CDN)
8. **Configure CORS properly**
9. **Set up rate limiting** (already configured in DRF)
10. **Use environment variables** for sensitive data

## 📧 Email Configuration

The backend sends emails for:
- Consultation booking confirmations
- New lead notifications to admin
- Job application confirmations
- New application notifications to HR

Configure email settings in `.env`:
```
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

## 🗄️ Database

### Development (SQLite)
Default configuration uses SQLite - no setup needed.

### Production (PostgreSQL)
Uncomment PostgreSQL configuration in `settings.py` and set environment variables:
```
DB_NAME=omnexa_ai
DB_USER=omnexa_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432
```

## 📦 Production Deployment

### Using Gunicorn

```bash
pip install gunicorn
gunicorn omnexa_ai.wsgi:application --bind 0.0.0.0:8000
```

### Using Systemd (Linux)

Create `/etc/systemd/system/omnexa-ai.service`:
```ini
[Unit]
Description=OMNEXA AI Django Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/OmnexaAI
ExecStart=/path/to/venv/bin/gunicorn omnexa_ai.wsgi:application --bind 0.0.0.0:8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable omnexa-ai
sudo systemctl start omnexa-ai
```

## 🛡️ Admin Panel Features

All content is manageable from Django Admin at `/admin/`:

- **Contact**: Manage leads, bookings, newsletter subscribers
- **Services**: Edit 11 services with full details
- **Solutions**: Manage industry-specific solutions
- **Case Studies**: Add/edit client success stories
- **Blog**: Create and publish blog posts
- **About**: Manage team members, company values, milestones
- **Home**: Edit hero section, stats, CTAs, testimonials
- **Chatbot**: View chat sessions, manage knowledge base
- **Careers**: Post job openings, review applications

## 📝 License

© 2025 OMNEXA AI — All rights reserved
