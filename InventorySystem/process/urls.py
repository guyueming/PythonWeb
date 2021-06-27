
from django.urls import path
from . import views


urlpatterns = [
    path('technology/add/', views.technology_add, name='technology_add'),
    path('technology/list/', views.TechnologyListView.as_view(), name='technology_list'),
    path('technology/enable/', views.technology_enable),
    path('technology/del/', views.technology_delete),

    path('specification/add/', views.specification_add, name='specification_add'),
    path('specification/list/', views.SpecificationListView.as_view(), name='specification_list'),
    path('specification/enable/', views.specification_enable),
    path('specification/del/', views.specification_delete),
]
