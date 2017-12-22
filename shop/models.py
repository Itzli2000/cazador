import os
from random import randint

from django.db import models
from django.db.models.aggregates import Count
from django.db.models import permalink

from sorl.thumbnail import get_thumbnail

from utilities.utils import get_filename


def get_upload_path(instance, filename):
    name, ext = os.path.splitext(filename)
    return "shop/{}".format(get_filename(ext))


class Category(models.Model):
    name = models.CharField(verbose_name="Categoría",
                            max_length=100,
                            unique=True)
    slug = models.SlugField(max_length=200, db_index=True)
    order = models.IntegerField(verbose_name="Orden", default=1)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField("Creado el", auto_now_add=True)
    updated_at = models.DateTimeField("Actualizado a las", auto_now=True)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.name


class Presentation(models.Model):
    name = models.CharField(verbose_name="Categoría",
                            max_length=100,
                            unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField("Creado el", auto_now_add=True)
    updated_at = models.DateTimeField("Actualizado a las", auto_now=True)

    class Meta:
        verbose_name = "Presentación"
        verbose_name_plural = "Presentaciones"

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, verbose_name="Categoría")
    presentation = models.ForeignKey(Presentation, verbose_name="Presentación")
    name = models.CharField(verbose_name="Nombre",
                            max_length=100,
                            db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(verbose_name="Imagen",
                              help_text="Imagen en formato png o jpg",
                              upload_to=get_upload_path,
                              blank=True,
                              null=True)
    price = models.DecimalField(verbose_name="Precio",
                                max_digits=8,
                                decimal_places=2)
    description = models.TextField(verbose_name="Descripción",
                                   blank=True)
    additional_information = models.TextField(
        verbose_name="Información adicional", blank=True
    )
    stock = models.PositiveIntegerField()
    is_available = models.BooleanField(
        default=True,
        verbose_name='¿Disponible?'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField("Creado el", auto_now_add=True)
    updated_at = models.DateTimeField("Actualizado a las", auto_now=True)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        index_together = (('id', 'slug'))

    def __str__(self):
        return self.name

    @permalink
    def get_absolute_url(self):
        return (
            'detail_product_one',
            None,
            {
                'category_id': self.category.pk,
                'product_id': self.id,
            }
        )

    def random(self):
        count = self.aggregate(count=Count('id'))['count']
        random_index = randint(0, count - 1)
        return self.all()[random_index]
