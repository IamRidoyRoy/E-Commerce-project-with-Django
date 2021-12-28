from django.urls import path
from . import views


urlpatterns = [
    path('', views.mystore, name= 'mystore'),
    path('<slug:category_slug>/', views.mystore, name= 'products_by_category'),
    path('<slug:category_slug>/<slug:product_slug>', views.product_detail, name= 'product_detail'),

]
