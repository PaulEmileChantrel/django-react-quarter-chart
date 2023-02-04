from django.shortcuts import render
from rest_framework import generics
from .models import *
from .serializers import *
# Create your views here.
class CompagniesView(generics.ListAPIView):
    queryset = Compagnies.objects.all()
    serializer_class = CompagniesSerializer