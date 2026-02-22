from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('donor/dashboard/', views.donor_dashboard, name='donor_dashboard'),
    path('donor/profile/', views.donor_profile, name='donor_profile'),
    path('donors/search/', views.search_donors, name='search_donors'),

    path('request/blood/', views.create_blood_request, name='create_blood_request'),

    path('staff/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('staff/donors/', views.manage_donors, name='manage_donors'),
    path('staff/requests/', views.manage_requests, name='manage_requests'),

    path('agent/dashboard/', views.agent_dashboard, name='agent_dashboard'),
]