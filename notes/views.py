from django.db import models

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from .models import Note


class NotesListView(LoginRequiredMixin, ListView):
    model = Note
    template_name = 'notes/notes_list.html'
    context_object_name = 'notes'

    def get_queryset(self):
        queryset = Note.objects.filter(user=self.request.user)
        query = self.request.GET.get('q')
        sort = self.request.GET.get('sort')

        # Filter by search
        if query:
            queryset = queryset.filter(
                models.Q(title__icontains=query) | models.Q(content__icontains=query)
            )

        # Sorting logic
        if sort == 'alpha':
            queryset = queryset.order_by('title')  # Alphabetical
        elif sort == 'date':
            queryset = queryset.order_by('-created_at')  # Most recent first

        return queryset

class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    fields = ['title', 'content']
    template_name = 'notes/note_form.html'
    success_url = reverse_lazy('notes-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class NoteUpdateView(LoginRequiredMixin, UpdateView):
    model = Note
    fields = ['title', 'content']
    template_name = 'notes/note_form.html'
    success_url = reverse_lazy('notes-list')

class NoteDeleteView(LoginRequiredMixin, DeleteView):
    model = Note
    template_name = 'notes/note_confirm_delete.html'
    success_url = reverse_lazy('notes-list')


class NoteDetailView(LoginRequiredMixin, DetailView):
    model = Note
    template_name = 'notes/note_detail.html'
    context_object_name = 'note'

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)
