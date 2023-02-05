from django.urls import path
from .views import CompanieView

urlpatterns = [
    path('', CompanieView.as_view()),
]