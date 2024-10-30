from django.contrib.auth.models import Group 

def get_groups():
    

    groups = Group.objects.all()
    
    return [ group.name for group in groups]

def get_group_and_roles():
    from .models import Roles


    roles  = Roles.objects.all().prefetch_related('group')
    groups = Group.objects.all()
    
  
    
    return {  group.name:[ role.name  for role in roles  if role.group == group ]  for group in groups  }


def get_roles():
    from .models import Roles


    roles = Roles.objects.all()
    
    return [ role.name for  role in roles ]



