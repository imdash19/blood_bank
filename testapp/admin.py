"""
Blood Bank Management System - Admin Configuration
"""

from django.contrib import admin
from .models import *


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'phone', 'city', 'state', 'created_at']
    list_filter = ['role', 'city', 'state']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'phone', 'city']
    date_hierarchy = 'created_at'


@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'blood_group', 'age', 'gender', 'total_donations', 'is_available', 'created_at']
    list_filter = ['blood_group', 'gender', 'is_available', 'created_at']
    search_fields = ['user__first_name', 'user__last_name', 'user__email']
    date_hierarchy = 'created_at'

    def get_full_name(self, obj):
        return obj.user.get_full_name() or obj.user.username

    get_full_name.short_description = 'Donor Name'


@admin.register(BloodStock)
class BloodStockAdmin(admin.ModelAdmin):
    list_display = ['blood_group', 'units_available', 'units_required', 'status', 'last_updated']
    list_filter = ['blood_group']
    ordering = ['blood_group']


@admin.register(BloodRequest)
class BloodRequestAdmin(admin.ModelAdmin):
    list_display = ['request_id', 'patient_name', 'blood_group', 'units_required', 'urgency', 'status', 'city',
                    'created_at']
    list_filter = ['blood_group', 'urgency', 'status', 'city', 'created_at']
    search_fields = ['request_id', 'patient_name', 'requester_name', 'hospital_name', 'city']
    date_hierarchy = 'created_at'
    readonly_fields = ['request_id', 'created_at']


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ['get_donor_name', 'donation_date', 'blood_group', 'units_donated', 'donation_type',
                    'donation_center']
    list_filter = ['blood_group', 'donation_type', 'donation_date']
    search_fields = ['donor__user__first_name', 'donor__user__last_name', 'donation_center']
    date_hierarchy = 'donation_date'

    def get_donor_name(self, obj):
        return obj.donor.user.get_full_name() or obj.donor.user.username

    get_donor_name.short_description = 'Donor Name'


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    date_hierarchy = 'created_at'