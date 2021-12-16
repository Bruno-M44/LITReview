from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", include("authentication.urls")),
    path("feeds/", include("feeds.urls")),
    path("subscriptions/", include("subscriptions.urls")),
    path("reviews/", include("reviews.urls")),
    path("tickets/", include("tickets.urls")),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
