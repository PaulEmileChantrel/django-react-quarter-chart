from django.urls import path
from .views import index

urlpatterns = [
    path('', index),
    path('chart', index),
    path('info/<str:ticker>', index),
]