from django.contrib.auth.models import Group,AbstractBaseUser 

from rest_framework_simplejwt.tokens import RefreshToken  

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




def get_jwt_token(user:AbstractBaseUser) -> dict[str:str]:
    
    refresh = RefreshToken.for_user(user)
    access  = refresh.access_token
    
    
    
    return {
        "access":str(access),
        "refresh":str(refresh)
    }
    
    
    