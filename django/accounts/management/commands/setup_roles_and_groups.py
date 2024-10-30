from typing import Any

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group 


from ...models import Roles
from ...constants import GROUPS_AND_ROLES


class Command(BaseCommand):
    
    
    help = "SetUp For Create Groups and accosiated Roles" 
    
    def handle(self, *args: Any, **options: Any) -> str | None:
        
        for group,roles in GROUPS_AND_ROLES.items():
            
        
            
             
            Group.objects.get_or_create(name=group)
            _group  = Group.objects.get(name=group)
           
           
            for role in roles:
               
               Roles.objects.get_or_create(name=role,group=_group)   
        
        
        
        self.stdout.write(self.style.SUCCESS("Roles and groups set up successfully"))
    
    
    