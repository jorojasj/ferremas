from django.urls import path, include
from .views import *
from django.contrib.auth import views as auth_views
from app import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('producto', ProductoViewset)


urlpatterns = [
    path('', views.index, name='index'),
    #Registration
    path('cargarLogin/', views.cargarLogin, name='cargarLogin'),
    path('registrar/', views.registro, name='registrar'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    #Producto
    path('agregarProducto/', views.agregarProducto, name='agregarProducto'),
    path('modificarProducto/<id>/', views.modificarProducto, name='modificarProducto'),
    path('listarProducto/', views.listarProducto, name='listarProducto'),
    path('eliminarProducto/<id>', views.eliminarProducto, name='eliminarProducto'),
    path('detalleProducto/<id>', views.detalleProducto, name='detalleProducto'),
    #Carrito
    path('carrito/', views.carrito, name='carrito'),
    path('añadirCarrito/<id>', views.añadirCarrito, name='añadirCarrito'),
    path('eliminarProductoCarrito/<int:item_id>', views.eliminarProductoCarrito, name='eliminarProductoCarrito'),
    path('aumentarCantidadProducto/<int:item_id>/', views.aumentar_cantidad_producto, name='aumentar_cantidad_producto'),
    path('vaciarCarrito/', views.vaciar_carrito, name='vaciar_carrito'),
    path('productos', views.productos, name='producto'),
    #API_PRODUCTOS
    path('api/', include(router.urls)),
]