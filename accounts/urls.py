from django.urls import path
from accounts.views import LoginView, RegisterUserView

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('register/', RegisterUserView.as_view(), name='register-user')
]
