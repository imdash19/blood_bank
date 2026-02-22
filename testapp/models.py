from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

# Blood Group Choices
BLOOD_GROUP_CHOICES = [
    ('A+', 'A+'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B-', 'B-'),
    ('AB+', 'AB+'),
    ('AB-', 'AB-'),
    ('O+', 'O+'),
    ('O-', 'O-'),
]

# User Role Choices
USER_ROLE_CHOICES = [
    ('donor', 'Donor'),
    ('admin', 'Admin'),
    ('agent', 'Agent'),
]

# Request Status Choices
REQUEST_STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('fulfilled', 'Fulfilled'),
    ('rejected', 'Rejected'),
]


class UserProfile(models.Model):
    """Extended user profile for different roles"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=USER_ROLE_CHOICES, default='donor')
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=10, blank=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"


class Donor(models.Model):
    """Donor information and blood details"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='donor_profile')
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    weight = models.FloatField(help_text="Weight in kg")
    last_donation_date = models.DateField(null=True, blank=True)
    is_available = models.BooleanField(default=True)
    medical_conditions = models.TextField(blank=True, help_text="Any medical conditions")
    emergency_contact = models.CharField(max_length=17, blank=True)
    total_donations = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.blood_group}"

    @property
    def age(self):
        from datetime import date
        today = date.today()
        return today.year - self.date_of_birth.year - (
                    (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))

    class Meta:
        verbose_name = "Donor"
        verbose_name_plural = "Donors"
        ordering = ['-created_at']


class BloodStock(models.Model):
    """Blood stock inventory by blood group"""
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES, unique=True)
    units_available = models.IntegerField(default=0)
    units_required = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.blood_group} - {self.units_available} units"

    @property
    def status(self):
        if self.units_available >= self.units_required:
            return "sufficient"
        elif self.units_available > 0:
            return "low"
        else:
            return "critical"

    class Meta:
        verbose_name = "Blood Stock"
        verbose_name_plural = "Blood Stock"
        ordering = ['blood_group']


class BloodRequest(models.Model):
    """Blood request from patients/hospitals"""
    request_id = models.CharField(max_length=20, unique=True, editable=False)
    requester_name = models.CharField(max_length=200)
    requester_phone = models.CharField(max_length=17)
    requester_email = models.EmailField(blank=True)
    patient_name = models.CharField(max_length=200)
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES)
    units_required = models.IntegerField()
    hospital_name = models.CharField(max_length=200)
    hospital_address = models.TextField()
    city = models.CharField(max_length=100)
    reason = models.TextField(help_text="Reason for blood requirement")
    urgency = models.CharField(max_length=20, choices=[
        ('normal', 'Normal'),
        ('urgent', 'Urgent'),
        ('critical', 'Critical')
    ], default='normal')
    status = models.CharField(max_length=20, choices=REQUEST_STATUS_CHOICES, default='pending')
    assigned_donor = models.ForeignKey(Donor, on_delete=models.SET_NULL, null=True, blank=True,
                                       related_name='blood_requests')
    admin_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    fulfilled_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.request_id:
            from datetime import datetime
            self.request_id = f"BR{datetime.now().strftime('%Y%m%d%H%M%S')}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.request_id} - {self.patient_name} ({self.blood_group})"

    class Meta:
        verbose_name = "Blood Request"
        verbose_name_plural = "Blood Requests"
        ordering = ['-created_at']


class Donation(models.Model):
    """Record of blood donations"""
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE, related_name='donations')
    donation_date = models.DateField()
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES)
    units_donated = models.IntegerField(default=1)
    donation_center = models.CharField(max_length=200)
    hemoglobin_level = models.FloatField(help_text="Hemoglobin level in g/dL")
    blood_pressure = models.CharField(max_length=20, help_text="e.g., 120/80")
    donation_type = models.CharField(max_length=50, choices=[
        ('whole_blood', 'Whole Blood'),
        ('plasma', 'Plasma'),
        ('platelets', 'Platelets'),
        ('red_cells', 'Red Blood Cells'),
    ], default='whole_blood')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.donor.user.get_full_name()} - {self.donation_date}"

    class Meta:
        verbose_name = "Donation"
        verbose_name_plural = "Donations"
        ordering = ['-donation_date']


class ContactMessage(models.Model):
    """Contact form messages"""
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=17, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"

    class Meta:
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"
        ordering = ['-created_at']