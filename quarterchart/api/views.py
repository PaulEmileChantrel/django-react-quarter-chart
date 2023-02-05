from django.shortcuts import render
from rest_framework import generics
from .models import *
from .serializers import *
# Create your views here.
class CompanieView(generics.ListAPIView):
    queryset = Companie.objects.all()
    serializer_class = CompanieSerializer