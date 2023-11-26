from django.contrib import admin
from api.models import Parking, Coordinate, Category, Price, Location, Terminal, Parkomat, ParkingSpot, Comment, Booking, Transaction, Comment


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


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ('vehicle_type', 'min_price', 'max_price')
    list_filter = ('vehicle_type',)


@admin.register(Parking)
class ParkingAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'blocked', 'aggregating', 'total_spots', 'handicapped_spots', 'empty_spots', 'category', 'location',
        'center')
    list_filter = ('blocked', 'aggregating', 'category', 'location')


@admin.register(Terminal)
class TerminalAdmin(admin.ModelAdmin):
    list_display = ('id', 'center', 'category')
    list_filter = ('center', 'category')


@admin.register(Parkomat)
class ParkomatAdmin(admin.ModelAdmin):
    list_display = ('id', 'center', 'category')
    list_filter = ('center', 'category')


@admin.register(ParkingSpot)
class ParkingSpotAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_reserved', 'is_empty')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'parking_spot', 'credentials', 'booking_start_time', 'duration', 'booking_end_time', 'total_price')
    list_filter = ('parking_spot', 'booking_start_time')
    search_fields = ('credentials',)
    date_hierarchy = 'booking_start_time'
    ordering = ('-booking_start_time',)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking', 'payment_id', 'transaction_status')
    list_filter = ('booking', 'transaction_status')
    search_fields = ('payment_id',)
    ordering = ('-id',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'parking', 'fio', 'rating')
    list_filter = ('parking', 'rating')
    search_fields = ('fio',)
    ordering = ('-id',)