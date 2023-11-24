from .models import Mock
from rest_framework.serializers import ModelSerializer


class MockSerializer(ModelSerializer):
    class Meta:
        model = Mock
        fields = '__all__'
