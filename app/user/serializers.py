"""Serializer for the API View."""
from django.contrib.auth import get_user_model,authenticate

from rest_framework import  serializers

from django.utils.translation import  gettext as _


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User object."""
    class Meta:
        model=get_user_model()
        fields=['email','password','name'] #哪些資料要解析
        extra_kwargs={'password':{'write_only':True,'min_length':5}} #額外定義password 不要以文明的方式呈現以及至少五位數
    #當上方驗鄭成功才會執行下面的create  否則會丟出一個error
    def create(self, validated_data):
        """Create and return a user with encrypted  password."""
        return get_user_model().objects.create_user(**validated_data)

    def update(self,instance,validated_data):
        """Update and return user"""
        password=validated_data.pop('password',None)
        user=super().update(instance,validated_data)

        if password:
            user.set_password(password)
            user.save()
        return user

class AuthTokenSerializer(serializers.Serializer):
    """Serializer for user auth Token"""
    email=serializers.EmailField()
    password=serializers.CharField(
        style={'input_type':'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user."""
        email=attrs.get('email')
        password=attrs.get('password')
        user=authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        if not user :
            msg=_('Unable to authenticate with provided credenttials.')
            raise  serializers.ValidationError(msg,code='authorization')

        attrs['user']=user
        return attrs