"""
序列化
Token API 用於登入時生成的Token
User  API

"""
from django.contrib.auth import (
                                    get_user_model, #取得AUTH_USER_MODLE
                                    authenticate #驗證輸入數據與資料庫是否吻合
                                )

from rest_framework import serializers #序列化

from django.utils.translation import gettext as _ #返回友好的字串輸出


class UserSerializer(serializers.ModelSerializer):
    """
    創建使用者

    註冊用戶時需要輸入三個欄位：
    1. email
    2. password
    3. name

    額外定義密碼的欄位：
    - 密碼必須至少包含5個字符
    - 並且不以可讀方式呈現（即'write_only'），這樣確保密碼不會被包含在序列化輸出中。
    """

    class Meta:
        """
        這裡指定了要使用的模型，因為在settings.py 中定義了AUTH_USER_MODEL 為 'core.User'，
        所以這裡可以使用 get_user_model() 動態獲取該模型，這樣代碼更靈活，不需要顯式導入
        from core.models import User。
        """
        model = get_user_model()  # 這裡動態加載了模型，相當於使用 model = User。
        fields = ['email', 'password', 'name']  # 定義了需要序列化和驗證的字段。

        # 額外定義 password 欄位的屬性：
        # 'write_only' 確保密碼字段不會被返回的Json檔案中出現，'min_length' 設定密碼至少要5個字符。
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    # 當上方驗證成功後，Django REST Framework 會自動調用這個 create 方法。
    # 如果驗證失敗，會返回對應的錯誤信息，而不會調用 create 方法。
    def create(self, validated_data):
        """
        'validated_data' 包含經過驗證後的數據，即 email、name 和 password。
        當所有字段都通過驗證後，這個方法會被調用來創建並保存新用戶。

        使用 get_user_model().objects.create_user(**validated_data) 來創建用戶。
        'create_user' 是 Django 自帶的用戶創建方法，會正確地處理密碼的哈希。
        """
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
    """
    序列化使用者驗證的Token

    在使用者登入帳號密碼時產出一個Token讓伺服器回傳給用戶端存在Cookie或是Local Storage

    因此共有兩個資料欄位需要驗證
    email:使用serializer內建的email field驗證
    password：額外定義使用者輸入密碼欄位的input_style 不以文明方式呈現 且不允許空格
    """
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )


    def validate(self, attrs):
        """
        Validate函數為serializer內建功能 用來作進一步驗證 上方的email跟password 只能作輸入驗證
        無法去作輸入的email是否在數據庫中 以及密碼是否正確的驗證  所以需要進一步使用validate驗證

        attrs:為Pytho中的一個字典 包含所有初步驗證過後的資料 以上方為例字典的key有 email ,password
        """
        email = attrs.get('email') #得到使用者輸入的acc
        password = attrs.get('password')#pw
        user = authenticate(
            username=email,#django 內建定義username 為驗證的字段 但我們使用的是email
            password=password,
        )
        if not user:#驗證失敗 user is None 否則user 會是一個存在的物件 包含username email is_active 等等資訊
            msg = _('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user #將user資料放到attr字段後進行return 方便後續之後直接使用
        return attrs
