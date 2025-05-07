from flask import Blueprint, render_template

venta_bp = Blueprint('venta', __name__)

@venta_bp.route('/venta')
def venta():
    return render_template('venta.html')
