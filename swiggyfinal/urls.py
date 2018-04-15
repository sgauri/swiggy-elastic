from django.contrib import admin
from django.urls import path, re_path
from mswiggy import views

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('^restaurant/add/$', views.restaurant_add, name='restaurant_add'),
    re_path('^restaurant/update/$', views.restaurant_update, name='restaurant_update'),
    re_path('^restaurant/delete/$', views.restaurant_delete, name='restaurant_delete'),
    re_path('^driver/add/$', views.driver_add, name='driver_add'),
    re_path('^driver/location/update/$', views.driver_location_update, name='driver_location_update'),
    re_path('^order/place/$', views.order_place, name='order_place'),
    re_path('^create/menu/$', views.create_menu, name='create_menu'),
]