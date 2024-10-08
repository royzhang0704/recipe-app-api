"""
Serializer for recipe APIs
"""
from rest_framework import serializers

from core.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipes."""
    class Meta:
        model=Recipe
        fields=['id','title','time_minutes','prices','link']
        read_only_fields=['id']

class RecipeDetailSerializer(serializers.ModelSerializer):
    """Serializer for detail recipe"""

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields+['description']
