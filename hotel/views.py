import json

from django.views     import View
from django.shortcuts import get_object_or_404
from django.http      import JsonResponse
from django.db.models import Min, Max

from .models          import Hotel

class MainBannerView(View):
    def get(self, request):
        try:
            hotels  = Hotel.objects.all()[:10]
            banners = [{
                'index'    : i+1,
                'hotelName': hotels[i].name,
                'desc'     : hotels[i].introduction,
                'image'    : hotels[i].thumbnail_url,
            } for i in range(len(hotels))]
            return JsonResponse({'data': banners}, status=200)
        except ValueError as e:
            return JsonResponse({'message': f"{e} IS MISSING"}, status=400)

class MagazineView(View):
    def get(self, request):
        try:
            hotels    = Hotel.objects.all()[:2]
            magazines = [{
                'index'    : i+1,
                'hotelName': hotels[i].name,
                'type'     : hotels[i].category.name,
                'location' : hotels[i].location.name,
                'descTitle': hotels[i].description_title,
                'desc'     : hotels[i].description_first,
                'image'    : hotels[i].thumbnail_url,
            }  for i in range(len(hotels))]
            return JsonResponse({'data': magazines}, status=200)
        except ValueError as e:
            return JsonResponse({'message': f"{e} IS MISSING"}, status=400)

class PicksView(View):
    def get(self, request):
        hotels=Hotel.objects.all()
        picks=[
            rooms=Room.objects.filter(hotel_id=i)
            prices=rooms.aggregate(min_p=Min(price_weekday), max_p=Max(price_peak))
            {
            'id':hotels[i].id,
            'name':hotels[i].name,
            'engName':hotels[i].english_name,
            'desc':hotels[i].introduction,
            'mainImg':hotels[i].thumbnail_url,
            'location':hotels[i].location.name,
            'type':hotels[i].category.name,
            'minPrice':prices['min_p'],
            'maxPrice':prices['max_p'],
            'stars':list(hotels[i].tags.all())
            }
        for i in range(len(hotels))]

        return JsonResponse({'hotels': picks}, status=200)

