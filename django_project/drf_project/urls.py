from django.contrib import admin
from django.urls import path, include
from mainapp.views import index
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('products/', include('mainapp.urls', namespace='products')),
    path('auth/', include('authapp.urls', namespace='auth')),
    path('baskets/', include('basket.urls', namespace='baskets')),
    path('admin-staff/', include('adminapp.urls', namespace='admins')),
    path('', include('social_django.urls', namespace='social'))

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
