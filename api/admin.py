from django.contrib import admin
from api.models import Parking, Coordinate, Category, Price, Space, Location


@admin.register(Coordinate)
class CoordinateAdmin(admin.ModelAdmin):
    list_display = ('longitude', 'latitude')


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('type',)
    list_filter = ('type',)


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
    list_display = ('id', 'blocked', 'aggregating', 'category', 'location', 'center', 'space')
    list_filter = ('blocked', 'aggregating', 'category', 'location')
