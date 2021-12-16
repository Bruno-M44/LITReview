from django.forms import ModelForm, ChoiceField, Select
from feeds.models import UserFollows
from django.contrib.auth.models import User


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
