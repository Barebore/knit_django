from rest_framework import viewsets
from .models import Category, Article, Media, Term, TestRichText
from .serializers import (CategorySerializer, ArticleSerializer,
                           MediaSerializer, TermSerializer, TestRichTextSerializer,)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import LimitOffsetPagination
import spacy
from spacy.matcher import PhraseMatcher
from spacy.lang.ru.examples import sentences
from rest_framework.response import Response

nlp = spacy.load('ru_core_news_sm')

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filterset_fields = ('category', )
    filter_backends = (DjangoFilterBackend,)
    pagination_class = LimitOffsetPagination

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        # получаем текст статьи
        article_text = serializer.data['content'].lower()

        # получаем все термины и создаем словарь терминов и их экземпляров моделей
        terms = {term.term.lower(): term for term in Term.objects.all()}
        
        # преобразуем термины в doc objects
        patterns = [nlp.make_doc(term) for term in terms.keys()]
        
        # инициализируем PhraseMatcher
        matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
        matcher.add("TerminologyList", patterns)

        # создаем объект Doc с помощью nlp
        doc = nlp(article_text)

        # отбираем те термины, которые содержатся в тексте статьи
        matches = matcher(doc)
        relevant_terms = [terms[doc[start:end].text.lower()] for _, start, end in matches]

        # сериализуем отобранные термины
        term_serializer = TermSerializer(relevant_terms, many=True)

        # включаем сериализованные термины в ответ
        response_data = serializer.data
        response_data['relevant_terms'] = term_serializer.data

        return Response(response_data)

class MediaViewSet(viewsets.ModelViewSet):
    queryset = Media.objects.all()
    serializer_class = Media

class TermViewSet(viewsets.ModelViewSet):
    queryset = Term.objects.all()
    serializer_class = TermSerializer

class TermViewSet(viewsets.ModelViewSet):
    queryset = Term.objects.all()
    serializer_class = TermSerializer

class TestRichTextViewSet(viewsets.ModelViewSet):
    queryset = TestRichText.objects.all()
    serializer_class = TestRichTextSerializer