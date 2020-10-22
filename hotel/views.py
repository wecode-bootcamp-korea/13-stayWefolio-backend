import json

from django.views     import View
from django.shortcuts import get_object_or_404
from django.http      import JsonResponse

from .models          import Hotel

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
        }  for hotel in hotels]
        return JsonResponse({'data': magazines}, status=200)

