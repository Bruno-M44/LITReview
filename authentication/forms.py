from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms import TextInput, CharField, PasswordInput
from django.contrib.auth import get_user_model


class UserAuthenticationForm(AuthenticationForm):
    username = CharField(widget=TextInput(attrs={
                "placeholder": "Nom d'utilisateur", "class": "width_100"}),
        label="")
    password = CharField(widget=PasswordInput(attrs={
                "placeholder": "Mot de passe", "class": "width_100"}),
        label="")


class UserForm(UserCreationForm):
    username = CharField(widget=TextInput(attrs={
        "placeholder": "Nom d'utilisateur", "class": "width_100"}), label="")
    password1 = CharField(widget=PasswordInput(attrs={
        "placeholder": "Mot de passe", "class": "width_100"}), label="")
    password2 = CharField(widget=PasswordInput(attrs={
        "placeholder": "Confirmer mot de passe", "class": "width_100"}),
        label="")

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ["username", "password1", "password2"]