from django.urls import path
from rest_framework.routers import DefaultRouter

from notes.views_api import NoteViewSet
from notes.views import NotesListView, NoteCreateView, NoteUpdateView, NoteDeleteView, NoteDetailView


router = DefaultRouter()
router.register(r'notes', NoteViewSet, basename='note')


urlpatterns = [
    path('', NotesListView.as_view(), name='notes-list'),
    path('add/', NoteCreateView.as_view(), name='note-add'),
    path('<int:pk>/', NoteDetailView.as_view(), name='note-detail'),
    path('<int:pk>/edit/', NoteUpdateView.as_view(), name='note-edit'),
    path('<int:pk>/delete/', NoteDeleteView.as_view(), name='note-delete'),
]

urlpatterns += router.urls
