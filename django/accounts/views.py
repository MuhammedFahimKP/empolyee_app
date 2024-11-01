from django.contrib.auth import  get_user_model

from django_filters.rest_framework import DjangoFilterBackend


from rest_framework import generics,status
from rest_framework.request import Request
from rest_framework.response import Response 
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.authentication import JWTAuthentication 

from drf_spectacular.utils import extend_schema,OpenApiResponse,OpenApiParameter


from .permissions import IsAdminUser
from .serializers import (

    AdminLoginSerializer,
    EmployeeRetriveSerailizer,
    EmployeeCreatUpdateSearilizer,
)
from .pagination  import EmployeeLimitOffsetPagination
from .filters     import EmployeeFilterSet




USER = get_user_model()

class EmpoloyeeListCreateAPIView(generics.GenericAPIView): 
    
    serializer_class       = None
    queryset               = USER.objects.all() 
    pagination_class       = EmployeeLimitOffsetPagination
    filter_backends        = (DjangoFilterBackend,)
    filterset_class        = EmployeeFilterSet
    permission_classes     = (IsAuthenticated,IsAdminUser)
    authentication_classes = (JWTAuthentication,)
    
    def get_serializer_class(self):
        
        if self.request.method == 'GET':
            return EmployeeRetriveSerailizer
        
        
        return EmployeeCreatUpdateSearilizer
    
    
    
    
    # @extend_schema( 
        
    #     auth=['JWTAuthenication']
        
        
    # )
    def get(self,request:Request) ->  Response:
        
        queryset         = self.filter_queryset(self.get_queryset())      
        
        serializer_class = self.get_serializer_class()
        serializer       = serializer_class(queryset,many=True)
        
        
        
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            
            serializer = serializer_class(page,many=True)
            
            return self.get_paginated_response(serializer.data)
        
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    
    
    
         
    
    
    @extend_schema(responses={201:OpenApiResponse(response=EmployeeRetriveSerailizer),}) 
    def post(self,request:Request) -> Response :
        
           
        
        
        
        
        serializer_calass = self.get_serializer_class()    
        serializer        = serializer_calass(data=request.data,context={'request':request})
        
        if serializer.is_valid(raise_exception=True):
            
            data = serializer.save()
            
            return Response(data,status=status.HTTP_201_CREATED)
        
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
         



    
        
    



employee_list_create_view = EmpoloyeeListCreateAPIView.as_view()




class EmployeeRetriveUpdateDestroyAPIView(generics.GenericAPIView):
    
    
    serializer_class       = None
    lookup_field           = 'pk'
    permission_classes     = (IsAuthenticated,IsAdminUser)
    authentication_classes = (JWTAuthentication,)
    
    
    def handle_404(self,pk:int) -> Response:
        return Response({'detail':f'employee with id {pk} not found'},status=status.HTTP_404_NOT_FOUND)
    
   
    
    
    def get_object(self,**kwargs):
        
        try:
            
            user = USER.objects.get(**kwargs)            
            return user
        
        except USER.DoesNotExist:
            return None 
    
    
    def get_serializer_class(self):
        
        if self.request.method == 'GET':
            return EmployeeRetriveSerailizer
        
        
        return EmployeeCreatUpdateSearilizer
         
    
    def get(self,request:Request,pk:int) -> Response:
         
         
        user = self.get_object(id=pk)
        
        if user is None:

            return self.handle_404(pk)
        
        
        serializer_class = self.get_serializer_class()
        serializer       = serializer_class(user)
            
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    
    
    @extend_schema(responses={200:OpenApiResponse(response=EmployeeRetriveSerailizer),})
    def put(self,request:Request,pk:int) -> Request :
        
        
        user  =  self.get_object(id=pk)
        
        serializer_class = self.get_serializer_class()
        serializer       = serializer_class(data=request.data,instance=user,context={'request':request})
        
        
        if user is None:
            return self.handle_404(pk)
    
        if serializer.is_valid(raise_exception=True):
            
            data = serializer.save()
            return Response(data,status=status.HTTP_200_OK)
            
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)    
    
    

    
    def delete(self,request:Request,pk:int) -> Response:
        
        user = self.get_object(id=pk)
        
        if user is None:
            
            return self.handle_404(pk)
        
        user.delete()
        
        return Response({},status=status.HTTP_204_NO_CONTENT)
    
    
employee_retrive_update_destroy_view = EmployeeRetriveUpdateDestroyAPIView.as_view()    
    
    
class AdminLoginAPIView(generics.GenericAPIView):
    
    serializer_class = AdminLoginSerializer
    
    def post(self,request:Request) -> Request:
        
        
        serializer_class = self.get_serializer_class()
        serializer       = serializer_class(data=request.data)  
        
        
        if serializer.is_valid(raise_exception=True):
            data  = serializer.data    
            return Response(data,status=status.HTTP_200_OK)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
admin_login_api_view = AdminLoginAPIView.as_view()