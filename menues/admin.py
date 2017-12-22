from django.contrib import admin

from .models import Category, Menu


class MenuItemInLine(admin.TabularInline):
    model = Menu
    raw_id_fields = ['category']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [MenuItemInLine]
    ordering = ("name",)


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    ordering = ("name",)
