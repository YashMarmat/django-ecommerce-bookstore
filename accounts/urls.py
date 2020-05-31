
from django.urls import path
from .views import SignUpView

urlpatterns = [
    path('accounts/', SignUpView.as_view(), name = 'signup'),
]