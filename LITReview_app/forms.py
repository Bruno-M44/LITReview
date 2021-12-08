from django.forms import TextInput, CharField, PasswordInput, ModelForm, \
    ChoiceField, RadioSelect, Select
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model
from .models import Ticket, Review, UserFollows
from django.contrib.auth.models import User


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


class SubscriptionsForm(ModelForm):
    class Meta:
        model = UserFollows
        fields = ["followed_user"]

    def __init__(self, user="", *args, **kwargs):
        self.user = user
        users_to_exclude = [user.followed_user.username for user in
                            UserFollows.objects.filter(user=self.user)]
        users_to_exclude.append(self.user.username)
        users_to_print = User.objects.all().exclude(
            username__in=users_to_exclude)
        super().__init__(*args, **kwargs)
        users_choices = []
        for user in users_to_print:
            users_choices.append((user, user))
        users_choices = tuple(users_choices)
        self.fields["followed_user"] = ChoiceField(label="Nom d'utilisateur",
                                                   widget=Select,
                                                   choices=users_choices)
