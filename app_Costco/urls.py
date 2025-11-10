from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio_costco, name='inicio_costco'),
    path('usuarios/agregar/', views.agregar_usuario, name='agregar_usuario'),
    path('usuarios/', views.ver_usuario, name='ver_usuario'),
    path('usuarios/actualizar/<int:usuario_id>/', views.actualizar_usuario, name='actualizar_usuario'),
    path('usuarios/realizar_actualizacion/<int:usuario_id>/', views.realizar_actualizacion_usuario, name='realizar_actualizacion_usuario'),
    path('usuarios/borrar/<int:usuario_id>/', views.borrar_usuario, name='borrar_usuario'),
    # --- PRODUCTO ---
path('productos/agregar/', views.agregar_producto, name='agregar_producto'),
path('productos/', views.ver_producto, name='ver_producto'),
path('productos/actualizar/<int:producto_id>/', views.actualizar_producto, name='actualizar_producto'),
path('productos/realizar_actualizacion/<int:producto_id>/', views.realizar_actualizacion_producto, name='realizar_actualizacion_producto'),
path('productos/borrar/<int:producto_id>/', views.borrar_producto, name='borrar_producto'),
# --- PEDIDO ---
path('pedidos/agregar/', views.agregar_pedido, name='agregar_pedido'),
path('pedidos/', views.ver_pedido, name='ver_pedido'),
path('pedidos/actualizar/<int:pedido_id>/', views.actualizar_pedido, name='actualizar_pedido'),
path('pedidos/realizar_actualizacion/<int:pedido_id>/', views.realizar_actualizacion_pedido, name='realizar_actualizacion_pedido'),
path('pedidos/borrar/<int:pedido_id>/', views.borrar_pedido, name='borrar_pedido'),

]