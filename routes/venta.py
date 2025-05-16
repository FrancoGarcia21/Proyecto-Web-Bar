from flask import Blueprint, render_template, request, redirect, url_for, flash
from controllers.stock import obtener_productos
from controllers.venta import cargar_venta

venta_bp = Blueprint('venta', __name__)

############## Ruta de ventana original
@venta_bp.route('/venta')
def venta():
    """ Ruta que lleva a la ventana venta con los productos """
    productos = obtener_productos()
    return render_template('venta.html', productos=productos)

############## Ruta agregar una venta
@venta_bp.route('/venta/pedido')
def cargar_venta_route():
    """ Ruta que carga un pedido a la base """
    pedido = cargar_venta()
    return True