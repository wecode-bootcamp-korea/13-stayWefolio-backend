import json

from django.views     import View
from django.shortcuts import get_object_or_404
from django.http      import JsonResponse

from .models          import Booking, BookedRoom
from user.models      import User
from hotel.models     import Room

class BookingView(View):
    def get(self, request):
              room_id    = request.GET.get('room_id')
              room       = Room.objects.get(id=room_id)
       year1,month1,day1 = request.GET.get('start').split('-')
       year2,month2,day2 = request.GET.get('end').split('-')
              date_start = datetime.date(int(year1), int(month1), int(day1))
              date_end   = datetime.date(int(year2), int(month2), int(day2))
              delta      = datetime.timedelta(days=1)

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

        bookings      = Booking.objects.filter(room_id=room_id)
        booked_dates  = [{'date_from':booking.date_from,'date_to':booking.date_to} for booking in bookings]
        name          = User.objects.get(id=request.user).name
        email         = User.objects.get(id=request.user).email
        stay_at_least = Room.objects.get(id=room_id).stay_at_least

        booking=[{'stay_at_least':stay_at_least,
            'user':{
                'name':name,
                'email':email
            },
            'booked_dates':booked_dates,
            'prices':prices
        }]
        return JsonResponse({'booking_info':booking}, status=200)
