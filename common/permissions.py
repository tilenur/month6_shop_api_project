from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuth(BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and not request.user.is_staff
    
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
    
class IsAnon(BasePermission):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class CanEditWithIn15Minutes(BasePermission):

    def has_object_permission(self, request, view, obj):
        from django.utils import timezone
        from datetime import timedelta
        time_passed = timezone.now() - obj.created_at
        return time_passed <= timedelta(minutes=5)