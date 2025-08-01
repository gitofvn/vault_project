from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

from credentials.models import Credential
from credentials.forms import CredentialForm
from utils.encryption import encrypt_password, decrypt_password


class CredentialListView(LoginRequiredMixin, ListView):
    model = Credential
    template_name = 'credentials/credential_list.html'
    context_object_name = 'credentials'

    def get_queryset(self):
        return Credential.objects.filter(user=self.request.user)


class CredentialCreateView(LoginRequiredMixin, CreateView):
    model = Credential
    form_class = CredentialForm
    template_name = 'credentials/credential_add.html'
    success_url = reverse_lazy('credential-list')

    def form_valid(self, form):
        form.save(user=self.request.user)
        return redirect(self.success_url)


class CredentialDetailView(LoginRequiredMixin, DetailView):
    model = Credential
    template_name = 'credentials/credential_detail.html'
    context_object_name = 'credential'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['decrypted_password'] = decrypt_password(
            self.request.user,
            self.object.password_encrypted
        )
        context['form'] = CredentialForm()  # for labels
        return context


class CredentialUpdateView(LoginRequiredMixin, UpdateView):
    model = Credential
    form_class = CredentialForm
    template_name = 'credentials/credential_edit.html'
    success_url = reverse_lazy('credential-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method == "GET":
            decrypted_password = decrypt_password(
                self.request.user,
                self.object.password_encrypted
            )
            kwargs.setdefault('initial', {})['password'] = decrypted_password
        kwargs['show_password'] = True
        return kwargs

    def form_valid(self, form):
        form.save(user=self.request.user)
        return redirect(self.success_url)


class CredentialDeleteView(LoginRequiredMixin, DeleteView):
    model = Credential
    template_name = 'credentials/credential_confirm_delete.html'
    success_url = reverse_lazy('credential-list')
