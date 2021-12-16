from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DeleteView, UpdateView
from feeds.models import Ticket
from .forms import TicketForm
from django.urls import reverse_lazy


class TicketCreationView(LoginRequiredMixin, CreateView):
    login_url = "index"
    redirect_field_name = "next"
    model = Ticket
    form_class = TicketForm
    template_name = "tickets/ticket_creation.html"
    success_url = reverse_lazy("flux")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TicketUpdateView(UpdateView):
    model = Ticket
    form_class = TicketForm
    success_url = reverse_lazy("posts")
    pk_url_kwarg = "ticket_id"
    template_name = "tickets/ticket_update.html"


class TicketDeleteView(DeleteView):
    model = Ticket
    success_url = reverse_lazy("posts")
    pk_url_kwarg = "ticket_id"
    template_name = "tickets/ticket_confirm_delete.html"
