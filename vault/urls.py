from django.contrib.auth import views as auth_views
from django.contrib import admin

from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('notes/', include('notes.urls')),

]
