from PIL import Image
from rest_framework import serializers

from .models import Category, Pattern

# class PatternSerializer(serializers.ModelSerializer):
#     category_title = serializers.ReadOnlyField(source='category.title')

#     class Meta:
#         model = Pattern
#         fields = '__all__'
#         extra_fields = ['category_title']

#     def get_field_names(self, declared_fields, info):
#         expanded_fields = super().get_field_names(declared_fields, info)
#         return expanded_fields + self.Meta.extra_fields


class ImageFieldSerializer(serializers.Serializer):
    def to_representation(self, value):
        if value and hasattr(value, 'url'):
            img = Image.open(value.path)
            width, height = img.size
            request = self.context.get('request')
            img_url = request.build_absolute_uri(value.url)
            return {
                'width': width,
                'height': height,
                'img': img_url
            }
        return None

class PatternSerializer(serializers.ModelSerializer):
    pattern = ImageFieldSerializer()
    class Meta:
        model = Pattern
        fields = 'id', 'title', 'category', 'pattern'

class PatternDetailSerializer(serializers.ModelSerializer):
    pattern = ImageFieldSerializer()
    scheme = ImageFieldSerializer()
    scheme_description = ImageFieldSerializer()

    class Meta:
        model = Pattern
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
