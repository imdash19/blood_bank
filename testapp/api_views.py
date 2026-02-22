"""
Blood Bank Management System - DRF ViewSets
Enterprise-grade API views with filtering, search, pagination, and custom actions
"""

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db.models import Q, Sum, Count
from django_filters.rest_framework import DjangoFilterBackend
from datetime import date, timedelta

from .models import (
    UserProfile, Donor, BloodStock, BloodRequest,
    Donation, ContactMessage, BLOOD_GROUP_CHOICES
)
from .serializers import (
    UserSerializer, UserProfileSerializer,
    DonorListSerializer, DonorDetailSerializer,
    BloodStockSerializer,
    BloodRequestListSerializer, BloodRequestDetailSerializer,
    DonationSerializer, ContactMessageSerializer,
    RegisterSerializer, LoginSerializer, ChangePasswordSerializer,
    StatisticsSerializer
)
from .permissions import IsAdminOrReadOnly, IsOwnerOrAdmin, IsDonorOwner
from .pagination import StandardResultsPagination, LargeResultsPagination


# ==================== AUTHENTICATION VIEWS ====================

class CustomAuthToken(ObtainAuthToken):
    """Custom token authentication with user details"""
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        
        # Get user profile
        try:
            profile = user.profile
            role = profile.role
        except:
            role = 'donor'
        
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'email': user.email,
            'full_name': user.get_full_name(),
            'role': role,
            'is_superuser': user.is_superuser,
            'is_staff': user.is_staff,
        }, status=status.HTTP_200_OK)


class RegisterViewSet(viewsets.GenericViewSet):
    """User registration endpoint"""
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    
    def create(self, request):
        """Register new user"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate token
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'message': 'Registration successful',
            'token': token.key,
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)


class AuthViewSet(viewsets.GenericViewSet):
    """Authentication management endpoints"""
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['post'])
    def change_password(self, request):
        """Change user password"""
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        
        # Check old password
        if not user.check_password(serializer.validated_data['old_password']):
            return Response({
                'error': 'Old password is incorrect'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Set new password
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        return Response({
            'message': 'Password changed successfully'
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'])
    def logout(self, request):
        """Logout user (delete token)"""
        try:
            request.user.auth_token.delete()
            return Response({
                'message': 'Logout successful'
            }, status=status.HTTP_200_OK)
        except:
            return Response({
                'error': 'Invalid token'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user details"""
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


# ==================== USER VIEWSETS ====================

class UserViewSet(viewsets.ModelViewSet):
    """User management ViewSet"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    pagination_class = StandardResultsPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['username', 'email', 'date_joined']
    ordering = ['-date_joined']
    
    def get_queryset(self):
        """Filter queryset based on user role"""
        if self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)


class UserProfileViewSet(viewsets.ModelViewSet):
    """User profile management ViewSet"""
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    pagination_class = StandardResultsPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['role', 'city', 'state']
    search_fields = ['user__username', 'user__email', 'phone', 'city']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']


# ==================== DONOR VIEWSETS ====================

class DonorViewSet(viewsets.ModelViewSet):
    """Donor management ViewSet with advanced filtering"""
    queryset = Donor.objects.select_related('user', 'user__profile').all()
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['blood_group', 'gender', 'is_available']
    search_fields = [
        'user__first_name', 'user__last_name', 'user__email',
        'user__profile__city', 'user__profile__phone'
    ]
    ordering_fields = ['total_donations', 'created_at', 'last_donation_date']
    ordering = ['-total_donations']
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return DonorListSerializer
        return DonorDetailSerializer
    
    def get_queryset(self):
        """Custom queryset with filters"""
        queryset = super().get_queryset()
        
        # Filter by city
        city = self.request.query_params.get('city', None)
        if city:
            queryset = queryset.filter(user__profile__city__icontains=city)
        
        # Filter by minimum weight
        min_weight = self.request.query_params.get('min_weight', None)
        if min_weight:
            queryset = queryset.filter(weight__gte=min_weight)
        
        # Filter eligible donors (can donate now)
        eligible_only = self.request.query_params.get('eligible', None)
        if eligible_only == 'true':
            eligible_date = date.today() - timedelta(days=90)
            queryset = queryset.filter(
                Q(last_donation_date__isnull=True) |
                Q(last_donation_date__lte=eligible_date)
            ).filter(is_available=True)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def available(self, request):
        """Get all available donors"""
        queryset = self.get_queryset().filter(is_available=True)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_blood_group(self, request):
        """Get donors grouped by blood group"""
        blood_group = request.query_params.get('blood_group', None)
        if not blood_group:
            return Response({
                'error': 'blood_group parameter is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        queryset = self.get_queryset().filter(
            blood_group=blood_group,
            is_available=True
        )
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def toggle_availability(self, request, pk=None):
        """Toggle donor availability status"""
        donor = self.get_object()
        donor.is_available = not donor.is_available
        donor.save()
        
        return Response({
            'message': f'Donor availability set to {donor.is_available}',
            'is_available': donor.is_available
        })


# ==================== BLOOD STOCK VIEWSETS ====================

class BloodStockViewSet(viewsets.ModelViewSet):
    """Blood stock management ViewSet"""
    queryset = BloodStock.objects.all()
    serializer_class = BloodStockSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    pagination_class = None  # No pagination for blood stock (only 8 groups)
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['blood_group']
    ordering_fields = ['blood_group', 'units_available', 'last_updated']
    ordering = ['blood_group']
    
    @action(detail=False, methods=['get'])
    def critical(self, request):
        """Get critical blood stock (status = critical)"""
        queryset = self.get_queryset().filter(units_available=0)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def low(self, request):
        """Get low blood stock"""
        queryset = self.get_queryset().exclude(units_available=0).filter(
            units_available__lt=models.F('units_required')
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get blood stock summary"""
        total_units = BloodStock.objects.aggregate(
            total=Sum('units_available')
        )['total'] or 0
        
        critical_count = BloodStock.objects.filter(units_available=0).count()
        low_count = BloodStock.objects.exclude(units_available=0).filter(
            units_available__lt=models.F('units_required')
        ).count()
        
        return Response({
            'total_units': total_units,
            'critical_groups': critical_count,
            'low_stock_groups': low_count,
            'sufficient_groups': 8 - critical_count - low_count
        })


# ==================== BLOOD REQUEST VIEWSETS ====================

class BloodRequestViewSet(viewsets.ModelViewSet):
    """Blood request management ViewSet"""
    queryset = BloodRequest.objects.select_related('assigned_donor').all()
    permission_classes = [AllowAny]  # Public can create requests
    pagination_class = StandardResultsPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['blood_group', 'urgency', 'status', 'city']
    search_fields = ['request_id', 'patient_name', 'hospital_name', 'requester_name']
    ordering_fields = ['created_at', 'urgency', 'status']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """Return appropriate serializer"""
        if self.action == 'list':
            return BloodRequestListSerializer
        return BloodRequestDetailSerializer
    
    def get_permissions(self):
        """Custom permissions based on action"""
        if self.action in ['create']:
            return [AllowAny()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminUser()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        """Custom queryset with filters"""
        queryset = super().get_queryset()
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__lte=end_date)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def pending(self, request):
        """Get all pending requests"""
        queryset = self.get_queryset().filter(status='pending')
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def urgent(self, request):
        """Get urgent and critical requests"""
        queryset = self.get_queryset().filter(
            urgency__in=['urgent', 'critical'],
            status='pending'
        ).order_by('-urgency', 'created_at')
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Approve a blood request"""
        blood_request = self.get_object()
        blood_request.status = 'approved'
        blood_request.save()
        
        return Response({
            'message': 'Request approved successfully',
            'request': BloodRequestDetailSerializer(blood_request).data
        })
    
    @action(detail=True, methods=['post'])
    def fulfill(self, request, pk=None):
        """Mark request as fulfilled"""
        blood_request = self.get_object()
        
        if not blood_request.assigned_donor:
            return Response({
                'error': 'Cannot fulfill request without assigned donor'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        blood_request.status = 'fulfilled'
        blood_request.fulfilled_at = date.today()
        blood_request.save()
        
        return Response({
            'message': 'Request fulfilled successfully',
            'request': BloodRequestDetailSerializer(blood_request).data
        })
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Reject a blood request"""
        blood_request = self.get_object()
        blood_request.status = 'rejected'
        blood_request.admin_notes = request.data.get('reason', '')
        blood_request.save()
        
        return Response({
            'message': 'Request rejected',
            'request': BloodRequestDetailSerializer(blood_request).data
        })


# ==================== DONATION VIEWSETS ====================

class DonationViewSet(viewsets.ModelViewSet):
    """Donation management ViewSet"""
    queryset = Donation.objects.select_related('donor').all()
    serializer_class = DonationSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    pagination_class = StandardResultsPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['blood_group', 'donation_type', 'donation_center']
    search_fields = ['donor__user__first_name', 'donor__user__last_name', 'donation_center']
    ordering_fields = ['donation_date', 'created_at']
    ordering = ['-donation_date']
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent donations (last 30 days)"""
        thirty_days_ago = date.today() - timedelta(days=30)
        queryset = self.get_queryset().filter(donation_date__gte=thirty_days_ago)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get donation statistics"""
        total_donations = Donation.objects.count()
        total_units = Donation.objects.aggregate(
            total=Sum('units_donated')
        )['total'] or 0
        
        by_type = Donation.objects.values('donation_type').annotate(
            count=Count('id')
        )
        
        return Response({
            'total_donations': total_donations,
            'total_units': total_units,
            'by_type': list(by_type)
        })


# ==================== CONTACT MESSAGE VIEWSETS ====================

class ContactMessageViewSet(viewsets.ModelViewSet):
    """Contact message management ViewSet"""
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    pagination_class = StandardResultsPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_read']
    search_fields = ['name', 'email', 'subject', 'message']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_permissions(self):
        """Public can create, admin can view/update"""
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated(), IsAdminUser()]
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark message as read"""
        message = self.get_object()
        message.is_read = True
        message.save()
        
        return Response({
            'message': 'Message marked as read',
            'data': ContactMessageSerializer(message).data
        })


# ==================== DASHBOARD & STATISTICS ====================

class DashboardViewSet(viewsets.GenericViewSet):
    """Dashboard statistics endpoint"""
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get dashboard statistics"""
        fulfilled_count = BloodRequest.objects.filter(status='fulfilled').count()
        
        stats = {
            'total_donors': Donor.objects.count(),
            'available_donors': Donor.objects.filter(is_available=True).count(),
            'total_requests': BloodRequest.objects.count(),
            'pending_requests': BloodRequest.objects.filter(status='pending').count(),
            'fulfilled_requests': fulfilled_count,
            'total_donations': Donation.objects.count(),
            'units_in_stock': BloodStock.objects.aggregate(
                Sum('units_available')
            )['units_available__sum'] or 0,
            'lives_saved': fulfilled_count * 3,
            'critical_blood_groups': list(
                BloodStock.objects.filter(units_available=0).values_list('blood_group', flat=True)
            )
        }
        
        serializer = StatisticsSerializer(stats)
        return Response(serializer.data)
