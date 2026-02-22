"""
Blood Bank Management System - Main URL Configuration
"""

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
    # ==================== DJANGO ADMIN ====================
    path('admin/', admin.site.urls),
    
    # ==================== REST API v1 ====================
    # IMPORTANT: API routes must come BEFORE traditional routes
    path('api/v1/', include('testapp.api_urls')),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # DRF Browsable API Auth
    path('api-auth/', include('rest_framework.urls')),
    
    # ==================== TRADITIONAL WEB INTERFACE ====================
    # Traditional routes (your existing views)
    path('', include('testapp.urls')),
]

# ==================== MEDIA & STATIC FILES (Development) ====================
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# ==================== ADMIN CUSTOMIZATION ====================
admin.site.site_header = "Blood Bank Management System"
admin.site.site_title = "BBMS Admin"
admin.site.index_title = "Welcome to Blood Bank Management System"
