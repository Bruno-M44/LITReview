from django.forms import CharField, ModelForm
from feeds.models import Ticket


class TicketForm(ModelForm):
    title = CharField(label="Titre")

    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]

    def __init__(self, user="", *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
