"""
Database models.
"""

import uuid
import os
from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db.models import CharField, DecimalField, IntegerField


def recipe_image_file_path(instance, filename):
    """生成圖片路徑"""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'recipe', filename)


class UserManager(BaseUserManager):
    """
    用來管理創建的User屬於管理者還是一般使用者
    """

    def create_user(self, email, password=None, **extra_fields):
        """創建一個一般使用者"""
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User Table"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Recipe(models.Model):
    """
    食譜Table
    auth_user_model定義為User()
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )  # 食譜與user 關係為 many to one  每個食譜只能為一個User擁有 但一個user 可以有多個食譜
    title = CharField(max_length=255)
    description = CharField(blank=True, max_length=255)
    time_minutes = IntegerField()
    price = DecimalField(max_digits=5, decimal_places=2)
    link = CharField(max_length=255, blank=True)
    tags = models.ManyToManyField('Tag')  # 一個Recipe 可以有多個Tag 一個Tag也可屬於多個Recipe
    ingredients = models.ManyToManyField('Ingredient')
    image = models.ImageField(null=True, upload_to=recipe_image_file_path)

    def __str__(self):
        return self.title


class Tag(models.Model):
    """食譜標籤Table"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )  # many to one 若User被刪除 連同這個Tag Object一併刪除
    name = CharField(max_length=255)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """食譜的原料"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,)

    def __str__(self):
        return self.name
