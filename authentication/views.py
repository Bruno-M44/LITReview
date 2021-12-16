from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .forms import UserForm, UserAuthenticationForm


class IndexView(LoginView):
    template_name = "authentication/index.html"
    authentication_form = UserAuthenticationForm


class RegistrationView(CreateView):
    model = User
    form_class = UserForm
    template_name = "authentication/user_creation.html"
    success_url = reverse_lazy("flux")


