from django.urls import path

from .views import IndexView, RegistrationView, FluxView, TicketCreationView, \
    ReviewTicketCreationView, ReviewCreationView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("registration/", RegistrationView.as_view(), name="registration"),
    path("flux/", FluxView.as_view(), name="flux"),
    path("ticket_creation/", TicketCreationView.as_view(),
         name="ticket_creation"),
    path("review_creation/", ReviewCreationView.as_view(),
         name="review_creation"),
    path("ticket_review_creation/", ReviewTicketCreationView.as_view(),
         name="ticket_review_creation")
]
