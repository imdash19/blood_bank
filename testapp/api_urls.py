"""
Blood Bank Management System - API URLs (DRF Router-based)
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from .api_views import (
    CustomAuthToken, RegisterViewSet, AuthViewSet,
    UserViewSet, UserProfileViewSet,
    DonorViewSet, BloodStockViewSet, BloodRequestViewSet,
    DonationViewSet, ContactMessageViewSet, DashboardViewSet
)

# Initialize DRF Router
router = DefaultRouter()

# Register ViewSets with the router
router.register(r'users', UserViewSet, basename='user')
router.register(r'profiles', UserProfileViewSet, basename='profile')
router.register(r'donors', DonorViewSet, basename='donor')
router.register(r'blood-stock', BloodStockViewSet, basename='blood-stock')
router.register(r'blood-requests', BloodRequestViewSet, basename='blood-request')
router.register(r'donations', DonationViewSet, basename='donation')
router.register(r'contact-messages', ContactMessageViewSet, basename='contact-message')
router.register(r'dashboard', DashboardViewSet, basename='dashboard')

# Authentication endpoints (non-router)
auth_patterns = [
    path('register/', RegisterViewSet.as_view({'post': 'create'}), name='register'),
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('auth/', include([
        path('change-password/', AuthViewSet.as_view({'post': 'change_password'}), name='change-password'),
        path('logout/', AuthViewSet.as_view({'post': 'logout'}), name='logout'),
        path('me/', AuthViewSet.as_view({'get': 'me'}), name='me'),
    ])),
]

# Combine all URL patterns
urlpatterns = [
    # Authentication endpoints
    path('auth/', include(auth_patterns)),
    
    # API endpoints (router-generated)
    path('', include(router.urls)),
]


"""
Generated API Endpoints:

AUTHENTICATION:
    POST   /api/auth/register/              - Register new user
    POST   /api/auth/login/                 - Login (get token)
    POST   /api/auth/auth/logout/           - Logout (delete token)
    POST   /api/auth/auth/change-password/  - Change password
    GET    /api/auth/auth/me/               - Get current user

USERS:
    GET    /api/users/                      - List users
    POST   /api/users/                      - Create user
    GET    /api/users/{id}/                 - Get user detail
    PUT    /api/users/{id}/                 - Update user
    PATCH  /api/users/{id}/                 - Partial update
    DELETE /api/users/{id}/                 - Delete user

PROFILES:
    GET    /api/profiles/                   - List profiles
    POST   /api/profiles/                   - Create profile
    GET    /api/profiles/{id}/              - Get profile detail
    PUT    /api/profiles/{id}/              - Update profile
    PATCH  /api/profiles/{id}/              - Partial update
    DELETE /api/profiles/{id}/              - Delete profile

DONORS:
    GET    /api/donors/                     - List donors
    POST   /api/donors/                     - Create donor
    GET    /api/donors/{id}/                - Get donor detail
    PUT    /api/donors/{id}/                - Update donor
    PATCH  /api/donors/{id}/                - Partial update
    DELETE /api/donors/{id}/                - Delete donor
    GET    /api/donors/available/           - Get available donors
    GET    /api/donors/by_blood_group/      - Filter by blood group
    POST   /api/donors/{id}/toggle_availability/ - Toggle availability

BLOOD STOCK:
    GET    /api/blood-stock/                - List blood stock
    POST   /api/blood-stock/               - Create blood stock
    GET    /api/blood-stock/{id}/          - Get blood stock detail
    PUT    /api/blood-stock/{id}/          - Update blood stock
    PATCH  /api/blood-stock/{id}/          - Partial update
    DELETE /api/blood-stock/{id}/          - Delete blood stock
    GET    /api/blood-stock/critical/      - Get critical stock
    GET    /api/blood-stock/low/           - Get low stock
    GET    /api/blood-stock/summary/       - Get stock summary

BLOOD REQUESTS:
    GET    /api/blood-requests/            - List blood requests
    POST   /api/blood-requests/            - Create blood request
    GET    /api/blood-requests/{id}/       - Get request detail
    PUT    /api/blood-requests/{id}/       - Update request
    PATCH  /api/blood-requests/{id}/       - Partial update
    DELETE /api/blood-requests/{id}/       - Delete request
    GET    /api/blood-requests/pending/    - Get pending requests
    GET    /api/blood-requests/urgent/     - Get urgent requests
    POST   /api/blood-requests/{id}/approve/ - Approve request
    POST   /api/blood-requests/{id}/fulfill/ - Fulfill request
    POST   /api/blood-requests/{id}/reject/  - Reject request

DONATIONS:
    GET    /api/donations/                 - List donations
    POST   /api/donations/                 - Create donation
    GET    /api/donations/{id}/            - Get donation detail
    PUT    /api/donations/{id}/            - Update donation
    PATCH  /api/donations/{id}/            - Partial update
    DELETE /api/donations/{id}/            - Delete donation
    GET    /api/donations/recent/          - Get recent donations
    GET    /api/donations/statistics/      - Get donation statistics

CONTACT MESSAGES:
    GET    /api/contact-messages/          - List messages
    POST   /api/contact-messages/          - Create message
    GET    /api/contact-messages/{id}/     - Get message detail
    PUT    /api/contact-messages/{id}/     - Update message
    PATCH  /api/contact-messages/{id}/     - Partial update
    DELETE /api/contact-messages/{id}/     - Delete message
    POST   /api/contact-messages/{id}/mark_read/ - Mark as read

DASHBOARD:
    GET    /api/dashboard/statistics/      - Get dashboard statistics
"""
