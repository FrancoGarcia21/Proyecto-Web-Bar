from flask import Blueprint, render_template, request, redirect, url_for, flash
from controllers.stock import obtener_productos, obtener_categorias,obtener_productos_de_categoria
from controllers.venta import cargar_venta
from utils.decoradores import login_required, role_required


venta_bp = Blueprint('venta', __name__)

############## Ruta de ventana original
@venta_bp.route('/venta')
@login_required
@role_required('administrador', 'vendedor', 'cajero')
def venta():
    """ Ruta que lleva a la ventana venta con los productos """
    categorias = obtener_categorias()
    return render_template('venta.html', categorias=categorias)

############## Ruta Buscar una categoria
@venta_bp.route('/venta/buscar-categoria/<int:id_categoria>')
@login_required
@role_required('administrador', 'vendedor', 'cajero')
def buscar_categoria_route(id_categoria):
    """ Busco una categoria para mostrar los elementos """
    productos = obtener_productos_de_categoria(id_categoria)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Petición AJAX → solo fragmento HTML
        return render_template('VentaLista.html', productos=productos)

    # Petición normal → vista completa
    categorias = obtener_categorias()
    return render_template('ventaLista.html', productos=productos, categorias=categorias)

############## Ruta agregar una venta
@venta_bp.route('/venta/pedido')
@login_required
@role_required('administrador', 'vendedor', 'cajero')
def cargar_venta_route():
    """ Ruta que carga un pedido a la base """
    pedido = cargar_venta()
    return True