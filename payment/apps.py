from django.apps import AppConfig


class PaymentConfig(AppConfig):
    name = 'payment'
    verbose_name = 'PayPal'

    def ready(self):
        import payment.signals
