import json

from django.views     import View
from django.shortcuts import get_object_or_404
from django.http      import JsonResponse
from django.db.models import Min, Max

from .models          import Hotel, Room

class MainBannerView(View):
    def get(self, request):
        hotels  = Hotel.objects.all()[:10]
        banners = [{
            'name'         : hotel.name,
            'introduction' : hotel.introduction,
            'thumbnail_url': hotel.thumbnail_url,
        } for hotel in hotels]

        return JsonResponse({'data': banners}, status=200)

class MagazineView(View):
    def get(self, request):
        hotels    = Hotel.objects.all()[:2]
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
        hotels=Hotel.objects.all()
        picks=[
            {
            'id'           : hotel.id,
            'name'         : hotel.name,
            'english_name' : hotel.english_name,
            'introduction' : hotel.introduction,
            'thumbnail_url': hotel.thumbnail_url,
            'location'     : hotel.location.name,
            'category'     : hotel.category.name,
            'min_price'    : "{:,}".format(int(hotel.room_set.aggregate(min_p=Min('price_weekday'))['min_p'])),
            'max_price'    : "{:,}".format(int(hotel.room_set.aggregate(max_p=Max('price_peak'))['max_p'])),
            'tags'         : [tag.name for tag in hotel.tags.all()]
            }
        for hotel in hotels]
        
        return JsonResponse({'hotels': picks}, status=200)

class DetailPageView(View):
    def get(self, request,hotel_id):
        rooms=Room.objects.select_related('hotel').filter(hotel_id=hotel_id).order_by('id')
        print('aaa')
        detail=[{'common_info':{
              'hotel_name':rooms.first().hotel.name,
              'hotel_english_name':rooms.first().hotel.english_name,
              'hotel_introduction':rooms.first().hotel.introduction,
            },
            'rooms':[{
                'room_name':room.name,
                'room_type':room.types.get(id=room.id).name,
                'room_introduction':room.introduction,
                'checkin_time':room.hotel.checkin_time,
                'checkout_time':room.hotel.checkout_time,
                'min_people':room.min_people,
                'max_people':room.max_people,
                'area':int(room.area),
                'bed':[{'bed_type':bed.bed_type.name,'number_of_beds':bed.number}for bed in room.bed_set.all()],
                'tags':[tag.name for tag in room.hotel.tags.all()] if len(room.hotel.tags.all())<=3 else [tag.name for tag in room.hotel.tags.all()[:3]],
                'price':chr(0x20A9)+"{:,}".format(int(room.price))+'~',
                # name과 icon_url을 각각 리스트에 넣을지, 하나의 딕셔너리에 넣을지 해보고 결정
                'facility':[{'name':facility.name, 'icon_url':facility.icon_url} for facility in room.facilities.all()],
                'service':[{'name':service.name, 'icon_url':service.icon_url} for service in room.hotel.services.all()]
            } for room in rooms]}
            
        ]
        return JsonResponse({'detail':detail}, status=200)
