from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from accounts.validators import validate_password_complexity


UserModel = get_user_model()


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
        model = UserModel
        fields = ['username', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if UserModel.objects.filter(email=email).exists():
            raise ValidationError("This email is already in use.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if UserModel.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        validate_password_complexity(password)
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        reenter = cleaned_data.get('reenter_password')

        if password and reenter and password != reenter:
            self.add_error('reenter_password', "Passwords do not match.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email'].lower()
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
