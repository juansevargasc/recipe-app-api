"""
URL mappings for the recipe app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from recipe import views


router = DefaultRouter()
# This will create endpoint "/recipes", it will support CRUD methods
router.register("recipes", views.RecipeViewSet)
router.register("tags", views.TagViewSet)
router.register("ingredients", views.IngredientViewSet)

# Name for reverse look up
app_name = "recipe"

# Include the router urls
urlpatterns = [path("", include(router.urls))]
