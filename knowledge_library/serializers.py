from rest_framework import serializers

from .models import Article, Category, Media, Term, TestRichText


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'image']

class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ['id', 'article', 'media_type', 'file']

class ArticleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    media = MediaSerializer(many=True, read_only=True, source='media_set')

    class Meta:
        model = Article
        fields = ['id', 'category', 'title', 'content', 'pub_date', 'media']

class TermSerializer(serializers.ModelSerializer):
    class Meta:
        model = Term
        fields = ['term', 'definition']

class TestRichTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestRichText
        fields = ['id', 'title', 'content']