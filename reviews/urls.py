from django.urls import path
from .views import ReviewTicketCreationView, ReviewCreationView, \
    ReviewUpdateView, ReviewDeleteView


urlpatterns = [
    path("review_creation/<int:ticket_id>/", ReviewCreationView.as_view(),
         name="review_creation"),
    path("ticket_review_creation/", ReviewTicketCreationView.as_view(),
         name="ticket_review_creation"),
    path("review_update/<int:review_id>/", ReviewUpdateView.as_view(),
         name="review_update"),
    path("review_delete/<int:review_id>/", ReviewDeleteView.as_view(),
         name="review_delete"),
]