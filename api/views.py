from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Parking
from .serializer import ParkingSerializer


# Create your views here.

@api_view(['GET'])
def get_parkings(request):
    parkings = Parking.objects.all()
    serializer = ParkingSerializer(parkings, many=True)
    return Response(serializer.data)
