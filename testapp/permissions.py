"""
Blood Bank Management System - Custom Permissions
"""

from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admins to edit objects.
    Read-only for others.
    """
    def has_permission(self, request, view):
        # Read permissions allowed for any authenticated user
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        # Write permissions only for admin users
        return request.user and request.user.is_superuser


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners or admins to edit objects.
    """
    def has_object_permission(self, request, view, obj):
        # Admin can do anything
        if request.user.is_superuser:
            return True
        
        # Read permissions for authenticated users
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        # Write permissions only for owner
        if hasattr(obj, 'user'):
            return obj.user == request.user
        return obj == request.user


class IsDonorOwner(permissions.BasePermission):
    """
    Custom permission for donor objects.
    """
    def has_object_permission(self, request, view, obj):
        # Admin can do anything
        if request.user.is_superuser:
            return True
        
        # Donor can only edit own profile
        return obj.user == request.user
