from django.contrib import admin
from api.models import Parking, Coordinate, Category, Price, Space, Location, LocationCoordinate, PriceParking

# Register your models here.

admin.site.register(Parking)
admin.site.register(Coordinate)
admin.site.register(Category)
admin.site.register(Price)
admin.site.register(Space)
admin.site.register(Location)
admin.site.register(LocationCoordinate)
admin.site.register(PriceParking)
