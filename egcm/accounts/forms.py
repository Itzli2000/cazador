import datetime
from collections import OrderedDict

from django import forms
from django.contrib.auth.tokens import default_token_generator
from django.forms.utils import ErrorList
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template import Context
from django.template import loader
from django.template.loader import get_template
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import ugettext_lazy as _

from .models import User, Profile, BillingAddress, ShippingAddress


class RegistrationForm(forms.Form):
    username = forms.CharField(
        label='Nombre de usuario',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Nombre de usuario',
                'class': 'form-control'
            }
        ),
        max_length=30,
        min_length=3,
    )
    email = forms.EmailField(
        label='',
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Correo Electrónico',
                'class': 'form-control',
            }
        ),
        max_length=100,
        min_length=3
    )
    password1 = forms.CharField(
        label='',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña',
                'class': 'form-control',
            }
        ),
        max_length=50,
        min_length=6
    )
    password2 = forms.CharField(
        label='',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Repetir Contraseña',
                'class': 'form-control',
            }
        ),
        max_length=50,
        min_length=6
    )

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password1 != password2:
            self._errors['password2'] = ErrorList(
                ['Las contraseñas deben de coincidir']
            )

        return self.cleaned_data

    def save(self, datas):
        u = User.objects.create_user(
            datas['username'],
            datas['email'],
            datas['password1']
        )

        u.is_active = False
        u.activation_key = datas['activation_key']
        u.key_expires = datetime.datetime.strftime(
            datetime.datetime.now() + datetime.timedelta(days=2),
            '%Y-%m-%d %H:%M:%S'
        )
        u.save()
        # Save profile
        profile = Profile()
        profile.user = u
        profile.save()
        return u

    def send_email(self, datas):
        link = settings.URL_DOMAIN + '/activacion/' + datas['activation_key']
        c = Context({'activation_link': link, 'username': datas['username']})
        msg = get_template(
            'mail/activationemail.html'
        ).render(Context(c))

        mail = EmailMessage(
            datas['email_subject'],
            msg,
            to=[datas['email']],
            from_email='no-reply@egcm.mx'
        )
        mail.content_subtype = 'html'
        mail.send()


class UserForm(forms.ModelForm):
    username = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Nombre de usuario',
                'class': 'form-control',
                'disabled': 'disabled',
            }
        ),
        max_length=30,
        min_length=3,
    )
    email = forms.EmailField(
        label='',
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Correo Electrónico',
                'class': 'form-control',
                'disabled': 'disabled',
            }
        ),
        max_length=100,
        min_length=3
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
        ]
        exclude = [
            'activation_key',
            'key_expires',
            'is_admin',
            'is_active'
        ]


class ProfileForm(forms.ModelForm):
    name = forms.CharField(
        label='Nombre Completo',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    website = forms.CharField(
        label='Sitio Web',
        widget=forms.URLInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    ubication = forms.CharField(
        label='Ubicación',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    bio = forms.CharField(
        label='Bio',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control'
            }
        )
    )

    class Meta:
        model = Profile
        fields = [
            'image',
            'name',
            'website',
            'ubication',
            'bio'
        ]
        exclude = ['user', 'is_active']


class ChangePasswordForm(forms.Form):
    password1 = forms.CharField(
        label='',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña',
                'class': 'form-control',
            }
        ),
        max_length=50,
        min_length=6
    )
    password2 = forms.CharField(
        label='',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Repetir Contraseña',
                'class': 'form-control',
            }
        ),
        max_length=50,
        min_length=6
    )

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password1 != password2:
            self._errors['password2'] = ErrorList(
                ['Las contraseñas deben de coincidir']
            )

        return self.cleaned_data


class ShippingAddressForm(forms.ModelForm):
    line1 = forms.CharField(
        label='Línea 1',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    line2 = forms.CharField(
        label='Línea 2',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    city = forms.CharField(
        label='Ciudad',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    state = forms.CharField(
        label='Estado',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    country = forms.CharField(
        label='País',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    zip_code = forms.CharField(
        label='Código Postal',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    phone_number = forms.CharField(
        label='Teléfono',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    class Meta:
        model = ShippingAddress
        fields = [
            'line1',
            'line2',
            'city',
            'state',
            'country',
            'zip_code',
            'phone_number'
        ]
        exclude = ['is_active']


class BillingAddressForm(forms.ModelForm):
    line1 = forms.CharField(
        label='Línea 1',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    line2 = forms.CharField(
        label='Línea 2',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    city = forms.CharField(
        label='Ciudad',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    state = forms.CharField(
        label='Estado',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    country = forms.CharField(
        label='País',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    zip_code = forms.CharField(
        label='Código Postal',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    phone_number = forms.CharField(
        label='Teléfono',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    class Meta:
        model = BillingAddress
        fields = [
            'line1',
            'line2',
            'city',
            'state',
            'country',
            'zip_code',
            'phone_number'
        ]
        exclude = ['is_active']


class PasswordResetForm(forms.Form):
    email = forms.EmailField(label=_("Email"), max_length=254)

    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email,
                  html_email_template_name=None):
        """
        Sends a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(
            subject, body, from_email, [to_email])
        if html_email_template_name is not None:
            html_email = loader.render_to_string(
                html_email_template_name, context)
            email_message.attach_alternative(html_email, 'text/html')

        email_message.send()

    def get_users(self, email):
        """Given an email, return matching user(s) who should receive a reset.

        This allows subclasses to more easily customize the default policies
        that prevent inactive users and users with unusable passwords from
        resetting their password.

        """
        active_users = get_user_model()._default_manager.filter(
            email__iexact=email, is_active=True)
        return (u for u in active_users if u.has_usable_password())

    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name=None):
        """
        Generates a one-use only link for resetting password and sends to the
        user.
        """
        email = self.cleaned_data["email"]
        for user in self.get_users(email):
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            context = {
                'email': user.email,
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
            }

            self.send_mail(subject_template_name, email_template_name,
                           context, from_email, user.email,
                           html_email_template_name=html_email_template_name)


class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    new_password1 = forms.CharField(label=_("New password"),
                                    widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=_("New password confirmation"),
                                    widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(SetPasswordForm, self).__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        return password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.user.save()
        return self.user


class PasswordChangeForm(SetPasswordForm):
    """
    A form that lets a user change their password by entering their old
    password.
    """
    error_messages = dict(SetPasswordForm.error_messages, **{
        'password_incorrect': _("Your old password was entered incorrectly. "
                                "Please enter it again."),
    })
    old_password = forms.CharField(label=_("Old password"),
                                   widget=forms.PasswordInput)

    def clean_old_password(self):
        """
        Validates that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password


PasswordChangeForm.base_fields = OrderedDict(
    (k, PasswordChangeForm.base_fields[k])
    for k in ['old_password', 'new_password1', 'new_password2']
)

