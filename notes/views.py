from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from notes.forms import NoteForm
from notes.models import Note
from utils.encryption import encrypt_password, decrypt_password


class NotesListView(LoginRequiredMixin, ListView):
    model = Note
    template_name = 'notes/notes_list.html'
    context_object_name = 'notes'
    paginate_by = 10

    def get_queryset(self):
        queryset = Note.objects.filter(user=self.request.user)
        query = self.request.GET.get('q')
        sort = self.request.GET.get('sort')

        if query:
            queryset = queryset.filter(title__icontains=query)

        if sort == 'alpha':
            queryset = queryset.order_by('title')
        elif sort == 'date':
            queryset = queryset.order_by('-created_at')

        return queryset


class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    form_class = NoteForm
    template_name = 'notes/note_add.html'
    success_url = reverse_lazy('notes-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.content = encrypt_password(self.request.user, form.cleaned_data['content'])
        return super().form_valid(form)


class NoteUpdateView(LoginRequiredMixin, UpdateView):
    model = Note
    form_class = NoteForm
    template_name = 'notes/note_edit.html'
    success_url = reverse_lazy('notes-list')

    def get_initial(self):
        initial = super().get_initial()
        initial['content'] = decrypt_password(self.request.user, self.object.content)
        return initial

    def form_valid(self, form):
        form.instance.content = encrypt_password(self.request.user, form.cleaned_data['content'])
        return super().form_valid(form)


class NoteDeleteView(LoginRequiredMixin, DeleteView):
    model = Note
    template_name = 'notes/note_confirm_delete.html'
    success_url = reverse_lazy('notes-list')


class NoteDetailView(LoginRequiredMixin, DetailView):
    model = Note
    template_name = 'notes/note_detail.html'
    context_object_name = 'note'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['note'].content = decrypt_password(self.request.user, context['note'].content)
        return context

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)
