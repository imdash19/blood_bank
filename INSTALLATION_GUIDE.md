# 🚀 REST API Installation Guide for Blood Bank Management System

## 📋 Complete Step-by-Step Setup

---

## 1️⃣ INSTALL REQUIRED PACKAGES

### Run this command in your terminal:

```bash
pip install djangorestframework==3.14.0
pip install django-filter==23.3
pip install django-cors-headers==4.3.0
pip install markdown==3.5.1
pip install drf-spectacular==0.26.5
pip install whitenoise==6.6.0
```

### OR install all at once:

```bash
pip install djangorestframework==3.14.0 django-filter==23.3 django-cors-headers==4.3.0 markdown==3.5.1 drf-spectacular==0.26.5 whitenoise==6.6.0
```

---

## 2️⃣ UPDATE requirements.txt

Create or update your `requirements.txt` file:

```text
Django==5.2.7
mysqlclient==2.2.0

# REST API Packages ⭐ NEW
djangorestframework==3.14.0
django-filter==23.3
django-cors-headers==4.3.0
markdown==3.5.1
drf-spectacular==0.26.5
whitenoise==6.6.0
```

---

## 3️⃣ REPLACE settings.py

**Location:** `blood_bank/settings.py`

Replace your current `settings.py` with the provided `blood_bank_settings_UPDATED.py` file.

**What's Added:**
- ✅ `rest_framework` in INSTALLED_APPS
- ✅ `rest_framework.authtoken` in INSTALLED_APPS
- ✅ `django_filters` in INSTALLED_APPS
- ✅ `corsheaders` in INSTALLED_APPS
- ✅ `drf_spectacular` in INSTALLED_APPS
- ✅ `corsheaders.middleware.CorsMiddleware` in MIDDLEWARE
- ✅ `whitenoise.middleware.WhiteNoiseMiddleware` in MIDDLEWARE
- ✅ `REST_FRAMEWORK` configuration
- ✅ `SPECTACULAR_SETTINGS` configuration
- ✅ `CORS` settings
- ✅ `LOGGING` configuration

---

## 4️⃣ UPDATE urls.py

**Location:** `blood_bank/urls.py`

Update your main `urls.py`:

```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView
)

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),
    
    # Traditional Web Interface
    path('', include('testapp.urls')),
    
    # REST API v1 ⭐ NEW
    path('api/v1/', include('testapp.api_urls')),
    
    # API Documentation ⭐ NEW
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # DRF Browsable API Auth
    path('api-auth/', include('rest_framework.urls')),
]

# Media files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Admin customization
admin.site.site_header = "Blood Bank Management System"
admin.site.site_title = "BBMS Admin"
admin.site.index_title = "Welcome to BBMS"
```

---

## 5️⃣ CREATE NEW FILES IN testapp/

Navigate to your `testapp/` directory and create these files:

### A. Create `serializers.py`

```bash
cd testapp/
touch serializers.py
```

**Copy the content from the provided `serializers.py` file.**

**File:** `testapp/serializers.py`
- Contains: UserSerializer, DonorSerializer, BloodStockSerializer, etc.
- Total: ~500 lines

---

### B. Create `api_views.py`

```bash
touch api_views.py
```

**Copy the content from the provided `api_views.py` file.**

**File:** `testapp/api_views.py`
- Contains: All ModelViewSets (DonorViewSet, BloodRequestViewSet, etc.)
- Total: ~400 lines

---

### C. Create `api_urls.py`

```bash
touch api_urls.py
```

**Copy the content from the provided `api_urls.py` file.**

**File:** `testapp/api_urls.py`
- Contains: DRF Router configuration
- Registers all API endpoints

---

### D. Create `permissions.py`

```bash
touch permissions.py
```

**Copy the content from the provided `permissions.py` file.**

**File:** `testapp/permissions.py`
- Contains: Custom permission classes
- Total: ~30 lines

---

### E. Create `pagination.py`

```bash
touch pagination.py
```

**Copy the content from the provided `pagination.py` file.**

**File:** `testapp/pagination.py`
- Contains: Custom pagination classes
- Total: ~40 lines

---

## 6️⃣ CREATE logs DIRECTORY

```bash
# In your project root (where manage.py is)
mkdir logs
```

---

## 7️⃣ RUN DATABASE MIGRATIONS

```bash
# Create migrations for authtoken
python manage.py migrate
```

This will create the authentication token table.

---

## 8️⃣ COLLECT STATIC FILES (Optional for now)

```bash
python manage.py collectstatic --noinput
```

---

## 9️⃣ START THE SERVER

```bash
python manage.py runserver
```

---

## 🎯 VERIFY INSTALLATION

### Check these URLs:

1. **Web Interface** (Existing)
   ```
   http://127.0.0.1:8000/
   ```

2. **API Root** (New)
   ```
   http://127.0.0.1:8000/api/v1/
   ```

3. **Swagger API Docs** (New)
   ```
   http://127.0.0.1:8000/api/docs/
   ```

4. **ReDoc API Docs** (New)
   ```
   http://127.0.0.1:8000/api/redoc/
   ```

5. **Django Admin**
   ```
   http://127.0.0.1:8000/admin/
   ```

---

## ✅ VERIFICATION CHECKLIST

- [ ] All packages installed successfully
- [ ] `settings.py` updated with REST_FRAMEWORK config
- [ ] `urls.py` updated with API routes
- [ ] `serializers.py` created in testapp/
- [ ] `api_views.py` created in testapp/
- [ ] `api_urls.py` created in testapp/
- [ ] `permissions.py` created in testapp/
- [ ] `pagination.py` created in testapp/
- [ ] `logs/` directory created
- [ ] Migrations run successfully
- [ ] Server starts without errors
- [ ] Can access http://127.0.0.1:8000/api/v1/
- [ ] Can access http://127.0.0.1:8000/api/docs/

---

## 🐛 TROUBLESHOOTING

### Error: "No module named 'rest_framework'"

**Solution:**
```bash
pip install djangorestframework
```

### Error: "No module named 'django_filters'"

**Solution:**
```bash
pip install django-filter
```

### Error: "No module named 'corsheaders'"

**Solution:**
```bash
pip install django-cors-headers
```

### Error: "TemplateDoesNotExist"

**Solution:**
- Make sure you copied `api_urls.py` to testapp/
- Check that `'testapp.api_urls'` is correctly included in main urls.py

### Error: "Table doesn't exist: authtoken_token"

**Solution:**
```bash
python manage.py migrate
```

---

## 📊 PROJECT STRUCTURE AFTER SETUP

```
blood_bank_project/
│
├── blood_bank/                 # Project config
│   ├── settings.py             # ⚙️ UPDATED
│   ├── urls.py                 # ⚙️ UPDATED
│   └── wsgi.py
│
├── testapp/                    # Your app
│   ├── templates/
│   ├── static/
│   ├── models.py
│   ├── views.py                # Existing (traditional views)
│   ├── urls.py                 # Existing (traditional URLs)
│   │
│   ├── serializers.py          # ⭐ NEW
│   ├── api_views.py            # ⭐ NEW
│   ├── api_urls.py             # ⭐ NEW
│   ├── permissions.py          # ⭐ NEW
│   └── pagination.py           # ⭐ NEW
│
├── logs/                       # ⭐ NEW
│   └── debug.log
│
├── media/
├── staticfiles/                # ⭐ NEW (after collectstatic)
├── requirements.txt            # ⚙️ UPDATED
└── manage.py
```

---

## 🚀 TEST THE API

### 1. Register a new user:

```bash
curl -X POST http://localhost:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "TestPass123!",
    "password_confirm": "TestPass123!",
    "first_name": "Test",
    "last_name": "User"
  }'
```

### 2. Login and get token:

```bash
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "TestPass123!"
  }'
```

Save the token from response!

### 3. Use token to access API:

```bash
curl -X GET http://localhost:8000/api/v1/donors/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

---

## ✨ NEXT STEPS

1. ✅ Test all API endpoints in Swagger: http://127.0.0.1:8000/api/docs/
2. ✅ Create some donors and blood requests
3. ✅ Test filtering and search
4. ✅ Review the API documentation
5. ✅ Start building your frontend!

---

**Installation Complete!** 🎉

Your Blood Bank Management System now has both:
- 🌐 Traditional web interface
- 🚀 RESTful API with documentation

Need help? Check the `REST_API_README.md` for detailed API documentation!
