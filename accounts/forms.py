from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class RegisterUserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        label='Password'
    )
    reenter_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Re-enter Password'}),
        label='Confirm Password'
    )

    class Meta:
        model = User
        fields = ['username', 'email']

        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        reenter = cleaned_data.get('reenter_password')

        if password and reenter and password != reenter:
            raise ValidationError("Passwords do not match.")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
