"""
Views for the recipe API's.
"""
from rest_framework import (
    viewsets,
    mixins,
    status,
)  # Additional funct. to a view  # noqa
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe, Tag, Ingredient
from recipe import serializers

# from rest_framework.parsers import MultiPartParser


class RecipeViewSet(viewsets.ModelViewSet):
    """
    View for manage recipe API's.
    ModelViewSet will help on the different endpoints.
    It helps with the logic of this.
    """

    serializer_class = (
        serializers.RecipeDetailSerializer
    )  # We changed to be detail the default one.  noqa
    queryset = Recipe.objects.all()
    # Specifies authentication
    authentication_classes = [TokenAuthentication]
    # This means you need to be authenticated.
    permission_classes = [IsAuthenticated]

    # parser_classes = [MultiPartParser]

    def get_queryset(self):
        """
        Retrieve recipes for authenticated users. Desc order by recipe id
        self.request.user means the user that authenticated at the request
        """
        return self.queryset.filter(user=self.request.user).order_by("-id")

    def get_serializer_class(self):
        """
        Return the serializer class for request.
        It will depend if the action is list.
        We are customizing the serializer
        for the following Default Router config:
        endpoint:
        recipes/	type: GET	self.action: list
        Action: List all recipes
        """
        if self.action == "list":
            return serializers.RecipeSerializer
        elif self.action == "upload_image":
            return serializers.RecipeImageSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """
        Create a new recipe.
        When we create a new recipe
        we call this method.

        Here it is assumed that the serializer is validated.
        """
        serializer.save(user=self.request.user)

    @action(methods=["POST"], detail=True, url_path="upload-image")
    def upload_image(self, request, pk=None):
        """
        Upload an image to recipe.
        Detail means it is a specific id of a recipe.
        The non-detail view would be a list of recipes.

        """
        recipe = self.get_object()
        serializer = self.get_serializer(recipe, data=request.data)

        if serializer.is_valid():
            serializer.save()  # Safe to db.
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BaseRecipeAttrViewSet(
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Base viewset for the recipe attributes."""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset to authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by("-name")


class TagViewSet(BaseRecipeAttrViewSet):
    """
    Manage tags in the database.
    It is important that GenericViewSet is the last to inherit from.
    UpdateModelMixin allowed to update using patch.
    """

    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()


class IngredientViewSet(BaseRecipeAttrViewSet):
    """Viewset for Ingredients. Manage Ingredients in the database."""

    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()
