# 🩸 Blood Bank Management System

## Full-Stack Django Application with RESTful API

[![Django](https://img.shields.io/badge/Django-5.2.7-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.14.0-red.svg)](https://www.django-rest-framework.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0+-blue.svg)](https://www.mysql.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-yellow.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-brightgreen.svg)](LICENSE)

A comprehensive blood bank management system built with Django, featuring both traditional web interface and RESTful API. Manages donors, blood inventory, requests, and donations with modern healthcare UI/UX.

---

## 📋 Table of Contents

* [Features](#-features)
* [Technology Stack](#-technology-stack)
* [Project Structure](#-project-structure)
* [Installation](#-installation)
* [Configuration](#-configuration)
* [Database Setup](#-database-setup)
* [Running the Application](#-running-the-application)
* [API Documentation](#-api-documentation)
* [User Roles](#-user-roles)
* [Deployment](#-deployment)
* [Testing](#-testing)

---

## ✨ Features

### Core Functionality

#### 👥 User Management

* User registration with role-based access (Donor, Admin, Agent)
* Secure authentication with Django's built-in auth system
* Token-based authentication for REST API
* Profile management with extended user information
* Password change and reset functionality

#### 🩸 Donor Management

* Complete donor registration with medical details
* Blood group classification (A+, A-, B+, B-, AB+, AB-, O+, O-)
* Donor availability toggle
* Donation history tracking
* Eligibility verification (age 18-65, weight 45kg+)
* Last donation date tracking (90-day waiting period)
* Search donors by blood group and location

#### 💉 Blood Stock Management

* Real-time inventory for all 8 blood groups
* Automatic status calculation (Sufficient/Low/Critical)
* Units available vs. required tracking
* Low stock alerts
* Auto-update via database triggers

#### 📋 Blood Request Management

* Public blood request submission (no login required)
* Urgency levels (Normal, Urgent, Critical)
* Request status tracking (Pending, Approved, Fulfilled, Rejected)
* Unique request ID generation
* Hospital information capture
* Admin approval workflow
* Donor assignment system

#### 💝 Donation Recording

* Complete donation history
* Blood pressure and hemoglobin tracking
* Donation center records
* Donation type classification
* Auto-update donor statistics

#### 📊 Dashboard & Analytics

* Admin dashboard with comprehensive statistics
* Blood stock overview
* Pending requests monitoring
* Donation trends
* Lives saved calculation (1 donation = 3 lives)

### Technical Features

#### 🎨 Modern UI/UX

* Responsive design (Mobile, Tablet, Desktop)
* Medical-themed color palette
* Smooth CSS animations
* Card-based layouts
* Font Awesome icons

#### 🔐 Security

* CSRF protection
* SQL injection prevention
* XSS protection
* Password hashing (PBKDF2)
* Token authentication (API)
* Rate limiting

#### 🌐 RESTful API

* Token-based authentication
* Pagination (20 items/page)
* Filtering and search
* Sorting and ordering
* Swagger/ReDoc documentation
* CORS enabled

---

## 🛠 Technology Stack

### Backend

* **Framework**: Django 5.2.7
* **REST API**: Django REST Framework 3.14.0
* **Database**: MySQL 8.0+
* **Authentication**: Token + Session

### Frontend

* **Templates**: Django Templates
* **CSS**: Custom CSS3
* **JavaScript**: Vanilla JS (ES6+)
* **Icons**: Font Awesome 6.4
* **Fonts**: Google Fonts

### Deployment

* **Server**: Gunicorn
* **Static Files**: WhiteNoise
* **Platform**: PythonAnywhere

---

## 📁 Project Structure

```
Blood Bank Management System/
│
├── blood_bank/                    
│   ├── __init__.py
│   ├── settings.py                
│   ├── urls.py                    
│   ├── wsgi.py                    
│   └── asgi.py                    
│
├── bbms_app/                      
│   │
│   ├── migrations/                
│   │   └── __init__.py
│   │
│   ├── templates/                 
│   │   ├── base.html              
│   │   ├── home.html              
│   │   ├── about.html             
│   │   ├── contact.html           
│   │   │
│   │   ├── auth/                  
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   │
│   │   ├── donor/                 
│   │   │   ├── dashboard.html
│   │   │   ├── profile.html
│   │   │   └── search.html
│   │   │
│   │   ├── request/               
│   │   │   └── create.html
│   │   │
│   │   └── admin/                 
│   │       ├── dashboard.html
│   │       ├── manage_donors.html
│   │       ├── manage_requests.html
│   │       └── agent_dashboard.html
│   │
│   ├── static/                    
│   │   ├── css/
│   │   │   └── style.css          
│   │   ├── js/
│   │   │   └── main.js            
│   │   └── images/
│   │
│   ├── __init__.py
│   ├── admin.py                   
│   ├── models.py                  
│   ├── views.py                   
│   ├── urls.py                    
│   │
│   ├── serializers.py             
│   ├── api_views.py               
│   ├── api_urls.py                
│   ├── permissions.py             
│   ├── pagination.py              
│   │
│   └── tests.py                   
│
├── media/                         
├── static/                        
├── logs/                          
│   └── debug.log
│
├── database_schema.sql            
├── requirements.txt               
├── manage.py                      
├── .env.example                   
├── .gitignore                     
├── README.md                      
├── REST_API_README.md             
└── render.yaml                    
```

---

## 🚀 Installation

```bash
# 1. Clone repository
git clone https://github.com/imdash19/blood_bank.git
cd blood_bank

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create database
mysql -u root -p
CREATE DATABASE blood_bank_db;
SOURCE database_schema.sql;

# 5. Configure .env file
cp .env.example .env

# 6. Run migrations
python manage.py migrate

# 7. Create superuser
python manage.py createsuperuser

# 8. Collect static files
python manage.py collectstatic

# 9. Run server
python manage.py runserver
```

---

## ⚙️ Configuration

### Environment Variables (.env)

```bash
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=blood_bank_db
DB_USER=root
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=3306

CORS_ALLOW_ALL_ORIGINS=True
```

### Required Packages

```text
Django==5.2.7
djangorestframework==3.14.0
django-filter==23.3
django-cors-headers==4.3.0
markdown==3.5.1
drf-spectacular==0.26.5
mysqlclient==2.2.7
Pillow==12.1.0
python-decouple==3.8
gunicorn==25.1.0
whitenoise==6.6.0
```

---

## 🌐 Deployment

### PythonAnywhere Deployment

1. Upload project
2. Create virtualenv
3. Install requirements
4. Configure WSGI → `blood_bank.wsgi:application`
5. Set `DEBUG=False`, `ALLOWED_HOSTS`
6. Run migrate + collectstatic
7. Reload app

---

## 🧪 Testing

```bash
python manage.py test
```

---

## 📊 Project Statistics

* Total Code: 3500+ lines
* API Endpoints: 49
* Test Coverage: 85%+

---

## 🤝 Contributing

1. Fork
2. Branch
3. Commit
4. PR

---

## 📝 License

MIT License

---

## 🙏 Acknowledgments

* Django
* DRF
* MySQL

---

## 📞 Support

* Email: [bbd.python@gmail.com](mailto:bbd.python@gmail.com)
* Issues: https://github.com/imdash19/blood_bank/issues

---

## 🎯 Future Enhancements

* Notifications
* Mobile app
* Analytics

---

**Made with ❤️ for saving lives!**
