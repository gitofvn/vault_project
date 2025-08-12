from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.db.models import Q

from credentials.models import Credential
from credentials.forms import CredentialForm
from utils.encryption import decrypt_password


class CredentialListView(LoginRequiredMixin, ListView):
    model = Credential
    template_name = 'credentials/credential_list.html'
    context_object_name = 'credentials'
    paginate_by = 10

    def get_queryset(self):
        qs = Credential.objects.filter(user=self.request.user)

        q = self.request.GET.get('q')
        sort = self.request.GET.get('sort')

        if q:
            qs = qs.filter(
                Q(site_name__icontains=q) |
                Q(username__icontains=q) |
                Q(email__icontains=q) |
                Q(site_url__icontains=q)
            )

        if sort == 'alpha':
            qs = qs.order_by('site_name')
        elif sort == 'date':
            qs = qs.order_by('-created_at')

        return qs


class CredentialCreateView(LoginRequiredMixin, CreateView):
    model = Credential
    form_class = CredentialForm
    template_name = 'credentials/credential_add.html'
    success_url = reverse_lazy('credential-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['show_password'] = True
        return kwargs

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
        context['form'] = CredentialForm()
        return context


class CredentialUpdateView(LoginRequiredMixin, UpdateView):
    model = Credential
    form_class = CredentialForm
    template_name = 'credentials/credential_edit.html'
    success_url = reverse_lazy('credential-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        if self.request.method == "GET":
            decrypted_password = decrypt_password(self.request.user, self.object.password_encrypted)
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
