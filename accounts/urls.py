from django.urls import path
from django.contrib.auth.views import LogoutView

from accounts.views import LoginView, RegisterUserView, DashboardView


urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('register/', RegisterUserView.as_view(), name='register-user'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

]
