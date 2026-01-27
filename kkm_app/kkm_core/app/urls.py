from django.urls import path
from . import views


urlpatterns = [
     path('', views.kkm_index, name='kkm_index'),
     path('get_current_time/', views.get_current_time, name='get_current_time'),
]