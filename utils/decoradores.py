from functools import wraps
from flask import session, redirect, url_for, flash

################ DECORADOR PARA LOGIN
def login_required(f):
  """ Decorador para la validacion, asi no pongo a cad arato el if X in session """
  @wraps(f)
  def decorador(*args, **kwargs):
        if 'usuario' not in session:
            flash("⚠️ Debes iniciar sesión para acceder a esta página.", "error")
            return redirect(url_for('login.login'))  # 'login' es el nombre del blueprint
        return f(*args, **kwargs)
  return decorador


################ DECORADOR PARA LOS ROLES
def role_required(*roles):
  """ Decorador que permite ingresar solo si tiene alguno de los roles asigados en *roles """
  def decorador(f):
        @wraps(f)
        def funcion_envuelta(*args, **kwargs):
            rol_usuario = session.get('rol')
            if rol_usuario not in roles:
                flash("🚫 No tienes permiso para acceder a esta sección.", "error")
                return redirect(url_for('login.login'))
            return f(*args, **kwargs)
        return funcion_envuelta
  return decorador