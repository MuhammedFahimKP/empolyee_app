from django.urls import path


from .views import (
    
    employee_api_view
)


urlpatterns =    [

    path('',employee_api_view,name='employee-create-list'),
    path('<int:pk>/',employee_api_view,name='employee-retrive-update-destroy-view')
]