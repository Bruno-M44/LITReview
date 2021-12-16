from django.urls import path
from .views import FluxView, PostsView

urlpatterns = [
    path("flux/", FluxView.as_view(), name="flux"),
    path("posts/", PostsView.as_view(), name="posts"),
]