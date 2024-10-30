from django.contrib.auth import get_user_model

from rest_framework import serializers

from  .utils import get_group_and_roles,get_roles,get_groups


USER = get_user_model()

        

class EmployeeRetriveSerailizer(serializers.ModelSerializer):
    
    role = serializers.SerializerMethodField()
    department = serializers.SerializerMethodField()
    
    
    def get_role(self,obj):        
        return obj.role.name
    
    
    def get_department(self,obj):
        return obj.role.group.name
        
        
    
    
    
    class Meta:
        
        model = USER
        
        fields = [
            'id',
            'email',
            'name',
            'role',
            'department',
        ] 
            
        
class EmployeeCreatSearilizer(serializers.ModelSerializer):
    
    role       = serializers.ChoiceField(choices=get_roles(),write_only=True)
    department = serializers.ChoiceField(choices=get_groups(),write_only=True)
    passkey    = serializers.CharField(min_length=6,max_length=16,write_only=True)
     
    
    def validate(self, data):
        
        email = data['email']
        
        
        email_taken = USER.objects.filter(email=email).exists()
        
        if email_taken is True :
            
            raise serializers.ValidationError({'email':'email already taken '})
        
        
        
        role  = data['role']
        group = data['department'] 
        
        
        
        roles = get_group_and_roles().get(group.upper())
        
        
        
        if roles is None:
            
            raise serializers.ValidationError({'group': f'no {group} named department exist '})
        
        _roles = [ __role  for __role in roles ]
        
        if role.upper() not in _roles: 
            
            errors = {'role' : f'{role}  is not valid  role option in the department'}
            errors[f"roles in the {group} department"] = _roles 
            
            raise serializers.ValidationError(errors)
        
        
        password = data.pop('passkey')
        group    = data.pop('department')
        
        
        data['password']  = password
        data['group']     = group 
        data['is_active'] = True 

        return data
    
    
    
    def create(self, validated_data):
        
        
        instance = USER.objects.create(**validated_data)
        
        response_data = self.to_representation(instance)
        
        
        response_data['role']       = validated_data['role']
        response_data['department'] = validated_data['group']
        
        print(response_data)
        
        return response_data
    
    
    class Meta:
        
        model  = USER
        fields = [
            
            'email',
            'name',
            'passkey',
            'department',
            'role',
        ] 