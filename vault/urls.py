from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from notes.views_api import NoteViewSet
from credentials.views_api import CredentialViewSet


router = DefaultRouter()
router.register(r'notes', NoteViewSet, basename='api-notes')
router.register(r'credentials', CredentialViewSet, basename='api-credentials')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('notes/', include('notes.urls')),        
    path('credentials/', include('credentials.urls')),

    path('api/', include(router.urls)),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]