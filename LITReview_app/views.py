from django.views.generic import CreateView, TemplateView, View, ListView, \
    DetailView, DeleteView, UpdateView
from django.contrib.auth.models import User
from django.contrib.auth import logout
from .models import Ticket, Review, UserFollows
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.shortcuts import render, redirect
from itertools import chain
from django.db.models import CharField, Value
from django.http import Http404

from .forms import UserForm, UserAuthenticationForm, TicketCreationForm, \
    ReviewCreationForm, SubscriptionsForm


class IndexView(LoginView):
    template_name = "LITReview_app/index.html"
    authentication_form = UserAuthenticationForm


class RegistrationView(CreateView):
    model = User
    form_class = UserForm
    template_name = "LITReview_app/user_form.html"
    success_url = reverse_lazy("flux")


class FluxView(LoginRequiredMixin, View):
    login_url = "index"
    redirect_field_name = "next"
    template_name = "LITReview_app/flux.html"

    def get(self, request):
        # reviews = get_users_viewable_reviews(request.user)
        # returns queryset of reviews
        reviews = Review.objects.order_by("-time_created")
        reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

        # tickets = get_users_viewable_tickets(request.user)
        # returns queryset of tickets
        tickets = Ticket.objects.order_by("-time_created")
        tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

        # combine and sort the two types of posts
        posts = sorted(
            chain(reviews, tickets),
            key=lambda post: post.time_created,
            reverse=True
        )
        return render(request, self.template_name,
                      context={"posts": posts,
                               "user_connected": self.request.user})


class TicketCreationView(LoginRequiredMixin, CreateView):
    login_url = "index"
    redirect_field_name = "next"
    model = Ticket
    form_class = TicketCreationForm
    template_name = "LITReview_app/ticket_creation.html"
    success_url = reverse_lazy("flux")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TicketUpdateView(UpdateView):
    model = Ticket
    form_class = TicketCreationForm
    success_url = reverse_lazy("posts")
    pk_url_kwarg = "ticket_id"
    template_name = "LITReview_app/ticket_update.html"


class ReviewCreationView(LoginRequiredMixin, View):
    login_url = "index"
    redirect_field_name = "next"
    template_name = "LITReview_app/review_creation.html"

    def get(self, request, ticket_id):
        form = ReviewCreationForm()
        try:
            ticket = Ticket.objects.get(id=ticket_id)
        except Ticket.DoesNotExist:
            raise Http404("Le ticket n'existe pas")
        return render(request, self.template_name,
                      context={
                          "form": form,
                          "ticket": ticket})

    def post(self, request, ticket_id):
        if request.method == "POST":
            form = ReviewCreationForm(request.user, request.POST)
            if form.is_valid():
                form = form.save(commit=False)
                form.user = request.user
                form.ticket = Ticket.objects.get(id=ticket_id)
                form.save()
            return redirect("/LITReview_app/flux")

        else:
            form = ReviewCreationForm()

        return render(request, self.template_name,
                      context={
                          "form": form})


class ReviewUpdateView(LoginRequiredMixin, View):
    login_url = "index"
    redirect_field_name = "next"
    template_name = "LITReview_app/review_update.html"

    def get(self, request, review_id):
        try:
            review = Review.objects.get(id=review_id)
        except Review.DoesNotExist:
            raise Http404("La critique n'existe pas")
        form = ReviewCreationForm(initial={"headline": review.headline,
                                           "rating": review.rating,
                                           "body": review.body})
        return render(request, self.template_name,
                      context={"review": review,
                               "form": form})

    def post(self, request, review_id):
        if request.method == "POST":
            form = ReviewCreationForm(request.user, request.POST)
            if form.is_valid():
                form = form.save(commit=False)
                form.user = request.user
                ticket_id = Review.objects.get(id=review_id).ticket.id
                form.ticket = Ticket.objects.get(id=ticket_id)
                form.save()
            return redirect("/LITReview_app/posts")

        else:
            form = ReviewCreationForm()

        return render(request, self.template_name,
                      context={
                          "form": form})


class ReviewTicketCreationView(LoginRequiredMixin, View):
    login_url = "index"
    redirect_field_name = "next"
    template_name = "LITReview_app/review_ticket_creation.html"

    def get(self, request):
        ticket_form = TicketCreationForm()
        review_form = ReviewCreationForm()
        return render(request, self.template_name,
                      context={"ticket_form": ticket_form,
                               "review_form": review_form})

    def post(self, request):
        if request.method == "POST":
            ticket_form = TicketCreationForm(request.user, request.POST,
                                             request.FILES)
            # request.FILES allows to save the image

            review_form = ReviewCreationForm(request.user, request.POST)

            if ticket_form.is_valid() and review_form.is_valid():
                ticket_form = ticket_form.save(commit=False)
                ticket_form.user = request.user

                ticket_form.save()
                review_form = review_form.save(commit=False)
                review_form.user = request.user
                review_form.ticket = ticket_form
                review_form.save()
                return redirect("/LITReview_app/flux")

        else:
            ticket_form = TicketCreationForm()
            review_form = ReviewCreationForm()

        return render(request, self.template_name,
                      context={"ticket_form": ticket_form,
                               "review_form": review_form})


class SubscriptionsView(LoginRequiredMixin, View):
    login_url = "index"
    redirect_field_name = "next"
    template_name = "LITReview_app/subscriptions.html"

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


class PostsView(LoginRequiredMixin, View):
    login_url = "index"
    redirect_field_name = "next"
    template_name = "LITReview_app/posts.html"

    def get(self, request):
        # reviews = get_users_viewable_reviews(request.user)
        # returns queryset of reviews
        reviews = Review.objects.order_by("-time_created").\
            filter(user=request.user)
        reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

        # tickets = get_users_viewable_tickets(request.user)
        # returns queryset of tickets
        tickets = Ticket.objects.order_by("-time_created").\
            filter(user=request.user)
        tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

        # combine and sort the two types of posts
        posts = sorted(
            chain(reviews, tickets),
            key=lambda post: post.time_created,
            reverse=True
        )
        return render(request, self.template_name,
                      context={"posts": posts,
                               "user_connected": self.request.user})


class ReviewDeleteView(DeleteView):
    model = Review
    success_url = reverse_lazy("posts")
    pk_url_kwarg = "review_id"


class TicketDeleteView(DeleteView):
    model = Ticket
    success_url = reverse_lazy("posts")
    pk_url_kwarg = "ticket_id"




