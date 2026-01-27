from django.urls import path
from . import views


urlpatterns = [
     path('', views.kkm_index, name='kkm_index'),
]