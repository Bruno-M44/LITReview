from django.contrib import admin

from .models import Ticket, Review, UserFollows

# Register your models here.
admin.site.register([Ticket, Review, UserFollows])
