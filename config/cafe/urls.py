from django.urls import path
from .views import MyView, AboutView, ContactView

urlpatterns = [
    path('', MyView.as_view() , name='home'),
    path('contact/', ContactView.as_view() , name='contact'),
    path('about/', AboutView.as_view() , name='about'),
]
