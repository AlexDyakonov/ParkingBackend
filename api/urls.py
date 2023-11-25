from django.contrib import admin
from django.urls import path
from django.urls import include, path
from ParkingBackend import settings
from django.conf.urls.static import static
from . import views

app_name = "api"

urlpatterns = [
    path('parkings', views.get_parkings, name="parkings"),
    path('parkings/put_ek', views.put_ek, name="parkings-put_ek"),
    path('terminals', views.get_terminals, name="terminals"),
    path('parkomats', views.get_parkomats, name="parkomats"),
]
