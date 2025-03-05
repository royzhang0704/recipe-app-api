from django.contrib.auth import (
    get_user_model, #取得AUTH_USER_MODLE
    authenticate 
    )

from rest_framework import serializers 

from django.utils.translation import gettext as _ #返回友好的字串輸出


from rest_framework import serializers
from django.contrib.auth import authenticate

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        # 身份验证逻辑
        email = data.get('username')
        password = data.get('password')
    
        user = authenticate(
            username=email, 
            password=password
        )
        
        if not user:
            raise serializers.ValidationError('帳密錯誤')
        
        data['user'] = user
        return data
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()  
        fields = ['email', 'password', 'name']  
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}
        
    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    """
    這裡相當於執行：
    return User.objects.create_user( email="example@gmail.com", password="test123", name="test" )
    """

    def update(self, instance, validated_data):
        """Update and return user"""
        password = validated_data.pop('password', None) #若用戶update instance 裡面包括password字段 把他從validate_data 這個字典裡面移除 並賦予給password這個物件,
        #若更新得內容不包括密碼 password=None
        user = super().update(instance, validated_data) #更新其他字段 如email,name 但不包括password字段

        if password:#如果用戶提交了新的密碼，進行以下步驟。因為密碼需要特殊處理，不能直接像其他字段那樣更新。
            user.set_password(password)
            user.save()
        return user #return update後的User物件


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )


    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            username=email,
            password=password,
        )
        if not user:
            msg = _('帳號密碼錯誤,無法生成Token')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user 
        return attrs
