from django.contrib import admin
from .models import Category, Article, Media, Term, TestRichText, TinyMCEText


class MediaInline(admin.TabularInline):
    model = Media
    extra = 1


class ArticleAdmin(admin.ModelAdmin):
    inlines = [MediaInline]
    list_display = ('title', 'pub_date', 'category')
    list_filter = ['pub_date']
    search_fields = ['title']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


class TermAdmin(admin.ModelAdmin):
    list_display = ['term', 'definition']
    search_fields = ['term', 'definition']


admin.site.register(TinyMCEText)
admin.site.register(TestRichText)
admin.site.register(Term, TermAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Article, ArticleAdmin)
