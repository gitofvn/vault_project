from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib import messages

from accounts.forms import RegisterUserForm
from credentials.models import Credential
from notes.models import Note


class LoginView(LoginView):
    template_name = 'accounts/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)


class RegisterUserView(CreateView):
    form_class = RegisterUserForm
    template_name = 'accounts/register-user.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request, "Account created successfully! Please log in.")
        return super().form_valid(form)


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context['total_credentials'] = Credential.objects.filter(user=user).count()
        context['total_notes'] = Note.objects.filter(user=user).count()

        context['recent_credentials'] = Credential.objects.filter(user=user).order_by('-created_at')[:5]
        context['recent_notes'] = Note.objects.filter(user=user).order_by('-created_at')[:5]

        return context
