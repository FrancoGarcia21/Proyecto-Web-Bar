from flask import Blueprint, render_template
from controllers.usuario import obtener_usuarios

usuario_bp = Blueprint('usuario', __name__)

@usuario_bp.route('/usuario')
def usuario():
    """ Función para obtener el listado de empleados """
    usuarios = obtener_usuarios()
    return render_template('usuario.html', usuarios=usuarios)
