from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from tinymce.models import HTMLField


class Category(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(default='default.jpg', null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        app_label = 'knowledge_library'

class Article(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.title

    class Meta:
        app_label = 'knowledge_library'

class Media(models.Model):
    ARTICLE = 1
    VIDEO = 2
    IMAGE = 3
    MEDIA_TYPES = [
        (ARTICLE, 'Article'),
        (VIDEO, 'Video'),
        (IMAGE, 'Image'),
    ]
    
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    media_type = models.PositiveSmallIntegerField(choices=MEDIA_TYPES)
    file = models.FileField(upload_to='media_knowledge/')

    def __str__(self):
        return f'{self.get_media_type_display()}'
    
    class Meta:
        app_label = 'knowledge_library'

class Term(models.Model):
    term = models.CharField(max_length=255)
    definition = models.TextField()

    def __str__(self):
        return self.term
    
    class Meta:
        app_label = 'knowledge_library'
    
class TestRichText(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextUploadingField()

    def __str__(self):
        return self.title
    
    class Meta:
        app_label = 'knowledge_library'
    
class TinyMCEText(models.Model):
    title = models.CharField(max_length=200)
    content = HTMLField()

    def __str__(self):
        return self.title
    
    class Meta:
        app_label = 'knowledge_library'
