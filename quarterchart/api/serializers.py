from rest_framework import serializers
from .models import Compagnies

class CompagniesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compagnies
        fields = '__all__'