from django.db import models
from django.contrib.auth.models import Group,AbstractBaseUser


from .managers import MyUserManger

# Create your models here.


class Roles(models.Model):
    
    name   = models.CharField(max_length=150)
    group  = models.ForeignKey(Group,on_delete=models.CASCADE)
    
    
    def __str__(self) -> str :
        return f'{self.group.name + self.name}'
    


class MyUser(AbstractBaseUser):
    
    
    email          = models.EmailField(db_index=True,unique=True)
    name           = models.CharField(max_length=100)
    role           = models.ForeignKey(Roles,on_delete=models.CASCADE) 
    
    is_active      = models.BooleanField(default=False)    
    date_joined    = models.DateTimeField(auto_now_add=True)
    last_login     = models.DateTimeField(auto_now=True)
    
    
    objects        = MyUserManger()
    
    
    

    
    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['name']
    
    
    class Meta:
        ordering = ['email']
    
    
    
    
    