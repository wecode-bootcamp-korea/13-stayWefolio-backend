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
        hotels    = Hotel.objects.select_related('category','location').all().order_by('id')[:2]
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