from django.urls import path


from .views import (
    
    employee_api_view
)


urlpatterns =    [

    path('',employee_api_view),
    path('<int:pk>/',employee_api_view)
]