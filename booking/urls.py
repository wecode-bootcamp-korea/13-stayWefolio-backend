from django.urls import path
from .views      import BookingView

urlpatterns = [
    path('/new', BookingView.as_view()),
]