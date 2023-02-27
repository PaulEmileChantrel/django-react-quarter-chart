from rest_framework import serializers
from .models import Companie,CompanieInfo,CompanieIncomeStatement

class CompanieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Companie
        fields = '__all__'

class CreateCompanieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Companie
        fields = ['name','ticker']


class CompanieInfoSerializer(serializers.ModelSerializer):
    next_earnings_date = serializers.DateTimeField(format="%m-%d")
    class Meta:
        model =  CompanieInfo
        fields = ['summary','sector','industry','website','next_earnings_date']
 
class CompanieFullInfoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Companie
        fields = ['market_cap','name','ticker','companie_info','image_link']
    
    companie_info = CompanieInfoSerializer(read_only=True)
    

class CompanieIncomeSerializer(serializers.Serializer):

    class Meta:
        model = CompanieIncomeStatement
        fields = '__all__'




class NextEarningsSerializer(serializers.ModelSerializer):
    next_earnings_date = serializers.DateTimeField(format="%m-%d")
    class Meta:
        model =  CompanieInfo
        fields = ['ticker','id','next_earnings_date']
        
    
 