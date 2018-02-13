import os

from django.db import models
from django.db.models import permalink

from tinymce.models import HTMLField

from utilities.utils import get_filename


def get_upload_path(instance, filename):
    name, ext = os.path.splitext(filename)
    return "blog/{}".format(get_filename(ext))


class Category(models.Model):
    title = models.CharField(verbose_name='Título',
                             max_length=100, unique=True)
    slug = models.SlugField(max_length=100, db_index=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField("Creado el", auto_now_add=True)
    updated_at = models.DateTimeField("Actualizado a las", auto_now=True)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(verbose_name='Título',
                             max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    image = models.ImageField(verbose_name="Imagen",
                              help_text="Imagen en formato png o jpg",
                              upload_to=get_upload_path,
                              blank=True,
                              null=True)
    author = HTMLField(verbose_name='Autor', blank=True, unique=True)
    excerpt = HTMLField(verbose_name='Texto corto', blank=True)
    body = HTMLField(verbose_name='Entrada')
    posted = models.DateField(db_index=True, auto_now_add=True)
    category = models.ForeignKey(Category)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField("Creado el", auto_now_add=True)
    updated_at = models.DateTimeField("Actualizado a las", auto_now=True)

    class Meta:
        verbose_name = "Entrada"
        verbose_name_plural = "Entradas"

    def __str__(self):
        return self.title

    @permalink
    def get_absolute_url(self):
        return ('view_post', None, {'slug': self.slug})
