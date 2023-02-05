from django.urls import path
from .views import CompanieView,CreateCompanieView

urlpatterns = [
    path('', CompanieView.as_view()),
    path('add',CreateCompanieView.as_view())
]