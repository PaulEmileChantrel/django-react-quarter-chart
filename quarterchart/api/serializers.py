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
    class CompanieInfoSubSerializer(serializers.ModelSerializer):
        class Meta:
            model = CompanieInfo
            exclude = ["name"]
    
    companie_info = CompanieInfoSubSerializer()
    
    class Meta:
        model =  Companie
        fields = "__all__"
 
    def create(self, validated_data):
        print('ok')
        companie_info_data = validated_data.pop('companie_info')
        companie_instance = Companie.objects.create(**validated_data)
        CompanieInfo.objects.create(name=companie_instance,
                              **companie_info_data)
        return companie_instance