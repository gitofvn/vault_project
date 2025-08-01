from django import forms

from credentials.models import Credential
from utils.encryption import encrypt_password


class CredentialForm(forms.ModelForm):
    password = forms.CharField()

    class Meta:
        model = Credential
        fields = ['site_name', 'username', 'email', 'phone_number', 'site_url', 'other', 'password']
        widgets = {
            'site_url': forms.TextInput(attrs={
                'placeholder': 'e.g., google.com'
            }),
            'other': forms.Textarea(attrs={
                'rows': 2,
                'style': 'resize: vertical;',
            }),
        }

    def __init__(self, *args, **kwargs):
        show_password = kwargs.pop('show_password', False)
        super().__init__(*args, **kwargs)

        if show_password:
            self.fields['password'].widget = forms.TextInput()
        else:
            self.fields['password'].widget = forms.PasswordInput()

    def clean_site_url(self):
        site_url = self.cleaned_data.get('site_url', '').strip()
        if site_url and not site_url.startswith(('http://', 'https://')):
            site_url = 'https://' + site_url
        return site_url

    def save(self, user, commit=True):
        instance = super().save(commit=False)
        instance.user = user

        instance.password_encrypted = encrypt_password(user, self.cleaned_data['password'])

        if commit:
            instance.save()
        return instance




