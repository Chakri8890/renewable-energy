from django.urls import path
from .import views
urlpatterns = [
    path('',views.home,name='home'),
    path('city-input/', views.city_input, name='city_input'),
    path('input',views.input,name='input'),
    path('output',views.output,name='output')
]
