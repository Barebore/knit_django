from rest_framework import serializers
from .models import Pattern, Category
from PIL import Image
from django.core.files.storage import default_storage as storage



# class PatternSerializer(serializers.ModelSerializer):
#     category_title = serializers.ReadOnlyField(source='category.title')

#     class Meta:
#         model = Pattern
#         fields = '__all__'
#         extra_fields = ['category_title']

#     def get_field_names(self, declared_fields, info):
#         expanded_fields = super().get_field_names(declared_fields, info)
#         return expanded_fields + self.Meta.extra_fields


class PatternSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pattern
        fields = 'id', 'title', 'category', 'pattern'


class PatternDetailSerializer(serializers.ModelSerializer):
    pattern_resolution = serializers.SerializerMethodField()
    scheme_resolution = serializers.SerializerMethodField()
    scheme_description_resolution = serializers.SerializerMethodField()

    class Meta:
        model = Pattern
        fields = '__all__'

    def get_pattern_resolution(self, obj):
        if obj.pattern:
            image_path = obj.pattern.path
            if storage.exists(image_path):
                with storage.open(image_path, 'rb') as image_file:
                    image = Image.open(image_file)
                    return f'{image.width}x{image.height}'
        return None

    def get_scheme_resolution(self, obj):
        if obj.scheme:
            image_path = obj.scheme.path
            if storage.exists(image_path):
                with storage.open(image_path, 'rb') as image_file:
                    image = Image.open(image_file)
                    return f'{image.width}x{image.height}'
        return None

    def get_scheme_description_resolution(self, obj):
        if obj.scheme_description:
            image_path = obj.scheme_description.path
            if storage.exists(image_path):
                with storage.open(image_path, 'rb') as image_file:
                    image = Image.open(image_file)
                    return f'{image.width}x{image.height}'
        return None

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
