import json
import datetime

from django.views     import View
from django.shortcuts import get_object_or_404
from django.http      import JsonResponse
from django.db.models import Q

from .models          import Booking, BookedRoom
from user.models      import User
from hotel.models     import Room

class BookingView(View):
    def get(self, request):
        room_id           = request.GET.get('room_id')
        room              = get_object_or_404(Room, id=room_id)
        year1,month1,day1 = request.GET.get('start').split('-')
        year2,month2,day2 = request.GET.get('end').split('-')
        bookings          = Booking.objects.filter(Q(date_from__month=month1) | Q(date_from__month=month2), room_id=room_id)
        date_start        = datetime.date(int(year1), int(month1), int(day1))
        date_end          = datetime.date(int(year2), int(month2), int(day2))
        delta             = datetime.timedelta(days=1)

        date_list = []
        while date_start<=date_end:
            date_list.append(date_start)
            date_start += delta
            
        prices={}
        PEAK_MONTH = [1,2,5,6,7,8,12]
        for date in date_list:
            if date.month in PEAK_MONTH:
                prices[f"{str(date)}"]=room.price_peak
            else:
                if date.weekday()<6:
                    prices[f"{str(date)}"]=room.price_weekday
                else:
                    prices[f"{str(date)}"]=room.price_weekend

        booking=[{'stay_at_least' : room.stay_at_least,
            'user':{
                'name' : get_object_or_404(User, id=request.user).name,
                'email': get_object_or_404(User, id=request.user).email
            },
            'booked_dates': [{'date_from':booking.date_from,'date_to':booking.date_to} for booking in bookings],
            'prices'      : prices
        }]
        return JsonResponse({'booking_info':booking}, status=200)
