from django.contrib import admin

from .models import Category, Presentation, Product


class ProductItemInLine(admin.TabularInline):
    model = Product
    raw_id_fields = ['category']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [ProductItemInLine]
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name', )}
    ordering = ("name",)


@admin.register(Presentation)
class PresentationAdmin(admin.ModelAdmin):
    list_display = ['name']
    ordering = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name', 
        'category',
        'slug',
        'price',
        'stock', 
        'is_available',
    ]
    list_filter = ['is_available', ]
    list_editable = ['price', 'stock', 'is_available']
    prepopulated_fields = {'slug': ('name', )}
    ordering = ("name",)
