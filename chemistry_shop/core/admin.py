from django.contrib import admin

from .models import *


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'photo', 'price', 'time_create', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    prepopulated_fields = {'slug': ("title",)}


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ("name",)}


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Category, CategoryAdmin)
