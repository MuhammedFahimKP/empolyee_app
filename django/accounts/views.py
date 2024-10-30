from django.contrib.auth import  get_user_model

from rest_framework import generics,status
from rest_framework.request import Request
from rest_framework.response import Response 

from .serializers import EmployeeCreatSearilizer,EmployeeRetriveSerailizer

from .pagination  import EmployeeLimitOffsetPagination



USER = get_user_model()

class EmpoloyeeListCreateDestroyRetriveUpdateAPIView(generics.GenericAPIView): 
    
    serializer_class = EmployeeCreatSearilizer
    queryset         = USER.objects.all() 
    
    pagination_class = EmployeeLimitOffsetPagination
    
    
    
    def get(self,request:Request,pk: int | None = None) -> Response:
        
        if pk is not None:
            
            return self.retrive(request,pk)
        
        return self.list(request)
         
    
    
    def get_object(self,**kwargs):
        
        try:
            
            user = USER.objects.get(**kwargs)            
            return user
        
        except USER.DoesNotExist:
            return None 
    
    
    def get_serializer_class(self):
        
        if self.request.method == 'GET':
            return EmployeeRetriveSerailizer
        
        return EmployeeCreatSearilizer
         
    
    def retrive(self,request:Request,pk:int) -> Response:
         
         
        user = self.get_object(id=pk)
        
        if user is None:

            return Response({'datail':f'user with {pk} not found'},status=status.HTTP_404_NOT_FOUND)
        
        
        serializer_class = self.get_serializer_class()
        serializer       = serializer_class(user)
            
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    
    def list(self,request:Request) ->  Response:
        
        instances = self.get_queryset().prefetch_related('role')        
        
        serializer_class = self.get_serializer_class()
        serializer       = serializer_class(instances,many=True)
        
        
        page = self.paginate_queryset(instances)
        
        if page is not None:
            
            serializer = serializer_class(page,many=True)
            
            return self.get_paginated_response(serializer.data)
            
            
            
        
        
        
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    
    
    
    def post(self,request:Request) -> Response :
        
        
        serializer_calass = self.get_serializer_class()    
        serializer        = serializer_calass(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            
            data = serializer.save()
            
            return Response(data,status=status.HTTP_201_CREATED)
        
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    



employee_api_view = EmpoloyeeListCreateDestroyRetriveUpdateAPIView.as_view()
