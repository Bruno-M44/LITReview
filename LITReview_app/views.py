from django.views.generic import CreateView, TemplateView, View, ListView
from django.contrib.auth.models import User
from .models import Ticket, Review
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.shortcuts import render, redirect
from itertools import chain
from django.db.models import CharField, Value

from .forms import UserForm, UserAuthenticationForm, TicketCreationForm, \
    ReviewCreationForm


class IndexView(LoginView):
    template_name = "LITReview_app/index.html"
    authentication_form = UserAuthenticationForm


class RegistrationView(CreateView):
    model = User
    form_class = UserForm
    template_name = "LITReview_app/user_form.html"
    success_url = reverse_lazy("flux")


class FluxView(View):
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
    model = Ticket
    form_class = TicketCreationForm
    template_name = "LITReview_app/ticket_creation.html"
    success_url = reverse_lazy("flux")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ReviewCreationView(View):
    template_name = "LITReview_app/review_creation.html"

    def get(self, request):
        review_form = ReviewCreationForm()
        print(self.request.META)
        return render(request, self.template_name,
                      context={"review_form": review_form})


class ReviewTicketCreationView(View):
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
