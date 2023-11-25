from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Parking, Parkomat, Terminal
from .serializer import ParkingSerializer, TerminalSerializer, ParkomatSerializer


# Create your views here.

@api_view(['GET'])
def get_parkings(request):
    parkings = Parking.objects.all()
    serializer = ParkingSerializer(parkings, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_terminals(request):
    terminals = Terminal.objects.all()
    serializer = TerminalSerializer(terminals, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_parkomats(request):
    parkomats = Parkomat.objects.all()
    serializer = ParkomatSerializer(parkomats, many=True)
    return Response(serializer.data)
