import datetime

from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from django.contrib.auth.tokens import default_token_generator
from django.core.urlresolvers import reverse
from django.shortcuts import resolve_url

from annoying.decorators import render_to


from .models import User, Profile, ShippingAddress, BillingAddress
from .forms import (
    RegistrationForm,
    ProfileForm,
    UserForm,
    ChangePasswordForm,
    ShippingAddressForm,
    BillingAddressForm,
    PasswordResetForm,
)

from utilities.utils import generate_activation_key, get_or_create


@render_to('register.html')
def register(request):
    if request.user.is_authenticated():
        return redirect('/')
    registration_form = RegistrationForm()

    datas = {}
    datas["email"] = ""
    datas["username"] = ""

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            datas['username'] = form.cleaned_data['username']
            datas['email'] = form.cleaned_data['email']
            datas['password1'] = form.cleaned_data['password1']
            # We generated a random activation key
            datas['activation_key'] = generate_activation_key(datas[
                                                              'username'])
            datas['email_path'] = '/activationemail.html'
            datas['email_subject'] = 'Activación de cuenta'

            try:
                form.save(datas)
                form.send_email(datas)
                request.session['registered'] = True
                return redirect('/')
            except:
                messages.error(request, "Usuario o email ya en uso")

        else:
            messages.error(request, form.errors)
            registration_form = form
            datas['username'] = request.POST.get('username', '')
            datas['email'] = request.POST.get('email', '')

    return {
        'registration_form': registration_form,
        'email': datas["email"],
        'username': datas["username"]
    }


@render_to('activation.html')
def activation(request, key):
    activation_expired = False
    already_active = False
    id_user = ''
    user = get_object_or_404(User, activation_key=key)
    if not user.is_active:
        if timezone.now() > user.key_expires:
            activation_expired = True
            id_user = user.id
        else:
            user.is_active = True
            user.save()
    else:
        already_active = True

    return {
        'activation_expired': activation_expired,
        'id_user': id_user,
        'already_active': already_active
    }


def new_activation_link(request, user_id):
    form = RegistrationForm()
    datas = {}
    user = get_object_or_404(id=user_id)
    if user is not None and not user.is_active:
        datas['username'] = user.username
        datas['email'] = user.email
        datas['email_path'] = '/mail/resendemail.html'
        datas['email_subject'] = 'Activación de cuenta'
        datas['activation_key'] = generate_activation_key(datas['username'])

        user.activation_key = datas['activation_key']
        user.key_expires = datetime.datetime.strftime(
            datetime.datetime.now() + datetime.timedelta(days=2),
            "%Y-%m-%d %H:%M:%S")
        user.save()

        form.send_email(datas)
        request.session['new_link'] = True

    return redirect('/')


@login_required
@render_to('profile.html')
def profile(request):
    profile = Profile.objects.get(user=request.user)
    user_form = UserForm(instance=request.user)
    if request.method == 'POST':
        profile_form = ProfileForm(
            instance=profile,
            data=request.POST,
            files=request.FILES,
        )

        if profile_form.is_valid():
            profile_form.save(commit=False)
            profile_form.user = request.user
            messages.success(
                request,
                'Se ha actualizado su perfil correctamente'
            )
            profile_form.save()
        else:
            messages.error(request, profile_form.errors)
    else:
        profile_form = ProfileForm(instance=profile)
    return {
        'profile': profile,
        'profile_form': profile_form,
        'user_form': user_form
    }


@csrf_protect
@render_to("custom_registration/password_reset_form.html")
def password_reset(
        request, is_admin_site=False,
        template_name='custom_registration/password_reset_form.html',
        email_template_name='registration/password_reset_email.html',
        subject_template_name='registration/password_reset_subject.txt',
        password_reset_form=PasswordResetForm,
        token_generator=default_token_generator,
        post_reset_redirect=None,
        from_email=None,
        current_app=None,
        extra_context=None,
        html_email_template_name=None):
    if post_reset_redirect is None:
        post_reset_redirect = reverse('password_reset_done')
    else:
        post_reset_redirect = resolve_url(post_reset_redirect)
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            opts = {
                'use_https': request.is_secure(),
                'token_generator': token_generator,
                'from_email': from_email,
                'email_template_name': email_template_name,
                'subject_template_name': subject_template_name,
                'request': request,
                'html_email_template_name': html_email_template_name,
            }
            form.save(**opts)
            return HttpResponseRedirect(post_reset_redirect)
    else:
        form = password_reset_form()

    return {
        'form': form,
    }


@login_required
@render_to('change_password.html')
def change_password(request):
    change_password_form = ChangePasswordForm()
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            user = User.objects.get(pk=request.user.pk)
            password1 = form.cleaned_data['password1']
            user.set_password(password1)
            user.save()
            update_session_auth_hash(request, user)
            messages.success(
                request,
                'Se ha actualizado su contraseña correctamente'
            )
            return redirect('change_pass')
        else:
            messages.error(request, form.errors)
            change_password_form = form

    return {
        'change_password_form': change_password_form
    }


@render_to("custom_registration/password_change_done.html")
def password_change_done(request):
    return {
    }


@render_to('custom_registration/password_reset_done.html')
def password_reset_done(request, current_app=None, extra_context=None):
    return {
        'title': u'Reestablecimiento de la contraseña exitoso',
    }


@login_required
@render_to('shipping_address.html')
def shipping(request):
    ins = get_or_create(ShippingAddress, request.user)

    shipping_address_form = ShippingAddressForm(instance=ins)
    if request.method == 'POST':
        form = ShippingAddressForm(
            instance=ins,
            data=request.POST
        )
        if form.is_valid():
            form.save(commit=False)
            form.user = request.user
            form.save()
            messages.success(request, 'Se guardó correctamente.')
            return redirect('shipping')
        else:
            messages.error(request, form.errors)
            shipping_address_form = form

    return {
        'shipping_address_form': shipping_address_form
    }


@login_required
@render_to('billing_address.html')
def billing(request):
    ins = get_or_create(BillingAddress, request.user)

    billing_address_form = BillingAddressForm(instance=ins)
    if request.method == 'POST':
        form = BillingAddressForm(
            instance=ins,
            data=request.POST
        )
        if form.is_valid():
            form.save(commit=False)
            form.user = request.user
            form.save()
            messages.success(request, 'Se guardó correctamente.')
            return redirect('billing')
        else:
            messages.error(request, form.errors)
            billing_address_form = form

    return {
        'billing_address_form': billing_address_form
    }
