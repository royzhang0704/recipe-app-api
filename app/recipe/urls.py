"""
URL mapping for the recipe app.
"""
from django.urls import path,include

from . import views

from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register("recipe",views.RecipeViewSet)
router.register("tag",views.TagViewSet)
router.register('ingredient',views.IngredientViewSet)
app_name='recipe'

urlpatterns=[
    path('',include(router.urls)),
]
