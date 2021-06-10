from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('add/', views.add_wood, name='add_wood'),
    path('list/', views.WoodListView.as_view(), name='wood_list'),
    path('enable/', views.enable),
    path('submit/', views.submit),
]