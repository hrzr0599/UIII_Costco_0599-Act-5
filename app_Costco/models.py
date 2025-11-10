from django.db import models

class Usuario(models.Model):
    # Campos de Usuario
    nombre_usuario = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    direccion = models.TextField()
    telefono = models.CharField(max_length=20, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre_usuario

class Producto(models.Model):
    # Campos de Producto
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    categoria = models.CharField(max_length=100, blank=True, null=True)
    codigo_barras = models.CharField(max_length=50, unique=True, blank=True, null=True)
    imagen_url = models.URLField(blank=True, null=True)  # Nuevo campo
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class Pedido(models.Model):
    # Relación uno a muchos: Un Usuario puede tener muchos Pedidos
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='pedidos')

    # Campos de Pedido
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    estado_pedido = models.CharField(max_length=50, default='Pendiente')
    direccion_envio = models.TextField()
    total_pedido = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    metodo_pago = models.CharField(max_length=50)
    fecha_entrega_estimada = models.DateField(blank=True, null=True)
    numero_seguimiento = models.CharField(max_length=100, blank=True, null=True)

    # Relación muchos a muchos: Un Pedido puede tener muchos Productos y un Producto puede estar en muchos Pedidos
    productos = models.ManyToManyField(Producto, related_name='pedidos')

    def __str__(self):
        return f"Pedido #{self.id} de {self.usuario.nombre_usuario}"
