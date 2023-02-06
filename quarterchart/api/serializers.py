from rest_framework import serializers
from .models import Companie,CompanieInfo

class CompanieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Companie
        fields = '__all__'

class CreateCompanieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Companie
        fields = ['name','ticker']

class CompanieInfoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model =  CompanieInfo
        fields = ['summary','sector','industry','website']
 
class CompanieFullInfoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Companie
        fields = ['market_cap','name','ticker','companie_info','image_link']
    
    companie_info = CompanieInfoSerializer(read_only=True)
    