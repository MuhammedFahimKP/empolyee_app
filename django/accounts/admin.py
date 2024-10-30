from typing import Any
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.core.handlers.wsgi import WSGIRequest
from django.http.response import HttpResponse


from .models import MyUser
# Register your models here.



# class MyAdminSite(admin.AdminSite):

    
    
#     def login(self, request: WSGIRequest, extra_context: dict[str, Any] | None = ...) -> HttpResponse:
#         return super().login(request, extra_context)
    
#     def has_permission(self, request):
        
#         print(request)
#         return request.user.is_active and request.user.groups.filter(name="Admins").exists()
    
    
    
@admin.register(MyUser)
class MyUserAdminConf(UserAdmin):

    ordering           = ('-date_joined',)
    list_display       = (
        'email',
        'name',
        'role__name',
        'role__group__name',
        'last_login',
        
    )

    list_display_links = (
        'email',
        'name',
        'name',
    )


     
    readonly_fields = ["date_joined","last_login"]
    
    filter_horizontal=()
    list_filter=()
    fieldsets=()