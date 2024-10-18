from rest_framework import permissions

class CanCreateBankStaff(permissions.BasePermission):
    message = 'Adding customers not allowed.'

    def has_permission(self, request, view):
        return request.user.is_superuser
    
