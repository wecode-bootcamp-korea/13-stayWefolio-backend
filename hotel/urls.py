from django.urls import path
from .views      import MainBannerView, MagazineView, PicksView

urlpatterns = [
    path('/banner', MainBannerView.as_view()),
    path('/magazine', MagazineView.as_view()),
    path('/picks', PicksView.as_view()),
]