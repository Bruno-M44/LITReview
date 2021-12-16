from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, DeleteView
from .forms import ReviewForm
from tickets.forms import TicketForm
from feeds.models import Ticket, Review
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy


class ReviewCreationView(LoginRequiredMixin, View):
    login_url = "index"
    redirect_field_name = "next"
    template_name = "reviews/review_creation.html"

    def get(self, request, ticket_id):
        form = ReviewForm()
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
            form = ReviewForm(request.user, request.POST)
            if form.is_valid():
                form = form.save(commit=False)
                form.user = request.user
                form.ticket = Ticket.objects.get(id=ticket_id)
                form.save()
            return redirect("/feeds/flux")

        else:
            form = ReviewForm()

        return render(request, self.template_name,
                      context={
                          "form": form})


class ReviewUpdateView(LoginRequiredMixin, View):
    login_url = "index"
    redirect_field_name = "next"
    template_name = "reviews/review_update.html"

    def get(self, request, review_id):
        try:
            review = Review.objects.get(id=review_id)
        except Review.DoesNotExist:
            raise Http404("La critique n'existe pas")
        form = ReviewForm(initial={"headline": review.headline,
                                   "rating": review.rating,
                                   "body": review.body})
        return render(request, self.template_name,
                      context={"review": review,
                               "form": form})

    def post(self, request, review_id):
        if request.method == "POST":
            form = ReviewForm(request.user, request.POST)
            if form.is_valid():
                form = form.save(commit=False)
                form.user = request.user
                ticket_id = Review.objects.get(id=review_id).ticket.id
                form.ticket = Ticket.objects.get(id=ticket_id)
                form.id = Review.objects.get(id=review_id).id
                form.time_created = Review.objects.get(id=review_id).\
                    time_created
                form.save()
            return redirect("/feeds/posts")

        else:
            form = ReviewForm()

        return render(request, self.template_name,
                      context={
                          "form": form})


class ReviewTicketCreationView(LoginRequiredMixin, View):
    login_url = "index"
    redirect_field_name = "next"
    template_name = "reviews/review_ticket_creation.html"

    def get(self, request):
        ticket_form = TicketForm()
        review_form = ReviewForm()
        return render(request, self.template_name,
                      context={"ticket_form": ticket_form,
                               "review_form": review_form})

    def post(self, request):
        if request.method == "POST":
            ticket_form = TicketForm(request.user, request.POST,
                                     request.FILES)
            # request.FILES allows to save the image

            review_form = ReviewForm(request.user, request.POST)

            if ticket_form.is_valid() and review_form.is_valid():
                ticket_form = ticket_form.save(commit=False)
                ticket_form.user = request.user

                ticket_form.save()
                review_form = review_form.save(commit=False)
                review_form.user = request.user
                review_form.ticket = ticket_form
                review_form.save()
                return redirect("/feeds/flux")

        else:
            ticket_form = TicketForm()
            review_form = ReviewForm()

        return render(request, self.template_name,
                      context={"ticket_form": ticket_form,
                               "review_form": review_form})


class ReviewDeleteView(DeleteView):
    model = Review
    success_url = reverse_lazy("posts")
    pk_url_kwarg = "review_id"
    template_name = "reviews/review_confirm_delete.html"
