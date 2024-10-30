from django.contrib.auth import get_user_model

from django_filters import rest_framework as filters




USER  = get_user_model()

class EmployeeFilterSet(filters.FilterSet):
    
    
    department = filters.CharFilter(method='filter_departments')
    
    
    
    def filter_departments(self,quesryset,name,value):    
        
        value       = value.upper()
        departments = value.split(',')
        
        return quesryset.filter(role__group__name__in=departments)
        
        
    
    
    
    
    
    
    class Meta:
        fields = ['department']
        model  = USER