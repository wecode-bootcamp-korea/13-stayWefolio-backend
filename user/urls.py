
from django.urls import path
from .views import SignUpView, LoginView, ActivateView

urlpatterns = [
    path('/signup', SignUpView.as_view()),
    path('/login', LoginView.as_view()),
    path('/<str:uidb64>/<str:token>', ActivateView.as_view()),
]