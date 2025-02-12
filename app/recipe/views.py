"""
Views for the recipe API's.
"""
from rest_framework import (
    viewsets,
    mixins # Additional funct. to a view  noqa
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import (
    Recipe,
    Tag,
    Ingredient
)
from recipe import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    """
    View for manage recipe API's.
    ModelViewSet will help on the different endpoints.
    It helps with the logic of this.
    """
    serializer_class = serializers.RecipeDetailSerializer  # We changed to be detail the default one.  noqa
    queryset = Recipe.objects.all()
    # Specifies authentication
    authentication_classes = [TokenAuthentication]
    # This means you need to be authenticated.
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Retrieve recipes for authenticated users. Desc order by recipe id
        self.request.user means the user that authenticated at the request
        """
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """
        Return the serializer class for request.
        It will depend if the action is list.
        We are customizing the serializer for the following Default Router config:
        endpoint: recipes/	type: GET	self.action: list	Action: List all recipes
        """
        if self.action == 'list':
            return serializers.RecipeSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """
        Create a new recipe.
        When we create a new recipe
        we call this method.

        Here it is assumed that the serializer is validated.
        """
        serializer.save(user=self.request.user)


class BaseRecipeAttrViewSet(
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Base viewset for the recipe attributes."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset to authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-name')


class TagViewSet(
    BaseRecipeAttrViewSet
):
    """
    Manage tags in the database.
    It is important that GenericViewSet is the last to inherit from.
    UpdateModelMixin allowed to update using patch.
    """
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()


class IngredientViewSet(
        BaseRecipeAttrViewSet
    ):
    """Viewset for Ingredients. Manage Ingredients in the database."""
    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()
