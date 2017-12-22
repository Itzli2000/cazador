import os

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

from utilities.utils import get_filename


def get_upload_path(instance, filename):
    name, ext = os.path.splitext(filename)
    return "avatar/{}-{}".format(instance.user.username, get_filename(ext))


class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        """Crete and saves an User with the given username,
        email and password
        """
        if not username:
            raise ValueError('El usuario debe tener un nombre de usuario.')
        if not email:
            raise ValueError('El usuario debe tener un email')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        """Creates and saves a superuser with the given username, email
        and password
        """
        user = self.create_user(
            username=username,
            email=email,
            password=password
        )

        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(verbose_name="Nombre de usuario",
                                max_length=100,
                                unique=True,
                                db_index=True)
    email = models.EmailField(verbose_name="Correo Electrónico",
                              max_length=100,
                              unique=True,
                              db_index=True)
    activation_key = models.CharField(max_length=100)
    key_expires = models.DateTimeField(null=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(verbose_name="¿Activo?", default=False)
    created_at = models.DateTimeField("Creado el", auto_now_add=True)
    updated_at = models.DateTimeField("Actualizado a las", auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        # Does the user have a specific permission?
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        if self.is_admin:
            return True
        return False


class Profile(models.Model):
    user = models.ForeignKey(User)
    image = models.ImageField(verbose_name="Imagen",
                              help_text="Imagen en formato png o jpg",
                              upload_to=get_upload_path,
                              blank=True,
                              null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    website = models.CharField(max_length=100, blank=True, null=True)
    ubication = models.CharField(max_length=100, blank=True, null=True)
    bio = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField("Creado el", auto_now_add=True)
    updated_at = models.DateTimeField("Actualizado a las", auto_now=True)

    class Meta:
        verbose_name = "Perfiles"
        verbose_name_plural = "Perfiles"

    def __str_(self):
        return self.name


class BillingAddress(models.Model):
    user = models.ForeignKey(User)
    line1 = models.CharField(max_length=100, verbose_name='Línea 1')
    line2 = models.CharField(
        max_length=100, verbose_name='Línea 2', blank=True, null=True
    )
    city = models.CharField(max_length=100, verbose_name='Ciudad')
    state = models.CharField(max_length=100, verbose_name='Estado')
    country = models.CharField(max_length=100, verbose_name='País')
    zip_code = models.CharField(max_length=5, verbose_name='Código Postal')
    phone_number = models.CharField(
        max_length=20,
        verbose_name='Teléfono',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Dirección de facturación"
        verbose_name_plural = "Direcciones de facturación"


class ShippingAddress(models.Model):
    user = models.ForeignKey(User)
    line1 = models.CharField(max_length=100, verbose_name='Línea 1')
    line2 = models.CharField(
        max_length=100, verbose_name='Línea 2', blank=True, null=True
    )
    city = models.CharField(max_length=100, verbose_name='Ciudad')
    state = models.CharField(max_length=100, verbose_name='Estado')
    country = models.CharField(max_length=100, verbose_name='País')
    zip_code = models.CharField(max_length=5, verbose_name='Código Postal')
    phone_number = models.CharField(
        max_length=20,
        verbose_name='Teléfono',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Dirección de envío"
        verbose_name_plural = "Direcciones de envío"
