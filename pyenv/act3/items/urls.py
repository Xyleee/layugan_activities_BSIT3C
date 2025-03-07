from django.urls import path
from . import views

urlpatterns = [
    path('items/', views.get_items, name='get_items'),
    path('items/<int:item_id>/', views.get_item, name='get_item'),
    path('items/add/', views.add_item, name='add_item'),
    path('items/update/<int:item_id>/', views.update_item, name='update_item'),
    path('items/delete/<int:item_id>/', views.delete_item, name='delete_item'),
]