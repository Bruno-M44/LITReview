from django.urls import path
from .views import SubscriptionsView


urlpatterns = [
    path("", SubscriptionsView.as_view(), name="subscriptions"),
]