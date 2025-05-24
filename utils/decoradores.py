from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(f):
  """ Decorador para la validacion, asi no pongo a cad arato el if X in session """
  @wraps(f)
  def decorador(*args, **kwargs):
        if 'usuario' not in session:
            flash("⚠️ Debes iniciar sesión para acceder a esta página.", "error")
            return redirect(url_for('login.login'))  # 'login' es el nombre del blueprint
        return f(*args, **kwargs)
  return decorador