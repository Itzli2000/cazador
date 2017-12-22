from annoying.decorators import render_to
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.template import Context

from .forms import ContactForm


@render_to("contact_form.html")
def contact_form(request):

    is_mail_sent = False
    form = ContactForm()

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            message = request.POST['message']
            phone = request.POST["phone"]
            name = request.POST["name"]

            ctx = {
                'message': message,
                'email': email,
                'phone': phone,
                'name': name
            }

            msg = get_template('mail/mail_form.html').render(
                Context(ctx)
            )
            mail = EmailMessage("Mensaje de EGCM",
                                msg,
                                to=['laura@yaxha.mx'],
                                from_email=email)
            mail.content_subtype = 'html'
            mail.send()

            is_mail_sent = True
            form = ContactForm()

        else:
            form = ContactForm()

    return {
        'form': form,
        'isMailSent': is_mail_sent
    }
