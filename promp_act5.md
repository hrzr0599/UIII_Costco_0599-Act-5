Perfecto ✅
Esta es la **Tercera Parte del Proyecto Costco (UIII_Costco_0599)** — CRUD completo del modelo **`Pedido`** con relaciones a **Usuario** y **Producto**.
A continuación te explico **paso a paso**, con **código completo**, estructura, vistas, plantillas, rutas y configuración final.

---

## 🧩 **TERCERA PARTE — CRUD DE PEDIDO**

---

### **1️⃣ Modelo base (`models.py`)**

✅ Ya está correctamente definido.
Solo asegúrate de que la clase `Pedido` tenga la relación **ForeignKey con Usuario** y **ManyToMany con Producto** (como ya mostraste).

No hay cambios aquí.

---

### **2️⃣ Realizar migraciones**

Ejecuta en la terminal:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### **3️⃣ Trabajamos con el MODELO: PEDIDO**

Ahora crearás las vistas CRUD de `Pedido` dentro de `app_Costco/views.py`.

---

### **4️⃣ Crear funciones CRUD en `views.py`**

Abre `app_Costco/views.py` y agrega este bloque:

```python
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
```

---

### **5️⃣ Combobox (Usuario y Productos)**

En `agregar_pedido.html` y `actualizar_pedido.html`, los combos se llenan con listas (`usuarios` y `productos`) enviadas desde las vistas.
El usuario podrá elegir **uno** y los productos, **varios** (campo multiple).

---

### **6️⃣ Modificar el `navbar.html`**

En `app_Costco/templates/navbar.html` agrega el menú **Pedido** así:

```html
<li class="nav-item dropdown">
  <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
    Pedidos
  </a>
  <ul class="dropdown-menu">
    <li><a class="dropdown-item" href="{% url 'agregar_pedido' %}">Agregar pedido</a></li>
    <li><a class="dropdown-item" href="{% url 'ver_pedido' %}">Ver pedidos</a></li>
  </ul>
</li>
```

---

### **7️⃣ Crear subcarpeta `pedido`**

Ruta completa:

```
app_Costco/templates/pedido/
```

---

### **8️⃣ Crear los archivos HTML del CRUD Pedido**

#### 📄 `agregar_pedido.html`

```html
{% extends "base.html" %}
{% block content %}
<h2>Agregar Pedido</h2>
<form method="post">
  {% csrf_token %}
  <div class="mb-3">
    <label>Usuario:</label>
    <select class="form-select" name="usuario">
      {% for u in usuarios %}
        <option value="{{ u.id }}">{{ u.nombre_usuario }}</option>
      {% endfor %}
    </select>
  </div>
  <div class="mb-3">
    <label>Dirección de Envío:</label>
    <textarea class="form-control" name="direccion_envio"></textarea>
  </div>
  <div class="mb-3">
    <label>Total Pedido:</label>
    <input class="form-control" name="total_pedido" type="number" step="0.01">
  </div>
  <div class="mb-3">
    <label>Método de Pago:</label>
    <input class="form-control" name="metodo_pago">
  </div>
  <div class="mb-3">
    <label>Estado del Pedido:</label>
    <input class="form-control" name="estado_pedido" value="Pendiente">
  </div>
  <div class="mb-3">
    <label>Seleccionar Productos:</label>
    <select class="form-select" name="productos" multiple>
      {% for p in productos %}
        <option value="{{ p.id }}">{{ p.nombre }}</option>
      {% endfor %}
    </select>
  </div>
  <button class="btn btn-primary">Guardar Pedido</button>
  <a class="btn btn-secondary" href="{% url 'ver_pedido' %}">Cancelar</a>
</form>
{% endblock %}
```

---

#### 📄 `ver_pedido.html`

```html
{% extends "base.html" %}
{% block content %}
<h2>Lista de Pedidos</h2>
<a class="btn btn-success mb-3" href="{% url 'agregar_pedido' %}">+ Nuevo Pedido</a>
<table class="table table-hover">
  <thead>
    <tr>
      <th>ID</th>
      <th>Usuario</th>
      <th>Fecha</th>
      <th>Estado</th>
      <th>Total</th>
      <th>Productos</th>
      <th>Acciones</th>
    </tr>
  </thead>
  <tbody>
    {% for p in pedidos %}
    <tr>
      <td>{{ p.id }}</td>
      <td>{{ p.usuario.nombre_usuario }}</td>
      <td>{{ p.fecha_pedido|date:"d/m/Y H:i" }}</td>
      <td>{{ p.estado_pedido }}</td>
      <td>${{ p.total_pedido }}</td>
      <td>
        {% for prod in p.productos.all %}
          {{ prod.nombre }}{% if not forloop.last %}, {% endif %}
        {% empty %}
          Sin productos
        {% endfor %}
      </td>
      <td>
        <a class="btn btn-sm btn-info" href="{% url 'actualizar_pedido' p.id %}">Editar</a>
        <a class="btn btn-sm btn-danger" href="{% url 'borrar_pedido' p.id %}">Borrar</a>
      </td>
    </tr>
    {% empty %}
    <tr><td colspan="7">No hay pedidos registrados.</td></tr>
    {% endfor %}
  </tbody>
</table>
{% endblock %}
```

---

#### 📄 `actualizar_pedido.html`

```html
{% extends "base.html" %}
{% block content %}
<h2>Actualizar Pedido</h2>
<form method="post" action="{% url 'realizar_actualizacion_pedido' pedido.id %}">
  {% csrf_token %}
  <div class="mb-3">
    <label>Usuario:</label>
    <select class="form-select" name="usuario">
      {% for u in usuarios %}
        <option value="{{ u.id }}" {% if pedido.usuario.id == u.id %}selected{% endif %}>
          {{ u.nombre_usuario }}
        </option>
      {% endfor %}
    </select>
  </div>
  <div class="mb-3">
    <label>Dirección de Envío:</label>
    <textarea class="form-control" name="direccion_envio">{{ pedido.direccion_envio }}</textarea>
  </div>
  <div class="mb-3">
    <label>Total Pedido:</label>
    <input class="form-control" name="total_pedido" value="{{ pedido.total_pedido }}">
  </div>
  <div class="mb-3">
    <label>Método de Pago:</label>
    <input class="form-control" name="metodo_pago" value="{{ pedido.metodo_pago }}">
  </div>
  <div class="mb-3">
    <label>Estado:</label>
    <input class="form-control" name="estado_pedido" value="{{ pedido.estado_pedido }}">
  </div>
  <div class="mb-3">
    <label>Productos:</label>
    <select class="form-select" name="productos" multiple>
      {% for p in productos %}
        <option value="{{ p.id }}" {% if p in pedido.productos.all %}selected{% endif %}>
          {{ p.nombre }}
        </option>
      {% endfor %}
    </select>
  </div>
  <button class="btn btn-primary">Actualizar</button>
  <a class="btn btn-secondary" href="{% url 'ver_pedido' %}">Cancelar</a>
</form>
{% endblock %}
```

---

#### 📄 `borrar_pedido.html`

```html
{% extends "base.html" %}
{% block content %}
<h2>Eliminar Pedido</h2>
<p>¿Seguro que deseas eliminar el pedido #{{ pedido.id }} del usuario <strong>{{ pedido.usuario.nombre_usuario }}</strong>?</p>
<form method="post">
  {% csrf_token %}
  <button class="btn btn-danger" type="submit">Sí, eliminar</button>
  <a class="btn btn-secondary" href="{% url 'ver_pedido' %}">Cancelar</a>
</form>
{% endblock %}
```

---

### **9️⃣ No usar `forms.py`**

✅ Cumplido: los formularios son manuales.

---

### **🔟 Rutas en `app_Costco/urls.py`**

Abre `app_Costco/urls.py` y agrega al final:

```python
# --- PEDIDO ---
path('pedidos/agregar/', views.agregar_pedido, name='agregar_pedido'),
path('pedidos/', views.ver_pedido, name='ver_pedido'),
path('pedidos/actualizar/<int:pedido_id>/', views.actualizar_pedido, name='actualizar_pedido'),
path('pedidos/realizar_actualizacion/<int:pedido_id>/', views.realizar_actualizacion_pedido, name='realizar_actualizacion_pedido'),
path('pedidos/borrar/<int:pedido_id>/', views.borrar_pedido, name='borrar_pedido'),
```

---

### **🔟 Registrar modelos en `admin.py` y migrar**

Archivo: `app_Costco/admin.py`

```python
from django.contrib import admin
from .models import Usuario, Producto, Pedido

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'fecha_pedido', 'estado_pedido', 'total_pedido')
    search_fields = ('usuario__nombre_usuario', 'numero_seguimiento')
    list_filter = ('estado_pedido', 'fecha_pedido')
```

Luego ejecuta:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### **1️⃣1️⃣ Trabajando con todos los modelos**

✅ `Usuario`, `Producto`, y `Pedido` totalmente operativos y relacionados.

---

### **1️⃣2️⃣ Colores suaves y diseño moderno**

Ya heredado de `base.html` (Bootstrap).
Puedes usar clases `btn`, `table-hover`, `mb-3`, etc.

---

### **1️⃣3️⃣ No validar datos**

✅ No se validan datos de formulario.

---

### **1️⃣4️⃣ Estructura completa actualizada**

```
UIII_Costco_0599/
│
├── backend_Costco/
│   ├── settings.py
│   ├── urls.py
│
├── app_Costco/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── navbar.html
│   │   ├── usuario/
│   │   │   └── (crud usuario)
│   │   ├── producto/
│   │   │   └── (crud producto)
│   │   └── pedido/
│   │       ├── agregar_pedido.html
│   │       ├── ver_pedido.html
│   │       ├── actualizar_pedido.html
│   │       └── borrar_pedido.html
│
└── manage.py
```

---

### **1️⃣5️⃣ Proyecto totalmente funcional**

✅ CRUD completo para Usuario, Producto y Pedido.
✅ Relación entre ellos operativa.
✅ Interfaz moderna y clara.

---

### **1️⃣6️⃣ Ejecutar servidor en puerto 8018**

```bash
python manage.py runserver 8018
```

Accede a:
👉 `http://127.0.0.1:8018/`

---

¿Deseas que te genere ahora un **archivo comprimido (.zip)** con toda la estructura lista del proyecto Costco (con templates, rutas, y modelos listos para ejecutar)?
