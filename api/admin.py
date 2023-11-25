from django.contrib import admin
from api.models import Parking, Coordinate, Category, Price, Space, Location, Terminal, Parkomat, Payment, Reservation


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


@admin.register(Terminal)
class TerminalAdmin(admin.ModelAdmin):
    list_display = ('id', 'center', 'category')
    list_filter = ('center', 'category')


@admin.register(Parkomat)
class ParkomatAdmin(admin.ModelAdmin):
    list_display = ('id', 'center', 'category')
    list_filter = ('center', 'category')


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('parking', 'created_at', 'duration', 'credentials')
    list_filter = ('parking', 'created_at')
    search_fields = ('parking__category__zone_purpose', 'created_at')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('status', 'payment_id', 'duration', 'credentials', 'secret_key')
    list_filter = ('parking', 'status')
    search_fields = ('parking__category__zone_purpose', 'payment_id')
