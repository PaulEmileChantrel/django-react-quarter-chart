from django.urls import path
from .views import CompagniesView

urlpatterns = [
    path('', CompagniesView.as_view()),
]