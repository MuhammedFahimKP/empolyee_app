from rest_framework.permissions import IsAdminUser as AdminOnlyPermission


class IsAdminUser(AdminOnlyPermission):
    
    
    def has_permission(self, request, view):
        
        if request.user is not None:
            return  request.user.role.name  == "SUPER ADMIN"