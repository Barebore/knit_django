from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=250)
    
    def __str__(self):
        return self.title


class Pattern(models.Model):
    title = models.CharField(max_length=65)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    pattern = models.ImageField(upload_to='pattern_image/')
    pattern_description = models.TextField()
    scheme = models.ImageField(upload_to='scheme_image/')
    scheme_description = models.ImageField(
        upload_to='scheme_description_image/',
        )
    #добавить поле 200х200 и только оно должно выдаваться, когда
    #запрашивается список файлов