from django.urls import path
from . import views


urlpatterns = [
     path('', views.kkm_index, name='kkm_index'),
     path('cart_of_patient/', views.cart_of_patient, name='cart_of_patient'),
]