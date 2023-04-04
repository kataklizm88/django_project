from django.urls import path
from basket.views import basket_edit, BasketRemoveView, BasketAddView

app_name = 'basket'

urlpatterns = [
    path('basket-add/<int:product_id>/', BasketAddView.as_view(), name="basket_add"),
    path('basket-remove/<int:pk>/', BasketRemoveView.as_view(), name="basket_remove"),
    path('edit/<int:id>/<int:quantity>/', basket_edit, name="basket_edit")
]
