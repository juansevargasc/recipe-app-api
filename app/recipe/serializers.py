"""
Serializers for recipes APIs
"""
from rest_framework import serializers

from core.models import (
    Recipe,
    Tag
)


class TagSerializer(serializers.ModelSerializer):
    """Serializers for tags."""


    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipes."""
    tags = TagSerializer(many=True, required=False)  # By default nested serializers are read only  # noqa

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'link', 'tags']
        read_only_fields = ['id']

    def _get_or_create_tags(self, tags, recipe):
        """Handle getting or creating tags as needed."""
        auth_user = self.context['request'].user

        # Iterate tags we popped and then add them to recipe.  # noqa
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(
                user=auth_user,
                **tag,  # This allows to include more parameters from the tag model.  # noqa
                # as opposed to
                # name = tag['name']
            )
            # Add them to recipe.
            recipe.tags.add(tag_obj)


    def create(self, validated_data):
        """Customizing creating a recipe."""
        tags = validated_data.pop('tags', [])  # pop tags, if they don't exist, then default to empty list [].  # noqa

        # Creates the recipe without tags in it yet.
        recipe = Recipe.objects.create(**validated_data)
        self._get_or_create_tags(tags, recipe)

        return recipe

    def update(self, instance, validated_data):
        """Update recipe."""
        tags = validated_data.pop('tags', None)
        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance



class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for recipe detail view."""


    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']
