from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.db.models import F
import uuid
from datetime import timedelta

class Coordinate(models.Model):
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    latitude = models.DecimalField(max_digits=10, decimal_places=7)

    class Meta:
        verbose_name_plural = "Координаты"

    def __str__(self):
        return f"[{self.latitude}, {self.longitude}]"


class Location(models.Model):
    class LocationType(models.TextChoices):
        LINE_STRING = "line_string"
        POLYGON = "polygon"

    type = models.CharField(
        null=False,
        max_length=30,
        choices=LocationType.choices
    )

    coordinates = models.ManyToManyField(to=Coordinate, related_name='locations')

    class Meta:
        verbose_name_plural = "Локации"

    def __str__(self):
        return f"Location ({self.type})"


class Category(models.Model):
    class CategoryType(models.TextChoices):
        POINT = "point"
        LINE = "line"
        POLYGON = "polygon"

    zone_purpose = models.CharField(
        max_length=30,
        choices=CategoryType.choices
    )

    class Meta:
        verbose_name_plural = "Категория"

    def __str__(self):
        return f"Category ({self.get_zone_purpose_display()})"


class Price(models.Model):
    class VehicleType(models.TextChoices):
        CAR = "car"

    vehicle_type = models.CharField(
        max_length=30,
        choices=VehicleType.choices,
        default=VehicleType.CAR)
    min_price = models.IntegerField(null=False)
    max_price = models.IntegerField(null=False)

    class Meta:
        verbose_name_plural = "Цены"

    def __str__(self):
        return f"Price ({self.vehicle_type}, Min: {self.min_price}, Max: {self.max_price})"


class Parking(models.Model):
    blocked = models.BooleanField(null=False, default=False)
    aggregating = models.BooleanField(null=False, default=False)
    total_spots = models.IntegerField(null=True)
    handicapped_spots = models.IntegerField(null=True)
    empty_spots = models.IntegerField(null=True)
    category = models.ForeignKey(to=Category, null=False, on_delete=models.PROTECT)
    location = models.ForeignKey(to=Location, null=False, on_delete=models.PROTECT)
    center = models.ForeignKey(to=Coordinate, null=False, on_delete=models.PROTECT)
    prices = models.ManyToManyField(to=Price, related_name='parkings')

    class Meta:
        verbose_name_plural = "Парковки"

    def __str__(self):
        return f"Parking ({self.category}, Location: {self.location}, Center: {self.center})"


class ParkingSpot(models.Model):
    is_reserved = models.BooleanField(null=False, default=False)
    is_empty = models.BooleanField(null=False, default=True)
    reservation_start_time = models.DateTimeField(auto_now_add=False, null=True)
    reservation_duration = models.DurationField(null=True)
    parking = models.ForeignKey(to=Parking, null=True, on_delete=models.CASCADE)


@receiver(pre_save, sender=ParkingSpot)
def update_empty_spots(sender, instance, **kwargs):
    if instance.pk:
        old_parking_spot = ParkingSpot.objects.get(pk=instance.pk)
        old_is_empty = old_parking_spot.is_empty
        new_is_empty = instance.is_empty

        if old_is_empty != new_is_empty:
            if new_is_empty:
                Parking.objects.filter(pk=instance.parking.pk).update(empty_spots=F('empty_spots') + 1)
            else:
                Parking.objects.filter(pk=instance.parking.pk).update(empty_spots=F('empty_spots') - 1)


@receiver(post_save, sender=Parking)
def create_parking_spots(sender, instance, created, **kwargs):
    if created:
        for _ in range(instance.total_spots):
            ParkingSpot.objects.create(parking=instance, is_empty=True)
        instance.empty_spots = instance.total_spots
        instance.save()


pre_save.connect(update_empty_spots, sender=ParkingSpot)
post_save.connect(create_parking_spots, sender=Parking)


class Terminal(models.Model):
    center = models.ForeignKey(to=Coordinate, null=False, on_delete=models.PROTECT)
    category = models.ForeignKey(to=Category, null=False, on_delete=models.PROTECT, default=Category.CategoryType.POINT)

    class Meta:
        verbose_name_plural = "Терминалы"


class Parkomat(models.Model):
    center = models.ForeignKey(to=Coordinate, null=False, on_delete=models.PROTECT)
    category = models.ForeignKey(to=Category, null=False, on_delete=models.PROTECT, default=Category.CategoryType.POINT)

    class Meta:
        verbose_name_plural = "Паркоматы"


class Booking(models.Model):
    parking_spot = models.ForeignKey(to=ParkingSpot, null=False, on_delete=models.CASCADE)
    credentials = models.CharField(max_length=50, null=False)
    booking_start_time = models.DateTimeField(auto_now_add=True, null=False) # booking - время, когда машина стоит на парковке
    duration = models.DurationField(null=False, default=timedelta(hours=1))
    total_price = models.IntegerField(null=True) # в копейках

    def booking_end_time(self):
        return self.booking_start_time + self.duration
    
    class Meta:
        verbose_name_plural = "Брони"

    def __str__(self):
        return f"Booking for Parking {self.parking} created at {self.created_at} for {self.credentials}"


class Transaction(models.Model):
    booking = models.ForeignKey(to=Booking, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=50, db_index=True) # API ID
    secret_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    TRANSACTION_STATUS_CHOICES = [
        ('pending', 'Ожидание оплаты'),
        ('paid', 'Оплачено'),
        ('failed', 'Ошибка оплаты'),
        ('refunded', 'Возврат средств'),
    ]

    transaction_status = models.CharField(
        max_length=10,
        choices=TRANSACTION_STATUS_CHOICES,
        default='pending',
    )

    class Meta:
        verbose_name_plural = "Оплаты"

    def __str__(self):
        return f"Transaction for Parking {self.parking} with ID {self.payment_id} ({self.status}) for {self.credentials}"


class Comment(models.Model):
    parking = models.ForeignKey(to=Parking, null=False, on_delete=models.CASCADE)
    text = models.TextField(null=False)

    def __str__(self):
        return f"Comment: {self.text}"
