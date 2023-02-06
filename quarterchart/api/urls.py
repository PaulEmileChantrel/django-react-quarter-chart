from django.urls import path
from .views import CompanieView,CreateCompanieView,FilterCompanieView,GetCompanieInfo

urlpatterns = [
    path('', CompanieView.as_view()),
    path('add',CreateCompanieView.as_view()),
    path('filterCompanie/',FilterCompanieView.as_view()),
    path('get-companie-info',GetCompanieInfo.as_view()),
]