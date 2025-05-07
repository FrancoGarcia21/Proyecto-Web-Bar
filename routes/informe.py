from flask import Blueprint, render_template

informe_bp = Blueprint('informe', __name__)

@informe_bp.route('/informe')
def informe():
    return render_template('informe.html')
