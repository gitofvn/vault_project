from django import forms

from credentials.models import Credential, Category
from utils.encryption import encrypt_password


class CredentialForm(forms.ModelForm):
    password = forms.CharField()

    class Meta:
        model = Credential
        fields = ['category', 'site_name', 'username', 'email', 'phone_number', 'site_url', 'other', 'password']
        widgets = {
            'other': forms.Textarea(attrs={
                'rows': 2,
                'style': 'resize: vertical;',
            })
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Pass user to filter categories
        show_password = kwargs.pop('show_password', False)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['category'].queryset = Category.objects.filter(user=user)

        self.fields['category'].required = False

        if show_password:
            self.fields['password'].widget = forms.TextInput()
        else:
            self.fields['password'].widget = forms.PasswordInput()


    def save(self, user, commit=True):
        instance = super().save(commit=False)
        instance.user = user
        instance.password_encrypted = encrypt_password(user, self.cleaned_data['password'])

        if commit:
            instance.save()
        return instance





