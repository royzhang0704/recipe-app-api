""" 測試食材API"""
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.urls import reverse

from django.test import TestCase


from rest_framework import status

from rest_framework.test import APIClient

from core.models import Ingredient,Recipe

from recipe.serializers import IngredientSerializer


Ingredient_URL=reverse('recipe:ingredient-list')

def ingredient_detail_url(ingredient_id):
    """返回完整的食材URL"""
    return reverse('recipe:ingredient-detail',args=[ingredient_id])

def create_user(email="user@example.com",password="test123"):
    """創建使用者函數 方便測試 不用每一次在不同Funtion 都要創建一次"""
    return get_user_model().objects.create_user(email=email,password=password)

class PublicIngredientApiTest(TestCase):
    """未經驗證使用者請求原料API"""
    def setUp(self):
        self.client=APIClient()
    def test_auth_required(self):
        """查看必須為驗證過的用戶"""
        res=self.client.get(Ingredient_URL)

        self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED) #沒驗證的請求需跳出401

class PrivateIngredientApitest(TestCase):
    """ 測試私有API  Request"""
    def setUp(self):
        self.user=create_user()
        self.client=APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredient(self):
        """ 瀏覽列表"""
        Ingredient.objects.create(user=self.user,name="Kale")
        Ingredient.objects.create(user=self.user,name="Roy")

        res=self.client.get(Ingredient_URL)

        ingredients=Ingredient.objects.all().order_by('-name')
        serializer=IngredientSerializer(ingredients,many=True)
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(res.data,serializer.data)

    def test_ingredients_limited_to_user(self):
        """限制使用者"""
        user2=create_user(email="test@example.com")
        Ingredient.objects.create(user=user2,name="test2")
        own=Ingredient.objects.create(user=self.user,name="lily")

        res=self.client.get(Ingredient_URL)

        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(len(res.data),1)

        self.assertEqual(res.data[0]['name'],own.name)
        self.assertEqual(res.data[0]['id'],own.id)

    def test_update_ingredient(self):
        """Test updating an ingredient."""
        ingredient = Ingredient.objects.create(user=self.user, name='Cilantro')

        payload = {'name': 'Coriander'}
        url = ingredient_detail_url(ingredient.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        ingredient.refresh_from_db()
        self.assertEqual(ingredient.name, payload['name'])

    def test_delete_ingredient(self):
        """Test deleting an ingredient."""
        ingredient = Ingredient.objects.create(user=self.user, name='Lettuce')

        url = ingredient_detail_url(ingredient.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        ingredients = Ingredient.objects.filter(user=self.user)
        self.assertFalse(ingredients.exists())

    def test_filter_ingredients_assigned_to_recipes(self):
        """Test listing ingedients to those assigned to recipes."""
        in1 = Ingredient.objects.create(user=self.user, name='Apples')
        in2 = Ingredient.objects.create(user=self.user, name='Turkey')
        recipe = Recipe.objects.create(
            title='Apple Crumble',
            time_minutes=5,
            price=Decimal('4.50'),
            user=self.user,
        )
        recipe.ingredients.add(in1)

        res = self.client.get(Ingredient_URL, {'assigned_only': 1})

        s1 = IngredientSerializer(in1)
        s2 = IngredientSerializer(in2)
        self.assertIn(s1.data, res.data)
        self.assertNotIn(s2.data, res.data)

    def test_filtered_ingredients_unique(self):
        """Test filtered ingredients returns a unique list."""
        ing = Ingredient.objects.create(user=self.user, name='Eggs')
        Ingredient.objects.create(user=self.user, name='Lentils')
        recipe1 = Recipe.objects.create(
            title='Eggs Benedict',
            time_minutes=60,
            price=Decimal('7.00'),
            user=self.user,
        )
        recipe2 = Recipe.objects.create(
            title='Herb Eggs',
            time_minutes=20,
            price=Decimal('4.00'),
            user=self.user,
        )
        recipe1.ingredients.add(ing)
        recipe2.ingredients.add(ing)

        res = self.client.get(Ingredient_URL, {'assigned_only': 1})

        self.assertEqual(len(res.data), 1)