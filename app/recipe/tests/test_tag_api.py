from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from core.models import Tag,Recipe
from rest_framework import status
from django.test import TestCase
from recipe import serializers
from decimal import Decimal

from recipe.serializers import TagSerializer

tag_url = reverse('recipe:tag-list')

def detail_url(tag_id):
    """返回一個詳細的URL"""
    return reverse("recipe:tag-detail", args=[tag_id])

def create_user(email="test@example.com", password="password123"):
    """創建一個User到資料庫裡面"""
    return get_user_model().objects.create_user(email=email, password=password)

class PublicTagApiTest(TestCase):
    """測試未經驗證的API Request"""
    def setUp(self):
        self.client = APIClient()  # 模擬的API請求客戶端，方便作一些HTTP請求

    def test_auth_required(self):
        """測試尚未驗證使用者嘗試請求tag的URL"""
        res = self.client.get(tag_url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateTagApiTest(TestCase):
    """測試通過驗證的API request"""
    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """測試使用者是否能獲取自己的Tag"""
        Tag.objects.create(user=self.user, name="Vegan")
        Tag.objects.create(user=self.user, name="Dessert")

        res = self.client.get(tag_url)

        tags = Tag.objects.all().order_by('-name')  # 修正為只過濾自己的tag
        serializer = serializers.TagSerializer(tags, many=True)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(res.status_code,status.HTTP_200_OK)

    def test_tag_limited_to_user(self):
        """測試回傳的Tag 是否只包含自己的"""
        other_user = create_user(email="other@example.com", password="passwordtest2")
        Tag.objects.create(user=other_user, name="test2")
        tag = Tag.objects.create(user=self.user, name="test1")

        res = self.client.get(tag_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)
        self.assertEqual(res.data[0]['id'], tag.id)

    def test_update_tag(self):
        """測試更新是否成功"""
        tag = Tag.objects.create(user=self.user, name='before')
        payload = {'name': 'after'}
        url = detail_url(tag.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        tag.refresh_from_db()
        self.assertEqual(tag.name, payload['name'])  # 修正的 name 檢查

    def test_delete_tag(self):
        """刪除Tag """
        tag = Tag.objects.create(user=self.user, name="test")  # 修正的 objects
        url = detail_url(tag.id)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        tags = Tag.objects.filter(user=self.user)
        self.assertFalse(tags.exists())

    def test_filter_tags_assigned_to_recipes(self):
        """Test listing tags to those assigned to recipes."""
        tag1 = Tag.objects.create(user=self.user, name='Breakfast')
        tag2 = Tag.objects.create(user=self.user, name='Lunch')
        recipe = Recipe.objects.create(
            title='Green Eggs on Toast',
            time_minutes=10,
            price=Decimal('2.50'),
            user=self.user,
        )
        recipe.tags.add(tag1)

        res = self.client.get(tag_url, {'assigned_only': 1})

        s1 = TagSerializer(tag1)
        s2 = TagSerializer(tag2)
        self.assertIn(s1.data, res.data)
        self.assertNotIn(s2.data, res.data)

    def test_filtered_tags_unique(self):
        """Test filtered tags returns a unique list."""
        tag = Tag.objects.create(user=self.user, name='Breakfast')
        Tag.objects.create(user=self.user, name='Dinner')
        recipe1 = Recipe.objects.create(
            title='Pancakes',
            time_minutes=5,
            price=Decimal('5.00'),
            user=self.user,
        )
        recipe2 = Recipe.objects.create(
            title='Porridge',
            time_minutes=3,
            price=Decimal('2.00'),
            user=self.user,
        )
        recipe1.tags.add(tag)
        recipe2.tags.add(tag)

        res = self.client.get(tag_url, {'assigned_only': 1})

        self.assertEqual(len(res.data), 1)
