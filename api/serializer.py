from .models import Parking
from .models import Coordinate
from .models import Location
from .models import Price
from .models import Space
from .models import Category
from rest_framework.serializers import ModelSerializer


class CoordinateSerializer(ModelSerializer):
    class Meta:
        model = Coordinate
        fields = '__all__'


class LocationSerializer(ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class PriceSerializer(ModelSerializer):
    class Meta:
        model = Price
        fields = '__all__'


class SpaceSerializer(ModelSerializer):
    class Meta:
        model = Space
        fields = '__all__'


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ParkingSerializer(ModelSerializer):
    class Meta:
        model = Parking
        fields = '__all__'