from django.forms import CharField, Textarea, ModelForm, ChoiceField, RadioSelect
from feeds.models import Review


class ReviewForm(ModelForm):
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
    body = CharField(label="Commentaire", widget=Textarea)

    class Meta:
        model = Review
        fields = ["headline", "rating", "body"]

    def __init__(self, user="", *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
