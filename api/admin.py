from django.contrib import admin
from api.models import Parking, Coordinate, Category, Price, Space, Location, LocationCoordinate, PriceParking

@admin.register(Coordinate)
class CoordinateAdmin(admin.ModelAdmin):
    list_display = ('longitude', 'latitude')

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('location_type',)
    list_filter = ('location_type',)

@admin.register(LocationCoordinate)
class LocationCoordinateAdmin(admin.ModelAdmin):
    list_display = ('location', 'coordinate')
    list_filter = ('location', 'coordinate')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('zone_purpose',)
    list_filter = ('zone_purpose',)

@admin.register(Space)
class SpaceAdmin(admin.ModelAdmin):
    list_display = ('handicapped', 'total')

@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ('vehicle_type', 'min_price', 'max_price')
    list_filter = ('vehicle_type',)

@admin.register(Parking)
class ParkingAdmin(admin.ModelAdmin):
    list_display = ('blocked', 'aggregating', 'category', 'location', 'center', 'space')
    list_filter = ('blocked', 'aggregating', 'category', 'location')

@admin.register(PriceParking)
class PriceParkingAdmin(admin.ModelAdmin):
    list_display = ('price', 'parking')
    list_filter = ('price', 'parking')