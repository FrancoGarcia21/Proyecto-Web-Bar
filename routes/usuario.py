from flask import Blueprint, render_template, request, redirect, url_for
from controllers.usuario import obtener_usuarios, cargar_usuario, modificar_usuario

usuario_bp = Blueprint('usuario', __name__)

############## Ruta OBTENER Usuarios
@usuario_bp.route('/usuario')
def usuario():
    """ Función para obtener el listado de empleados """
    usuarios = obtener_usuarios()
    return render_template('usuario.html', usuarios=usuarios)

############## Ruta CARGAR NUEVO Usuario
@usuario_bp.route('/usuario/cargar', methods=['POST'])
def cargar_usuario_route():
    """ Función para cargar usuario , recibe datos desde el formulario """
    dni = request.form.get('dni')
    nombre = request.form.get('fullName')
    fecha_nacimiento = request.form.get('birthday')
    puesto = request.form.get('puesto')
    estado = request.form.get('estado')
    clave = request.form.get('password')

    # Llamar a la función del controlador para insertar el usuario
    cargar_usuario(dni, nombre, fecha_nacimiento, puesto, estado, clave)
    
    return redirect(url_for('usuario.usuario'))  # Redirige al listado actualizado


############## Ruta MODIFICAR ESTADO de un Usuario
@usuario_bp.route('/usuario/modificar', methods=['POST'])
def modificar_usuario_route():
    """ Función para modificar el estado de un usuario """
    dni = request.form.get('dni')
    estado = request.form.get('estado')
    
    modificar_usuario(dni, estado)
    
    return redirect(url_for('usuario.usuario'))