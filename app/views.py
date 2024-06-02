from django.shortcuts import get_object_or_404, render, redirect
from .forms import *
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from rest_framework import viewsets
from .serializers import *
from .utils import obtener_tipo_cambio
from decimal import Decimal


class ProductoViewset(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

# Create your views here.
def index(request):
    tipo_cambio = obtener_tipo_cambio()
    productos = Producto.objects.all()

    for producto in productos:
        producto.precio_dolar = producto.precio/tipo_cambio

    return render(request, 'index.html', {'productos':productos})

def cargarLogin(request):
    return render(request, 'registration/login.html')

def registro(request):
    data = {
        'form': CustomUserCreationForm()
    }
    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(username=formulario.cleaned_data['username'], password=formulario.cleaned_data['password1'])
            login(request, user)
            messages.success(request, "Te has registrado con exito")
            return redirect(to='index')
        data['form'] = formulario    
    return render(request, 'registration/registrar.html', data)

@login_required
def aumentar_cantidad_producto(request, item_id):
    cart = get_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    if request.method == 'POST':
        cantidad = int(request.POST.get('cantidad', 1))
        cart_item.cantidad = cantidad
        cart_item.save()
    return redirect('carrito')

def get_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        cart_id = request.session.get('cart_id')
        if cart_id:
            cart = get_object_or_404(Cart, id=cart_id)
        else:
            cart = Cart.objects.create()
            request.session['cart_id'] = cart.id
    return cart

@login_required
def carrito(request):
    cart = get_cart(request)
    total_cart = cart.cartitem_set.aggregate(total=Sum('subtotal'))['total']
    tipo_cambio = obtener_tipo_cambio()
    tipo_cambio_decimal = Decimal(tipo_cambio)
    total_cart_dolar = total_cart / tipo_cambio_decimal if total_cart else 0
    return render(request, 'carrito.html', {
        'cart': cart,
        'total_cart': total_cart,
        'total_cart_dolar': total_cart_dolar
    })

@login_required
def añadirCarrito(request, id):
    producto = get_object_or_404(Producto, id_producto=id)
    cart = get_cart(request)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, producto=producto)
    if not created:
        cart_item.cantidad += 1
        cart_item.save()

    return redirect('carrito')

def eliminarProductoCarrito(request, item_id):
    cart = get_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    cart_item.delete()
    messages.success(request, "Eliminado Correctamente")
    return redirect('carrito')

@login_required
def vaciar_carrito(request):
    cart = get_cart(request)
    cart.cartitem_set.all().delete()
    return redirect('carrito')

def agregarProducto(request):
    data = {
        'form': ProductoForm()
    }
    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Guardado correctamente")
        else:
            data['form'] = formulario    

    return render(request, 'agregarProducto.html', data)

def listarProducto(request):
    productos = Producto.objects.all()
    data = {
        'productos':productos
    }
    return render(request, 'listarProducto.html', data)

def modificarProducto(request, id):
    producto = get_object_or_404(Producto, id_producto=id)
    data = {
        'form':ProductoForm(instance=producto)   
    }
    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, instance=producto, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Modificado correctamente")
            return redirect(to="listarProducto")
        else:
            data['form'] = formulario 

    return render(request, 'modificarProducto.html', data)

def eliminarProducto(request, id):
    producto = get_object_or_404(Producto, id_producto=id)
    producto.delete()
    messages.success(request, "Eliminado Correctamente")
    return redirect(to="listarProducto")

def detalleProducto(request, id):
    producto = get_object_or_404(Producto, id_producto=id)
    return render(request, 'detalleProducto.html',{'producto': producto})

def productos(request):
    tipo_cambio = obtener_tipo_cambio()
    productos = Producto.objects.all()

    for producto in productos:
        producto.precio_dolar = producto.precio/tipo_cambio

    return render(request, 'productos.html', {'productos':productos})


