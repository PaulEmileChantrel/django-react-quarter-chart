from django.urls import path
from .views import CompanieView,CreateCompanieView,FilterCompanieView

urlpatterns = [
    path('', CompanieView.as_view()),
    path('add',CreateCompanieView.as_view()),
    path('filterCompanie/',FilterCompanieView.as_view())
]