from datetime import datetime

from django.contrib import messages
from django.contrib.auth import mixins as auth_mixins
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic as views

from booking.bookings.forms import BookingForm
from booking.bookings.models import UserBooking
from booking.common.mixins import GetContextMixin
from booking.rooms.models import Room


class CreateBookingView(auth_mixins.LoginRequiredMixin, GetContextMixin, views.CreateView):
    queryset = UserBooking.objects.select_related('room', 'user').all()
    template_name = 'bookings/create_booking.html'
    success_url = reverse_lazy('index_user')
    form_class = BookingForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['room'] = self.request.GET.get('room_pk')

        # Extract check-in and check-out dates from the URL parameters
        check_in = self.request.GET.get('check_in')
        check_out = self.request.GET.get('check_out')

        # Format the dates to exclude time components if they are provided
        if check_in:
            kwargs['check_in'] = datetime.strptime(check_in, '%Y-%m-%d').date()
        if check_out:
            kwargs['check_out'] = datetime.strptime(check_out, '%Y-%m-%d').date()

        kwargs['adults'] = self.request.GET.get('adults')

        if 'check_in' in kwargs and 'check_out' in kwargs and 'room' in kwargs:
            room_obj = Room.objects.get(pk=kwargs['room'])
            price_per_night = room_obj.price_per_night
            delta = (kwargs['check_out'] - kwargs['check_in']).days
            kwargs['cost_of_stay'] = delta * price_per_night

        return kwargs

    def form_valid(self, form):
        # Check if the user has enough money
        if form.is_valid():
            if self.request.user.profile.money >= form.cleaned_data['cost_of_stay']:
                # Withdraw money from the user's profile
                cost_of_stay = form.cleaned_data['cost_of_stay']
                self.request.user.profile.money -= cost_of_stay
                self.request.user.profile.save()

                # Get the room owner and increase their money
                room_owner = form.cleaned_data['room'].hotel.user
                room_owner.profile.money += cost_of_stay
                room_owner.profile.save()

                # Proceed with the booking
                response = super().form_valid(form)
                return response
            else:
                # User doesn't have enough money, show a message and redirect back to the form
                messages.error(self.request, "Not Enough Money you need to deposit")
                return redirect(reverse('create_booking'))
        else:
            return self.form_invalid(form)


class BookingListView(auth_mixins.LoginRequiredMixin, views.ListView):
    model = UserBooking
    template_name = 'bookings/booking_list.html'

    def get_queryset(self):
        return UserBooking.objects.filter(user_id=self.request.user.pk)

