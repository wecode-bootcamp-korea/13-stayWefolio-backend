from django.urls import path
from .views      import (MainBannerView, 
                        MagazineView, 
                        PicksView, 
                        PicksDetailView,
                        DetailPageView)

urlpatterns = [
    path('/banner', MainBannerView.as_view()),
    path('/magazine', MagazineView.as_view()),
    path('/picks', PicksView.as_view()),
    path('/picks/<int:hotel_id>', PicksDetailView.as_view()),
    path('/places/<int:hotel_id>', DetailPageView.as_view()),
]