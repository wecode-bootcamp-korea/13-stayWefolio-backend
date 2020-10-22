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
            'hotel_name': hotel.name,
            'desc'      : hotel.introduction,
            'image'     : hotel.thumbnail_url,
        } for hotel in hotels]

        return JsonResponse({'data': banners}, status=200)

class MagazineView(View):
    def get(self, request):
        hotels    = Hotel.objects.all()[:2]
        magazines = [{
            'hotel_name': hotel.name,
            'type'      : hotel.category.name,
            'location'  : hotel.location.name,
            'desc_title': hotel.description_title,
            'desc'      : hotel.description_first,
            'image'     : hotel.thumbnail_url,
        } for hotel in hotels]

        return JsonResponse({'data': magazines}, status=200)

class PicksView(View):
    def get(self, request):
        hotels=Hotel.objects.all()
        picks=[
            {
            'id'      : hotel.id,
            'name'    : hotel.name,
            'engName' : hotel.english_name,
            'desc'    : hotel.introduction,
            'mainImg' : hotel.thumbnail_url,
            'location': hotel.location.name,
            'type'    : hotel.category.name,
            'minPrice': "{:,}".format(int(hotel.room_set.aggregate(min_p=Min('price_weekday'))['min_p'])),
            'maxPrice': "{:,}".format(int(hotel.room_set.aggregate(max_p=Max('price_peak'))['max_p'])),
            'stars'   : [tag.name for tag in hotel.tags.all()]
            }
        for hotel in hotels]

        return JsonResponse({'hotels': picks}, status=200)