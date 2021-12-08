from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import IndexView, RegistrationView, FluxView, TicketCreationView, \
    ReviewTicketCreationView, ReviewCreationView, SubscriptionsView, \
    PostsView, ReviewUpdateView, ReviewDeleteView, TicketUpdateView, \
    TicketDeleteView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("registration/", RegistrationView.as_view(), name="registration"),
    path("flux/", FluxView.as_view(), name="flux"),
    path("ticket_creation/", TicketCreationView.as_view(),
         name="ticket_creation"),
    path("ticket_update/<int:ticket_id>/", TicketUpdateView.as_view(),
         name="ticket_update"),
    path("review_creation/<int:ticket_id>/", ReviewCreationView.as_view(),
         name="review_creation"),
    path("ticket_review_creation/", ReviewTicketCreationView.as_view(),
         name="ticket_review_creation"),
    path("review_update/<int:review_id>/", ReviewUpdateView.as_view(),
         name="review_update"),
    path("review_delete/<int:review_id>/", ReviewDeleteView.as_view(),
         name="review_delete"),
    path("ticket_delete/<int:ticket_id>/", TicketDeleteView.as_view(),
         name="ticket_delete"),
    path("subscriptions/", SubscriptionsView.as_view(), name="subscriptions"),
    path("posts/", PostsView.as_view(), name="posts"),
    path("logout/", LogoutView.as_view(), name="logout"),
] # + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
