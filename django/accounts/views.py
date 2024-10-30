from django.contrib.auth import  get_user_model

from rest_framework import generics,status
from rest_framework.request import Request
from rest_framework.response import Response 
from rest_framework.exceptions import MethodNotAllowed

from django_filters.rest_framework import DjangoFilterBackend


from .serializers import EmployeeCreatUpdateSearilizer,EmployeeRetriveSerailizer,EmployeeeUpdateSerilizer
from .pagination  import EmployeeLimitOffsetPagination
from .filters     import EmployeeFilterSet



USER = get_user_model()

class EmpoloyeeListCreateDestroyRetriveUpdateAPIView(generics.GenericAPIView): 
    
    serializer_class = EmployeeCreatUpdateSearilizer
    queryset         = USER.objects.all() 
    pagination_class = EmployeeLimitOffsetPagination
    filter_backends  = (DjangoFilterBackend,)
    filterset_class  = EmployeeFilterSet
    lookup_field     = 'pk'
    
    
    
    
    
    
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
         
    
    def retrive(self,request:Request,pk:int) -> Response:
         
         
        user = self.get_object(id=pk)
        
        if user is None:

            return self.handle_404(pk)
        
        
        serializer_class = self.get_serializer_class()
        serializer       = serializer_class(user)
            
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    
    def list(self,request:Request) ->  Response:
        
        queryset         = self.filter_queryset(self.get_queryset())      
        
        serializer_class = self.get_serializer_class()
        serializer       = serializer_class(queryset,many=True)
        
        
        
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            
            serializer = serializer_class(page,many=True)
            
            return self.get_paginated_response(serializer.data)
        
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    
    
    def get(self,request:Request,pk: int | None = None) -> Response:
        
        if pk is not None:
            
            return self.retrive(request,pk)
        
        return self.list(request)
         
    
    
    def post(self,request:Request,*args, **kwargs) -> Response :
        
        
        if 'pk' in  kwargs.keys():
            raise MethodNotAllowed(method='POST')
        
        
        serializer_calass = self.get_serializer_class()    
        serializer        = serializer_calass(data=request.data,context={'request':request})
        
        if serializer.is_valid(raise_exception=True):
            
            data = serializer.save()
            
            return Response(data,status=status.HTTP_201_CREATED)
        
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    
    def put(self,request:Request,pk:int) -> Request :
        
        
        user  =  self.get_object(id=pk)
        
        serializer = self.get_serializer_class()(data=request.data,instance=user,context={'request':request})
        
        
        
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
         
    
    
    



employee_api_view = EmpoloyeeListCreateDestroyRetriveUpdateAPIView.as_view()
