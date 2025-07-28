from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from accounts.forms import RegisterUserForm


class LoginView(LoginView):
    template_name = 'accounts/login.html'


class RegisterUserView(CreateView):
    form_class = RegisterUserForm
    template_name = 'accounts/register-user.html'
    success_url = reverse_lazy('login')
