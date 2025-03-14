"""
Tests for models.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal

from core import models


def create_user(email='user@example.com', password='testpass123'):
    """Create and return a new user."""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe(self):
        """Test creating a recipe is successful."""
        user = create_user(
            'test@example.com',
            'password123',
        )

        recipe = models.Recipe.objects.create(
            user=user,
            title="Sample recipe",
            time_minutes=5,
            price=Decimal('5.50'),  # 確保使用 'price' 而非 'prices'
            description="Sample recipe description",
        )

        self.assertEqual(str(recipe), recipe.title)

    def test_create_tag(self):
        """Test creating a tag."""
        user = create_user()
        tag = models.Tag.objects.create(user=user, name='Tag1')

        self.assertEqual(str(tag), tag.name)

    def test_create_ingredient(self):
        """Test creating an ingredient."""
        user = create_user()
        ingredient = models.Ingredient.objects.create(
            user=user, name="Test ingredient")

        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_with_tags(self):
        """Test creating a recipe with tags."""
        user = create_user()
        tag1 = models.Tag.objects.create(user=user, name='Vegan')
        tag2 = models.Tag.objects.create(user=user, name='Dessert')

        recipe = models.Recipe.objects.create(
            user=user,
            title="Sample recipe",
            time_minutes=10,
            price=Decimal('7.50')
        )
        recipe.tags.add(tag1, tag2)

        self.assertIn(tag1, recipe.tags.all())
        self.assertIn(tag2, recipe.tags.all())

    def test_recipe_with_ingredients(self):
        """Test creating a recipe with ingredients."""
        user = create_user()
        ingredient1 = models.Ingredient.objects.create(
            user=user, name="Chicken")
        ingredient2 = models.Ingredient.objects.create(user=user, name="Salt")

        recipe = models.Recipe.objects.create(
            user=user,
            title="Grilled Chicken",
            time_minutes=20,
            price=Decimal('10.00')
        )
        recipe.ingredients.add(ingredient1, ingredient2)

        self.assertIn(ingredient1, recipe.ingredients.all())
        self.assertIn(ingredient2, recipe.ingredients.all())
