from .models import Parking
from .models import Parkomat, Terminal
from .models import Location
from .models import Price
from .models import Category
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework.serializers import DecimalField


class CoordinateSerializer(Serializer):
    longitude = DecimalField(max_digits=10, decimal_places=7)
    latitude = DecimalField(max_digits=10, decimal_places=7)

    def to_representation(self, instance):
        return [instance.longitude, instance.latitude]


class LocationSerializer(ModelSerializer):
    coordinates = CoordinateSerializer(read_only=True, many=True)

    class Meta:
        model = Location
        fields = ('type', 'coordinates')


class PriceSerializer(ModelSerializer):
    class Meta:
        model = Price
        fields = ('vehicle_type', 'min_price', 'max_price')


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ('zone_purpose',)


class ParkingSerializer(ModelSerializer):
    category = CategorySerializer()
    location = LocationSerializer()
    center = CoordinateSerializer()
    prices = PriceSerializer(read_only=True, many=True)

    class Meta:
        model = Parking
        fields = (
            'id', 'blocked', 'aggregating', 'category', 'location', 'center', 'prices', 'total_spots', 'empty_spots',
            'handicapped_spots')


class TerminalSerializer(ModelSerializer):
    category = CategorySerializer()
    center = CoordinateSerializer()

    class Meta:
        model = Terminal
        fields = ('id', 'category', 'center')


class ParkomatSerializer(ModelSerializer):
    category = CategorySerializer()
    center = CoordinateSerializer()

    class Meta:
        model = Parkomat
        fields = ('id', 'category', 'center')
