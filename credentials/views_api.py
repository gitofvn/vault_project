from rest_framework import viewsets, permissions
from drf_spectacular.utils import extend_schema, extend_schema_view

from credentials.models import Credential
from credentials.serializers import CredentialSerializer

@extend_schema_view(
    list=extend_schema(tags=['Credentials']),
    retrieve=extend_schema(tags=['Credentials']),
    create=extend_schema(tags=['Credentials']),
    update=extend_schema(tags=['Credentials']),
    partial_update=extend_schema(tags=['Credentials']),
    destroy=extend_schema(tags=['Credentials']),
)


class CredentialViewSet(viewsets.ModelViewSet):
    serializer_class = CredentialSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Credential.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
