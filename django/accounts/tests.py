

from django.urls import reverse
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group




from rest_framework import status
from rest_framework.test import APITestCase

from .models import  Roles  # assuming Role is a related model
from .serializers import EmployeeCreatUpdateSearilizer
from .utils import get_group_and_roles
from .constants import GROUPS_AND_ROLES


USER  = get_user_model()
class TestUserViewSetTestCase(APITestCase):
    def setUp(self):
        # Setup initial data for testing

        self.list_create_url  = reverse("employee-create-list") 
    
        
        
        #setting up roles and groups for testdb
        for group,roles in GROUPS_AND_ROLES.items():    
             
            Group.objects.get_or_create(name=group)
            _group  = Group.objects.get(name=group)
           
           
            for role in roles:
               
               Roles.objects.get_or_create(name=role,group=_group)
               
        #setting up user for Read Update Delete operation      
        user = USER.objects.create(**{
            "email" : "sde1@gmail.com",
            "name":"sde1",
            "role":"DEVELOPER",
            "password":"*&@#$%^",
            "group":"IT",
            "is_active":True,
        
        })
        
        
        self.user_id     = user.id
        self.admin_email = 'admin1@gmail.com'
        
        admin_user       =  USER.objects.create(name='admin1',email=self.admin_email,password=settings.TEST_ADMIN_PASSWORD,group='ADMINS',role='SUPER ADMIN' ,is_active=True) 
        response ,token  =  self.login_admin()
        
        if token is not None:
            self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
               
        
    
    
    def retrive_update_destroy_url(self):
        return reverse("employee-retrive-update-destroy",kwargs={"pk":self.user_id})
    
    
   
    
    
    def login_admin(self):
        
        url = reverse('admin-login-api')
        
        data = {
            'email':self.admin_email,
            'passkey': settings.TEST_ADMIN_PASSWORD,
        }
        
        
        
        
        response = self.client.post(url,data)
        
        
        
        if response.status_code == 200 :
            token = response.data['access']
            return (response, token)       
        
        return (response,token)
    
    
    def test_1_employee_create(self):
        
        url  = self.list_create_url
        #data for create user 
        data = {
            "email" : "develpor1@gmail.com",
            "name":"sde-1",
            "role":"DEVELOPER",
            "passkey":"*&@#$%^",
            "department":"IT"
        
        }
        
        
        
        
        response = self.client.post(url,data=data)
       
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        
    
    
    def test_2_employees_lists(self):
        
        url      = self.list_create_url
        response = self.client.get(url)
                
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
    
    
    def test_3_employee_retrival(self):
        
        
        url      =  self.retrive_update_destroy_url()
        response =  self.client.get(url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
        
    
    def test_4_employee_update(self):
        
        url      = self.retrive_update_destroy_url()
        data     = {
            
            "email" : "hranalyst1@gmail.com",
            "name":"hranalyst-1",
            "role":"HR ANALYST",
            "passkey":"&**&@#$%^",
            "department":"HR"
        
        }
        
        response = self.client.put(url,data)    
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        
        
    def test_5_employee_destroy(self):
        
        url      = self.retrive_update_destroy_url()
        response = self.client.delete(url)
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
               
     
    
         
        
        
           