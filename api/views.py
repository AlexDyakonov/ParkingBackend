from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Mock
from .serializer import MockSerializer


# Create your views here.

@api_view(['GET'])
def get_mocks(request):
    mocks = Mock.objects.all()
    serializer = MockSerializer(mocks, many=True)
    return Response(serializer.data)
