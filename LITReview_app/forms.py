from django.forms import TextInput, CharField, PasswordInput, ModelForm, \
    ChoiceField, RadioSelect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model
from .models import Ticket, Review


class UserForm(UserCreationForm):
    username = CharField(widget=TextInput(attrs={
        "placeholder": "Nom d'utilisateur"}), label="")
    password1 = CharField(widget=PasswordInput(attrs={
        "placeholder": "Mot de passe"}), label="")
    password2 = CharField(widget=PasswordInput(attrs={
        "placeholder": "Confirmer mot de passe"}), label="")

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ["username", "password1", "password2"]


class UserAuthenticationForm(AuthenticationForm):
    username = CharField(widget=TextInput(attrs={
                "placeholder": "Nom d'utilisateur"}), label="")
    password = CharField(widget=PasswordInput(attrs={
                "placeholder": "Mot de passe"}), label="")


class TicketCreationForm(ModelForm):
    title = CharField(label="Titre")

    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]

    def __init__(self, user="", *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)


class ReviewCreationForm(ModelForm):
    NOTES = (
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    )
    headline = CharField(label="Titre")
    rating = ChoiceField(label="Note", widget=RadioSelect, choices=NOTES)
    body = CharField(label="Commentaire")

    class Meta:
        model = Review
        fields = ["headline", "rating", "body"]

    def __init__(self, user="", *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)


