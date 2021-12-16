from django.urls import path
from .views import TicketCreationView, TicketUpdateView, TicketDeleteView

urlpatterns = [
    path("ticket_creation/", TicketCreationView.as_view(),
         name="ticket_creation"),
    path("ticket_update/<int:ticket_id>/", TicketUpdateView.as_view(),
         name="ticket_update"),
    path("ticket_delete/<int:ticket_id>/", TicketDeleteView.as_view(),
         name="ticket_delete"),
]
