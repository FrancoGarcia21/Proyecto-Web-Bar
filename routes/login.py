from flask import Blueprint, render_template,request, redirect, flash, session, url_for
from controllers.login import verificacion_usuario

login_bp = Blueprint('login', __name__)

@login_bp.route('/login')
def login():
    """ muestra el login """
    return render_template('login.html')

################## verificacion se sesion
@login_bp.route('/login/verificacion', methods=["POST"])
def verificar_usuario_route():
    """ Verificación para ingreso """

    id_usuario = request.form.get('dni_usuario')
    password = request.form.get('password')

    print(id_usuario, password)

    autorizado  = verificacion_usuario(id_usuario, password)

    if autorizado == "ok":
        session['usuario'] = id_usuario
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
        print("ENTRO AL FALSE")
        flash("❌ ERROR EN EL INGRESO DE DATOS - Usuario o contraseña incorrecta.", "error")
    elif resultado == "ok":
        print("ENTRO AL OK")
        flash(mensaje_personalizado, "success")
    elif resultado == "Conexion_Error":
        print("ENTRO AL ERROR DE CONEXION")
        flash("❌ Error de conexión con la base de datos.", "error")
    else:
        print("ENTRO AL ELSE FINAL")
        flash("❌ Ocurrió un error inesperado.", "error")
    