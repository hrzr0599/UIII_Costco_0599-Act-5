from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Usuario

def inicio_costco(request):
    return render(request, 'inicio.html')

# Mostrar formulario para agregar usuario y procesar POST
def agregar_usuario(request):
    if request.method == 'POST':
        nombre_usuario = request.POST.get('nombre_usuario', '').strip()
        email = request.POST.get('email', '').strip()
        nombre = request.POST.get('nombre', '').strip()
        apellido = request.POST.get('apellido', '').strip()
        direccion = request.POST.get('direccion', '').strip()
        telefono = request.POST.get('telefono', '').strip()

        usuario = Usuario(
            nombre_usuario=nombre_usuario,
            email=email,
            nombre=nombre,
            apellido=apellido,
            direccion=direccion,
            telefono=telefono
        )
        usuario.save()
        return redirect('ver_usuario')
    # GET -> mostrar formulario
    return render(request, 'usuario/agregar_usuario.html')

# Ver lista de usuarios
def ver_usuario(request):
    usuarios = Usuario.objects.all().order_by('-fecha_registro')
    return render(request, 'usuario/ver_usuario.html', {'usuarios': usuarios})

# Mostrar formulario de actualización (carga datos)
def actualizar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    return render(request, 'usuario/actualizar_usuario.html', {'usuario': usuario})

# Procesar actualización (POST)
def realizar_actualizacion_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    if request.method == 'POST':
        usuario.nombre_usuario = request.POST.get('nombre_usuario', usuario.nombre_usuario).strip()
        usuario.email = request.POST.get('email', usuario.email).strip()
        usuario.nombre = request.POST.get('nombre', usuario.nombre).strip()
        usuario.apellido = request.POST.get('apellido', usuario.apellido).strip()
        usuario.direccion = request.POST.get('direccion', usuario.direccion).strip()
        usuario.telefono = request.POST.get('telefono', usuario.telefono).strip()
        usuario.save()
        return redirect('ver_usuario')
    return redirect('actualizar_usuario', usuario_id=usuario_id)

# Confirmar y borrar usuario
def borrar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    if request.method == 'POST':
        usuario.delete()
        return redirect('ver_usuario')
    return render(request, 'usuario/borrar_usuario.html', {'usuario': usuario})



from .models import Producto

# Agregar producto
def agregar_producto(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        precio = request.POST.get('precio')
        stock = request.POST.get('stock')
        categoria = request.POST.get('categoria')
        codigo_barras = request.POST.get('codigo_barras')
        imagen_url = request.POST.get('imagen_url')

        Producto.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            stock=stock,
            categoria=categoria,
            codigo_barras=codigo_barras,
            imagen_url=imagen_url
        )
        return redirect('ver_producto')
    return render(request, 'producto/agregar_producto.html')


# Ver productos
def ver_producto(request):
    productos = Producto.objects.all().order_by('-fecha_creacion')
    return render(request, 'producto/ver_producto.html', {'productos': productos})


# Mostrar formulario de actualización
def actualizar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'producto/actualizar_producto.html', {'producto': producto})


# Realizar actualización
def realizar_actualizacion_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        producto.nombre = request.POST.get('nombre')
        producto.descripcion = request.POST.get('descripcion')
        producto.precio = request.POST.get('precio')
        producto.stock = request.POST.get('stock')
        producto.categoria = request.POST.get('categoria')
        producto.codigo_barras = request.POST.get('codigo_barras')
        producto.imagen_url = request.POST.get('imagen_url')
        producto.save()
        return redirect('ver_producto')
    return redirect('actualizar_producto', producto_id=producto_id)


# Borrar producto
def borrar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        producto.delete()
        return redirect('ver_producto')
    return render(request, 'producto/borrar_producto.html', {'producto': producto})


from .models import Usuario, Producto, Pedido
from django.shortcuts import render, redirect, get_object_or_404

# -----------------------------
# CRUD PEDIDO
# -----------------------------

# AGREGAR PEDIDO
def agregar_pedido(request):
    usuarios = Usuario.objects.all()
    productos = Producto.objects.all()

    if request.method == 'POST':
        usuario_id = request.POST.get('usuario')
        direccion_envio = request.POST.get('direccion_envio')
        total_pedido = request.POST.get('total_pedido')
        metodo_pago = request.POST.get('metodo_pago')
        estado_pedido = request.POST.get('estado_pedido')
        productos_ids = request.POST.getlist('productos')

        usuario = Usuario.objects.get(id=usuario_id)
        pedido = Pedido.objects.create(
            usuario=usuario,
            direccion_envio=direccion_envio,
            total_pedido=total_pedido,
            metodo_pago=metodo_pago,
            estado_pedido=estado_pedido
        )
        pedido.productos.set(productos_ids)
        return redirect('ver_pedido')

    return render(request, 'pedido/agregar_pedido.html', {
        'usuarios': usuarios,
        'productos': productos
    })


# VER PEDIDOS
def ver_pedido(request):
    pedidos = Pedido.objects.all().order_by('-fecha_pedido')
    return render(request, 'pedido/ver_pedido.html', {'pedidos': pedidos})


# ACTUALIZAR PEDIDO (mostrar formulario)
def actualizar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    usuarios = Usuario.objects.all()
    productos = Producto.objects.all()
    return render(request, 'pedido/actualizar_pedido.html', {
        'pedido': pedido,
        'usuarios': usuarios,
        'productos': productos
    })


# REALIZAR ACTUALIZACIÓN DE PEDIDO
def realizar_actualizacion_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    if request.method == 'POST':
        pedido.usuario_id = request.POST.get('usuario')
        pedido.direccion_envio = request.POST.get('direccion_envio')
        pedido.total_pedido = request.POST.get('total_pedido')
        pedido.metodo_pago = request.POST.get('metodo_pago')
        pedido.estado_pedido = request.POST.get('estado_pedido')
        pedido.save()

        productos_ids = request.POST.getlist('productos')
        pedido.productos.set(productos_ids)
        return redirect('ver_pedido')
    return redirect('actualizar_pedido', pedido_id=pedido_id)


# BORRAR PEDIDO
def borrar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    if request.method == 'POST':
        pedido.delete()
        return redirect('ver_pedido')
    return render(request, 'pedido/borrar_pedido.html', {'pedido': pedido})
