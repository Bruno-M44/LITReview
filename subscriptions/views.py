from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from .forms import SubscriptionsForm
from feeds.models import UserFollows
from django.contrib.auth.models import User
from django.shortcuts import render


class SubscriptionsView(LoginRequiredMixin, View):
    login_url = "index"
    redirect_field_name = "next"
    template_name = "subscriptions/subscriptions.html"

    def get(self, request):
        form = SubscriptionsForm(user=request.user)
        try:
            subscriptions = UserFollows.objects.filter(user=request.user)
        except UserFollows.DoesNotExist:
            subscriptions = ""
        try:
            subscribers = UserFollows.objects.filter(
                followed_user=request.user)
        except UserFollows.DoesNotExist:
            subscribers = ""
        return render(request, self.template_name,
                      context={"form": form,
                               "subscriptions": subscriptions,
                               "subscribers": subscribers})

    def post(self, request):
        if request.method == "POST":
            got_followed_user = User.objects.get(
                username=request.POST.get("followed_user", ""))
            if "add_user_sub" in request.POST:
                UserFollows(user=request.user,
                            followed_user=got_followed_user).save()
                return self.get(request)

            elif "delete_user_sub" in request.POST:
                UserFollows.objects.filter(followed_user=got_followed_user,
                                           user=request.user).delete()
                return self.get(request)
