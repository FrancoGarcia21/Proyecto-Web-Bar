from flask import Blueprint, render_template
from utils.decoradores import login_required


informe_bp = Blueprint('informe', __name__)

@informe_bp.route('/informe')
@login_required
def informe():
    """ Esta ruta lleva a informes """
    return render_template('informe.html')
