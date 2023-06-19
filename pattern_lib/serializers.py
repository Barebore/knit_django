from rest_framework import serializers
from .models import Pattern, Category


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
    class Meta:
        model = Pattern
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
