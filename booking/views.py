import json
import datetime

from django.views           import View
from django.shortcuts       import get_object_or_404
from django.http            import JsonResponse
from django.db.models       import Q

from .models                import Booking, BookedRoom
from user.models            import User
from hotel.models           import Room
from user.utils             import authorize_decorator

class BookingView(View):
    @authorize_decorator
    def get(self, request, room_id):
        room              = get_object_or_404(Room, id=room_id)
        year1,month1,day1 = request.GET.get('start').split('-')
        year2,month2,day2 = request.GET.get('end').split('-')
        bookings          = Booking.objects.filter(
                                                    Q(date_from__month=month1) | 
                                                    Q(date_from__month=month2), 
                                                    room_id=room_id
                                                )
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
                prices[f"{str(date)}"]=int(room.price_peak)
            else:
                if date.weekday()<6:
                    prices[f"{str(date)}"]=int(room.price_weekday)
                else:
                    prices[f"{str(date)}"]=int(room.price_weekend)

        booking=[{'stay_at_least' : room.stay_at_least,
            'room_id'   : room.id,
            'room_image': room.roomimage_set.first().image_url,
            'user':{
                'name' : get_object_or_404(User, id=request.user).name,
                'email': get_object_or_404(User, id=request.user).email
                },
            'booked_dates': [
                    {
                        'date_from' : booking.date_from,
                        'date_to'   : booking.date_to
                    } for booking in bookings
                ],
            'total'       : sum(prices.values()),
            'prices'      : prices
        }]
        return JsonResponse({'booking_info':booking}, status=200)
    
    @authorize_decorator
    def post(self, request, room_id):
        try:
            data    = json.loads(request.body)

            booking = Booking.objects.create(
                user_id                       = request.user,
                room_id                       = room_id,
                date_from                     = data['start'],
                date_to                       = data['end'],
                name                          = data['name'],
                phone_number                  = data['phone_number'],
                email                         = data['email'],
                adult                         = data['adult'],
                child                         = data['child'],
                infant                        = data['infant'],
                option_breakfast              = data['breakfast'],
                option_pickup                 = data['pickup'],
                demand                        = data['demand'],
                price                         = data['price'],
                discount                      = data['discount'],
                total                         = data['total'],
                payment_id                    = data['payment_id'],
                terms_information_collection  = data['term1'],
                terms_information_third_party = data['term2'],
                terms_information_refund      = data['term3'],
                terms_marketing               = data['term4']
            )

            BookedRoom(
                booking_id = booking.id,
                room_id    = room_id
            ).save()

            return JsonResponse({'message':"SUCCESS😎",'booking_id':booking.id}, status=200)

        except KeyError as e:
            return JsonResponse({'message':f"{e} IS MISSING"}, status=400)

class BookingConfirmView(View):
    @authorize_decorator
    def get(self, request):
        try:
            booking_id=request.GET['booking_id']
            booking=Booking.objects.select_related('user','room','room__hotel').get(id=booking_id)
            if request.user == booking.user.id:
                booking_info=[{
                        'name'       : booking.user.name,
                        'hotel_name' : booking.room.hotel.name,
                        'hotel_image': booking.room.hotel.thumbnail_url,
                        'room_name'  : booking.room.name,
                        'adult'      : booking.adult,
                        'child'      : booking.child,
                        'infant'     : booking.infant,
                        'date_from'  : booking.date_from,
                        'date_to'    : booking.date_to
                    }]
                return JsonResponse({'booking_info':booking_info}, status=200)
            return JsonResponse({'message': "INVALID USER"}, status=400)

        except KeyError as e:
            return JsonResponse({'message':f"{e} IS MISSING"}, status=400)
        
