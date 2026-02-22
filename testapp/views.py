"""
Blood Bank Management System - Views (CORRECTED)
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q, Count, Sum
from django.http import JsonResponse
from django.core.paginator import Paginator
from datetime import datetime, timedelta
from .models import *
import json


# ================== PUBLIC VIEWS ==================

def home(request):
    """Landing page with hero section"""
    blood_stocks = BloodStock.objects.all()
    stats = {
        'total_donors': Donor.objects.filter(is_available=True).count(),
        'blood_units': BloodStock.objects.aggregate(Sum('units_available'))['units_available__sum'] or 0,
        'requests_fulfilled': BloodRequest.objects.filter(status='fulfilled').count(),
        'active_requests': BloodRequest.objects.filter(status='pending').count(),
    }

    context = {
        'blood_stocks': blood_stocks,
        'stats': stats,
        'page': 'home'
    }
    return render(request, 'testapp/home.html', context)


def about(request):
    """About page"""
    return render(request, 'testapp/about.html', {'page': 'about'})


def contact(request):
    """Contact page with form"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        ContactMessage.objects.create(
            name=name,
            email=email,
            phone=phone,
            subject=subject,
            message=message
        )
        messages.success(request, 'Your message has been sent successfully!')
        return redirect('contact')

    return render(request, 'testapp/contact.html', {'page': 'contact'})


# ================== AUTHENTICATION VIEWS ==================

def user_login(request):
    """User login view - FIXED"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Debug: Print to console (remove in production)
        print(f"Login attempt - Username: {username}")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')

            # Debug: Print user info
            print(f"Login successful - is_superuser: {user.is_superuser}, is_staff: {user.is_staff}")

            # Redirect based on user type
            if user.is_superuser:
                return redirect('admin_dashboard')
            elif user.is_staff:
                return redirect('agent_dashboard')
            else:
                return redirect('donor_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
            print("Authentication failed!")

    return render(request, 'testapp/login.html')


def user_register(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        # Get form data
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        # Validation
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return redirect('register')

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        # Create user profile
        UserProfile.objects.create(
            user=user,
            role='donor',
            phone=request.POST.get('phone', ''),
            address=request.POST.get('address', ''),
            city=request.POST.get('city', ''),
            state=request.POST.get('state', ''),
            pincode=request.POST.get('pincode', '')
        )

        messages.success(request, 'Registration successful! Please login.')
        return redirect('login')

    return render(request, 'testapp/register.html')


@login_required
def user_logout(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


# ================== DASHBOARD VIEWS ==================

@login_required
def dashboard(request):
    """User dashboard - redirects based on role"""
    user = request.user

    if user.is_superuser:
        return redirect('admin_dashboard')

    if user.is_staff:
        return redirect('agent_dashboard')

    # Create profile if it doesn't exist
    profile, created = UserProfile.objects.get_or_create(
        user=user,
        defaults={'role': 'donor'}
    )

    return redirect('donor_dashboard')


@login_required
def donor_dashboard(request):
    """Donor dashboard"""
    try:
        donor = request.user.donor_profile
    except:
        donor = None

    # Get donor's donations
    donations = []
    if donor:
        donations = donor.donations.all()[:5]

    # Get blood requests that match donor's blood group
    matching_requests = []
    if donor:
        matching_requests = BloodRequest.objects.filter(
            blood_group=donor.blood_group,
            status='pending'
        )[:5]

    context = {
        'donor': donor,
        'donations': donations,
        'matching_requests': matching_requests,
        'page': 'dashboard'
    }
    return render(request, 'testapp/donor_dashboard.html', context)


@login_required
def donor_profile(request):
    """Donor profile management"""
    try:
        donor = request.user.donor_profile
    except:
        donor = None

    if request.method == 'POST':
        # Update user info
        request.user.first_name = request.POST.get('first_name')
        request.user.last_name = request.POST.get('last_name')
        request.user.email = request.POST.get('email')
        request.user.save()

        # Update or create profile
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        profile.phone = request.POST.get('phone')
        profile.address = request.POST.get('address')
        profile.city = request.POST.get('city')
        profile.state = request.POST.get('state')
        profile.pincode = request.POST.get('pincode')
        profile.save()

        # Update or create donor profile
        if donor:
            donor.blood_group = request.POST.get('blood_group')
            donor.date_of_birth = request.POST.get('date_of_birth')
            donor.gender = request.POST.get('gender')
            donor.weight = request.POST.get('weight')
            donor.medical_conditions = request.POST.get('medical_conditions', '')
            donor.emergency_contact = request.POST.get('emergency_contact', '')
            donor.is_available = request.POST.get('is_available') == 'on'
            donor.save()
        else:
            Donor.objects.create(
                user=request.user,
                blood_group=request.POST.get('blood_group'),
                date_of_birth=request.POST.get('date_of_birth'),
                gender=request.POST.get('gender'),
                weight=request.POST.get('weight'),
                medical_conditions=request.POST.get('medical_conditions', ''),
                emergency_contact=request.POST.get('emergency_contact', ''),
                is_available=True
            )

        messages.success(request, 'Profile updated successfully!')
        return redirect('donor_profile')

    context = {
        'donor': donor,
        'page': 'profile'
    }
    return render(request, 'testapp/profile.html', context)


# ================== ADMIN VIEWS ==================

@login_required
def admin_dashboard(request):
    """Admin dashboard with statistics - FIXED ACCESS CHECK"""
    # Check if user is superuser OR has admin role
    is_admin = request.user.is_superuser

    if not is_admin:
        # Also check if user has admin role in profile
        try:
            if request.user.profile.role == 'admin':
                is_admin = True
        except:
            pass

    if not is_admin:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('donor_dashboard')

    # Get statistics
    stats = {
        'total_donors': Donor.objects.count(),
        'available_donors': Donor.objects.filter(is_available=True).count(),
        'pending_requests': BloodRequest.objects.filter(status='pending').count(),
        'fulfilled_requests': BloodRequest.objects.filter(status='fulfilled').count(),
        'total_donations': Donation.objects.count(),
        'units_in_stock': BloodStock.objects.aggregate(Sum('units_available'))['units_available__sum'] or 0,
    }

    # Recent requests
    recent_requests = BloodRequest.objects.all()[:10]

    # Blood stock status
    blood_stocks = BloodStock.objects.all()

    # Recent donations
    recent_donations = Donation.objects.all()[:10]

    context = {
        'stats': stats,
        'recent_requests': recent_requests,
        'blood_stocks': blood_stocks,
        'recent_donations': recent_donations,
        'page': 'admin_dashboard'
    }
    return render(request, 'testapp/admin_dashboard.html', context)


@login_required
def manage_donors(request):
    """Manage all donors"""
    # Check admin access
    is_admin = request.user.is_superuser
    if not is_admin:
        try:
            if request.user.profile.role == 'admin':
                is_admin = True
        except:
            pass

    if not is_admin:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')

    # Get all donors with search and filter
    donors = Donor.objects.all().select_related('user')

    # Search
    search = request.GET.get('search', '')
    if search:
        donors = donors.filter(
            Q(user__first_name__icontains=search) |
            Q(user__last_name__icontains=search) |
            Q(user__email__icontains=search)
        )

    # Filter by blood group
    blood_group = request.GET.get('blood_group', '')
    if blood_group:
        donors = donors.filter(blood_group=blood_group)

    # Pagination
    paginator = Paginator(donors, 20)
    page_number = request.GET.get('page', 1)
    donors_page = paginator.get_page(page_number)

    context = {
        'donors': donors_page,
        'blood_groups': BLOOD_GROUP_CHOICES,
        'page': 'manage_donors'
    }
    return render(request, 'testapp/manage_donors.html', context)


@login_required
def manage_requests(request):
    """Manage blood requests"""
    # Check admin access
    is_admin = request.user.is_superuser
    if not is_admin:
        try:
            if request.user.profile.role == 'admin':
                is_admin = True
        except:
            pass

    if not is_admin:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')

    # Get all requests
    requests_list = BloodRequest.objects.all()

    # Filter by status
    status = request.GET.get('status', '')
    if status:
        requests_list = requests_list.filter(status=status)

    # Pagination
    paginator = Paginator(requests_list, 20)
    page_number = request.GET.get('page', 1)
    requests_page = paginator.get_page(page_number)

    context = {
        'requests': requests_page,
        'status_choices': REQUEST_STATUS_CHOICES,
        'page': 'manage_requests'
    }
    return render(request, 'testapp/manage_requests.html', context)


@login_required
def update_request_status(request, request_id):
    """Update blood request status"""
    if request.method == 'POST':
        blood_request = get_object_or_404(BloodRequest, id=request_id)
        new_status = request.POST.get('status')
        blood_request.status = new_status
        blood_request.admin_notes = request.POST.get('admin_notes', '')

        if new_status == 'fulfilled':
            blood_request.fulfilled_at = datetime.now()

        blood_request.save()
        messages.success(request, 'Request status updated successfully!')

    return redirect('manage_requests')


# ================== BLOOD REQUEST VIEWS ==================

def create_blood_request(request):
    """Public blood request form"""
    if request.method == 'POST':
        BloodRequest.objects.create(
            requester_name=request.POST.get('requester_name'),
            requester_phone=request.POST.get('requester_phone'),
            requester_email=request.POST.get('requester_email', ''),
            patient_name=request.POST.get('patient_name'),
            blood_group=request.POST.get('blood_group'),
            units_required=request.POST.get('units_required'),
            hospital_name=request.POST.get('hospital_name'),
            hospital_address=request.POST.get('hospital_address'),
            city=request.POST.get('city'),
            reason=request.POST.get('reason'),
            urgency=request.POST.get('urgency', 'normal'),
        )
        messages.success(request, 'Blood request submitted successfully! Our team will contact you soon.')
        return redirect('home')

    context = {
        'blood_groups': BLOOD_GROUP_CHOICES,
        'page': 'request_blood'
    }
    return render(request, 'testapp/create.html', context)


# ================== SEARCH DONORS VIEW ==================

def search_donors(request):
    """Search available donors"""
    blood_group = request.GET.get('blood_group', '')
    city = request.GET.get('city', '')

    donors = Donor.objects.filter(is_available=True)

    if blood_group:
        donors = donors.filter(blood_group=blood_group)

    if city:
        donors = donors.filter(user__profile__city__icontains=city)

    context = {
        'donors': donors,
        'blood_groups': BLOOD_GROUP_CHOICES,
        'page': 'search_donors'
    }
    return render(request, 'testapp/search.html', context)


# ================== AGENT DASHBOARD ==================

@login_required
def agent_dashboard(request):
    """Agent dashboard for managing requests"""
    if not request.user.is_staff and not request.user.is_superuser:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')

    pending_requests = BloodRequest.objects.filter(status='pending')

    context = {
        'pending_requests': pending_requests,
        'page': 'agent_dashboard'
    }
    return render(request, 'testapp/agent_dashboard.html', context)