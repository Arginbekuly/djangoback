#Rest framework modules
from rest_framework.permissions import BasePermission

class isOwner(BasePermission):
    """Only Owner can modify this content"""

    def has_object_permission(self, request, view, obj):
        """Checks object permission"""
        return obj.owner == request.user
    