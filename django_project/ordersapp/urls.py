from django.urls import path
from .views import OrderList, OrderItemCreate, OrderItemsUpdate, ordering_forming_complete, OrderRead, OrderDelete

app_name = 'ordersapp'

urlpatterns = [
    path('', OrderList.as_view(), name="order_list"),
    path('create/', OrderItemCreate.as_view(), name="orders_create"),
    path('forming/complete/<int:pk>/', ordering_forming_complete, name="ordering_forming_complete"),
    path('read/<int:pk>/', OrderRead.as_view(), name="order_read"),
    path('update/<int:pk>/', OrderItemsUpdate.as_view(), name="order_update"),
    path('delete/<int:pk>/', OrderDelete.as_view(), name="order_delete"),
]
