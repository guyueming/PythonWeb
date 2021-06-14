
from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add, name='order_add'),
    path('list/', views.OrderListView.as_view(), name='order_list'),
    path('submit/', views.submit),
    path('sure/', views.make_sure),
    path('complete/', views.make_complete),
    path('delete/', views.make_delete),
]
