from django.urls import path
from .views import index

urlpatterns = [
    path('', index,name = 'frontend-companielist'),
    path('chart/<str:ticker>', index),
    path('info/<str:ticker>', index),
]