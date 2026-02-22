"""
Blood Bank Management System - DRF Serializers
Enterprise-grade serializers with validation, nested relationships, and error handling
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from .models import (
    UserProfile, Donor, BloodStock, BloodRequest, 
    Donation, ContactMessage, BLOOD_GROUP_CHOICES
)
from datetime import date, timedelta


# ==================== USER SERIALIZERS ====================

class UserSerializer(serializers.ModelSerializer):
    """User serializer with password validation"""
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True, 
        required=True,
        style={'input_type': 'password'}
    )
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'password', 'password_confirm', 'full_name', 'is_active',
            'date_joined', 'last_login'
        ]
        read_only_fields = ['id', 'date_joined', 'last_login', 'full_name']
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def get_full_name(self, obj):
        """Get user's full name"""
        return obj.get_full_name() or obj.username

    def validate(self, attrs):
        """Validate password confirmation"""
        if attrs.get('password') != attrs.get('password_confirm'):
            raise serializers.ValidationError({
                "password": "Password fields didn't match."
            })
        return attrs

    def validate_email(self, value):
        """Ensure email uniqueness"""
        if self.instance:
            # Update case - exclude current user
            if User.objects.exclude(pk=self.instance.pk).filter(email=value).exists():
                raise serializers.ValidationError("Email already in use.")
        else:
            # Create case
            if User.objects.filter(email=value).exists():
                raise serializers.ValidationError("Email already in use.")
        return value.lower()

    def create(self, validated_data):
        """Create user with hashed password"""
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        """Update user with password handling"""
        validated_data.pop('password_confirm', None)
        password = validated_data.pop('password', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if password:
            instance.set_password(password)
        
        instance.save()
        return instance


class UserProfileSerializer(serializers.ModelSerializer):
    """User profile serializer"""
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = UserProfile
        fields = [
            'id', 'user', 'user_id', 'role', 'phone', 'address',
            'city', 'state', 'pincode', 'profile_image',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_phone(self, value):
        """Validate phone number format"""
        import re
        if value and not re.match(r'^\+?1?\d{9,15}$', value):
            raise serializers.ValidationError(
                "Phone number must be in format: '+999999999'. Up to 15 digits."
            )
        return value


# ==================== DONOR SERIALIZERS ====================

class DonorListSerializer(serializers.ModelSerializer):
    """Lightweight donor serializer for list views"""
    full_name = serializers.CharField(source='user.get_full_name', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    phone = serializers.CharField(source='user.profile.phone', read_only=True)
    city = serializers.CharField(source='user.profile.city', read_only=True)
    age = serializers.IntegerField(read_only=True)
    lives_saved = serializers.SerializerMethodField()

    class Meta:
        model = Donor
        fields = [
            'id', 'full_name', 'email', 'phone', 'blood_group',
            'age', 'gender', 'weight', 'city', 'is_available',
            'total_donations', 'lives_saved', 'last_donation_date'
        ]

    def get_lives_saved(self, obj):
        """Calculate lives saved (1 donation = 3 lives)"""
        return obj.total_donations * 3


class DonorDetailSerializer(serializers.ModelSerializer):
    """Detailed donor serializer with nested user info"""
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True, required=False)
    age = serializers.IntegerField(read_only=True)
    lives_saved = serializers.SerializerMethodField()
    can_donate = serializers.SerializerMethodField()
    next_eligible_date = serializers.SerializerMethodField()

    class Meta:
        model = Donor
        fields = [
            'id', 'user', 'user_id', 'blood_group', 'date_of_birth',
            'gender', 'weight', 'age', 'last_donation_date',
            'is_available', 'medical_conditions', 'emergency_contact',
            'total_donations', 'lives_saved', 'can_donate',
            'next_eligible_date', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'total_donations', 'created_at', 'updated_at']

    def get_lives_saved(self, obj):
        return obj.total_donations * 3

    def get_can_donate(self, obj):
        """Check if donor is eligible to donate"""
        if not obj.last_donation_date:
            return True
        # Must wait 3 months between donations
        eligible_date = obj.last_donation_date + timedelta(days=90)
        return date.today() >= eligible_date

    def get_next_eligible_date(self, obj):
        """Get next eligible donation date"""
        if not obj.last_donation_date:
            return None
        return obj.last_donation_date + timedelta(days=90)

    def validate_weight(self, value):
        """Validate donor weight (minimum 45kg)"""
        if value < 45:
            raise serializers.ValidationError(
                "Donor must weigh at least 45 kg to donate blood."
            )
        return value

    def validate_date_of_birth(self, value):
        """Validate donor age (18-65 years)"""
        today = date.today()
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        
        if age < 18:
            raise serializers.ValidationError("Donor must be at least 18 years old.")
        if age > 65:
            raise serializers.ValidationError("Donor must be under 65 years old.")
        
        return value


# ==================== BLOOD STOCK SERIALIZERS ====================

class BloodStockSerializer(serializers.ModelSerializer):
    """Blood stock serializer with status calculation"""
    status = serializers.CharField(read_only=True)
    deficit = serializers.SerializerMethodField()
    status_color = serializers.SerializerMethodField()

    class Meta:
        model = BloodStock
        fields = [
            'id', 'blood_group', 'units_available', 'units_required',
            'status', 'deficit', 'status_color', 'last_updated'
        ]
        read_only_fields = ['id', 'last_updated']

    def get_deficit(self, obj):
        """Calculate deficit or surplus"""
        return obj.units_available - obj.units_required

    def get_status_color(self, obj):
        """Get color code for status"""
        status_colors = {
            'sufficient': '#28A745',
            'low': '#FFC107',
            'critical': '#DC3545'
        }
        return status_colors.get(obj.status, '#6C757D')

    def validate_units_available(self, value):
        """Validate units available"""
        if value < 0:
            raise serializers.ValidationError("Units available cannot be negative.")
        return value


# ==================== BLOOD REQUEST SERIALIZERS ====================

class BloodRequestListSerializer(serializers.ModelSerializer):
    """Lightweight blood request serializer for lists"""
    urgency_display = serializers.CharField(source='get_urgency_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    days_pending = serializers.SerializerMethodField()

    class Meta:
        model = BloodRequest
        fields = [
            'id', 'request_id', 'requester_name', 'patient_name',
            'blood_group', 'units_required', 'hospital_name', 'city',
            'urgency', 'urgency_display', 'status', 'status_display',
            'days_pending', 'created_at'
        ]

    def get_days_pending(self, obj):
        """Calculate days since request creation"""
        if obj.status == 'fulfilled':
            return 0
        return (date.today() - obj.created_at.date()).days


class BloodRequestDetailSerializer(serializers.ModelSerializer):
    """Detailed blood request serializer"""
    urgency_display = serializers.CharField(source='get_urgency_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    assigned_donor_details = DonorListSerializer(source='assigned_donor', read_only=True)
    compatible_donors_count = serializers.SerializerMethodField()

    class Meta:
        model = BloodRequest
        fields = [
            'id', 'request_id', 'requester_name', 'requester_phone',
            'requester_email', 'patient_name', 'blood_group',
            'units_required', 'hospital_name', 'hospital_address',
            'city', 'reason', 'urgency', 'urgency_display',
            'status', 'status_display', 'assigned_donor',
            'assigned_donor_details', 'admin_notes',
            'compatible_donors_count', 'created_at', 'updated_at',
            'fulfilled_at'
        ]
        read_only_fields = [
            'id', 'request_id', 'created_at', 'updated_at', 'fulfilled_at'
        ]

    def get_compatible_donors_count(self, obj):
        """Count available compatible donors"""
        return Donor.objects.filter(
            blood_group=obj.blood_group,
            is_available=True
        ).count()

    def validate_units_required(self, value):
        """Validate units required"""
        if value < 1:
            raise serializers.ValidationError("At least 1 unit must be required.")
        if value > 10:
            raise serializers.ValidationError("Maximum 10 units per request.")
        return value

    def validate(self, attrs):
        """Cross-field validation"""
        # Check if changing to fulfilled status
        if self.instance and attrs.get('status') == 'fulfilled':
            if not self.instance.assigned_donor:
                raise serializers.ValidationError({
                    "status": "Cannot fulfill request without assigning a donor."
                })
        return attrs


# ==================== DONATION SERIALIZERS ====================

class DonationSerializer(serializers.ModelSerializer):
    """Donation serializer with donor details"""
    donor_name = serializers.CharField(source='donor.user.get_full_name', read_only=True)
    donor_email = serializers.EmailField(source='donor.user.email', read_only=True)

    class Meta:
        model = Donation
        fields = [
            'id', 'donor', 'donor_name', 'donor_email', 'donation_date',
            'blood_group', 'units_donated', 'donation_center',
            'hemoglobin_level', 'blood_pressure', 'donation_type',
            'notes', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def validate_hemoglobin_level(self, value):
        """Validate hemoglobin level (minimum 12.5 g/dL)"""
        if value < 12.5:
            raise serializers.ValidationError(
                "Hemoglobin level must be at least 12.5 g/dL for donation."
            )
        return value

    def validate(self, attrs):
        """Validate donation eligibility"""
        donor = attrs.get('donor')
        donation_date = attrs.get('donation_date')
        
        # Check if donor exists and last donation date
        if donor and donor.last_donation_date:
            days_since_last = (donation_date - donor.last_donation_date).days
            if days_since_last < 90:
                raise serializers.ValidationError({
                    "donation_date": f"Donor must wait 90 days between donations. "
                                   f"Next eligible date: {donor.last_donation_date + timedelta(days=90)}"
                })
        
        return attrs


# ==================== CONTACT MESSAGE SERIALIZERS ====================

class ContactMessageSerializer(serializers.ModelSerializer):
    """Contact message serializer"""
    
    class Meta:
        model = ContactMessage
        fields = [
            'id', 'name', 'email', 'phone', 'subject',
            'message', 'is_read', 'created_at'
        ]
        read_only_fields = ['id', 'is_read', 'created_at']

    def validate_message(self, value):
        """Validate message length"""
        if len(value.strip()) < 10:
            raise serializers.ValidationError(
                "Message must be at least 10 characters long."
            )
        return value


# ==================== AUTHENTICATION SERIALIZERS ====================

class RegisterSerializer(serializers.ModelSerializer):
    """User registration serializer"""
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password_confirm = serializers.CharField(write_only=True, required=True)
    profile = UserProfileSerializer(required=False)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'profile'
        ]
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate(self, attrs):
        """Validate password confirmation"""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({
                "password": "Password fields didn't match."
            })
        return attrs

    def create(self, validated_data):
        """Create user with profile"""
        validated_data.pop('password_confirm')
        profile_data = validated_data.pop('profile', {})
        password = validated_data.pop('password')
        
        # Create user
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        
        # Create profile
        UserProfile.objects.create(user=user, **profile_data)
        
        return user


class LoginSerializer(serializers.Serializer):
    """Login serializer"""
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class ChangePasswordSerializer(serializers.Serializer):
    """Change password serializer"""
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(
        required=True,
        write_only=True,
        validators=[validate_password]
    )
    new_password_confirm = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        """Validate password confirmation"""
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({
                "new_password": "Password fields didn't match."
            })
        return attrs


# ==================== STATISTICS SERIALIZERS ====================

class StatisticsSerializer(serializers.Serializer):
    """Dashboard statistics serializer"""
    total_donors = serializers.IntegerField()
    available_donors = serializers.IntegerField()
    total_requests = serializers.IntegerField()
    pending_requests = serializers.IntegerField()
    fulfilled_requests = serializers.IntegerField()
    total_donations = serializers.IntegerField()
    units_in_stock = serializers.IntegerField()
    lives_saved = serializers.IntegerField()
    critical_blood_groups = serializers.ListField(child=serializers.CharField())
