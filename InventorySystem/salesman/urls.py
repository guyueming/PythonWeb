
from django.urls import path
from . import views


urlpatterns = [
    path('add/', views.add, name='salesman_add'),
    path('list/', views.SalesmanListView.as_view(), name='salesman_list'),
    path('submit/', views.submit),
    path('enable/', views.enable),
]
