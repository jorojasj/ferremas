from django.shortcuts import get_object_or_404, render, redirect
from .forms import *
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    productos = Producto.objects.all()
    data = {
        'productos':productos
    }
    return render(request, 'index.html', data)

def login(request):
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
def carrito(request):
    return render(request, 'carrito.html')

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



