from django.urls import path
from .views      import BookingView, BookingConfirmView

urlpatterns = [
    path('/<int:room_id>', BookingView.as_view()),
    path('/confirmation', BookingConfirmView.as_view()),
]