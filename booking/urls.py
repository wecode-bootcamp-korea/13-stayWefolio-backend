from django.urls import path
from .views      import BookingView

urlpatterns = [
    path('/<int:room_id>', BookingView.as_view()),
]