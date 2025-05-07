from flask import Blueprint, render_template
from controllers.stock import obtener_productos


stock_bp = Blueprint('stock', __name__)

@stock_bp.route('/stock')
def stock():
    productos = obtener_productos()
    return render_template('stock.html', productos=productos, mostrar='lista')

