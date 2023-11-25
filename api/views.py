from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Parking, Parkomat, Terminal
from .serializer import ParkingSerializer, TerminalSerializer, ParkomatSerializer
from rest_framework import status
import json
from .utils import load_parkings_from_ek


# Create your views here.

@api_view(['GET'])
def get_parkings(request):
    parkings = Parking.objects.all()
    serializer = ParkingSerializer(parkings, many=True)
    return Response(serializer.data)


@api_view(['PUT'])
def put_ek(request):
    json_data = request.data['parkings']
    if not json_data:
        return Response({'error': 'JSON data is required'}, status=status.HTTP_400_BAD_REQUEST)

    load_parkings_from_ek(json_data)
    return Response({'success': 'Data uploaded successfully'}, status=status.HTTP_201_CREATED)


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
