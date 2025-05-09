from flask import Blueprint, render_template, request, redirect, url_for
from controllers.stock import obtener_productos, cargar_producto_nuevo,modificar_stock, obtener_un_producto

import logging

logging.basicConfig(level=logging.DEBUG)

stock_bp = Blueprint('stock', __name__)

############################### Ruta  de MOSTRAR lista de productos
@stock_bp.route('/stock')
def stock():
    productos = obtener_productos()
    return render_template('stock.html', productos=productos, mostrar='lista')


############################### Ruta de CARGAR producto
@stock_bp.route('/stock/cargar', methods=['POST'])
def cargar_producto_nuevo_route():
    """ Ruta para cargar un producto nuevo """
    id_producto = request.form.get('producto')
    nombre_producto = request.form.get('nombreProducto')
    cantidad_stock = int(request.form.get('cantidad'))
    costo_unitario = request.form.get('costo')
    limite_alarmante = int(request.form.get('limite'))
    id_categoria = request.form.get('categoria')
    
    cargar_producto_nuevo(id_producto, nombre_producto, cantidad_stock, costo_unitario, limite_alarmante, id_categoria)

    return redirect(url_for('stock.stock'))

############################### Ruta AGREGAR STOCK
@stock_bp.route('/stock/modificarStock', methods=['POST'])
def modificar_stock_route():
    """ Ruta para modificar el stock"""
    id_producto = request.form.get('producto')
    cantidad_stock = request.form.get('cantidad')
    
    modificar_stock(id_producto, cantidad_stock)
    
    return redirect(url_for('stock.stock'))