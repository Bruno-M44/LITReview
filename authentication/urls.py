from django.urls import path
from .views import IndexView, RegistrationView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("registration/", RegistrationView.as_view(), name="registration"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
