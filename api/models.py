from django.db import models


class Coordinate(models.Model):
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    latitude = models.DecimalField(max_digits=10, decimal_places=7)

    class Meta:
        verbose_name_plural = "Координаты"


class Location(models.Model):
    class LocationType(models.TextChoices):
        LINE_STRING = "line_string"
        POLYGON = "polygon"

    location_type = models.CharField(
        null=False,
        max_length=30,
        choices=LocationType.choices
    )

    class Meta:
        verbose_name_plural = "Локации"
    


class LocationCoordinate(models.Model):
    location = models.ForeignKey(to=Location, null=False, on_delete=models.CASCADE)
    coordinate = models.ForeignKey(to=Coordinate, null=False, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Локация-Координаты"
        # db_table_comment = "Сопоставляет id локации с id координат. Необходимо для задания нескольких координат к одной локации."


class Category(models.Model):
    class CategoryType(models.TextChoices):
        LINE = "line"
        POLYGON = "polygon"

    zone_purpose = models.CharField(
        max_length=30,
        choices=CategoryType.choices
    )

    class Meta:
        verbose_name_plural = "Категория"


class Space(models.Model):
    handicapped = models.IntegerField(null=False)
    total = models.IntegerField(null=False)
    class Meta:
        verbose_name_plural = "Парковочные места"


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


class Parking(models.Model):
    blocked = models.BooleanField(null=False, default=False)
    aggregating = models.BooleanField(null=False, default=False)
    category = models.ForeignKey(to=Category, null=False, on_delete=models.PROTECT)
    location = models.ForeignKey(to=Location, null=False, on_delete=models.PROTECT)
    center = models.ForeignKey(to=Coordinate, null=False, on_delete=models.PROTECT)
    space = models.ForeignKey(to=Space, null=False, on_delete=models.PROTECT)
    class Meta:
        verbose_name_plural = "Парковки"


class PriceParking(models.Model):
    price = models.ForeignKey(to=Price, null=False, on_delete=models.CASCADE)
    parking = models.ForeignKey(to=Parking, null=False, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Цены парковок"
        # db_table_comment = "Сопоставляет парковку с возможными на ней ценами."
