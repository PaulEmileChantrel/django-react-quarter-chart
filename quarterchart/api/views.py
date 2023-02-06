from django.shortcuts import render
from rest_framework import generics,status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from django.db.models import Q
from .serializers import CompanieSerializer,CreateCompanieSerializer,CompanieInfoSerializer
# Create your views here.
class CompanieView(generics.ListAPIView):
    queryset = Companie.objects.all()
    serializer_class = CompanieSerializer

class FilterCompanieView(generics.ListAPIView):
    serializer_class = CompanieSerializer

    def get_queryset(self):
        return Companie.objects.filter(Q(name__icontains=self.request.query_params['name'])|Q(ticker__icontains=self.request.query_params['name']))

class GetCompanieInfo(APIView):
    serializer_class = CompanieInfoSerializer
    lookup_url_kwarg = 'ticker'

    def get(self, request, format = None):
        ticker = request.GET.get(self.lookup_url_kwarg)
        if ticker != None:
            companie = Companie.objects.filter(ticker=ticker)
            if len(companie) > 0:
                data = CompanieInfoSerializer(companie[0]).data

                return Response(data, status=status.HTTP_200_OK)
            return Response({'Ticker Not Found' : 'Invalid Request'},status=status.HTTP_404_NOT_FOUND)
        return Response({'Bad Request' : 'Ticker not found in request'},status=status.HTTP_400_BAD_REQUEST)
class CreateCompanieView(APIView):
    serializer_class = CreateCompanieSerializer
    
    def post(self, request,format = None):
        #does the user has a session?
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        # is the data sent valid?
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            name = serializer.data.get('name')
            ticker = serializer.data.get('ticker')

            #check if company already exists
            queryset = Companie.objects.filter(ticker=ticker)
            if queryset.exists():
                company = queryset.first()
                # the company already exists
                return Response(CompanieSerializer(company).data,status=status.HTTP_208_ALREADY_REPORTED)
            else:
                company = Companie(name=name,ticker=ticker)
                company.save()
                return Response(CompanieSerializer(company).data,status=status.HTTP_201_CREATED)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
