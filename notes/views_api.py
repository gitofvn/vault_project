from rest_framework import viewsets, permissions
from drf_spectacular.utils import extend_schema_view, extend_schema

from notes.models import Note
from notes.serializers import NoteSerializer


@extend_schema_view(
    list=extend_schema(tags=['Notes']),
    retrieve=extend_schema(tags=['Notes']),
    create=extend_schema(tags=['Notes']),
    update=extend_schema(tags=['Notes']),
    partial_update=extend_schema(tags=['Notes']),
    destroy=extend_schema(tags=['Notes']),
)

class NoteViewSet(viewsets.ModelViewSet):
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)
