from django.urls import path
from mainapp.views import ProductListView

app_name = 'mainapp'


urlpatterns = [
    path('', ProductListView.as_view(), name="index"),
    path('<int:category_id>/', ProductListView.as_view(), name='product'),
    path('page/<int:page>/', ProductListView.as_view(), name='page')
]
