from django.urls import path
from .views      import MainBannerView, MagazineView

urlpatterns = [
    path('/banner', MainBannerView.as_view()),
    path('/magazine', MagazineView.as_view()),
]