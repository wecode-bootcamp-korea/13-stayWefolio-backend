import json

from django.views     import View
from django.shortcuts import get_object_or_404
from django.http      import JsonResponse
from django.db.models import Min, Max

from .models          import Hotel, Room, Category, Location, PriceRange

class MainBannerView(View):
    def get(self, request):
        BANNERS = request.GET.get('banners')
        if BANNERS:
            hotels  = Hotel.objects.all()[:int(BANNERS)]
        else:
            hotels  = Hotel.objects.all()
        banners = [{
            'hotel_id'     : hotel.id,
            'name'         : hotel.name,
            'introduction' : hotel.introduction,
            'thumbnail_url': hotel.thumbnail_url,
        } for hotel in hotels]

        return JsonResponse({'data': banners}, status=200)

class MagazineView(View):
    def get(self, request):
        MAGAZINE  = 2
        hotels    = Hotel.objects.select_related('category','location').order_by('id')[:MAGAZINE]
        magazines = [{
            'name'             : hotel.name,
            'category'         : hotel.category.name,
            'location'         : hotel.location.name,
            'description_title': hotel.description_title,
            'description_first': hotel.description_first,
            'thumbnail_url'    : hotel.thumbnail_url,
        } for hotel in hotels]
        return JsonResponse({'data': magazines}, status=200)

class PicksView(View):
    def get(self, request):
        filter_set={}
        if request.GET.get('category'):
            filter_set['category__name'] = request.GET['category'].strip("'")
        if request.GET.get('location'):
            filter_set['location__name__contains'] = request.GET['location'].strip("'")
        
        hotels=Hotel.objects.select_related('category','location').prefetch_related('room_set','tags').filter(**filter_set).order_by('id')
        
        if request.GET.get('price'):
            price=request.GET['price'].strip("'").split('~')
            if price[0] == '':
                min_price = 0
                max_price = int(price[1].replace(",","").strip('원'))
            elif price[1] == '':
                min_price = int(price[0].replace(",","").strip('원'))
                max_price = int(1e8)
            else:
                min_price = int(price[0].replace(",",""))
                max_price = int(price[1].replace(",","").strip('원'))
            hotel_price_range=[hotel.id for hotel in hotels if min_price<= hotel.room_set.aggregate(p=Min('price'))['p']<max_price]

            hotels=hotels.filter(id__in=hotel_price_range)

        offset = int(request.GET.get('offset'))
        LIMIT  = int(request.GET.get('limit'))

        if offset >= len(hotels):
            return JsonResponse({'message':'PAGE NOT FOUND😰😰'}, status=404)
        elif offset+LIMIT>len(hotels):
            hotels = hotels[offset:]
        else:
            hotels = hotels[offset:offset+LIMIT]

        locations={}
        picks=[{'filters':[
            {'options': ['타입전체']+[category.name for category in Category.objects.all()]},
            {'options': ['지역전체']+[locations.setdefault(location.name.split('/')[0],location.name.split('/')[0]) for location in Location.objects.all() if location.name.split('/')[0] not in locations]},
            {'options': ['금액전체']+[price.name for price in PriceRange.objects.all()]}
        ]},{'picks':
        [{
            'id'           : hotel.id,
            'name'         : hotel.name,
            'english_name' : hotel.english_name,
            'introduction' : hotel.introduction,
            'thumbnail_url': hotel.thumbnail_url,
            'location'     : hotel.location.name,
            'category'     : hotel.category.name,
            'min_price'    : int(hotel.room_set.aggregate(min_p=Min('price_weekday'))['min_p']),
            'max_price'    : int(hotel.room_set.aggregate(max_p=Max('price_peak'))['max_p']),
            'tags'         : [tag.name for tag in hotel.tags.all()]
            }
        for hotel in hotels]}]
            
        return JsonResponse({'hotels': picks}, status=200)

class PicksDetailView(View):
    def get(self, request, hotel_id):
        hotel=Hotel.objects.select_related('category','location').prefetch_related(
                                                                'room_set',
                                                                'hotelimage_set',
                                                                'tags'
                                                                ).get(id=hotel_id)
        picks_detail=[{
            'id'                : hotel.id,
            'name'              : hotel.name,
            'english_name'      : hotel.english_name,
            'address'           : hotel.address,
            'introduction'      : hotel.introduction,
            'image_url'         : list(hotel.hotelimage_set.values_list('image_url', flat=True)),
            'category'          : hotel.category.name,
            'min_people'        : hotel.min_people,
            'max_people'        : hotel.max_people,
            'room_count'        : hotel.room_count,
            'min_price'         : int(hotel.room_set.aggregate(min_p=Min('price_weekday'))['min_p']),
            'max_price'         : int(hotel.room_set.aggregate(max_p=Max('price_peak'))['max_p']),
            'checkin_time'      : hotel.checkin_time,
            'checkout_time'     : hotel.checkout_time,
            'location'          : hotel.location.name,
            'tags'              : list(hotel.tags.values_list('name', flat=True)),
            'email'             : hotel.email,
            'phone_number'      : hotel.phone_number,
            'description_title' : hotel.description_title,
            'description_first' : hotel.description_first,
            'description_second': hotel.description_second,
            'description_third' : hotel.description_third,
            'longitude'         : hotel.longitude,
            'latitude'          : hotel.latitude
        }]

        return JsonResponse({'picks_detail':picks_detail}, status=200)

class DetailPageView(View):
    def get(self, request,hotel_id):
        rooms=Room.objects.select_related('hotel').prefetch_related(
                                                                    'roomimage_set',
                                                                    'bed_set',
                                                                    'facilities',
                                                                    'hotel__tags',
                                                                    'hotel__services'
                                                                    ).filter(hotel_id=hotel_id).order_by('id')
        
        detail=[{'common_info':{
              'hotel_image_url'   : rooms.first().hotel.thumbnail_url,
              'room_count'        : rooms.count(),
              'hotel_name'        : rooms.first().hotel.name,
              'hotel_english_name': rooms.first().hotel.english_name,
              'hotel_introduction': rooms.first().hotel.introduction,
            },
            'rooms':[{
                'room_id'          : room.id,
                'room_image'       : [image.image_url for image in room.roomimage_set.all()],
                'room_name'        : room.name,
                'room_type'        : room.roomtype_set.first().type.name,
                'room_introduction': room.introduction,
                'checkin_time'     : f"{room.hotel.checkin_time}"[:-3],
                'checkout_time'    : f"{room.hotel.checkout_time}"[:-3],
                'min_people'       : room.min_people,
                'max_people'       : room.max_people,
                'area'             : f"{int(room.area)}{chr(0x33A1)}",
                'bed'              : [
                                        {
                                            'bed_type'       : bed.bed_type.name,
                                            'number_of_beds' : bed.number
                                        } for bed in room.bed_set.all()
                                    ],
                'tags'             : [
                                        tag.name for tag in room.hotel.tags.all()] 
                                        if len(room.hotel.tags.all())<=3 
                                        else [tag.name for tag in room.hotel.tags.all()[:3]
                                    ],
                'price'            : chr(0x20A9)+"{:,}".format(int(room.price))+'~',
                'facility'         : [
                                        {
                                            'name'    : facility.name,
                                            'icon_url': facility.icon_url
                                        } for facility in room.facilities.all()
                                    ],
                'service'          : [
                                        {
                                        'name'    : service.name,
                                        'icon_url': service.icon_url
                                        } for service in room.hotel.services.all()
                                    ]
            } for room in rooms]}
            
        ]
        return JsonResponse({'detail':detail}, status=200)
