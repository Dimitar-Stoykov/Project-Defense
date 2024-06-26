from django import forms
from django.contrib.auth import get_user_model

from booking.hotels.models import Hotel
from booking.rooms.mixins import ReadOnlyMixin
from booking.rooms.models import Room, RoomPictures


UserModel = get_user_model()


class RoomBaseForm(forms.ModelForm):
    hotel = forms.ModelChoiceField(queryset=Hotel.objects.none(), widget=forms.Select(
        attrs={'class': 'form-control', 'placeholder': 'Select a hotel'}))

    class Meta:
        model = Room
        fields = ('room_number', 'price_per_night', 'capacity', 'hotel',)
        widgets = {
            'room_number': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter room number'}),
            'price_per_night': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter price per night'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter capacity'}),
        }


class RoomCreateForm(RoomBaseForm):
    def __init__(self, *args, user=None, **kwargs):
        super(RoomCreateForm, self).__init__(*args, **kwargs)
        self.fields['hotel'].queryset = Hotel.objects.filter(user=user)

    def clean(self):
        cleaned_data = super().clean()
        room_number = cleaned_data.get("room_number")
        hotel = cleaned_data.get("hotel")

        if Room.objects.filter(hotel=hotel, room_number=room_number).exists():
            self.add_error(None, 'A room with this number already exists for this hotel.')

        return cleaned_data


class RoomUpdateForm(ReadOnlyMixin, RoomBaseForm):
    readonly_fields = ('room_number', 'hotel',)

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        super(RoomUpdateForm, self).__init__(*args, **kwargs)
        if instance:
            self.fields['hotel'].queryset = Hotel.objects.filter(pk=instance.hotel.pk)

    def clean(self):
        cleaned_data = super().clean()
        room_number = cleaned_data.get("room_number")
        hotel = cleaned_data.get("hotel")

        if self.instance and Room.objects.filter(hotel=hotel, room_number=room_number).exclude(pk=self.instance.pk).exists():
            self.add_error(None, 'A room with this number already exists for this hotel.')

        return cleaned_data


class ChooseHotelForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['hotel'].queryset = Hotel.objects.filter(user=user)

    hotel = forms.ModelChoiceField(queryset=Hotel.objects.none(), label='Select Hotel', widget=forms.Select(attrs={'class': 'form-control'}))


class RoomPictureUploadForm(forms.ModelForm):
    image = forms.URLField(label='Image', widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = RoomPictures
        fields = ('image', 'room',)

    def __init__(self, *args, hotel_id=None, **kwargs):
        super().__init__(*args, **kwargs)

        if hotel_id:
            rooms = Room.objects.filter(hotel_id=hotel_id)
            self.fields['room'].queryset = rooms
            self.fields['room'].widget.attrs.update({'class': 'form-control'})

