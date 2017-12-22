from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(
        label='Nombre',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Nombre',
                'class': 'form-control'
            }
        )
    )

    email = forms.EmailField(
        label='E-Mail',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'EMAIL',
                'class': 'form-control'
            }
        )
    )

    phone = forms.CharField(
        label='Teléfono',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Teléfono',
                'class': 'form-control'
            }
        )
    )

    message = forms.CharField(
        label='Mensaje',
        widget=forms.Textarea(
            attrs={
                'placeholder': 'MENSAJE',
                'rows': 4,
                'class': 'form-control'
            }
        )
    )
