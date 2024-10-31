from typing import Any

from django.contrib.auth.models import BaseUserManager,Group
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _


from .utils import get_group_and_roles





class MyUserManger(BaseUserManager):

    def email_validator(self,email):

        try:
            validate_email(email)

        except ValidationError:
            raise ValueError(_("Please enter a valid email address"))    
        
        
    def create(self, **kwargs: Any) -> Any:
        
        email    = kwargs.pop('email')
        name     = kwargs.pop('name')
        group    = kwargs.pop('group')
        role     = kwargs.pop('role')
        password = kwargs.pop('password')
        
        
        
        
        
            
        
        
        
        
        return self.create_user(email=email,name=name,password=password,group=group,role=role,**kwargs)

        
    def create_user(self,email ,name,password,group ,role, **other_fields):
        
        
        from .models import Roles
        
        _group = group.upper()
        _role  = role.upper()
        
        
        roles = get_group_and_roles().get(group)
        
        if roles is None:
            raise ValidationError(_(f'No {group} named group '))
        

        if role not in roles:            
            raise ValidationError(_(f'No {role} named role'))
        
        
        _group  = Group.objects.filter(name__iexact=_group)
        
        group = _group.first()
        role = Roles.objects.get(name=_role,group=group)
                
     
        if email:
            email = self.normalize_email(email)
            self.email_validator
            (email) 
        else:
            raise ValueError(_("You Must provide an Email Address"))    
     
        
        if not name:
            raise ValueError(_("You Must provide a First Name")) 
        
    

        user  = self.model(email=email,name=name,role=role,**other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,email,name,password,**other_fields):
        other_fields.setdefault('is_active',True)
        return self.create_user(email,name,password,group='ADMINS',role='SUPER ADMIN',**other_fields)