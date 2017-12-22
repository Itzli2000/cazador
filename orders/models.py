from django.db import models

from shop.models import Product
from accounts.models import User
from utilities.constants import SHIPPING_COST


class Order(models.Model):
    user = models.ForeignKey(User, verbose_name='Usuario')
    method = models.CharField(
        "Método de pago",
        blank=True,
        max_length=255
    )
    reference_code = models.CharField("Codigo de referencia",
                                      blank=True,
                                      max_length=255)
    transaction_id = models.CharField("ID Transaccion",
                                      blank=True,
                                      max_length=255)
    paid = models.BooleanField(default=False, verbose_name='Pagado')
    status = models.CharField(
        max_length=20,
        verbose_name='Estatus',
        blank=True
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField("Creado el", auto_now_add=True)
    updated_at = models.DateTimeField("Actualizado a las", auto_now=True)

    class Meta:
        verbose_name = 'Orden'
        verbose_name_plural = 'Órdenes'
        ordering = ('-created_at',)

    def __str__(self):
            return 'Orden {}'.format(self.reference_code)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    def get_total_with_shipping(self):
        return self.get_total_cost() + SHIPPING_COST


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items')
    product = models.ForeignKey(Product, related_name='order_items')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
