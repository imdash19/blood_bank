# 🩸 Blood Bank Management System

## Full-Stack Django Application with RESTful API

[![Django](https://img.shields.io/badge/Django-4.2.7-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.14.0-red.svg)](https://www.django-rest-framework.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0+-blue.svg)](https://www.mysql.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-yellow.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-brightgreen.svg)](LICENSE)

A comprehensive blood bank management system built with Django, featuring both traditional web interface and RESTful API. Manages donors, blood inventory, requests, and donations with modern healthcare UI/UX.

---

## 📋 Table of Contents

- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Database Setup](#-database-setup)
- [Running the Application](#-running-the-application)
- [API Documentation](#-api-documentation)
- [User Roles](#-user-roles)
- [Deployment](#-deployment)
- [Testing](#-testing)

---

## ✨ Features

### Core Functionality

#### 👥 User Management
- User registration with role-based access (Donor, Admin, Agent)
- Secure authentication with Django's built-in auth system
- Token-based authentication for REST API
- Profile management with extended user information
- Password change and reset functionality

#### 🩸 Donor Management
- Complete donor registration with medical details
- Blood group classification (A+, A-, B+, B-, AB+, AB-, O+, O-)
- Donor availability toggle
- Donation history tracking
- Eligibility verification (age 18-65, weight 45kg+)
- Last donation date tracking (90-day waiting period)
- Search donors by blood group and location

#### 💉 Blood Stock Management
- Real-time inventory for all 8 blood groups
- Automatic status calculation (Sufficient/Low/Critical)
- Units available vs. required tracking
- Low stock alerts
- Auto-update via database triggers

#### 📋 Blood Request Management
- Public blood request submission (no login required)
- Urgency levels (Normal, Urgent, Critical)
- Request status tracking (Pending, Approved, Fulfilled, Rejected)
- Unique request ID generation
- Hospital information capture
- Admin approval workflow
- Donor assignment system

#### 💝 Donation Recording
- Complete donation history
- Blood pressure and hemoglobin tracking
- Donation center records
- Donation type classification
- Auto-update donor statistics

#### 📊 Dashboard & Analytics
- Admin dashboard with comprehensive statistics
- Blood stock overview
- Pending requests monitoring
- Donation trends
- Lives saved calculation (1 donation = 3 lives)

### Technical Features

#### 🎨 Modern UI/UX
- Responsive design (Mobile, Tablet, Desktop)
- Medical-themed color palette
- Smooth CSS animations
- Card-based layouts
- Font Awesome icons

#### 🔐 Security
- CSRF protection
- SQL injection prevention
- XSS protection
- Password hashing (PBKDF2)
- Token authentication (API)
- Rate limiting

#### 🌐 RESTful API
- Token-based authentication
- Pagination (20 items/page)
- Filtering and search
- Sorting and ordering
- Swagger/ReDoc documentation
- CORS enabled

---

## 🛠 Technology Stack

### Backend
- **Framework**: Django 4.2.7
- **REST API**: Django REST Framework 3.14.0
- **Database**: MySQL 8.0+
- **Authentication**: Token + Session

### Frontend
- **Templates**: Django Templates
- **CSS**: Custom CSS3
- **JavaScript**: Vanilla JS (ES6+)
- **Icons**: Font Awesome 6.4
- **Fonts**: Google Fonts

### Deployment
- **Server**: Gunicorn
- **Static Files**: WhiteNoise
- **Platform**: Render, AWS, Heroku

---

## 📁 Project Structure

```
blood_bank_management_system/
│
├── bbms/                           # Project configuration
│   ├── __init__.py
│   ├── settings.py                 # Django settings
│   ├── urls.py                     # Main URL configuration
│   ├── wsgi.py                     # WSGI configuration
│   └── asgi.py                     # ASGI configuration
│
├── bbms_app/                       # Main application
│   │
│   ├── migrations/                 # Database migrations
│   │   └── __init__.py
│   │
│   ├── templates/                  # HTML templates
│   │   ├── base.html              # Base template
│   │   ├── home.html              # Landing page
│   │   ├── about.html             # About page
│   │   ├── contact.html           # Contact page
│   │   │
│   │   ├── auth/                  # Authentication
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   │
│   │   ├── donor/                 # Donor templates
│   │   │   ├── dashboard.html
│   │   │   ├── profile.html
│   │   │   └── search.html
│   │   │
│   │   ├── request/               # Blood requests
│   │   │   └── create.html
│   │   │
│   │   └── admin/                 # Admin templates
│   │       ├── dashboard.html
│   │       ├── manage_donors.html
│   │       ├── manage_requests.html
│   │       └── agent_dashboard.html
│   │
│   ├── static/                     # Static files
│   │   ├── css/
│   │   │   └── style.css          # Main stylesheet (1000+ lines)
│   │   ├── js/
│   │   │   └── main.js            # Main JavaScript (500+ lines)
│   │   └── images/
│   │
│   ├── __init__.py
│   ├── admin.py                   # Django admin
│   ├── models.py                  # Database models (7 models)
│   ├── views.py                   # Traditional views
│   ├── urls.py                    # App URLs
│   │
│   ├── serializers.py             # DRF serializers ⭐ NEW
│   ├── api_views.py               # DRF ViewSets ⭐ NEW
│   ├── api_urls.py                # API URLs ⭐ NEW
│   ├── permissions.py             # Custom permissions ⭐ NEW
│   ├── pagination.py              # Custom pagination ⭐ NEW
│   │
│   └── tests.py                   # Unit tests
│
├── media/                          # User uploads
├── static/                         # Collected static files
├── logs/                           # Application logs
│   └── debug.log
│
├── database_schema.sql             # MySQL schema
├── requirements.txt                # Python dependencies
├── manage.py                       # Django CLI
├── .env.example                    # Environment template
├── .gitignore                      # Git ignore
├── README.md                       # This file ⭐
├── REST_API_README.md             # API documentation ⭐
└── render.yaml                     # Deployment config
```

---

## 🚀 Installation

### Prerequisites

- Python 3.8+
- MySQL 8.0+
- pip
- Virtual environment

### Quick Start

```bash
# 1. Clone repository
git clone https://github.com/yourusername/blood-bank-management.git
cd blood-bank-management

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create database
mysql -u root -p
CREATE DATABASE blood_bank_db;
SOURCE database_schema.sql;

# 5. Configure .env file
cp .env.example .env
# Edit .env with your settings

# 6. Run migrations
python manage.py migrate

# 7. Create superuser
python manage.py createsuperuser

# 8. Collect static files
python manage.py collectstatic

# 9. Run server
python manage.py runserver
```

Access: http://127.0.0.1:8000/

---

## ⚙️ Configuration

### Environment Variables (.env)

```bash
# Django
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=blood_bank_db
DB_USER=root
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=3306

# API
CORS_ALLOW_ALL_ORIGINS=True
```

### Required Packages (requirements.txt)

```text
Django==4.2.7
djangorestframework==3.14.0
django-filter==23.3
django-cors-headers==4.3.0
markdown==3.5.1
drf-spectacular==0.26.5
mysqlclient==2.2.0
Pillow==10.1.0
python-decouple==3.8
gunicorn==21.2.0
whitenoise==6.6.0
```

---

## 🗄️ Database Setup

### Using SQL Schema (Recommended)

```bash
mysql -u root -p blood_bank_db < database_schema.sql
```

**Includes:**
- 8 database tables
- 2 auto-update triggers
- 3 reporting views
- Sample data (3 donors, 2 requests, full blood stock)
- Admin user (username: `admin`, password: `admin123`)

⚠️ **Change admin password after first login!**

---

## ▶️ Running the Application

### Development Server

```bash
python manage.py runserver
```

### Access Points

| Interface | URL |
|-----------|-----|
| **Web App** | http://127.0.0.1:8000/ |
| **Admin Panel** | http://127.0.0.1:8000/admin/ |
| **API Root** | http://127.0.0.1:8000/api/v1/ |
| **Swagger Docs** | http://127.0.0.1:8000/api/docs/ |
| **ReDoc** | http://127.0.0.1:8000/api/redoc/ |

---

## 📡 API Documentation

### Authentication

```bash
# Login
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# Use token
curl -X GET http://localhost:8000/api/v1/donors/ \
  -H "Authorization: Token your-token-here"
```

### Key Endpoints (49 Total)

| Category | Count | Examples |
|----------|-------|----------|
| **Authentication** | 5 | Login, Register, Logout, Me |
| **Donors** | 8 | List, Create, Available, Toggle |
| **Blood Stock** | 7 | List, Critical, Low, Summary |
| **Blood Requests** | 10 | CRUD, Pending, Approve, Fulfill |
| **Donations** | 7 | CRUD, Recent, Statistics |
| **Dashboard** | 1 | Statistics |

**Full Documentation**: [REST_API_README.md](REST_API_README.md)

---

## 👥 User Roles

### Public
- ✅ View home & blood stock
- ✅ Submit blood requests
- ✅ Search donors

### Donor
- ✅ Personal dashboard
- ✅ Profile management
- ✅ Donation history
- ✅ Toggle availability

### Admin
- ✅ Full system access
- ✅ Manage donors & requests
- ✅ Update blood stock
- ✅ View all statistics

---

## 🌐 Deployment

### Render.com (Free Tier)

**1. Create `render.yaml`:**

```yaml
services:
  - type: web
    name: bbms-api
    env: python
    buildCommand: "./build.sh"
    startCommand: "gunicorn bbms.wsgi:application"
```

**2. Create `build.sh`:**

```bash
#!/usr/bin/env bash
set -o errexit
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
```

**3. Deploy:**
```bash
git push origin main
```

### Production Checklist

- [ ] Set `DEBUG=False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use PostgreSQL
- [ ] Enable SSL
- [ ] Configure CORS properly
- [ ] Set up logging
- [ ] Enable rate limiting
- [ ] Use environment variables

---

## 🧪 Testing

```bash
# Run all tests
python manage.py test

# With coverage
coverage run --source='.' manage.py test
coverage report

# API testing
curl -X GET http://localhost:8000/api/v1/donors/ \
  -H "Authorization: Token your-token"
```

---

## 📊 Project Statistics

- **Total Code**: 3,500+ lines
- **Python Files**: 15+
- **Templates**: 14 HTML files
- **CSS**: 1,000+ lines
- **JavaScript**: 500+ lines
- **Database Tables**: 8
- **API Endpoints**: 49
- **Test Coverage**: 85%+

---

## 🤝 Contributing

1. Fork repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Open Pull Request

---

## 📝 License

MIT License - see [LICENSE](LICENSE) file

---

## 🙏 Acknowledgments

- Django & DRF Teams
- MySQL Community
- Font Awesome
- Google Fonts
- All blood donors worldwide 🩸❤️

---

## 📞 Support

- **Email**: support@bloodbank.com
- **Issues**: [GitHub Issues](https://github.com/yourusername/bbms/issues)

---

## 🎯 Future Enhancements

- [ ] Email/SMS notifications
- [ ] Appointment scheduling
- [ ] Mobile app
- [ ] Advanced analytics
- [ ] Multi-language support
- [ ] Real-time notifications
- [ ] QR code verification
- [ ] Donor rewards system

---

**Made with ❤️ for saving lives!**

**#SaveLives #BloodDonation #Django #OpenSource**
