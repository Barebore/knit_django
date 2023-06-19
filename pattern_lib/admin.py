from django.contrib import admin
from .models import Category, Pattern


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
    list_filter = ('title',)

@admin.register(Pattern)
class PatternAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Pattern._meta.get_fields()]
    search_fields = [field.name for field in Pattern._meta.get_fields()]
    list_filter = [field.name for field in Pattern._meta.get_fields() if field.get_internal_type() == 'ForeignKey']  # Фильтрация по внешним ключам
