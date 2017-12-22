import os

from django.db import models

from utilities.utils import get_filename


def get_upload_path(instance, filename):
    name, ext = os.path.splitext(filename)
    return "restaurant/{}".format(get_filename(ext))


class Category(models.Model):
    name = models.CharField(verbose_name="Categoría",
                            max_length=100,
                            unique=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(verbose_name="Orden", default=1)
    created_at = models.DateTimeField("Creado el", auto_now_add=True)
    updated_at = models.DateTimeField("Actualizado a las", auto_now=True)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.name


class Dish(models.Model):
    category = models.ForeignKey(Category, verbose_name="Categoría")
    name = models.CharField(verbose_name="Nombre",
                            max_length=100)
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
    additional_information = models.TextField(verbose_name="Información adicional",
                                              blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField("Creado el", auto_now_add=True)
    updated_at = models.DateTimeField("Actualizado a las", auto_now=True)

    class Meta:
        verbose_name = "Platillo"
        verbose_name_plural = "Platillos"

    def __str__(self):
        return self.name
