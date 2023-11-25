from django.db import models


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


class Space(models.Model):
    handicapped = models.IntegerField(null=False)
    total = models.IntegerField(null=False)

    class Meta:
        verbose_name_plural = "Парковочные места"

    def __str__(self):
        return f"Space (Handicapped: {self.handicapped}, Total: {self.total})"


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
    category = models.ForeignKey(to=Category, null=False, on_delete=models.PROTECT)
    location = models.ForeignKey(to=Location, null=False, on_delete=models.PROTECT)
    center = models.ForeignKey(to=Coordinate, null=False, on_delete=models.PROTECT)
    space = models.ForeignKey(to=Space, null=False, on_delete=models.PROTECT)
    prices = models.ManyToManyField(to=Price, related_name='parkings')

    class Meta:
        verbose_name_plural = "Парковки"

    def __str__(self):
        return f"Parking ({self.category}, Location: {self.location}, Center: {self.center})"


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
