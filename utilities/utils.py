from datetime import datetime
import locale
import hashlib
from io import BytesIO

from django.utils.crypto import get_random_string
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template

from xhtml2pdf import pisa


def get_filename(extension):
    """Returns a unique file name based on its extension parameter"""
    ts = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    return '{0}{1}'.format(ts, extension)


def number_format(num, places=0):
    return locale.format("%.*f", (places, num), True)


def generate_activation_key(username):
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+'
    secret_key = get_random_string(20, chars)
    return hashlib.sha256((secret_key + username).encode('utf-8')).hexdigest()


def generate_random_invoice_number():
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
    secret_key = get_random_string(18, chars)
    return hashlib.sha256((secret_key).encode('utf-8')).hexdigest()


def get_or_create(instance, user):
    try:
        ins = instance.objects.get(user=user)
    except instance.DoesNotExist:
        ins = instance(user=user)
        ins.save()
    return ins


def render_to_pdf(template_src, context_dict={}):
    template = get_template('pdf/oxxo_pdf.html')
    context = Context(context_dict)
    html = template.render(context)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type="application/pdf")
    return None
