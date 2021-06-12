
from django.urls import path
from . import views


urlpatterns = [
    path('add/', views.add, name='customer_add'),
    path('list/', views.CustomerListView.as_view(), name='customer_list'),
    path('submit/', views.submit),
    path('enable/', views.enable),
]
