from django.contrib import admin

from .models import Category, Dish


class DishItemInLine(admin.TabularInline):
    model = Dish
    raw_id_fields = ['category']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [DishItemInLine]
    ordering = ("name",)


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
