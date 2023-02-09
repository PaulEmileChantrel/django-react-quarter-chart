from django.urls import path
from .views import CompanieView,CreateCompanieView,FilterCompanieView,GetCompanieInfo,CompanyChartData

urlpatterns = [
    path('', CompanieView.as_view()),
    path('add',CreateCompanieView.as_view()),
    path('filterCompany/',FilterCompanieView.as_view()),
    path('get-company-info',GetCompanieInfo.as_view()),
    path('get-company-chart',CompanyChartData.as_view()),
]