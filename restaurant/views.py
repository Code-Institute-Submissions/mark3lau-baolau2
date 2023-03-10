from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import generic
from django.urls import reverse_lazy, reverse
from .models import Booking
from .forms import BookingForm, UpdateForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin


# To view the user's bookings
class BookingList(LoginRequiredMixin, generic.ListView):
    model = Booking
    template_name = 'your_booking.html'
    paginate_by = 6

    def get_queryset(self):
        # Filter the queryset by the current user
        return Booking.objects.filter(user=self.request.user)


# To view the home page
class HomePage(generic.ListView):
    template_name = 'index.html'
    queryset = Booking.objects.none()


# To view the menu
class Menu(generic.ListView):
    template_name = 'menu.html'
    queryset = Booking.objects.none()


# For the user to make a booking
class MakeBooking(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'make_booking.html'
    success_url = reverse_lazy('your_booking')
    success_message = "Your booking has been made successfully."

    # Set the current user as the owner of the new booking
    def form_valid(self, form):
        form.instance.user = self.request.user  
        return super().form_valid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, 
                       'There was an error processing your booking.')
        return response


# For the user to update an existing booking
class UpdateBooking(UpdateView):
    model = Booking
    fields = ('name', 'email', 'contact_number', 'number_of_people', 
              'booking_date', 'booking_time')
    template_name = 'update_booking.html'
    success_url = reverse_lazy('your_booking')
    success_message = "Your booking has been updated successfully."

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(name=self.request.user.username)

    def get_object(self, queryset=None):
        booking_id = self.kwargs['pk']
        return Booking.objects.get(pk=booking_id) 


# For the user to delete an existing booking
class DeleteBooking(DeleteView):
    model = Booking
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('your_booking')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)
    
    def delete(self, request, *args, **kwargs):
        booking = self.get_object()
        messages.success(request, f"The booking for {booking.name} on {booking.booking_date} at {booking.booking_time} has been deleted.")
        return super().delete(request, *args, **kwargs)