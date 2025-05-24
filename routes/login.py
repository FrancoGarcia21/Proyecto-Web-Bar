from flask import Blueprint, render_template,request, redirect, flash, session, url_for
from controllers.login import verificacion_usuario

login_bp = Blueprint('login', __name__)

@login_bp.route('/login')
def login():
    """ Muestra el login si no hay sesión activa """
    if 'usuario' in session:
        rol = session.get('rol')

        # Redirigir al home adecuado según el rol
        if rol == 'administrador':
            return redirect(url_for('home'))
        else:
            return redirect(url_for('venta.venta'))  # o la vista principal de cajeros/vendedores

    return render_template('login.html')

################## verificacion se sesion
@login_bp.route('/login/verificacion', methods=["POST"])
def verificar_usuario_route():
    """ Verificación para ingreso """

    id_usuario = request.form.get('dni_usuario')
    password = request.form.get('password')

    print(id_usuario, password)

    autorizado, rol  = verificacion_usuario(id_usuario, password)

    if autorizado == "ok":
        session['usuario'] = id_usuario
        session['rol'] = rol
        return redirect('/')  # Reemplaza con la ruta real
    else:
        mensajes(autorizado, 'Ingreso fallido')
        return redirect('/login')


################## LOG OUT
@login_bp.route('/logout')
def logout():
    """ Salir del sistema """
    session.pop('usuario', None)
    flash("✅ Sesión cerrada correctamente.", "success")
    return redirect(url_for('login.login'))

################## MENSAJES

def mensajes(resultado, mensaje_personalizado):
    """ MODULO DE MENSAJES GENERICO """
    if resultado == "false":
        flash("❌ ERROR EN EL INGRESO DE DATOS - Usuario o contraseña incorrecta.", "error")
    elif resultado == "ok":
        flash(mensaje_personalizado, "success")
    elif resultado == "Conexion_Error":
        flash("❌ Error de conexión con la base de datos.", "error")
    else: 
        flash("❌ Ocurrió un error inesperado.", "error")
    