from django.urls import path

from credentials.views_api import CredentialViewSet
from credentials.views import CredentialListView, CredentialCreateView, CredentialDetailView, CredentialUpdateView, CredentialDeleteView


urlpatterns = [
    path('', CredentialListView.as_view(), name='credential-list'),
    path('add/', CredentialCreateView.as_view(), name='credential-add'),
    path('<int:pk>/', CredentialDetailView.as_view(), name='credential-detail'),
    path('<int:pk>/edit/', CredentialUpdateView.as_view(), name='credential-edit'),
    path('<int:pk>/delete/', CredentialDeleteView.as_view(), name='credential-delete'),
]

