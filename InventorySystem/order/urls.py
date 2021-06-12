
from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.form_add, name='order_add'),
    path('list/', views.OrderListView.as_view(), name='order_list'),
    path('submit/', views.form_submit),
    path('enable/', views.form_complete),
]
