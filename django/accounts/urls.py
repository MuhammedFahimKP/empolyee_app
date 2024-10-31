from django.urls import path

from drf_spectacular.views import  SpectacularSwaggerView
from .views import (
    employee_list_create_view,
    employee_retrive_update_destroy_view,
    admin_login_api_view,
)


urlpatterns =    [
    
    #speactcular view for swagger:
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    path('employee/',employee_list_create_view,name='employee-create-list'),
    path('employee/<int:pk>/',employee_retrive_update_destroy_view,name='employee-retrive-update-destroy'),
    path('login/',admin_login_api_view,name="admin-login-api")
]