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
    path('parkings/<int:parking_id>/', views.get_parking_by_id, name='get_parking_by_id'),
    path('terminals', views.get_terminals, name="terminals"),
    path('parkomats', views.get_parkomats, name="parkomats"),

    path('parkings/<int:parking_id>/comments', views.get_comments, name="comments"),
    path('parkings/<int:parking_id>/comments/add', views.put_comment, name="put_comment"),

    path('parkings/<int:parking_id>/reserve', views.parking_reserve, name="parking-reserve"),
    path('payment/status', views.payment_status, name="payment-status"),
    # path('yookassa-webhook', views.yookassa_webhook, neme="yookassa-webhook"),
]
