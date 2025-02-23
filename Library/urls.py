from django.urls import path
from .views import *

urlpatterns = [
path('', LoginPage, name='login'),
path('home/', HomePage, name='home'),
]