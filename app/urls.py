from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
from app import views



urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('registrar/', views.registro, name='registrar'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('agregarProducto/', views.agregarProducto, name='agregarProducto'),
    path('modificarProducto/<id>/', views.modificarProducto, name='modificarProducto'),
    path('listarProducto/', views.listarProducto, name='listarProducto'),
    path('eliminarProducto/<id>', views.eliminarProducto, name='eliminarProducto'),
    path('detalleProducto/<id>', views.detalleProducto, name='detalleProducto'),
    path('carrito/', views.carrito, name='carrito'),


]