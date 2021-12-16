from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from .models import Ticket, Review, UserFollows
from django.db.models import CharField, Value
from itertools import chain
from django.shortcuts import render


class FluxView(LoginRequiredMixin, View):
    login_url = "index"
    redirect_field_name = "next"
    template_name = "feeds/flux.html"

    def get(self, request):
        followed_user = UserFollows.objects.filter(user=request.user)
        followed_user = [user.followed_user for user in followed_user]
        followed_user.append(request.user)

        tickets_with_review = [review.ticket.pk for review in
                               Review.objects.all()]

        reviews = Review.objects.order_by("-time_created"). \
            filter(user__in=followed_user)
        reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

        tickets = Ticket.objects.order_by("-time_created"). \
            filter(user__in=followed_user).exclude(pk__in=tickets_with_review)
        tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

        # combine and sort the two types of posts
        posts = sorted(
            chain(reviews, tickets),
            key=lambda post: post.time_created,
            reverse=True
        )
        return render(request, self.template_name,
                      context={"posts": posts,
                               "user_connected": self.request.user,
                               "range": range(5)})


class PostsView(LoginRequiredMixin, View):
    login_url = "index"
    redirect_field_name = "next"
    template_name = "feeds/posts.html"

    def get(self, request):
        tickets_with_review = [review.ticket.pk for review in
                               Review.objects.all()]

        reviews = Review.objects.order_by("-time_created"). \
            filter(user=request.user)
        reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

        tickets = Ticket.objects.order_by("-time_created"). \
            filter(user=request.user).exclude(pk__in=tickets_with_review)
        tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

        # combine and sort the two types of posts
        posts = sorted(
            chain(reviews, tickets),
            key=lambda post: post.time_created,
            reverse=True
        )
        return render(request, self.template_name,
                      context={"posts": posts,
                               "user_connected": self.request.user,
                               "range": range(5)})
